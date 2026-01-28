import flet as ft

from router import Router


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

    def set_page(e):
        index = e.control.selected_index
        routes = ["/", "/releases", "/my_library", "/discover"]
        page.go(routes[index])

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

    my_router = Router(page, navbar)

    async def view_pop(e):
        # print("--- VIEW POPPED ---")
        page.views.pop()
        top_view = page.views[-1]
        await page.push_route(top_view.route)  # type: ignore

    page.on_route_change = my_router.route_change
    page.on_view_pop = view_pop
    my_router.route_change("/")


if __name__ == "__main__":
    ft.run(main)
