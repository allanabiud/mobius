import flet as ft


def discover_page(page: ft.Page, navbar: ft.NavigationBar):
    def on_search_tap(e):
        page.go("/search")

    return ft.View(
        route="/discover",
        padding=0,
        navigation_bar=navbar,
        bgcolor=ft.Colors.SURFACE,
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    stops=[0.0, 0.3, 0.6, 0.9],
                    colors=[
                        ft.Colors.with_opacity(0.25, ft.Colors.YELLOW_ACCENT),
                        ft.Colors.with_opacity(0.12, ft.Colors.YELLOW_ACCENT),
                        ft.Colors.with_opacity(0.03, ft.Colors.YELLOW_ACCENT),
                        ft.Colors.TRANSPARENT,
                    ],
                ),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=0,
                    controls=[
                        ft.Container(
                            padding=ft.Padding.only(
                                top=20, left=20, right=20, bottom=20
                            ),
                            content=ft.SearchBar(
                                bar_hint_text="Search the Metron Comic Database",
                                bar_leading=ft.Icon(ft.Icons.SEARCH, size=28),
                                bar_bgcolor=ft.Colors.with_opacity(
                                    0.5, ft.Colors.SURFACE
                                ),
                                bar_border_side=ft.BorderSide(
                                    1.5, ft.Colors.OUTLINE_VARIANT
                                ),
                                bar_shape=ft.RoundedRectangleBorder(radius=10),
                                height=55,
                                on_tap=on_search_tap,
                                on_focus=on_search_tap,
                            ),
                        ),
                        ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[],
                        ),
                    ],
                ),
            )
        ],
    )
