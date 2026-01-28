import flet as ft
from utilities.formatters import format_month_year, get_issue_title


class IssueCard(ft.Container):
    def __init__(self, issue, mode="grid", on_menu_click=None):
        super().__init__()
        self.issue = issue
        self.mode = mode
        self.on_menu_click = on_menu_click

        if self.mode == "list":
            self.border = ft.Border(bottom=ft.BorderSide(1, "white10"))

        self.padding = ft.Padding.only(right=10) if mode == "list" else 0

        self.title_text = get_issue_title(issue)

        self.status_badges = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.DONE_ALL, color=ft.Colors.OUTLINE_VARIANT, size=16
                    ),
                    ft.Icon(ft.Icons.BOOK, color=ft.Colors.OUTLINE_VARIANT, size=16),
                ],
                spacing=2,
                tight=True,
            ),
            bgcolor="black87",
            padding=2,
            bottom=0,
            right=0,
            border_radius=ft.BorderRadius.only(top_left=4),
        )

        if self.mode == "grid":
            self.content = self._build_grid_view()
        else:
            self.content = self._build_list_view()

    def _build_grid_view(self):
        return ft.Column(
            [
                ft.Stack(
                    [
                        ft.Container(
                            content=ft.Image(
                                src=str(self.issue.image) if self.issue.image else "",
                                fit=ft.BoxFit.FIT_WIDTH,
                                border_radius=4,
                            ),
                            shadow=ft.BoxShadow(blur_radius=10, color="black"),
                        ),
                        self.status_badges,
                    ]
                ),
                ft.Text(
                    self.title_text,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    color="white",
                ),
            ],
            spacing=5,
        )

    def _build_list_view(self):
        raw_date = getattr(self.issue, "store_date", None) or self.issue.cover_date
        formatted_date = format_month_year(raw_date)

        return ft.Row(
            spacing=15,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src=str(self.issue.image) if self.issue.image else "",
                    height=90,
                    width=60,
                    fit=ft.BoxFit.FIT_HEIGHT,
                    border_radius=4,
                ),
                ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=4,
                    controls=[
                        ft.Text(
                            self.title_text,
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color="white",
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(
                            formatted_date if formatted_date else "No Date",
                            size=12,
                            color="white60",
                        ),
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.DONE_ALL, color="white24", size=16),
                                ft.Icon(ft.Icons.BOOK, color="white24", size=16),
                            ],
                            spacing=2,
                        ),
                    ],
                ),
                ft.IconButton(
                    icon=ft.Icons.MORE_VERT,
                    icon_color="white70",
                    icon_size=20,
                    on_click=lambda _: (
                        self.on_menu_click(self.issue) if self.on_menu_click else None
                    ),
                ),
            ],
        )
