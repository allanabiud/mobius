import flet as ft


class SeriesOverview(ft.Column):
    def __init__(self):
        super().__init__(
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=0,
            visible=False,
        )

    def _info_item(self, label: str, value: str | None):
        return ft.Column(
            [
                ft.Text(
                    label.upper(),
                    size=12,
                    color=ft.Colors.BLUE_ACCENT,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(value or "N/A", size=15, color=ft.Colors.WHITE),
            ],
            spacing=2,
        )

    def update_series(self, series):
        """Populates the UI with Metron series data."""
        self.controls = [
            ft.Container(
                padding=ft.Padding.only(left=20, top=20, right=20, bottom=10),
                content=ft.Column(
                    [
                        ft.Text(
                            "SUMMARY",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_ACCENT,
                        ),
                        ft.Text(
                            series.desc or "No description available.",
                            size=15,
                            color="white",
                        ),
                    ],
                    spacing=10,
                ),
            ),
            ft.Divider(height=1, color="white10"),
            ft.Container(
                padding=20,
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                self._info_item("Status", series.status),
                                self._info_item(
                                    "Series Type",
                                    (
                                        series.series_type.name
                                        if series.series_type
                                        else None
                                    ),
                                ),
                                self._info_item(
                                    "Genres",
                                    (
                                        ", ".join(g.name for g in series.genres)
                                        if series.genres
                                        else None
                                    ),
                                ),
                            ],
                            expand=1,
                            spacing=20,
                        ),
                        ft.Column(
                            [
                                self._info_item(
                                    "Publisher",
                                    series.publisher.name if series.publisher else None,
                                ),
                                self._info_item("Year Began", str(series.year_began)),
                                self._info_item(
                                    "Year Ended",
                                    (
                                        str(series.year_end)
                                        if series.year_end
                                        else "Present"
                                    ),
                                ),
                            ],
                            expand=1,
                            spacing=20,
                        ),
                    ]
                ),
            ),
            ft.Divider(height=1, color="white10"),
            ft.Container(
                padding=ft.Padding.only(left=20, top=10, right=20, bottom=20),
                content=ft.Column(
                    [
                        ft.Text(
                            "EXTERNAL DATA",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_ACCENT,
                        ),
                        ft.Row(
                            [
                                self._info_item(
                                    "Comic Vine ID",
                                    str(series.cv_id) if series.cv_id else "N/A",
                                ),
                                self._info_item(
                                    "GCD ID",
                                    str(series.gcd_id) if series.gcd_id else "N/A",
                                ),
                            ],
                            spacing=40,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "METRON",
                                    size=12,
                                    color=ft.Colors.BLUE_ACCENT,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    value=(
                                        str(series.resource_url)
                                        if series.resource_url
                                        else "N/A"
                                    ),
                                    size=13,
                                    color=ft.Colors.BLUE_200,
                                    italic=True,
                                    selectable=True,
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=15,
                ),
            ),
        ]
        self.visible = True
        self.update()
