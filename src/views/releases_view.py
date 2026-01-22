import flet as ft
from services.metron_service import MetronService
import datetime


class ReleasesView:
    _weekly_cache = {}

    def __init__(self, page: ft.Page):
        self.page = page
        self.metron = MetronService()
        self.new_comics_count = ft.Text("...", size=28, weight=ft.FontWeight.BOLD)
        self.debut_issues_count = ft.Text("...", size=28, weight=ft.FontWeight.BOLD)
        self.pull_list_count = ft.Text("...", size=28, weight=ft.FontWeight.BOLD)

    def create_action_card(self, content, on_click=None):
        """Helper to create consistent clickable cards"""
        return ft.Container(
            content=content,
            expand=1,
            height=120,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.SURFACE_CONTAINER_LOWEST),
            border_radius=12,
            padding=15,
            alignment=ft.Alignment.CENTER,
            on_click=on_click if on_click else lambda _: print("Card clicked"),
        )

    def build(self):
        # Trigger the data fetch
        self.update_releases_count()

        return ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_CENTER,
                end=ft.Alignment.BOTTOM_CENTER,
                stops=[0.0, 0.3, 0.6, 0.9],
                colors=[
                    ft.Colors.with_opacity(0.25, ft.Colors.GREEN_ACCENT),
                    ft.Colors.with_opacity(0.12, ft.Colors.GREEN_ACCENT),
                    ft.Colors.with_opacity(0.03, ft.Colors.GREEN_ACCENT),
                    ft.Colors.TRANSPARENT,
                ],
            ),
            content=ft.Column(
                expand=True,
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    # Title & Subtitle Area
                    ft.Container(
                        padding=ft.Padding.only(top=40, left=20, right=20, bottom=30),
                        content=ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text("Releases", size=28, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    "Discover new comics",
                                    size=18,
                                    color=ft.Colors.ON_SURFACE,
                                ),
                            ],
                        ),
                    ),
                    # Row of Action Cards
                    ft.Container(
                        padding=ft.Padding.only(left=20, right=20, bottom=20),
                        content=ft.Row(
                            spacing=10,
                            controls=[
                                # Card 1: Total
                                self.create_action_card(
                                    content=self._card_layout(
                                        ft.Icons.CALENDAR_TODAY_OUTLINED,
                                        ft.Colors.BLUE_ACCENT,
                                        self.new_comics_count,
                                        "New Comics",
                                    )
                                ),
                                # Card 2: #1s
                                self.create_action_card(
                                    content=self._card_layout(
                                        ft.Icons.LOOKS_ONE_OUTLINED,
                                        ft.Colors.YELLOW_ACCENT,
                                        self.debut_issues_count,
                                        "New #1's",
                                    )
                                ),
                                # Card 3: Pull List (Personalized)
                                self.create_action_card(
                                    content=self._card_layout(
                                        ft.Icons.DOWNLOADING_OUTLINED,
                                        ft.Colors.GREEN_ACCENT,
                                        self.pull_list_count,
                                        "Your Pulls",
                                    )
                                ),
                            ],
                        ),
                    ),
                    # Scrollable content area
                    ft.Container(
                        expand=True,
                        padding=ft.Padding.symmetric(horizontal=20),
                        content=ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.ADAPTIVE,
                            spacing=12,
                            controls=[
                                # List of comic issues will go here
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _card_layout(self, icon, color, count_control, label):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=2,
            controls=[
                ft.Icon(icon, color=color, size=24),
                count_control,
                ft.Text(label, size=13, color=ft.Colors.ON_SURFACE),
            ],
        )

    def update_releases_count(self):
        try:
            start, end, _ = self.comic_week_range(datetime.date.today())

            all_week_issues = self.metron.fetch_with_retry(
                self.metron.session.issues_list,
                {
                    "store_date_range_after": start,
                    "store_date_range_before": end,
                },
            )

            missing_series_list = self.metron.session.collection_missing_series()
            missing_series_names = {s.name for s in missing_series_list}

            if all_week_issues:
                # Total
                self.new_comics_count.value = str(len(all_week_issues))

                # New #1s
                self.debut_issues_count.value = str(
                    len([i for i in all_week_issues if i.number == "1"])
                )

                # Your Pulls
                pulls = [
                    i for i in all_week_issues if i.series.name in missing_series_names
                ]
                self.pull_list_count.value = str(len(pulls))

            self.page.update()

        except Exception as e:
            print(f"Error in optimized fetch: {e}")
            self.new_comics_count.value = "0"
            self.debut_issues_count.value = "0"
            self.pull_list_count.value = "0"
            self.page.update()

    @staticmethod
    def comic_week_range(target_date: datetime.date):
        """
        Returns:
        - start (Sunday, ISO string)
        - end (Saturday, ISO string)
        - wednesday_date (datetime.date)
        """

        # Python weekday(): Monday=0 ... Sunday=6
        days_since_sunday = (target_date.weekday() + 1) % 7
        sunday = target_date - datetime.timedelta(days=days_since_sunday)

        wednesday = sunday + datetime.timedelta(days=3)
        saturday = sunday + datetime.timedelta(days=6)

        return sunday.isoformat(), saturday.isoformat(), wednesday
