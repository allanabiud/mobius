import flet as ft
import asyncio
from services.metron_service import MetronService
from datetime import datetime, date, time


def search_page(page: ft.Page):
    metron = MetronService()

    state = {
        "last_query": None,
        "active_tab": 0,
        "last_query_per_tab": [None, None, None, None],
    }

    series_results = ft.ListView(expand=True, spacing=0, padding=0)
    issues_results = ft.ListView(expand=True, spacing=0, padding=0)
    character_results = ft.ListView(expand=True, spacing=0, padding=0)
    creator_results = ft.ListView(expand=True, spacing=0, padding=0)

    result_columns = [
        series_results,
        issues_results,
        character_results,
        creator_results,
    ]

    def handle_tab_click(e):
        state["active_tab"] = int(e.data)
        idx = state["active_tab"]

        if (
            state["last_query"]
            and state["last_query_per_tab"][idx] != state["last_query"]
        ):
            result_columns[idx].controls.clear()
            execute_search(idx, state["last_query"])
        page.update()

    def handle_clear(e):
        search_field.value = ""
        for col in result_columns:
            col.controls.clear()
        page.update()

    def format_month_year(value) -> str | None:
        if not value:
            return None

        if isinstance(value, (datetime, date)):
            return value.strftime("%B, %Y")

        if isinstance(value, str):
            try:
                dt = datetime.strptime(value, "%Y-%m-%d")
                return dt.strftime("%B, %Y")
            except ValueError:
                return value

        if isinstance(value, time):
            return None

        return None

    def leading_thumb(image_url=None):
        return ft.Container(
            width=50,
            height=70,
            alignment=ft.Alignment.CENTER,
            content=(
                ft.Image(
                    src=str(image_url),
                    width=50,
                    height=70,
                    fit=ft.BoxFit.COVER,
                    border_radius=4,
                )
                if image_url
                else ft.Icon(
                    ft.Icons.DESCRIPTION,
                    size=28,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                )
            ),
        )

    def execute_search(index, query=None):
        search_query = query if query else search_field.value.strip()
        if not search_query:
            return

        state["last_query"] = search_query
        state["last_query_per_tab"][index] = search_query

        if index == 0:
            page.run_task(search_series, search_query)
        elif index == 1:
            page.run_task(search_issues, search_query)

    async def search_series(query):
        series_results.controls = [
            ft.ProgressBar(width=400, color=ft.Colors.BLUE_ACCENT, bgcolor="#1a1c1e")
        ]
        page.update()
        await asyncio.sleep(0)

        try:
            results = metron.session.series_list(params={"name": query})
            series_results.controls.clear()

            if not results:
                series_results.controls.append(
                    ft.ListTile(title=ft.Text("No series found."))
                )
            else:
                for i, base in enumerate(results):
                    img = None
                    try:
                        issues = metron.session.issues_list(
                            params={"series_id": base.id, "number": 1}
                        )
                        img = issues[0].image if issues else None
                    except Exception:
                        pass
                    series_results.controls.append(create_series_tile(base, img))

        except Exception as e:
            series_results.controls = [
                ft.ListTile(title=ft.Text(f"Error: {e}", color=ft.Colors.RED))
            ]
        page.update()

    async def search_issues(query):
        issues_results.controls = [
            ft.ProgressBar(width=400, color=ft.Colors.BLUE_ACCENT, bgcolor="#1a1c1e")
        ]
        page.update()
        await asyncio.sleep(0)

        try:
            results = metron.session.issues_list(params={"series_name": query})
            issues_results.controls.clear()
            if not results:
                issues_results.controls.append(
                    ft.ListTile(title=ft.Text("No issues found."))
                )
            else:
                for issue in results:
                    issues_results.controls.append(create_issue_tile(issue))
        except Exception as e:
            issues_results.controls = [
                ft.ListTile(title=ft.Text(f"Error: {e}", color=ft.Colors.RED))
            ]
        page.update()

    def create_series_tile(base, img_url):
        return ft.ListTile(
            leading=leading_thumb(img_url),
            title=ft.Text(base.display_name),
            subtitle=ft.Text(f"{base.issue_count} issues"),
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
            on_click=lambda _, sid=base.id: page.go(
                f"/series/{sid}",
            ),
        )

    def create_issue_tile(issue):
        formatted_date = format_month_year(issue.cover_date)

        return ft.ListTile(
            leading=leading_thumb(issue.image),
            title=ft.Text(issue.issue_name),
            subtitle=ft.Text(formatted_date) if formatted_date else None,
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
            on_click=lambda _: print(f"Clicked Issue {issue.id}"),
        )

    search_field = ft.TextField(
        hint_text="Search the Metron Comic Database",
        prefix_icon=ft.Icon(ft.Icons.SEARCH, size=24),
        suffix_icon=ft.IconButton(ft.Icons.CLEAR_ROUNDED, on_click=handle_clear),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE),
        filled=True,
        border_radius=12,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.Colors.OUTLINE_VARIANT,
        border_width=1.5,
        cursor_color=ft.Colors.BLUE_ACCENT,
        focused_border_color=ft.Colors.OUTLINE,
        focused_border_width=2,
        text_size=16,
        autofocus=True,
        content_padding=ft.Padding(10, 0, 10, 0),
        on_submit=lambda _: execute_search(state["active_tab"]),
    )

    return ft.View(
        route="/search",
        padding=0,
        appbar=ft.AppBar(
            leading=ft.IconButton(
                ft.Icons.ARROW_BACK_SHARP, on_click=lambda _: page.go("/discover")
            ),
            title=search_field,
            center_title=False,
            bgcolor=ft.Colors.SURFACE,
            toolbar_height=70,
        ),
        controls=[
            ft.Tabs(
                expand=True,
                length=4,
                selected_index=0,
                content=ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.TabBar(
                            label_color=ft.Colors.WHITE,
                            unselected_label_color=ft.Colors.OUTLINE,
                            indicator_color=ft.Colors.BLUE_ACCENT,
                            scrollable=True,
                            tab_alignment=ft.TabAlignment.CENTER,
                            on_click=handle_tab_click,
                            tabs=[
                                ft.Tab(label="Series"),
                                ft.Tab(label="Issues"),
                                ft.Tab(label="Characters"),
                                ft.Tab(label="Creators"),
                            ],
                        ),
                        ft.Container(
                            expand=True,
                            content=ft.TabBarView(expand=True, controls=result_columns),  # type: ignore
                        ),
                    ],
                ),
            )
        ],
    )
