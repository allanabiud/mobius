import flet as ft

from utilities.utils import GradientWrapper


def my_library_page(page: ft.Page, navbar: ft.NavigationBar):
    main_content = ft.Column(
        expand=True,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.SafeArea(
                content=ft.Container(
                    padding=ft.Padding.only(top=60, left=20, right=20, bottom=20),
                    content=ft.Column(
                        spacing=6,
                        controls=[
                            ft.Text(
                                "My Library",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Your collection and reading lists",
                                size=18,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                        ],
                    ),
                )
            ),
            ft.Container(
                expand=True,
                padding=ft.Padding.symmetric(horizontal=20),
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    spacing=12,
                    controls=[
                        ft.Text("Your collection of comics will appear here."),
                    ],
                ),
            ),
        ],
    )

    return ft.View(
        route="/library",
        padding=0,
        navigation_bar=navbar,
        controls=[GradientWrapper(content=main_content, color=ft.Colors.ORANGE_ACCENT)],
    )
