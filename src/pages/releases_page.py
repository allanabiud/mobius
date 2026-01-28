import flet as ft
from services.metron_service import MetronService
from utilities.utils import GradientWrapper
from .components.action_card import ActionCard


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

    async def update_releases_count():
        try:
            stats = metron.get_weekly_releases_stats()

            new_comics_count.content = ft.Text(
                str(stats["total"]), size=26, weight=ft.FontWeight.BOLD
            )
            debut_issues_count.content = ft.Text(
                str(stats["debuts"]), size=26, weight=ft.FontWeight.BOLD
            )
            pull_list_count.content = ft.Text(
                str(stats["pulls"]), size=26, weight=ft.FontWeight.BOLD
            )

            page.update()
        except Exception as e:
            print(f"Error: {e}")

    main_content = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            ft.SafeArea(
                content=ft.Container(
                    padding=ft.Padding.only(top=60, left=20, right=20, bottom=20),
                    content=ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("Releases", size=32, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Discover new comics",
                                size=16,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                        ],
                    ),
                )
            ),
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=20),
                content=ft.Row(
                    spacing=10,
                    controls=[
                        ActionCard(
                            ft.Icons.CALENDAR_TODAY_OUTLINED,
                            ft.Colors.BLUE_ACCENT,
                            new_comics_count,
                            "New Comics",
                        ),
                        ActionCard(
                            ft.Icons.LOOKS_ONE_OUTLINED,
                            ft.Colors.YELLOW_ACCENT,
                            debut_issues_count,
                            "New #1s",
                        ),
                        ActionCard(
                            ft.Icons.DOWNLOADING_OUTLINED,
                            ft.Colors.GREEN_ACCENT,
                            pull_list_count,
                            "Your Pulls",
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
                            "This Week's Catalog", size=20, weight=ft.FontWeight.BOLD
                        ),
                    ],
                ),
            ),
        ],
    )

    page.run_task(update_releases_count)

    return ft.View(
        route="/releases",
        padding=0,
        navigation_bar=navbar,
        controls=[
            GradientWrapper(
                content=main_content,
                color=ft.Colors.GREEN_ACCENT,
            )
        ],
    )
