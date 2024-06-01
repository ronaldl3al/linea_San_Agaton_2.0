# common.py

import flet as ft

class Common:
    def crear_botones_navegacion(page):
        return ft.Row(
            [
                ft.TextButton("SOCIOS", icon=ft.icons.PEOPLE, on_click=lambda _: page.go("/socios")),
                ft.VerticalDivider(),
                ft.TextButton("VEHICULOS", icon=ft.icons.LOCAL_TAXI, on_click=lambda _: page.go("/vehiculos")),
                ft.VerticalDivider(),
                ft.TextButton("AVANCES", icon=ft.icons.WORK, on_click=lambda _: page.go("/avances")),
                ft.VerticalDivider(),
                ft.TextButton("SANCIONES", icon=ft.icons.BLOCK, on_click=lambda _: page.go("/sanciones")),
                ft.VerticalDivider(),
                ft.TextButton("FINANZAS", icon=ft.icons.ATTACH_MONEY, on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=143),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
