import flet as ft


class ListManager(ft.Column):
    def __init__(self, card_type, on_item_menu_click):
        super().__init__(expand=True, spacing=0, visible=False)
        self.card_type = card_type
        self.on_item_menu_click = on_item_menu_click

        self.items = []
        self.view_mode = "list"
        self.sort_ascending = True

        self.display_container = ft.Container(expand=True)

        self.sort_btn = ft.IconButton(
            icon=ft.Icons.SORT_ROUNDED,
            icon_color=ft.Colors.OUTLINE_VARIANT,
            on_click=self.toggle_sort,
            tooltip="Sort Items",
        )

        self.toggle_btn = ft.IconButton(
            icon=ft.Icons.LIST_ALT_ROUNDED,
            icon_color=ft.Colors.OUTLINE_VARIANT,
            on_click=self.toggle_view,
            tooltip="Switch View Mode",
        )

        self.controls = [
            ft.Container(
                bgcolor=ft.Colors.TRANSPARENT,
                padding=ft.Padding.only(left=10, right=5),
                content=ft.Row(
                    controls=[
                        ft.Container(expand=True),
                        ft.Row([self.sort_btn, self.toggle_btn], spacing=0),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ),
            self.display_container,
        ]

    def toggle_view(self, e):
        self.view_mode = "list" if self.view_mode == "grid" else "grid"
        self.render()

    def toggle_sort(self, e):
        self.sort_ascending = not self.sort_ascending
        self.sort_btn.icon = (
            ft.Icons.SORT_ROUNDED
            if self.sort_ascending
            else ft.Icons.SORT_BY_ALPHA_ROUNDED
        )
        self.render()

    def set_items(self, new_items):
        self.items = new_items if new_items else []
        self.render()

    def render(self):
        sorted_list = sorted(
            self.items,
            key=lambda x: (
                int(x.number) if hasattr(x, "number") and str(x.number).isdigit() else 0
            ),
            reverse=not self.sort_ascending,
        )
        self.visible = True

        if self.view_mode == "grid":
            self.display_container.content = ft.GridView(
                controls=[
                    self.card_type(
                        i, mode="grid", on_menu_click=self.on_item_menu_click
                    )
                    for i in sorted_list
                ],
                runs_count=4,
                child_aspect_ratio=0.5,
                spacing=5,
                run_spacing=10,
                padding=10,
            )
            self.toggle_btn.icon = ft.Icons.LIST_ALT_ROUNDED
        else:
            self.display_container.content = ft.ListView(
                controls=[
                    self.card_type(
                        i, mode="list", on_menu_click=self.on_item_menu_click
                    )
                    for i in sorted_list
                ],
                padding=0,
                spacing=0,
            )
            self.toggle_btn.icon = ft.Icons.GRID_VIEW_ROUNDED

        self.update()
