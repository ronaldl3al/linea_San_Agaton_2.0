# vistas/sanciones_vista.py

import flet as ft

class SancionesPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/sanciones")
        self.page = page
        self.controls = [
            ft.AppBar(
                title=ft.Text("Sanciones"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu")),
                actions=[
                    ft.Row(
                        [
                            ft.TextButton("SOCIOS", icon=ft.icons.PEOPLE, on_click=lambda _: self.page.go("/socios")),
                            ft.VerticalDivider(),
                            ft.TextButton("VEHICULOS", icon=ft.icons.LOCAL_TAXI, on_click=lambda _: self.page.go("/vehiculos")),
                            ft.VerticalDivider(),
                            ft.TextButton("AVANCES", icon=ft.icons.WORK, on_click=lambda _: self.page.go("/avances")),
                            ft.VerticalDivider(),
                            ft.TextButton("SANCIONES", icon=ft.icons.BLOCK, on_click=lambda _: self.page.go("/sanciones")),
                            ft.VerticalDivider(),
                            ft.TextButton("FINANZAS", icon=ft.icons.ATTACH_MONEY, on_click=lambda _: self.page.go("/finanzas")),
                            ft.VerticalDivider(width=143),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            ),
            ft.Text("Aquí puedes gestionar las sanciones.")
        ]
