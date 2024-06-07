import flet as ft

def main(page: ft.Page):
    page.title = "Ejemplo de FilledTonalButton"
    
    filled_tonal_button = ft.FilledTonalButton(
        content=ft.Text(
            "Go To Search",
            weight="w700",
        ),
        width=180,
        height=40,
        on_click=lambda _: page.go("/main")
    )
    
    # Agregar el botón a la página
    page.add(filled_tonal_button)

ft.app(target=main)
