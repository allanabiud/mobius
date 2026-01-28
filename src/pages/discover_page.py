import flet as ft
import asyncio
from utilities.utils import GradientWrapper


def discover_page(page: ft.Page, navbar: ft.NavigationBar):

    def navigate_to_search(_):
        asyncio.create_task(page.push_route("/search"))

    main_content = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            ft.SafeArea(
                content=ft.Container(
                    padding=ft.Padding.only(top=10, left=20, right=10, bottom=20),
                    content=ft.Column(
                        spacing=5,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.SEARCH,
                                        icon_size=28,
                                        on_click=navigate_to_search,
                                    ),
                                ],
                            ),
                            ft.Text("Discover", size=32, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Explore the Metron Archive",
                                size=18,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                        ],
                    ),
                )
            ),
            ft.ListView(
                expand=True,
                padding=20,
                controls=[
                    ft.Text(
                        "Trending series and publishers will appear here",
                        italic=True,
                        color=ft.Colors.with_opacity(0.6, ft.Colors.ON_SURFACE),
                    )
                ],
            ),
        ],
    )

    return ft.View(
        route="/discover",
        padding=0,
        navigation_bar=navbar,
        controls=[
            GradientWrapper(
                content=main_content,
                color=ft.Colors.YELLOW_ACCENT,
            )
        ],
    )
