import flet as ft

# import asyncio
from services.metron_service import MetronService


def series_page(page: ft.Page, series_id: int):
    metron = MetronService()

    loader = ft.ProgressBar(
        visible=True,
        color=ft.Colors.BLUE_ACCENT,
        bgcolor="#1a1c1e",
    )

    hero_image = ft.Image(
        src="",
        fit=ft.BoxFit.COVER,
        opacity=0.4,
        width=float("inf"),
        visible=False,
    )

    pub_info_text = ft.Text("", size=14, color="white70")

    series_name_text = ft.Text(
        "",
        size=32,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    overview_column = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        spacing=0,
    )

    issues_grid = ft.GridView(
        expand=True,
        runs_count=4,
        child_aspect_ratio=0.5,
        spacing=5,
        run_spacing=10,
        padding=10,
    )

    def info_item(label: str, value: str | None):
        return ft.Column(
            [
                ft.Text(
                    label.upper(),
                    size=12,
                    color=ft.Colors.BLUE_ACCENT,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(value or "N/A", size=15, color=ft.Colors.WHITE),
            ],
            spacing=2,
        )

    def issue_card(issue):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Image(
                            src=str(issue.image) if issue.image else "",
                            fit=ft.BoxFit.FIT_WIDTH,
                            border_radius=4,
                        ),
                        shadow=ft.BoxShadow(blur_radius=10, color="black"),
                    ),
                    ft.Text(
                        (
                            f"{issue.series.name} #{issue.number}"
                            if issue.series and issue.series.name
                            else f"Issue #{issue.number}"
                        ),
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        color="white",
                    ),
                ],
                spacing=5,
            ),
            on_click=lambda _: print(f"Clicked issue {issue.id}"),
        )

    async def load_details():
        loader.visible = True
        page.update()

        try:
            series = metron.session.series(series_id)
            issues = metron.session.issues_list(params={"series_id": series_id})

            series_name_text.value = series.name
            pub_info_text.value = series.publisher.name if series.publisher else ""

            if issues and issues[0].image:
                hero_image.src = str(issues[0].image)
                hero_image.visible = True

            overview_column.controls = [
                ft.Container(
                    padding=ft.Padding.only(left=20, top=20, right=20, bottom=10),
                    content=ft.Column(
                        [
                            ft.Text(
                                "SUMMARY",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_ACCENT,
                            ),
                            ft.Text(
                                series.desc or "No description available.",
                                size=15,
                                color="white",
                            ),
                        ],
                        spacing=10,
                    ),
                ),
                ft.Divider(height=1, color="white10"),
                ft.Container(
                    padding=20,
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    info_item("Status", series.status),
                                    info_item(
                                        "Series Type",
                                        (
                                            series.series_type.name
                                            if series.series_type
                                            else None
                                        ),
                                    ),
                                    info_item(
                                        "Genres",
                                        (
                                            ", ".join(g.name for g in series.genres)
                                            if series.genres
                                            else None
                                        ),
                                    ),
                                ],
                                expand=1,
                                spacing=20,
                            ),
                            ft.Column(
                                [
                                    info_item(
                                        "Publisher",
                                        (
                                            series.publisher.name
                                            if series.publisher
                                            else None
                                        ),
                                    ),
                                    info_item("Year Began", str(series.year_began)),
                                    info_item(
                                        "Year Ended",
                                        (
                                            str(series.year_end)
                                            if series.year_end
                                            else "Present"
                                        ),
                                    ),
                                ],
                                expand=1,
                                spacing=20,
                            ),
                        ],
                    ),
                ),
            ]

            issues_grid.controls = [issue_card(i) for i in issues]

        except Exception as e:
            overview_column.controls = [ft.Text(f"Error: {e}", color=ft.Colors.RED)]

        finally:
            loader.visible = False
            page.update()

    page.run_task(load_details)

    header = ft.Stack(
        height=220,
        controls=[
            ft.Container(bgcolor="#2a2c2e", content=hero_image),
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    colors=[ft.Colors.TRANSPARENT, "#1a1c1E"],
                ),
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color="white",
                            # on_click=lambda _: page.go("/search"),
                            on_click=lambda _: page.on_view_pop(ft.ViewPopEvent(page.views[-1])),  # type: ignore
                        ),
                        ft.Container(expand=True),
                        pub_info_text,
                        series_name_text,
                    ],
                    spacing=5,
                ),
            ),
        ],
    )

    return ft.View(
        route=f"/series/{series_id}",
        bgcolor=ft.Colors.SURFACE,
        padding=0,
        spacing=0,
        controls=[
            ft.Tabs(
                expand=True,
                length=2,
                content=ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        loader,
                        header,
                        ft.TabBar(
                            indicator_color=ft.Colors.BLUE_ACCENT,
                            scrollable=False,
                            tab_alignment=ft.TabAlignment.FILL,
                            tabs=[
                                ft.Tab(label="OVERVIEW"),
                                ft.Tab(label="ISSUES"),
                            ],
                        ),
                        ft.TabBarView(
                            expand=True,
                            controls=[
                                overview_column,
                                issues_grid,
                            ],
                        ),
                    ],
                ),
            )
        ],
    )
