import flet as ft


def app_nav_bar(page: ft.Page):
    return ft.NavigationBar(
        selected_index={
            "/": 0,
            "/releases": 1,
            "/library": 2,
            "/discover": 3,
        }.get(page.route, 0),
        label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Home",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.NEW_RELEASES_OUTLINED,
                selected_icon=ft.Icons.NEW_RELEASES,
                label="Releases",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.COLLECTIONS_BOOKMARK_OUTLINED,
                selected_icon=ft.Icons.COLLECTIONS_BOOKMARK,
                label="Library",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SEARCH_OUTLINED,
                selected_icon=ft.Icons.SEARCH,
                label="Discover",
            ),
        ],
        on_change=lambda e: page.go(
            ["/", "/releases", "/library", "/discover"][e.control.selected_index]
        ),
    )
