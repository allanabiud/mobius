import flet as ft


class SeriesManagementSheet(ft.BottomSheet):
    def __init__(self, page: ft.Page, on_submit=None):
        super().__init__(content=ft.Container(), scrollable=True)
        self.main_page = page
        self.on_submit = on_submit

        self.title_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD)

        self.action_dropdown = ft.Dropdown(
            label="Action",
            options=[
                ft.dropdown.Option("Add", "Add to Collection"),
                ft.dropdown.Option("Remove", "Remove from Collection"),
                ft.dropdown.Option("Mark", "Mark as Read"),
            ],
            value="Add",
            on_select=self.handle_action_change,
        )

        self.selection_type = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="all", label="All Issues"),
                    ft.Radio(value="range", label="Range"),
                ]
            ),
            value="all",
            on_change=lambda e: self.update_range_visibility(e.data == "range"),
        )

        self.start_input = ft.TextField(
            label="Start #", expand=True, keyboard_type=ft.KeyboardType.NUMBER
        )
        self.end_input = ft.TextField(
            label="End #", expand=True, keyboard_type=ft.KeyboardType.NUMBER
        )
        self.range_inputs = ft.Row([self.start_input, self.end_input], visible=False)

        self.format_selector = ft.Dropdown(
            label="Format",
            options=[
                ft.dropdown.Option("Print"),
                ft.dropdown.Option("Digital"),
                ft.dropdown.Option("Both"),
            ],
            value="Print",
        )

        self.dynamic_content = ft.Column(spacing=15)
        self.confirm_btn = ft.FilledButton(
            "Confirm",
            bgcolor=ft.Colors.BLUE_ACCENT,
            color="white",
            on_click=self.handle_confirm,
        )

        self.content = ft.Container(
            padding=20,
            content=ft.Column(
                [
                    self.title_text,
                    ft.Divider(height=5),
                    self.action_dropdown,
                    self.dynamic_content,
                    ft.Divider(height=5),
                    ft.Row(
                        [
                            ft.TextButton("Cancel", on_click=self.close),
                            self.confirm_btn,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                tight=True,
            ),
        )
        self.update_ui_for_action("Add")

    def update_range_visibility(self, is_visible):
        self.range_inputs.visible = is_visible
        self.update()

    def handle_action_change(self, e):
        self.update_ui_for_action(e.data)
        self.update()

    def update_ui_for_action(self, action):
        self.dynamic_content.controls = [
            ft.Text(f"Select issues to {action.lower()}:", size=14, color="white70"),
            self.selection_type,
            self.range_inputs,
            self.format_selector if action == "Add" else ft.Container(),
        ]
        self.confirm_btn.content = f"{action} Issues"
        self.confirm_btn.bgcolor = (
            ft.Colors.BLUE_ACCENT
            if action == "Add"
            else ft.Colors.RED_700 if action == "Remove" else ft.Colors.GREEN_700
        )

    def show(self, series_name):
        self.title_text.value = series_name
        self.open = True
        self.update()

    def handle_confirm(self, e):
        if self.on_submit:
            self.on_submit(
                {
                    "action": self.action_dropdown.value,
                    "type": self.selection_type.value,
                    "start": self.start_input.value,
                    "end": self.end_input.value,
                    "format": self.format_selector.value,
                }
            )
        self.close()

    def close(self, e=None):
        self.open = False
        self.update()


class IssueManagementSheet(ft.BottomSheet):
    def __init__(self, page: ft.Page, on_submit=None):
        super().__init__(content=ft.Container())
        self.main_page = page
        self.on_submit = on_submit

        self.title_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD)

        # Toggle Buttons logic
        self.btn_collected = self._create_toggle_btn(
            ft.Icons.BOOK_OUTLINED, ft.Icons.BOOK, ft.Colors.ORANGE_ACCENT, "Collected"
        )
        self.btn_read = self._create_toggle_btn(
            ft.Icons.DONE_ALL_OUTLINED,
            ft.Icons.DONE_ALL,
            ft.Colors.GREEN_ACCENT,
            "Read",
        )

        self.content = ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    self.title_text,
                    ft.Divider(height=5),
                    ft.Row(
                        [
                            self._labeled_toggle(self.btn_collected, "Collected"),
                            self._labeled_toggle(self.btn_read, "Read"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=40,
                    ),
                    ft.Divider(height=5),
                    ft.Row(
                        [
                            ft.OutlinedButton(
                                "Share",
                                icon=ft.Icons.SHARE,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=5),
                    ft.Row(
                        [
                            ft.TextButton("Cancel", on_click=self.close),
                            ft.FilledButton(
                                "Update",
                                bgcolor=ft.Colors.BLUE_ACCENT,
                                color="white",
                                on_click=self.handle_confirm,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                tight=True,
                spacing=15,
            ),
        )

    def _create_toggle_btn(self, icon, sel_icon, color, tip):
        return ft.IconButton(
            icon=icon,
            selected_icon=sel_icon,
            icon_size=38,
            selected_icon_color=color,
            tooltip=tip,
            on_click=self.toggle_btn,
        )

    def _labeled_toggle(self, btn, label):
        return ft.Column(
            [btn, ft.Text(label, size=12)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def toggle_btn(self, e):
        e.control.selected = not e.control.selected
        e.control.update()

    def show(self, title, is_collected=False, is_read=False):
        self.title_text.value = title
        self.btn_collected.selected = is_collected
        self.btn_read.selected = is_read
        self.open = True
        self.update()

    def handle_confirm(self, e):
        if self.on_submit:
            self.on_submit(self.btn_collected.selected, self.btn_read.selected)
        self.close()

    def close(self, e=None):
        self.open = False
        self.update()
