import flet as ft

from pages.home_page import home_page
from pages.releases_page import releases_page
from pages.my_library_page import my_library_page
from pages.settings_page import settings_page
from pages.discover_page import discover_page
from pages.search_page import search_page
from pages.series_page import series_page


def main(page: ft.Page):
    page.title = "Mobius"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        page_transitions=ft.PageTransitionsTheme(
            android=ft.PageTransitionTheme.NONE,
            ios=ft.PageTransitionTheme.NONE,
            linux=ft.PageTransitionTheme.NONE,
            macos=ft.PageTransitionTheme.NONE,
            windows=ft.PageTransitionTheme.NONE,
        )
    )
    page.padding = 0

    navbar = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Home"),
            ft.NavigationBarDestination(
                icon=ft.Icons.NEW_RELEASES_OUTLINED, label="Releases"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.COLLECTIONS_BOOKMARK_OUTLINED, label="Library"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SEARCH_OUTLINED, label="Discover"
            ),
        ],
        on_change=lambda e: set_page(e),
    )

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(home_page(page, navbar))
        elif page.route == "/releases":
            page.views.append(releases_page(page, navbar))
        elif page.route == "/my_library":
            page.views.append(my_library_page(page, navbar))
        elif page.route == "/settings":
            page.views.append(settings_page(page))
        elif page.route == "/discover":
            page.views.append(discover_page(page, navbar))
        elif page.route == "/search":
            page.views.append(search_page(page))
        elif page.route.startswith("/series/"):
            series_id = int(page.route.split("/")[-1])
            page.views.append(series_page(page, series_id))

        page.update()

    def set_page(e):
        index = e.control.selected_index
        if index == 0:
            page.go("/")
        elif index == 1:
            page.go("/releases")
        elif index == 2:
            page.go("/my_library")
        elif index == 3:
            page.go("/discover")

    async def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        await page.push_route(top_view.route)  # type: ignore

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change("/")


if __name__ == "__main__":
    ft.app(main)
