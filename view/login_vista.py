import flet as ft
from controller.auth_controlador import AuthControlador
import mysql.connector.errors
from utils.helpers import mostrar_mensaje
from utils.colors import Colores

class LoginPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/login")
        self.page = page
        self.bgcolor = Colores.NEGRO
        self.page.title = "INICIO DE SESIÓN"
        self.auth_controlador = AuthControlador()
        self.vista_login()

    def nombre_login(self):
        return ft.Text(
            "Linea San Agatón",
            size=40,
            weight=ft.FontWeight.BOLD,
            color=Colores.BLANCO,
            font_family="Arial Black italic",
        )

    def texto_bienvenida(self):
        return ft.Text(
            "¡Bienvenido de vuelta!",
            weight=ft.FontWeight.BOLD,
            size=20,
            color=Colores.BLANCO,
        )

    def campos_texto(self):
        self.username = ft.TextField(
            label="Usuario",
            label_style=ft.TextStyle(color=Colores.BLANCO, size=20),
            text_style=ft.TextStyle(color=ft.colors.WHITE),
            filled=True,
            border_color=Colores.BLANCO,
            bgcolor=ft.colors.TRANSPARENT,
            width=300,
            height=50,
            border_radius=20,
            prefix_icon=ft.icons.LOGIN,
            focused_border_color=Colores.GRIS,
            focus_color=Colores.GRIS,
        )
        self.password = ft.TextField(
            label="Contraseña",
            label_style=ft.TextStyle(color=Colores.BLANCO, size=20),
            text_style=ft.TextStyle(color=ft.colors.WHITE),
            password=True,
            filled=True,
            border_color=Colores.BLANCO,
            bgcolor=ft.colors.TRANSPARENT,
            width=300,
            height=50,
            border_radius=20,
            can_reveal_password=True,
            prefix_icon=ft.icons.PASSWORD,
            focused_border_color=Colores.GRIS,
            focus_color=Colores.GRIS,
        )
        return self.username, self.password

    def boton_login(self):
        return ft.ElevatedButton(
            text="INICIAR",
            on_click=self.login,
            bgcolor=Colores.GRIS,
            color=ft.colors.WHITE,
        )

    def contenedor_login(self):
        logo = self.nombre_login()
        texto_bienvenida = self.texto_bienvenida()
        username, password = self.campos_texto()
        boton_login = self.boton_login()

        return ft.Container(
            content=ft.Column(
                [
                    logo,
                    ft.Container(height=30),
                    texto_bienvenida,
                    ft.Container(height=20),
                    username,
                    password,
                    ft.Row(
                        [boton_login],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=30,
            width=425,
            height=590,
            border_radius=20,
            alignment=ft.alignment.center,
            blur=ft.Blur(sigma_x=0, sigma_y=200),
            border=ft.Border(
                left=ft.BorderSide(color=Colores.BLANCO, width=1.5),
                top=ft.BorderSide(color=Colores.BLANCO, width=1.5),
                right=ft.BorderSide(color=Colores.BLANCO, width=1.5),
                bottom=ft.BorderSide(color=Colores.BLANCO, width=1.5),
            ),
        )

    def contenedor_fondo(self, contenedor_login: ft.Container):
        contenedor_imagen = ft.Container(
            content=ft.Image(
                src="https://iili.io/3AxmI0N.png",
                fit=ft.ImageFit.COVER,
            ),
            border_radius=20,
            expand=True,
        )
        contenedor_formulario = ft.Container(
            content=ft.Row(
                [contenedor_login],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.only(left=20, right=20, top=20),
        )
        stack = ft.Stack([contenedor_imagen, contenedor_formulario])
        return ft.Container(content=stack, expand=True)

    def vista_login(self):
        contenedor_login = self.contenedor_login()
        contenedor_fondo = self.contenedor_fondo(contenedor_login)
        self.controls.append(contenedor_fondo)

    def login(self, e):
        username = self.username.value
        password = self.password.value

        try:
            rol = self.auth_controlador.autenticar(username, password)
            if rol:
                self.page.go("/menu")
            else:
                mostrar_mensaje(self.page, "Credenciales incorrectas", tipo="error")
        except mysql.connector.Error as err:
            mostrar_mensaje(self.page, f"Error de base de datos: {err}", tipo="error")
