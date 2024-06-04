import flet as ft

class MenuPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/menu")
        self.page = page

        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("LINEA SAN AGATON", size=40, weight=ft.FontWeight.W_900),
                                ft.OutlinedButton(
                                    on_click=self.logout,
                                    text="Cerrar Sesión",
                                    icon=ft.icons.LOGOUT,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        bgcolor="red"
                                    )
                                )
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
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
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

    def logout(self, e):
        self.page.go("/login")

