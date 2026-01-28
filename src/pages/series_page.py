import flet as ft

from services.metron_service import MetronService
from pages.components.management_sheets import (
    SeriesManagementSheet,
    IssueManagementSheet,
)
from pages.components.issue_card import IssueCard
from pages.components.series_overview import SeriesOverview
from pages.components.list_manager import ListManager
from pages.components.page_header import PageHeader
from utilities.utils import launch_external_url


def series_page(page: ft.Page, series_id: int):
    metron = MetronService()
    series = None

    header = PageHeader()
    overview_view = SeriesOverview()
    loader = ft.ProgressBar(
        visible=True, color=ft.Colors.BLUE_ACCENT, bgcolor="#1a1c1e"
    )

    appbar_title = ft.Text(
        "",
        size=18,
        weight=ft.FontWeight.BOLD,
        visible=False,
    )

    issue_list_manager = ListManager(
        card_type=IssueCard,
        on_item_menu_click=lambda issue: show_issue_add_modal(issue),
    )

    series_sheet = SeriesManagementSheet(
        page, on_submit=lambda data: print(f"Series Data: {data}")
    )
    issue_sheet = IssueManagementSheet(
        page, on_submit=lambda c, r: print(f"Issue Status: {c}, {r}")
    )

    page.overlay.extend([series_sheet, issue_sheet])

    def show_series_add_modal(e):
        if series:
            series_sheet.show(series.name)

    def show_issue_add_modal(issue):
        title = (
            f"{issue.series.name} #{issue.number}"
            if issue.series
            else f"Issue #{issue.number}"
        )
        issue_sheet.show(title, is_collected=False, is_read=False)

    def update_ui_with_data(series_data, issues_data):
        nonlocal series
        series = series_data

        pub = series.publisher.name if series.publisher else ""
        yr = str(series.year_began) if series.year_began else ""
        subtitle = f"{pub} • {yr}" if pub and yr else (pub or yr)
        hero_url = (
            str(issues_data[0].image) if issues_data and issues_data[0].image else None
        )

        header.update_header(title=series.name, subtitle=subtitle, image_url=hero_url)
        overview_view.update_series(series)
        issue_list_manager.set_items(issues_data)

        appbar_title.value = series.name
        # appbar_title.visible = True
        page.update()

    async def load_details():
        loader.visible = True
        page.update()
        try:
            series_data, issues_data = metron.get_series_details(series_id)
            update_ui_with_data(series_data, issues_data)
        except Exception as e:
            overview_view.controls = [ft.Text(f"Error: {e}", color=ft.Colors.RED)]
        finally:
            loader.visible = False
            page.update()

    page.run_task(load_details)

    header_appbar = ft.AppBar(
        bgcolor=ft.Colors.TRANSPARENT,
        elevation=0,
        title=appbar_title,
        actions=[
            ft.IconButton(ft.Icons.ADD, icon_size=26, on_click=show_series_add_modal),
            ft.PopupMenuButton(
                icon=ft.Icons.MORE_VERT,
                items=[
                    ft.PopupMenuItem(content="Share", icon=ft.Icons.SHARE),
                    ft.PopupMenuItem(
                        content="Open in Browser",
                        icon=ft.Icons.OPEN_IN_BROWSER,
                        on_click=lambda _: page.run_task(
                            launch_external_url, page, series
                        ),
                    ),
                ],
            ),
        ],
    )

    return ft.View(
        route=f"/series/{series_id}",
        bgcolor=ft.Colors.SURFACE,
        padding=0,
        spacing=0,
        appbar=header_appbar,
        controls=[
            ft.Tabs(
                expand=True,
                length=2,
                content=ft.Container(
                    margin=ft.Margin.only(top=-75),
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[
                            header,
                            loader,
                            ft.TabBar(
                                indicator_color=ft.Colors.BLUE_ACCENT,
                                scrollable=False,
                                tab_alignment=ft.TabAlignment.FILL,
                                tabs=[ft.Tab(label="OVERVIEW"), ft.Tab(label="ISSUES")],
                            ),
                            ft.TabBarView(
                                expand=True,
                                controls=[overview_view, issue_list_manager],
                            ),
                        ],
                    ),
                ),
            )
        ],
    )
