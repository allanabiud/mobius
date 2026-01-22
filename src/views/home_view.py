import flet as ft


class HomeView:
    def __init__(self, page: ft.Page, on_settings_click):
        self.page = page
        self.on_settings_click = on_settings_click

    def build(self):
        return ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_CENTER,
                end=ft.Alignment.BOTTOM_CENTER,
                stops=[0.0, 0.3, 0.6, 0.9],
                colors=[
                    ft.Colors.with_opacity(0.25, ft.Colors.BLUE_ACCENT),
                    ft.Colors.with_opacity(0.12, ft.Colors.BLUE_ACCENT),
                    ft.Colors.with_opacity(0.03, ft.Colors.BLUE_ACCENT),
                    ft.Colors.TRANSPARENT,
                ],
            ),
            content=ft.Column(
                expand=True,
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    # AppBar
                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            spacing=15,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icon(ft.Icons.SETTINGS, size=26),
                                    on_click=self.on_settings_click,
                                ),
                                ft.IconButton(
                                    icon=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=26),
                                    on_click=lambda _: print("Profile clicked"),
                                ),
                            ],
                        ),
                        padding=ft.Padding.only(right=10, top=5),
                    ),
                    # Welcome / Title Section
                    ft.Container(
                        padding=ft.Padding.only(top=0, left=20, right=20, bottom=20),
                        content=ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text("Home", size=32, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    "Recommendations for you",
                                    size=18,
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                ),
                            ],
                        ),
                    ),
                    # Main Content Area
                    ft.Container(
                        expand=True,
                        padding=ft.Padding.symmetric(horizontal=20),
                        content=ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.ADAPTIVE,
                            controls=[
                                ft.Text("Recommendations will appear here", size=16),
                            ],
                        ),
                    ),
                ],
            ),
        )
