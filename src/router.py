import flet as ft
from pages.home_page import home_page
from pages.releases_page import releases_page
from pages.my_library_page import my_library_page
from pages.settings_page import settings_page
from pages.discover_page import discover_page
from pages.search_page import search_page
from pages.search_results_page import search_results_page
from pages.series_page import series_page


class Router:
    def __init__(self, page: ft.Page, navbar: ft.NavigationBar):
        self.page = page
        self.navbar = navbar

    def route_change(self, e):
        route = self.page.route or "/"

        # DEBUG PRINTS
        # print("--- ROUTE CHANGE DETECTED ---")
        # print(f"Current View Stack: {[v.route for v in self.page.views]}")

        if route in ["/", "/releases", "/my_library", "/discover", "/settings"]:
            self.page.views.clear()

        if not self.page.views or self.page.views[-1].route != route:
            if route == "/":
                self.page.views.append(home_page(self.page, self.navbar))
            elif route == "/releases":
                self.page.views.append(releases_page(self.page, self.navbar))
            elif route == "/my_library":
                self.page.views.append(my_library_page(self.page, self.navbar))
            elif route == "/settings":
                self.page.views.append(settings_page(self.page))
            elif route == "/discover":
                self.page.views.append(discover_page(self.page, self.navbar))
            elif route == ("/search"):
                self.page.views.append(search_page(self.page))
            elif route.startswith("/results"):
                try:
                    q_type = self.page.query.get("type")
                except KeyError:
                    q_type = "series"

                try:
                    q_text = self.page.query.get("q")
                except KeyError:
                    q_text = ""

                self.page.views.append(search_results_page(self.page, q_type, q_text))
            elif route.startswith("/series/"):
                series_id = int(route.split("/")[-1])
                self.page.views.append(series_page(self.page, series_id))

        self.page.update()
        # print(f"Updated View Stack: {[v.route for v in self.page.views]}")
