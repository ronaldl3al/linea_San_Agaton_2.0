# vistas/sanciones_vista.py

import flet as ft
from view.common.common import Common

class SancionesPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/sanciones")
        self.page = page
        self.controls = [
            ft.AppBar(
                title=ft.Text("Sanciones"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu")),
                actions=[Common.crear_botones_navegacion(self.page)]
            ),
            ft.Text("Aquí puedes gestionar las sanciones.")
        ]
