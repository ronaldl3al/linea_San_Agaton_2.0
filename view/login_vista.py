import flet as ft
from controller.auth_controlador import AuthControlador
import mysql.connector.errors


class LoginPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/login")
        self.page = page
        self.bgcolor = "#F4F9FA"
        self.page.title = "Login Page"

        # Configurar la ventana para que no sea redimensionable

        self.page.window_min_height=740
        self.page.window_min_width=1380
        self.page.window_max_height=740
        self.page.window_max_width=1380
        self.page.window_maximized=True
        self.page.window_maximizable=True
        



        self.auth_controlador = AuthControlador()
        self.vista_login()

    def vista_login(self):
        # Logo y Título
        logo = ft.Text("Linea San Agaton", size=30, weight=ft.FontWeight.BOLD, color="#F4F9FA")
        create_account_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD, color="#F4F9FA")
        welcome_back_text = ft.Text("¡Bienvenido de vuelta!", size=12, color="#F4F9FA")

        # Campos de entrada
        self.username = ft.TextField(
            label="Usuario",
            filled=True,
            border_color="#F4F9FA",
            bgcolor=ft.colors.TRANSPARENT,
            width=300,
            height=50,
            border_radius=20,
            prefix_icon=ft.icons.LOGIN,
        )
        self.password = ft.TextField(
            label="Contraseña",
            password=True,
            filled=True,
            border_color="#F4F9FA",
            bgcolor=ft.colors.TRANSPARENT,
            width=300,
            height=50,
            border_radius=20,
            can_reveal_password=True,
            prefix_icon=ft.icons.PASSWORD,
        )

        # Botones
        login_btn = ft.ElevatedButton(
            content=ft.Text('INICIAR'),
            on_click=self.login,
            bgcolor="#182241"
        )
        clear_btn = ft.ElevatedButton(
            text="Borrar",
            color=ft.colors.RED,
            bgcolor="#F4F9FA",
            on_click=self.clear_data,
        )
        exit_btn = ft.ElevatedButton(
            text="Salir",
            color=ft.colors.WHITE,
            bgcolor=ft.colors.RED,
            on_click=self.exit_app,
        )

        # Layout
        self.controls.append(
            ft.Container(
                content=ft.Container(
                    content=ft.Column(
                        [
                            logo,
                            ft.Container(height=20),
                            create_account_text,
                            welcome_back_text,
                            ft.Container(height=20),
                            self.username,
                            self.password,
                            ft.Row([login_btn, clear_btn, exit_btn], alignment=ft.MainAxisAlignment.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    padding=ft.padding.all(20),
                    width=550,  # Ancho ajustado para que coincida con el de socios
                    bgcolor="#0D1223",
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.center_left,
                        end=ft.alignment.center_right,
                        colors=["#0D1223", "#182241"]
                    ),
                    image_src="image\LOGO_SAN_AGATON_REMASTER1.png"
                ),
                alignment=ft.alignment.center_right,  # Alinear el contenedor al centro
                expand=True,
                
                bgcolor=ft.colors.TRANSPARENT,
                image_src="image\IMG_20240610_172030_545 (1).jpg-1.png",
                border_radius=20,
            ),
        )

    def login(self, e):
        username = self.username.value
        password = self.password.value
        
        try:
            rol = self.auth_controlador.autenticar(username, password)
            if rol:
                self.page.go("/menu")
            else:
                self.mostrar_snackbar("Datos ingresados incorrectos")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def clear_data(self, e):
        self.username.value = ""
        self.password.value = ""
        self.username.update()
        self.password.update()
    
    def mostrar_snackbar(self, mensaje):
        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor="#F4F9FA")
        self.page.snack_bar.open = True
        self.page.update()

    def mostrar_banner(self, mensaje):
        self.page.banner = ft.AlertDialog(
            content=ft.Text(mensaje, color=ft.colors.WHITE),
            bgcolor="#eb3936",  # Color rojo pastel
            actions=[
                ft.TextButton("CERRAR", on_click=lambda _: self.cerrar_banner(), style=ft.ButtonStyle(color=ft.colors.WHITE))
            ]
        )
        self.page.banner.open = True
        self.page.update()

    def cerrar_banner(self):
        self.page.banner.open = False
        self.page.update()

    def exit_app(self, e):
        self.page.window_close()