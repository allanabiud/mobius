import flet as ft
import datetime
from services.metron_service import MetronService


def releases_page(page: ft.Page, navbar: ft.NavigationBar):
    metron = MetronService()

    new_comics_count = ft.Container(
        content=ft.ProgressRing(width=20, height=20, stroke_width=2),
        alignment=ft.Alignment.CENTER,
    )
    debut_issues_count = ft.Container(
        content=ft.ProgressRing(width=20, height=20, stroke_width=2),
        alignment=ft.Alignment.CENTER,
    )
    pull_list_count = ft.Container(
        content=ft.ProgressRing(
            width=20, height=20, stroke_width=2, color=ft.Colors.BLUE_ACCENT
        ),
        alignment=ft.Alignment.CENTER,
    )

    def _card_layout(icon, color, count_control, label):
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

    def create_action_card(content, on_click=None):
        return ft.Container(
            content=content,
            expand=1,
            height=110,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.SURFACE),
            border_radius=12,
            padding=10,
            alignment=ft.Alignment.CENTER,
            on_click=on_click if on_click else lambda _: print("Card clicked"),
        )

    async def update_releases_count():
        try:
            target_date = datetime.date.today()
            days_since_sunday = (target_date.weekday() + 1) % 7
            sunday = target_date - datetime.timedelta(days=days_since_sunday)
            start = sunday.isoformat()
            end = (sunday + datetime.timedelta(days=6)).isoformat()

            all_week_issues = metron.fetch_with_retry(
                metron.session.issues_list,
                {
                    "store_date_range_after": start,
                    "store_date_range_before": end,
                },
            )

            missing_series_list = metron.session.collection_missing_series()
            missing_series_names = {s.name for s in missing_series_list}

            if all_week_issues:
                new_comics_count.content = ft.Text(
                    str(len(all_week_issues)), size=26, weight=ft.FontWeight.BOLD
                )
                debut_issues_count.content = ft.Text(
                    str(len([i for i in all_week_issues if i.number == "1"])),
                    size=26,
                    weight=ft.FontWeight.BOLD,
                )
                pulls = [
                    i for i in all_week_issues if i.series.name in missing_series_names
                ]
                pull_list_count.content = ft.Text(
                    str(len(pulls)), size=26, weight=ft.FontWeight.BOLD
                )

            page.update()
        except Exception as e:
            print(f"Error in fetching releases: {e}")

    view = ft.View(
        route="/releases",
        padding=0,
        navigation_bar=navbar,
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    stops=[0.0, 0.4, 1.0],
                    colors=[
                        ft.Colors.with_opacity(0.2, ft.Colors.GREEN_ACCENT),
                        ft.Colors.with_opacity(0.05, ft.Colors.GREEN_ACCENT),
                        ft.Colors.TRANSPARENT,
                    ],
                ),
                content=ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.SafeArea(
                            content=ft.Container(
                                padding=ft.Padding.only(
                                    left=20, right=20, top=40, bottom=20
                                ),
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "Releases",
                                            size=32,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            "Discover new comics",
                                            size=16,
                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                        ),
                                    ],
                                    spacing=2,
                                ),
                            )
                        ),
                        ft.Container(
                            padding=ft.Padding.symmetric(horizontal=20),
                            content=ft.Row(
                                spacing=10,
                                controls=[
                                    create_action_card(
                                        _card_layout(
                                            ft.Icons.CALENDAR_TODAY_OUTLINED,
                                            ft.Colors.BLUE_ACCENT,
                                            new_comics_count,
                                            "New Comics",
                                        )
                                    ),
                                    create_action_card(
                                        _card_layout(
                                            ft.Icons.LOOKS_ONE_OUTLINED,
                                            ft.Colors.YELLOW_ACCENT,
                                            debut_issues_count,
                                            "New #1s",
                                        )
                                    ),
                                    create_action_card(
                                        _card_layout(
                                            ft.Icons.DOWNLOADING_OUTLINED,
                                            ft.Colors.GREEN_ACCENT,
                                            pull_list_count,
                                            "Your Pulls",
                                        )
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            padding=ft.Padding.only(top=20, left=20, right=20),
                            content=ft.Column(
                                scroll=ft.ScrollMode.ADAPTIVE,
                                controls=[
                                    ft.Text(
                                        "This Week's Catalog",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )

    page.run_task(update_releases_count)
    return view
