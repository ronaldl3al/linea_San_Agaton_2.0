import flet as ft

class MenuPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/menu")
        self.page = page
        self.bgcolor = "#F4F9FA"

        self.controls = [
            ft.Container(
                bgcolor="#111111",
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.center_right,
                    colors=["#0D1223", "#182241"]
                ),
                border_radius=20,
                content = ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "INICIO",
                                    weight="w500",
                                    size=35,
                                    font_family="Arial Black italic"
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            expand=True
                        ),
                        ft.Row(
                            [
                                BotonesNav.crear_botones_navegacion(self.page),
                                ft.PopupMenuButton(
                                    bgcolor="#1E2A4A",
                                    items=[
                                        ft.PopupMenuItem(
                                            text="Cerrar Sesión",
                                            icon=ft.icons.LOGOUT,
                                            on_click=self.show_logout_popup,
                                        )
                                    ]
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),


                padding=20
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "Linea San Agatón",
                                weight="w900",
                                size=60,
                                font_family="Arial Black Italic",  # Especifica la familia de fuentes
                                italic=True,  # Aplica cursiva
                            ),
                            width=2000,
                        ),
                        ft.Row(
                            [
                                self.containers_datos(
                                    icon=ft.icons.PEOPLE_OUTLINE,
                                    title="SOCIOS",
                                    bgcolor="#22315D"
                                ),
                                self.containers_datos(
                                    icon=ft.icons.LOCAL_TAXI_OUTLINED,
                                    title="VEHICULOS",
                                    bgcolor="#22315D"
                                ),
                                self.containers_datos(
                                    icon=ft.icons.WORK_OFF_OUTLINED,
                                    title="AVANCES",
                                    bgcolor="#22315D"
                                ),
                                self.containers_datos(
                                    icon=ft.icons.BLOCK_OUTLINED,
                                    title="SANCIONES",
                                    bgcolor="#22315D"
                                ),
                                self.containers_datos(
                                    icon=ft.icons.ATTACH_MONEY_OUTLINED,
                                    title="FINANZAS",
                                    bgcolor="#22315D"
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=100
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                expand=True,
                alignment=ft.alignment.center,
                image_src="image/LOGO_SAN_AGATON_REMASTER1.png",  # Ruta de la imagen de fondo
                bgcolor="#111111",
                border_radius=20,
                padding=ft.padding.all(20),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.center_right,
                    colors=["#0D1223", "#182241"]
                )
            )
        ]

    def containers_datos(self, icon, title, bgcolor):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(icon, size=90, color="#F4F9FAaa"),
                            ft.Text(title, size=20, weight=ft.FontWeight.W_900, color="#F4F9FAaa"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            width=230,
            height=120,
            border_radius=5,
            bgcolor=bgcolor,
            padding=ft.padding.all(5),
            blur=ft.Blur(10, 10, ft.BlurTileMode.REPEATED)  # Aplicando desenfoque
        )

    def show_logout_popup(self, e):
        self.page.dialog = ft.AlertDialog(
            bgcolor= "#0C1222",
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

class BotonesNav:
    @staticmethod
    def crear_botones_navegacion(page):
        return ft.Row(
            [
                ft.TextButton("INICIO", scale=1.2,icon=ft.icons.HOME,style=ft.ButtonStyle(color="#F4F9FA"),   on_click=lambda _: page.go("/menu"), ),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("SOCIOS", scale=1.2,icon=ft.icons.PEOPLE_OUTLINE,  on_click=lambda _: page.go("/socios")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("VEHICULOS", scale=1.2,icon=ft.icons.LOCAL_TAXI_OUTLINED, on_click=lambda _: page.go("/vehiculos")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("AVANCES", scale=1.2,icon=ft.icons.WORK_OUTLINE, on_click=lambda _: page.go("/avances")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("SANCIONES", scale=1.2,icon=ft.icons.REPORT_OUTLINED, on_click=lambda _: page.go("/sanciones")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("FINANZAS", scale=1.2,icon=ft.icons.PAYMENTS_OUTLINED, on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=40,),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )