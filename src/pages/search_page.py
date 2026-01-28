import flet as ft
import asyncio


def search_page(page: ft.Page):
    categories = ["Series", "Issues", "Characters", "Creators", "Story Arcs"]
    state = {
        "active_index": 0,
        "history": [],
    }

    async def handle_category_click(index):
        state["active_index"] = index
        render_selection_row()
        page.update()

    async def handle_restore_query(query):
        search_field.value = query
        await search_field.focus()
        page.update()

    async def handle_delete_history(query):
        state["history"].remove(query)
        render_history_list()
        page.update()

    async def handle_clear(e):
        search_field.value = ""
        await search_field.focus()
        page.update()

    def handle_search_submit(e):
        query = search_field.value.strip()
        if not query:
            return

        if query in state["history"]:
            state["history"].remove(query)

        state["history"].insert(0, query)
        state["history"] = state["history"][:20]

        render_history_list()
        category = categories[state["active_index"]].lower()
        asyncio.create_task(page.push_route(f"/results?type={category}&q={query}"))

    selection_row = ft.Row(
        scroll=ft.ScrollMode.HIDDEN,
        spacing=10,
    )

    history_list_column = ft.Column(expand=True, spacing=0)

    search_field = ft.TextField(
        hint_text="Search the Metron Comic Database",
        prefix_icon=ft.Icon(ft.Icons.SEARCH, size=24),
        suffix_icon=ft.IconButton(ft.Icons.CLEAR_ROUNDED, on_click=handle_clear),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE),
        expand=True,
        filled=True,
        border_radius=12,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.Colors.OUTLINE_VARIANT,
        border_width=1.5,
        cursor_color=ft.Colors.BLUE_ACCENT,
        focused_border_color=ft.Colors.OUTLINE,
        focused_border_width=2,
        text_size=16,
        autofocus=True,
        on_submit=handle_search_submit,
        content_padding=ft.Padding(10, 0, 10, 0),
    )

    def render_selection_row():
        chips = []
        for i, name in enumerate(categories):
            is_active = state["active_index"] == i
            chips.append(
                ft.Container(
                    content=ft.Text(
                        name,
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=(
                            ft.Colors.WHITE
                            if is_active
                            else ft.Colors.ON_SURFACE_VARIANT
                        ),
                    ),
                    bgcolor=(
                        ft.Colors.BLUE_ACCENT
                        if is_active
                        else ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE)
                    ),
                    padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                    border_radius=10,
                    on_click=lambda e, idx=i: asyncio.create_task(
                        handle_category_click(idx)
                    ),
                    animate=ft.Animation(300, ft.AnimationCurve.DECELERATE),
                )
            )
        selection_row.controls = chips

    def render_history_list():
        history_list_column.controls = [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.HISTORY, color=ft.Colors.OUTLINE, size=20),
                title=ft.Text(item, size=15),
                visual_density=ft.VisualDensity.COMPACT,
                content_padding=ft.Padding.only(left=15, right=5),
                on_click=lambda e, q=item: asyncio.create_task(
                    page.push_route(
                        f"/results?type={categories[state['active_index']].lower()}&q={q}"
                    )
                ),
                trailing=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.NORTH_WEST_ROUNDED,
                            icon_size=20,
                            icon_color=ft.Colors.ON_SURFACE_VARIANT,
                            tooltip="Restore to search bar",
                            on_click=lambda e, q=item: asyncio.create_task(
                                handle_restore_query(q)
                            ),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_size=20,
                            icon_color=ft.Colors.ON_SURFACE_VARIANT,
                            tooltip="Delete from history",
                            on_click=lambda e, q=item: asyncio.create_task(
                                handle_delete_history(q)
                            ),
                        ),
                    ],
                    tight=True,
                    spacing=0,
                ),
            )
            for item in state["history"]
        ]

    render_selection_row()
    render_history_list()

    return ft.View(
        route="/search",
        padding=0,
        appbar=ft.AppBar(
            title=search_field,
            center_title=False,
            bgcolor=ft.Colors.SURFACE,
            toolbar_height=70,
        ),
        controls=[
            ft.Container(
                content=selection_row,
                padding=ft.Padding.symmetric(vertical=10, horizontal=10),
            ),
            ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
            ft.ListView(expand=True, controls=[history_list_column]),
        ],
    )
