# main.py

import flet as ft
from view.login_vista import LoginPage
from view.menu_vista import MenuPage

class SociosPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/socios")
        self.page = page
        self.controls = [
            ft.AppBar(title=ft.Text("Socios"), bgcolor=ft.colors.SURFACE_VARIANT, leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu"))),
            ft.Text("Aquí puedes gestionar los socios.")
        ]

class VehiculosPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/vehiculos")
        self.page = page
        self.controls = [
            ft.AppBar(title=ft.Text("Vehículos"), bgcolor=ft.colors.SURFACE_VARIANT, leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu"))),
            ft.Text("Aquí puedes gestionar los vehículos.")
        ]

class AvancesPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/avances")
        self.page = page
        self.controls = [
            ft.AppBar(title=ft.Text("Avances"), bgcolor=ft.colors.SURFACE_VARIANT, leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu"))),
            ft.Text("Aquí puedes ver los avances.")
        ]

class SancionesPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/sanciones")
        self.page = page
        self.controls = [
            ft.AppBar(title=ft.Text("Sanciones"), bgcolor=ft.colors.SURFACE_VARIANT, leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu"))),
            ft.Text("Aquí puedes gestionar las sanciones.")
        ]

class FinanzasPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/finanzas")
        self.page = page
        self.controls = [
            ft.AppBar(title=ft.Text("Finanzas"), bgcolor=ft.colors.SURFACE_VARIANT, leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu"))),
            ft.Text("Aquí puedes gestionar las finanzas.")
        ]

def main(page: ft.Page):
    def route_change(route):
        page.views.clear()

        if page.route == "/login":
            page.views.append(LoginPage(page))
        elif page.route == "/menu":
            page.views.append(MenuPage(page))
        elif page.route == "/socios":
            page.views.append(SociosPage(page))
        elif page.route == "/vehiculos":
            page.views.append(VehiculosPage(page))
        elif page.route == "/avances":
            page.views.append(AvancesPage(page))
        elif page.route == "/sanciones":
            page.views.append(SancionesPage(page))
        elif page.route == "/finanzas":
            page.views.append(FinanzasPage(page))

        page.update()

    page.on_route_change = route_change
    page.go("/login")

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
