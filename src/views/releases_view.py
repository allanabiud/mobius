import flet as ft
from datetime import date, timedelta

from services.metron_service import MetronService


class ReleasesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.list_column = ft.Column(spacing=8, expand=True)

    def build(self):
        self.page.run_thread(self.load_releases)

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Publishers with releases this week",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    padding=ft.Padding(left=20, right=20, top=10, bottom=10),
                ),
                self.list_column,
            ],
            expand=True,
        )

    def load_releases(self):
        # Create MetronService INSIDE the worker thread
        metron = MetronService()

        self.list_column.controls.clear()
        self.list_column.controls.append(ft.ProgressRing())
        self.page.update()

        start, end = self.this_week_range()

        try:
            issues = metron.fetch_with_retry(
                metron.session.issues_list,
                {
                    "publisher_name": "dc",
                    "store_date_range_after": start,
                    "store_date_range_before": end,
                },
            )

            self.list_column.controls.clear()

            if not issues:
                self.list_column.controls.append(
                    ft.Text("No DC releases found this week.")
                )
            else:
                for issue in issues:
                    self.list_column.controls.append(
                        ft.ListTile(
                            title=ft.Text(issue.issue_name),
                            subtitle=ft.Text(f"Issue #{issue.number}"),
                        )
                    )

        except Exception as e:
            self.list_column.controls.clear()
            self.list_column.controls.append(
                ft.Text(f"Failed to load releases: {e}", color=ft.Colors.RED)
            )

        self.page.update()

    @staticmethod
    def this_week_range():
        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start.isoformat(), end.isoformat()
