import flet as ft


class ActionCard(ft.Container):
    def __init__(
        self,
        icon: ft.IconData,
        color: str,
        count_control: ft.Control,
        label: str,
        on_click=None,
    ):
        super().__init__()
        self.expand = 1
        self.height = 110
        self.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.SURFACE)
        self.border_radius = 12
        self.padding = 10
        self.alignment = ft.Alignment.CENTER
        self.on_click = on_click if on_click else lambda _: None

        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=2,
            controls=[
                (
                    ft.Icon(icon=icon, color=color, size=24)
                    if isinstance(icon, str)
                    else ft.Icon(icon, color=color, size=24)
                ),
                count_control,
                ft.Text(label, size=13, color=ft.Colors.ON_SURFACE),
            ],
        )
