import flet as ft
import asyncio

from utilities.utils import GradientWrapper


def home_page(page: ft.Page, navbar: ft.NavigationBar):
    main_content = ft.Column(
        expand=True,
        controls=[
            ft.SafeArea(
                content=ft.Container(
                    padding=ft.Padding.only(top=10, left=20, right=10, bottom=20),
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.SETTINGS,
                                        icon_size=28,
                                        on_click=lambda _: asyncio.create_task(
                                            page.push_route("/settings")
                                        ),
                                    ),
                                ],
                            ),
                            ft.Text("Home", size=32, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Recommendations for you",
                                size=18,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                        ],
                        spacing=5,
                    ),
                )
            ),
            ft.ListView(),
        ],
    )

    return ft.View(
        route="/",
        padding=0,
        navigation_bar=navbar,
        controls=[GradientWrapper(content=main_content, color=ft.Colors.BLUE_ACCENT)],
    )
