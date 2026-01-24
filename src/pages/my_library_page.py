import flet as ft


def my_library_page(page: ft.Page, navbar: ft.NavigationBar):
    return ft.View(
        route="/library",
        padding=0,
        navigation_bar=navbar,
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    stops=[0.0, 0.3, 0.6, 0.9],
                    colors=[
                        ft.Colors.with_opacity(0.25, ft.Colors.ORANGE_ACCENT),
                        ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_ACCENT),
                        ft.Colors.with_opacity(0.03, ft.Colors.ORANGE_ACCENT),
                        ft.Colors.TRANSPARENT,
                    ],
                ),
                content=ft.Column(
                    expand=True,
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        ft.SafeArea(
                            content=ft.Container(
                                padding=ft.Padding.only(
                                    top=40, left=20, right=20, bottom=20
                                ),
                                content=ft.Column(
                                    spacing=6,
                                    controls=[
                                        ft.Text(
                                            "My Library",
                                            size=28,
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
                                    ft.Text(
                                        "Your collection of comics will appear here."
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
