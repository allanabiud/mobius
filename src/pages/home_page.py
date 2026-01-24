import flet as ft


def home_page(page: ft.Page, navbar: ft.NavigationBar):
    return ft.View(
        route="/",
        padding=0,
        navigation_bar=navbar,
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    colors=[
                        ft.Colors.with_opacity(0.25, ft.Colors.BLUE_ACCENT),
                        ft.Colors.TRANSPARENT,
                    ],
                ),
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=ft.Padding.only(right=10, top=5),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.SETTINGS,
                                        on_click=lambda _: page.go("/settings"),
                                    ),
                                    ft.IconButton(icon=ft.Icons.ACCOUNT_CIRCLE),
                                ],
                            ),
                        ),
                        ft.Container(
                            padding=20,
                            content=ft.Column(
                                [
                                    ft.Text("Home", size=32, weight=ft.FontWeight.BOLD),
                                    ft.Text(
                                        "Recommendations for you",
                                        size=18,
                                        color=ft.Colors.ON_SURFACE_VARIANT,
                                    ),
                                ]
                            ),
                        ),
                        ft.ListView(
                            expand=True,
                            padding=20,
                            controls=[ft.Text("Recommendations will appear here")],
                        ),
                    ],
                ),
            )
        ],
    )
