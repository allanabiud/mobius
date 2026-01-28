import flet as ft


async def launch_external_url(page: ft.Page, obj_or_url: any):  # type: ignore
    """
    Handles launching a browser for Series objects, Issue objects, or raw strings.
    Uses the modern Flet URL launching approach to avoid DeprecationWarnings.
    """
    url = None

    if isinstance(obj_or_url, str):
        url = obj_or_url
    elif hasattr(obj_or_url, "resource_url") and obj_or_url.resource_url:
        url = str(obj_or_url.resource_url)

    if url:
        try:
            await page.launch_url(url)
        except Exception as e:
            print(f"Failed to launch URL: {e}")
    else:
        snack = ft.SnackBar(
            content=ft.Text("No external link available for this item.")
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()


class GradientWrapper(ft.Container):
    def __init__(
        self,
        content: ft.Control,
        color: str,
        opacity: float = 0.25,
        stops: list[float] = [0.0, 0.4, 1.0],
    ):
        super().__init__()
        self.expand = True

        gradient_colors = [ft.Colors.with_opacity(opacity, color)]

        if len(stops) == 3:
            gradient_colors.append(ft.Colors.with_opacity(opacity / 4, color))

        gradient_colors.append(ft.Colors.TRANSPARENT)

        self.gradient = ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            stops=stops,
            colors=gradient_colors,
        )
        self.content = content
