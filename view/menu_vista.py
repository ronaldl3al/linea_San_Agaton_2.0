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
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=650
                        ),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.PEOPLE, size=50, color="white"),
                                    ft.Text("SOCIOS", size=20, weight=ft.FontWeight.W_900, color="white"),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            alignment=ft.alignment.center,
                            width=350,
                            height=80,
                            border_radius=10,
                            ink=True,
                            on_click=lambda e: self.page.go("/socios"),
                            bgcolor="blue",
                            margin=ft.margin.all(10)
                        ),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.LOCAL_TAXI, size=50, color="white"),
                                    ft.Text("VEHICULOS", size=20, weight=ft.FontWeight.W_900, color="white"),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            alignment=ft.alignment.center,
                            width=350,
                            height=80,
                            border_radius=10,
                            ink=True,
                            on_click=lambda e: self.page.go("/vehiculos"),
                            bgcolor="blue",
                            margin=ft.margin.all(10)
                        ),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.WORK, size=50, color="white"),
                                    ft.Text("AVANCES", size=20, weight=ft.FontWeight.W_900, color="white"),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            alignment=ft.alignment.center,
                            width=350,
                            height=80,
                            border_radius=10,
                            ink=True,
                            on_click=lambda e: self.page.go("/avances"),
                            bgcolor="blue",
                            margin=ft.margin.all(10)
                        ),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.BLOCK, size=50, color="white"),
                                    ft.Text("SANCIONES", size=20, weight=ft.FontWeight.W_900, color="white"),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            alignment=ft.alignment.center,
                            width=350,
                            height=80,
                            border_radius=10,
                            ink=True,
                            on_click=lambda e: self.page.go("/sanciones"),
                            bgcolor="blue",
                            margin=ft.margin.all(10)
                        ),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.ATTACH_MONEY, size=50, color="white"),
                                    ft.Text("FINANZAS", size=20, weight=ft.FontWeight.W_900, color="white"),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                            alignment=ft.alignment.center,
                            width=350,
                            height=80,
                            border_radius=10,
                            ink=True,
                            on_click=lambda e: self.page.go("/finanzas"),
                            bgcolor="blue",
                            margin=ft.margin.all(10)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    
                ),
                expand=True,
                alignment=ft.alignment.center,
                bgcolor="#333333",
                margin=5,
                border_radius=20
            )
        ]

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
