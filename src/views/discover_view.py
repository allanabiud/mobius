import flet as ft


class DiscoverView:
    def build(self):
        return ft.Column(
            controls=[
                ft.SearchBar(
                    bar_hint_text="Search the Metron Comic Database",
                    bar_leading=ft.Icon(ft.Icons.SEARCH),
                    bar_bgcolor=ft.Colors.TRANSPARENT,
                    bar_border_side=ft.BorderSide(1, ft.Colors.WHITE),
                    bar_shape=ft.RoundedRectangleBorder(radius=5),
                    controls=[],  # Empty for now, will add suggestions later
                ),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
