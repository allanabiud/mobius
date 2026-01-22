import flet as ft


class DiscoverView:
    def __init__(self, page: ft.Page, on_search_click):
        self.page = page
        self.on_search_click = on_search_click

    def build(self):
        return ft.Container(
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
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Container(
                        padding=ft.Padding.only(top=20, left=20, right=20, bottom=20),
                        content=ft.SearchBar(
                            bar_hint_text="Search the Metron Comic Database",
                            bar_leading=ft.Icon(ft.Icons.SEARCH, size=28),
                            bar_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.SURFACE),
                            bar_border_side=ft.BorderSide(
                                1.5, ft.Colors.OUTLINE_VARIANT
                            ),
                            bar_shape=ft.RoundedRectangleBorder(radius=10),
                            height=55,
                            on_tap=self.on_search_click,
                            controls=[],
                        ),
                    ),
                    # Discover content (Categories, Trending, Reading Lists, etc.) goes here
                ],
            ),
        )
