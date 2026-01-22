import flet as ft

from views.home_view import HomeView
from views.my_library_view import MyLibraryView
from views.releases_view import ReleasesView
from views.discover_view import DiscoverView
from views.sub_views.search_view import SearchView
from views.sub_views.settings_view import SettingsView


def main(page: ft.Page):
    page.title = "Mobius"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    def show_search(e=None):
        search = SearchView(page, on_back_click=show_discover)
        content_container.content = search.build()
        page.update()

    def show_discover(e=None):
        discover = DiscoverView(page, on_search_click=show_search)
        content_container.content = discover.build()
        page.update()

    def show_settings(e=None):
        settings = SettingsView(page, on_back_click=show_home)
        content_container.content = settings.build()
        page.update()

    def show_home(e=None):
        home = HomeView(page, on_settings_click=show_settings)
        content_container.content = home.build()
        page.update()

    # Initialize views
    home = HomeView(page, on_settings_click=show_settings)
    releases = ReleasesView(page)
    discover = DiscoverView(page, on_search_click=show_search)
    my_library = MyLibraryView()

    # Container to hold the current view
    content_container = ft.Container(expand=True)
    content_container.content = home.build()

    # Navigation change handler

    def on_nav_change(e):
        index = e.control.selected_index

        if index == 0:
            content_container.content = home.build()
        elif index == 1:
            content_container.content = releases.build()
        elif index == 2:
            content_container.content = my_library.build()
        elif index == 3:
            content_container.content = discover.build()

        page.update()

    # Profile icon click handler
    def on_profile_click(e):
        print("Profile clicked")

    # Settings icon click handler
    def on_settings_click(e):
        print("Settings clicked")

    # Navigation Bar
    page.navigation_bar = ft.NavigationBar(
        # bgcolor=ft.Colors.TRANSPARENT,
        # border=ft.Border(top=ft.BorderSide(0.5, ft.Colors.OUTLINE_VARIANT)),
        overlay_color=ft.Colors.TRANSPARENT,
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
                label="My Library",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SEARCH_OUTLINED,
                selected_icon=ft.Icons.SEARCH,
                label="Discover",
            ),
        ],
        on_change=on_nav_change,
    )
    page.add(content_container)


if __name__ == "__main__":
    ft.run(main)
