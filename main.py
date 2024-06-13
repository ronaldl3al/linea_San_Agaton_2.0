# main.py

import flet as ft
from view.login_vista import LoginPage
from view.menu_vista import MenuPage
from view.socios_vista import SociosPage
from view.vehiculos_vista import VehiculosPage
from view.avances_vista import AvancesPage
from view.sanciones_vista import SancionesPage
from view.finanzas_vista import FinanzasPage
import warnings

# Ignorar advertencias de desaprobación
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Función principal que se ejecuta al iniciar la aplicación
def main(page: ft.Page):
    # Función para manejar los cambios de ruta
    def route_change(route):
        page.views.clear()  # Limpiar las vistas actuales

        # Comprobar la ruta actual y agregar la vista correspondiente
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

        page.update()  # Actualizar la página para reflejar los cambios

    # Asignar la función route_change al evento on_route_change
    page.on_route_change = route_change

    # Establecer la ruta inicial a "/login"
    page.go("/login")

# Para ejecutar la aplicación como una app de escritorio
ft.app(target=main)

# Para ejecutar la aplicación en el navegador (descomentar la siguiente línea)
# ft.app(target=main, view=ft.WEB_BROWSER)
