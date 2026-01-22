import flet as ft


class SettingsView:
    def __init__(self, page: ft.Page, on_back_click):
        self.page = page
        self.on_back_click = on_back_click

        # State-driven controls
        self.dark_mode_status = ft.Text(
            "On" if page.theme_mode == ft.ThemeMode.DARK else "Off",
            color=ft.Colors.ON_SURFACE_VARIANT,
        )
        self.theme_switch = ft.Switch(
            value=True if page.theme_mode == ft.ThemeMode.DARK else False,
            active_color=ft.Colors.BLUE_ACCENT,
            on_change=self.toggle_theme,
        )

    def section_header(self, title):
        return ft.Container(
            padding=ft.Padding.only(left=20, top=25, bottom=10),
            content=ft.Text(
                title,
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_ACCENT,
                opacity=0.8,
            ),
        )

    def toggle_theme(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.DARK if self.theme_switch.value else ft.ThemeMode.LIGHT
        )
        self.dark_mode_status.value = "On" if self.theme_switch.value else "Off"
        self.page.update()

    def build(self):
        ICON_SIZE = 28

        # Chevron helper
        def chevron():
            return ft.Icon(
                ft.Icons.CHEVRON_RIGHT_ROUNDED, color=ft.Colors.OUTLINE, size=24
            )

        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.SURFACE,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    # Header
                    ft.Container(
                        padding=ft.Padding.only(top=10, left=10, right=20, bottom=5),
                        content=ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_SHARP,
                                    icon_size=24,
                                    on_click=self.on_back_click,
                                ),
                                ft.Text(
                                    "Settings", size=20, weight=ft.FontWeight.W_500
                                ),
                            ]
                        ),
                    ),
                    # Settings List
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            scroll=ft.ScrollMode.ADAPTIVE,
                            spacing=0,
                            controls=[
                                # APPEARANCE
                                self.section_header("Appearance"),
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.DARK_MODE_OUTLINED, size=ICON_SIZE
                                    ),
                                    title=ft.Text("Dark Mode"),
                                    subtitle=self.dark_mode_status,
                                    trailing=self.theme_switch,
                                    toggle_inputs=True,
                                ),
                                # App Settings
                                self.section_header("App Settings"),
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.NOTIFICATIONS_ACTIVE, size=ICON_SIZE
                                    ),
                                    title=ft.Text("Notifications"),
                                    subtitle=ft.Text("Edit Push Notifications "),
                                    trailing=chevron(),
                                    on_click=lambda _: print(
                                        "App Notifications clicked"
                                    ),
                                ),
                                # DATA
                                self.section_header("Data"),
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.SYNC_ROUNDED, size=ICON_SIZE
                                    ),
                                    title=ft.Text("Sync"),
                                    subtitle=ft.Text("Sync data with Metron"),
                                    trailing=chevron(),
                                    on_click=lambda _: print("Sync clicked"),
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.STORAGE_ROUNDED, size=ICON_SIZE
                                    ),
                                    title=ft.Text("Cache Management"),
                                    subtitle=ft.Text("Clear local comic metadata"),
                                    trailing=chevron(),
                                    on_click=lambda _: print("Cache clicked"),
                                ),
                                # ACCOUNT
                                self.section_header("Account"),
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.ACCOUNT_CIRCLE, size=ICON_SIZE
                                    ),
                                    title=ft.Text("Profile"),
                                    subtitle=ft.Text("Edit Metron Profile"),
                                    trailing=chevron(),
                                    on_click=lambda _: print("Profile clicked"),
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.MANAGE_ACCOUNTS, size=ICON_SIZE
                                    ),
                                    title=ft.Text("Account Settings"),
                                    subtitle=ft.Text("Manage Account Preferences"),
                                    trailing=chevron(),
                                    on_click=lambda _: print(
                                        "Account Settings clicked"
                                    ),
                                ),
                                # ABOUT
                                ft.Divider(
                                    height=40,
                                    thickness=1,
                                    color=ft.Colors.OUTLINE_VARIANT,
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.SUPPORT, size=ICON_SIZE),
                                    title=ft.Text("Contact Support"),
                                    trailing=chevron(),
                                    on_click=lambda _: print("Contact Support clicked"),
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.INFO_OUTLINE, size=ICON_SIZE
                                    ),
                                    title=ft.Text("About"),
                                    trailing=chevron(),
                                    on_click=lambda _: print("About clicked"),
                                ),
                                # LOGOUT
                                ft.Container(
                                    # expand=True,
                                    padding=ft.Padding.symmetric(
                                        horizontal=30, vertical=15
                                    ),
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Button(
                                        content=ft.Text(
                                            "Log Out", weight=ft.FontWeight.BOLD
                                        ),
                                        icon=ft.Icons.LOGOUT_ROUNDED,
                                        bgcolor=ft.Colors.BLUE_ACCENT,
                                        color=ft.Colors.WHITE,
                                        height=40,
                                        width=float("inf"),
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                        ),
                                        on_click=lambda _: print("Logout clicked"),
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )
