import flet as ft


class SearchView:
    def __init__(self, page: ft.Page, on_back_click):
        self.page = page
        self.on_back_click = on_back_click

        self.series_results = ft.Column(expand=True, scroll=ft.ScrollMode.ADAPTIVE)
        self.issues_results = ft.Column(expand=True, scroll=ft.ScrollMode.ADAPTIVE)
        self.character_results = ft.Column(expand=True, scroll=ft.ScrollMode.ADAPTIVE)
        self.creator_results = ft.Column(expand=True, scroll=ft.ScrollMode.ADAPTIVE)

        self.search_field = ft.TextField(
            hint_text="Search the Metron Comic Database",
            prefix_icon=ft.Icon(ft.Icons.SEARCH, size=28),
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.SURFACE),
            filled=True,
            # Border Styling
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.OUTLINE_VARIANT,
            border_width=1.5,
            # Cursor styling
            cursor_color=ft.Colors.YELLOW_ACCENT,
            # Focus Styling
            focused_border_color=ft.Colors.OUTLINE,
            focused_border_width=2,
            border_radius=10,
            text_size=18,
            autofocus=True,
            expand=True,
            on_submit=self.handle_search_submit,
        )

    def build(self):
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.SURFACE,
            content=ft.Tabs(
                length=4,
                selected_index=0,
                animation_duration=300,
                on_change=self.handle_tab_change,
                content=ft.Column(
                    expand=True,
                    spacing=10,
                    controls=[
                        # Search Header
                        ft.Container(
                            padding=ft.Padding.only(
                                top=10, left=10, right=20, bottom=5
                            ),
                            content=ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK_SHARP,
                                        icon_size=24,
                                        on_click=self.on_back_click,
                                    ),
                                    self.search_field,
                                ]
                            ),
                        ),
                        # TabBar
                        ft.TabBar(
                            label_color=ft.Colors.WHITE,
                            unselected_label_color=ft.Colors.OUTLINE,
                            indicator_color=ft.Colors.YELLOW_ACCENT,
                            tabs=[
                                ft.Tab(label="Series"),
                                ft.Tab(label="Issues"),
                                ft.Tab(label="Characters"),
                                ft.Tab(label="Creators"),
                            ],
                            scrollable=False,
                            tab_alignment=ft.TabAlignment.FILL,
                        ),
                        # TabBarView
                        ft.TabBarView(
                            expand=True,
                            controls=[
                                self.series_results,
                                self.issues_results,
                                self.character_results,
                                self.creator_results,
                            ],
                        ),
                    ],
                ),
            ),
        )

    def handle_tab_change(self, e):
        # e.data contains the index of the selected tab
        if self.search_field.value:
            self.execute_search(int(e.data))

    def handle_search_submit(self, e):
        # Trigger search for current active tab
        # We access the selected_index from the parent Tabs control
        # (This usually requires a reference to the Tabs object)
        pass

    def execute_search(self, index):
        # Map index to the correct result column
        target_columns = [
            self.series_results,
            self.issues_results,
            self.character_results,
            self.creator_results,
        ]
        active_column = target_columns[index]

        query = self.search_field.value

        active_column.controls = [
            ft.ListTile(title=ft.Text(f"Searching for {query}..."))
        ]
        self.page.update()
