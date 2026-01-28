import flet as ft


class PageHeader(ft.Stack):
    def __init__(self):
        super().__init__(height=230)

        self.hero_image = ft.Image(
            src="",
            fit=ft.BoxFit.COVER,
            opacity=0.4,
            width=float("inf"),
            visible=False,
        )
        self.info_text = ft.Text("", size=14, color="white70")
        self.title_text = ft.Text(
            "",
            size=28,
            weight=ft.FontWeight.BOLD,
            color="white",
        )

        self.controls = [
            ft.Container(bgcolor="#2a2c2e", content=self.hero_image),
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    colors=[ft.Colors.TRANSPARENT, "#1a1c1E"],
                ),
            ),
            ft.Container(
                padding=15,
                content=ft.Column(
                    [
                        ft.Container(expand=True),
                        self.info_text,
                        self.title_text,
                    ],
                    spacing=5,
                ),
            ),
        ]

    def update_header(self, title: str, subtitle: str, image_url: str | None):
        """Updates the header with dynamic content."""
        self.title_text.value = title
        self.info_text.value = subtitle

        if image_url:
            self.hero_image.src = image_url
            self.hero_image.visible = True

        self.update()
