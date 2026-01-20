import flet as ft


class MyLibraryView:
    def build(self):
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Your collection of comics will appear here."),
                    padding=ft.Padding(left=20, right=20, top=0, bottom=0),
                ),
            ],
            expand=True,
        )
