# main.py

import flet as ft
from view.login_vista import LoginPage
from view.menu_vista import MenuPage
from view.socios_vista import SociosPage
from view.vehiculos_vista import VehiculosPage
from view.avances_vista import AvancesPage
from view.sanciones_vista import SancionesPage
from view.finanzas_vista import FinanzasPage

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
