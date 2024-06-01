# vistas/socios_vista.py

import flet as ft
from controller.socios_controlador import SocioControlador

class SociosPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/socios")
        self.page = page
        self.socio_controlador = SocioControlador()
        self.socios_data = self.obtener_datos_socios()
        self.tabla_socios = self.crear_tabla_socios()
        
        self.controls = [
            ft.AppBar(
                title=ft.Text("Socios"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu")),
                actions=[
                    ft.Row(
                        [
                            ft.TextButton("SOCIOS", icon=ft.icons.PEOPLE, on_click=lambda _: self.page.go("/socios")),
                            ft.VerticalDivider(),
                            ft.TextButton("VEHICULOS", icon=ft.icons.LOCAL_TAXI, on_click=lambda _: self.page.go("/vehiculos")),
                            ft.VerticalDivider(),
                            ft.TextButton("AVANCES", icon=ft.icons.WORK, on_click=lambda _: self.page.go("/avances")),
                            ft.VerticalDivider(),
                            ft.TextButton("SANCIONES", icon=ft.icons.BLOCK, on_click=lambda _: self.page.go("/sanciones")),
                            ft.VerticalDivider(),
                            ft.TextButton("FINANZAS", icon=ft.icons.ATTACH_MONEY, on_click=lambda _: self.page.go("/finanzas")),
                            ft.VerticalDivider(width=143),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            ),
            ft.Column(
                [
                    self.tabla_socios,
                    ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.mostrar_bottomsheet_agregar)
                ],
                expand=True
            )
        ]

        # Inicializa el BottomSheet vacío
        self.bottom_sheet = ft.BottomSheet(
            ft.Container(),
            open=False,
            on_dismiss=self.cerrar_bottomsheet
        )
        self.page.overlay.append(self.bottom_sheet)

    def obtener_datos_socios(self):
        return self.socio_controlador.obtener_todos_socios()

    def crear_tabla_socios(self):
        socios = self.obtener_datos_socios()
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Cédula")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("Dirección")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Control")),
                ft.DataColumn(ft.Text("RIF")),
                ft.DataColumn(ft.Text("Fecha Nacimiento")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(socio['cedula'])),
                        ft.DataCell(ft.Text(socio['nombres'])),
                        ft.DataCell(ft.Text(socio['apellidos'])),
                        ft.DataCell(ft.Text(socio['direccion'])),
                        ft.DataCell(ft.Text(socio['numero_telefono'])),
                        ft.DataCell(ft.Text(socio['numero_control'])),
                        ft.DataCell(ft.Text(socio['rif'])),
                        ft.DataCell(ft.Text(socio['fecha_nacimiento'])),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(ft.icons.EDIT, on_click=lambda _, s=socio: self.mostrar_bottomsheet_editar(s)),
                                    ft.IconButton(ft.icons.DELETE, on_click=lambda _, s=socio: self.confirmar_eliminar_socio(s))
                                ]
                            )
                        )
                    ],
                ) for socio in socios
            ],
        )

    def mostrar_bottomsheet_agregar(self, e):
        self.bottom_sheet.content = self.crear_formulario_socio("Agregar Socio", self.guardar_socio)
        self.bottom_sheet.open = True
        self.page.update()

    def mostrar_bottomsheet_editar(self, socio):
        self.bottom_sheet.content = self.crear_formulario_socio("Editar Socio", self.actualizar_socio, socio)
        self.bottom_sheet.open = True
        self.page.update()

    def confirmar_eliminar_socio(self, socio):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar al socio {socio['nombres']} {socio['apellidos']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda _: self.eliminar_socio(socio['cedula']))
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def cerrar_dialogo(self):
        self.page.dialog.open = False
        self.page.update()

    def cerrar_bottomsheet(self, e=None):
        self.bottom_sheet.open = False
        self.page.update()

    def guardar_socio(self, cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento):
        self.socio_controlador.insertar_socio(cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento)
        self.mostrar_snackbar("Socio agregado correctamente")
        self.refrescar_datos()

    def actualizar_socio(self, cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento):
        self.socio_controlador.actualizar_socio(cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento)
        self.mostrar_snackbar("Socio actualizado correctamente")
        self.refrescar_datos()

    def eliminar_socio(self, cedula):
        self.socio_controlador.eliminar_socio(cedula)
        self.mostrar_snackbar("Socio eliminado correctamente")
        self.refrescar_datos()

    def mostrar_snackbar(self, mensaje):
        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje))
        self.page.snack_bar.open = True
        self.page.update()

    def refrescar_datos(self):
        self.socios_data = self.obtener_datos_socios()
        self.tabla_socios.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(socio['cedula'])),
                    ft.DataCell(ft.Text(socio['nombres'])),
                    ft.DataCell(ft.Text(socio['apellidos'])),
                    ft.DataCell(ft.Text(socio['direccion'])),
                    ft.DataCell(ft.Text(socio['numero_telefono'])),
                    ft.DataCell(ft.Text(socio['numero_control'])),
                    ft.DataCell(ft.Text(socio['rif'])),
                    ft.DataCell(ft.Text(socio['fecha_nacimiento'])),
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.EDIT, on_click=lambda _, s=socio: self.mostrar_bottomsheet_editar(s)),
                                ft.IconButton(ft.icons.DELETE, on_click=lambda _, s=socio: self.confirmar_eliminar_socio(s))
                            ]
                        )
                    )
                ],
            ) for socio in self.socios_data
        ]
        self.tabla_socios.update()
        self.cerrar_bottomsheet()
        self.page.update()

    def crear_formulario_socio(self, titulo, accion, socio=None):
        height = 40  # Ajustar la altura según sea necesario

        cedula = ft.TextField(label="Cédula", value=socio['cedula'] if socio else "", height=height)
        nombres = ft.TextField(label="Nombres", value=socio['nombres'] if socio else "", height=height)
        apellidos = ft.TextField(label="Apellidos", value=socio['apellidos'] if socio else "", height=height)
        direccion = ft.TextField(label="Dirección", value=socio['direccion'] if socio else "", height=height)
        telefono = ft.TextField(label="Teléfono", value=socio['numero_telefono'] if socio else "", height=height)
        control = ft.TextField(label="Control", value=socio['numero_control'] if socio else "", height=height)
        rif = ft.TextField(label="RIF", value=socio['rif'] if socio else "", height=height)
        fecha_nacimiento = ft.TextField(label="Fecha Nacimiento", value=socio['fecha_nacimiento'] if socio else "", height=height)

        return ft.Container(
            ft.Column([
                ft.Row([cedula, nombres], spacing=10),
                ft.Row([apellidos, direccion], spacing=10),
                ft.Row([telefono, control], spacing=10),
                ft.Row([rif, fecha_nacimiento], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", on_click=lambda _: accion(
                            cedula.value, nombres.value, apellidos.value, direccion.value, telefono.value, control.value, rif.value, fecha_nacimiento.value
                        ))
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ]),
            padding=20,
            border_radius=15,
        )

