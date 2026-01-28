import flet as ft
import asyncio
from services.metron_service import MetronService
from pages.components.issue_card import IssueCard
from pages.components.series_card import SeriesCard
from pages.components.management_sheets import IssueManagementSheet


def search_results_page(page: ft.Page, query_type: str, query_text: str):
    metron = MetronService()

    results_list = ft.ListView(expand=True, spacing=0, padding=0)
    progress_bar = ft.ProgressBar(
        visible=True, color=ft.Colors.BLUE_ACCENT, bgcolor=ft.Colors.SURFACE
    )
    status_text = ft.Text(
        size=14, color=ft.Colors.ON_SURFACE_VARIANT, weight=ft.FontWeight.W_500
    )

    issue_sheet = IssueManagementSheet(
        page, on_submit=lambda c, r: print(f"Issue Status updated: {c}, {r}")
    )
    page.overlay.append(issue_sheet)

    def handle_issue_menu(issue):
        title = (
            f"{issue.series.name} #{issue.number}"
            if hasattr(issue, "series") and issue.series
            else f"Issue #{issue.number}"
        )
        issue_sheet.show(title, is_collected=False, is_read=False)

    async def perform_search():
        try:
            if query_type == "series":
                results = metron.search_series(query_text)
                results_list.controls = [
                    SeriesCard(
                        series=item["series"],
                        image_url=item["image"],
                        on_click=lambda _, s_id=item["series"].id: asyncio.create_task(
                            page.push_route(f"/series/{s_id}")
                        ),
                    )
                    for item in results
                ]
            elif query_type == "issues":
                results = metron.search_issues(query_text)
                results_list.controls = [
                    IssueCard(issue, mode="list", on_menu_click=handle_issue_menu)
                    for issue in results
                ]

            status_text.value = (
                f"{len(results_list.controls)} results for '{query_text}'"
            )

        except Exception as e:
            status_text.value = f"Error: {str(e)}"
        finally:
            progress_bar.visible = False
            page.update()

    page.run_task(perform_search)

    return ft.View(
        route="/results",
        padding=0,
        appbar=ft.AppBar(
            bgcolor=ft.Colors.SURFACE,
            actions=[
                ft.IconButton(ft.Icons.SORT_ROUNDED),
                ft.IconButton(ft.Icons.FILTER_ALT_OUTLINED),
            ],
        ),
        controls=[
            progress_bar,
            ft.Container(
                padding=ft.Padding.only(left=15, top=10, bottom=5), content=status_text
            ),
            results_list,
        ],
    )
