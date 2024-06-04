import flet as ft

def main(page: ft.Page):

    def show_top_snackbar(e):
        snackbar_container.visible = True
        page.update()

    def hide_top_snackbar(e):
        snackbar_container.visible = False
        page.update()

    snackbar_container = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("This is a top SnackBar"),
                ft.IconButton(icon=ft.icons.CLOSE, on_click=hide_top_snackbar),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=ft.colors.BLUE,
        padding=10,
        visible=False,
        width=page.window_width,
        margin=ft.margin.all(0),
        alignment=ft.alignment.center,
    )

    page.add(snackbar_container)
    page.add(ft.ElevatedButton(text="Show Top SnackBar", on_click=show_top_snackbar))

ft.app(target=main)
