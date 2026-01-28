import flet as ft


class SeriesCard(ft.Container):
    def __init__(self, series, image_url=None, on_click=None):
        super().__init__()
        self.series = series
        self.image_url = image_url
        self.on_click = on_click
        self.border = ft.Border(bottom=ft.BorderSide(1, "white10"))

        self.content = ft.ListTile(
            leading=self._build_thumbnail(),
            title=ft.Text(
                series.display_name,
                size=16,
                weight=ft.FontWeight.W_500,
                color="white",
            ),
            subtitle=ft.Text(f"{series.issue_count} issues", size=13, color="white60"),
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, color="white24"),
            on_click=self.on_click,
        )

    def _build_thumbnail(self):
        return ft.Container(
            width=50,
            height=70,
            border_radius=4,
            bgcolor="white10",
            content=(
                ft.Image(
                    src=str(self.image_url),
                    fit=ft.BoxFit.COVER,
                    error_content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED),
                )
                if self.image_url
                else ft.Icon(ft.Icons.ALBUM, size=28, color="white24")
            ),
        )
