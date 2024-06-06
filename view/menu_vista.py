import flet as ft

class MenuPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/menu")
        self.page = page

        self.controls = [
            ft.AppBar(
                title=ft.Text("Inicio"),
                bgcolor=ft.colors.SURFACE_VARIANT,

                actions=[
                    Botones_nav.crear_botones_navegacion(self.page),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                text="Cerrar Sesión",
                                icon=ft.icons.LOGOUT,
                                on_click=self.show_logout_popup,
                            )
                        ]
                    )
                ]
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("LINEA SAN AGATON", size=40, weight=ft.FontWeight.W_900),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=650,
                            vertical_alignment= ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            [
                                self.containers_datos(
                                    icon=ft.icons.PEOPLE,
                                    title="SOCIOS",
                                    bgcolor="#44a08d88"
                                ),
                                self.containers_datos(
                                    icon=ft.icons.LOCAL_TAXI,
                                    title="VEHICULOS",
                                    bgcolor="#13547a88"
                                ),
                                self.containers_datos(
                                    icon=ft.icons.WORK,
                                    title="AVANCES",
                                    bgcolor = "#92222222"
                                ),
                                self.containers_datos(
                                    icon=ft.icons.BLOCK,
                                    title="SANCIONES",
                                    bgcolor="#0a3d6288"
                                ),
                                self.containers_datos(
                                    icon=ft.icons.ATTACH_MONEY,
                                    title="FINANZAS",
                                    bgcolor="#0a3d6288"
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=10
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
                expand=True,
                alignment=ft.alignment.center,
                image_src="image\LOGO_SAN_AGATON_REMASTER.png",  # Ruta de la imagen de fondo
                bgcolor="#111111"
            )
        ]

    def containers_datos(self, icon, title, bgcolor):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(icon, size=70, color="white"),
                            ft.Text(title, size=20, weight=ft.FontWeight.W_900, color="white"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
            ),
            alignment=ft.alignment.center,
            
            width=230,
            height=120,
            border_radius=5,
            ink=True,
            bgcolor=bgcolor,
            padding=ft.padding.all(3),
            margin=ft.margin.all(3),
            
            
        )

    def show_logout_popup(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Cierre de Sesión"),
            content=ft.Text("¿Está seguro de que desea cerrar sesión?"),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog, style=ft.ButtonStyle(color="red")),
                ft.TextButton("Cerrar Sesión", on_click=self.logout),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()

    def logout(self, e):
        self.page.dialog.open = False
        self.page.update()
        self.page.go("/login")

class Botones_nav:
    def crear_botones_navegacion(page):
        return ft.Row(
            [
                ft.TextButton("INICIO", icon=ft.icons.HOME, on_click=lambda _: page.go("/menu")),
                ft.TextButton("SOCIOS", icon=ft.icons.PEOPLE_OUTLINE, on_click=lambda _: page.go("/socios")),
                ft.TextButton("VEHICULOS", icon=ft.icons.LOCAL_TAXI_OUTLINED, on_click=lambda _: page.go("/vehiculos")),
                ft.TextButton("AVANCES", icon=ft.icons.WORK_OUTLINE, on_click=lambda _: page.go("/avances")),
                ft.TextButton("SANCIONES", icon=ft.icons.REPORT_OUTLINED, on_click=lambda _: page.go("/sanciones")),
                ft.TextButton("FINANZAS", icon=ft.icons.PAYMENTS_OUTLINED, on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=100),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )


