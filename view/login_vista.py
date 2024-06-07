# vistas/login_vista.py

import flet as ft
from controller.auth_controlador import AuthControlador

class LoginPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/login")
        self.page = page
        self.username_field = ft.TextField(label="Username", width=300)
        self.password_field = ft.TextField(label="Password", password=True, width=300)
        self.login_button = ft.ElevatedButton("Login", on_click=self.login)
        self.auth_controlador = AuthControlador()

        self.controls = [
            ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.SURFACE_VARIANT),
            self.username_field,
            self.password_field,
            self.login_button
        ]

    def login(self, e):
        username = self.username_field.value
        password = self.password_field.value
        rol = self.auth_controlador.autenticar(username, password)

        if rol:
            self.page.go("/menu")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Datos ingresados incorrectos"))
            self.page.snack_bar.open = True
            self.page.update()
