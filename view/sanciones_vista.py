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
                
                actions=[Botones_nav.crear_botones_navegacion(self.page)]
            ),
            ft.Text("Aquí puedes gestionar las sanciones.")
        ]
class Botones_nav:
        def crear_botones_navegacion(page):
            return ft.Row(
                [
                    ft.TextButton("INICIO", icon=ft.icons.HOME_OUTLINED, on_click=lambda _: page.go("/menu")),
                    
                    ft.TextButton("SOCIOS", icon=ft.icons.PEOPLE_OUTLINE, on_click=lambda _: page.go("/socios")),
                    
                    ft.TextButton("VEHICULOS", icon=ft.icons.LOCAL_TAXI_OUTLINED, on_click=lambda _: page.go("/vehiculos")),
                    
                    ft.TextButton("AVANCES", icon=ft.icons.WORK_OUTLINE, on_click=lambda _: page.go("/avances")),
                    
                    ft.TextButton("SANCIONES", icon=ft.icons.REPORT, on_click=lambda _: page.go("/sanciones")),
                    
                    ft.TextButton("FINANZAS", icon=ft.icons.PAYMENTS_OUTLINED, on_click=lambda _: page.go("/finanzas")),
                    
                    ft.VerticalDivider(width=100),

                ],
                alignment=ft.MainAxisAlignment.CENTER
            )