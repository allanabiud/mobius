import flet as ft
from views.my_library_view import MyLibraryView
from views.releases_view import ReleasesView
from views.discover_view import DiscoverView


def main(page: ft.Page):
    page.title = "Mobius"
    page.theme_mode = ft.ThemeMode.DARK

    # Container to hold the current view
    content_container = ft.Container(expand=True)

    # AppBar title text
    app_bar_title = ft.Text("My Library", weight=ft.FontWeight.BOLD, size=32)

    # Initialize views
    my_library = MyLibraryView()
    new_releases = ReleasesView(page)
    discover = DiscoverView()

    # Set initial view
    content_container.content = my_library.build()

    # Navigation change handler
    def on_nav_change(e):
        index = e.control.selected_index
        if index == 0:
            content_container.content = my_library.build()
            app_bar_title.value = "My Library"
        elif index == 1:
            content_container.content = new_releases.build()
            app_bar_title.value = "Releases"
        elif index == 2:
            content_container.content = discover.build()
            app_bar_title.value = "Discover"
        page.update()

    # Profile icon click handler
    def on_profile_click(e):
        print("Profile clicked")
        # Add your profile logic here

    # Settings icon click handler
    def on_settings_click(e):
        print("Settings clicked")
        # Add your settings logic here

    # Navigation Bar
    # Navigation Bar
    page.navigation_bar = ft.NavigationBar(
        border=ft.Border(top=ft.BorderSide(0.5, ft.Colors.OUTLINE_VARIANT)),
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOK_OUTLINED,
                selected_icon=ft.Icons.BOOK,
                label="My Library",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.NEW_RELEASES_OUTLINED,
                selected_icon=ft.Icons.NEW_RELEASES,
                label="Releases",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SEARCH_OUTLINED,
                selected_icon=ft.Icons.SEARCH,
                label="Discover",
            ),
        ],
        on_change=on_nav_change,
    )

    # Add AppBar with profile and settings icons
    page.add(
        ft.AppBar(
            title=app_bar_title,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    on_click=on_settings_click,
                ),
                ft.IconButton(
                    icon=ft.Icons.ACCOUNT_CIRCLE,
                    on_click=on_profile_click,
                ),
            ],
        ),
        content_container,
    )


if __name__ == "__main__":
    ft.run(main)
