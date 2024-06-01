# vistas/menu_vista.py

import flet as ft

class MenuPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/menu")
        self.page = page

        self.controls = [
            ft.AppBar(
                title=ft.Text("LINEA SAN AGATON"),
                bgcolor=ft.colors.SURFACE_VARIANT,
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
                            ft.VerticalDivider(width=106)
                        ],
                    ),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Cerrar Sesión", on_click=lambda _: self.logout()),
                        ]
                    )
                ]
            ),
            ft.Text("Bienvenido al menú principal! Selecciona una opción del menú."),
        ]

    def logout(self, e=None):
        self.page.go("/login")

    
    