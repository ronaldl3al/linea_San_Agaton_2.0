import flet as ft 
from controller.socios_controlador import SocioControlador
from view.common.common import Common
import mysql.connector.errors


class SociosPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/socios")
        self.page = page
        self.socio_controlador = SocioControlador()
        self.socios_data = self.obtener_datos_socios()
        self.tabla_socios = SociosTable(self, self.socios_data)
        
        self.controls = [
            ft.AppBar(
                title=ft.Text("Socios"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu")),
                actions=[Common.crear_botones_navegacion(self.page)]
            ),
            ft.Container(
                content=ft.ListView(
                    controls=[self.tabla_socios.data_table],
                    expand=True,
                    spacing=10,
                    padding=20,
                    auto_scroll=True
                ),
                expand=True
            ),
            ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.mostrar_bottomsheet_agregar)
        ]

        self.bottom_sheet = ft.BottomSheet(
            ft.Container(),
            open=False,
            on_dismiss=self.cerrar_bottomsheet
        )
        self.page.overlay.append(self.bottom_sheet)

    def obtener_datos_socios(self):
        return self.socio_controlador.obtener_todos_socios()

    def mostrar_bottomsheet_agregar(self, e):
        self.bottom_sheet.content = SociosForm(self, "Agregar Socio", self.guardar_socio).formulario
        self.bottom_sheet.open = True
        self.page.update()

    def mostrar_bottomsheet_editar(self, socio):
        self.bottom_sheet.content = SociosForm(self, "Editar Socio", self.actualizar_socio, socio).formulario
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
        try:
            if not cedula or not nombres or not apellidos:
                raise ValueError("Los campos 'Cédula', 'Nombres' y 'Apellidos' son obligatorios.")
            self.socio_controlador.insertar_socio(cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento)
            self.mostrar_snackbar("Socio agregado correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_snackbar(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_snackbar(f"Error de base de datos: {err}")

    def actualizar_socio(self, cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento):
        try:
            if not cedula or not nombres or not apellidos:
                raise ValueError("Los campos 'Cédula', 'Nombres' y 'Apellidos' son obligatorios.")
            self.socio_controlador.actualizar_socio(cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento)
            self.mostrar_snackbar("Socio actualizado correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_snackbar(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_snackbar(f"Error de base de datos: {err}")

    def eliminar_socio(self, cedula):
        try:
            self.socio_controlador.eliminar_socio(cedula)
            self.mostrar_snackbar("Socio eliminado correctamente")
        except mysql.connector.errors.IntegrityError:
            self.mostrar_snackbar("No puedes eliminar este socio sin primero eliminar los vehículos asociados.")
        self.refrescar_datos()

    def mostrar_snackbar(self, mensaje):
        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje))
        self.page.snack_bar.open = True
        self.page.update()

    def refrescar_datos(self):
        self.socios_data = self.obtener_datos_socios()
        self.tabla_socios.actualizar_filas(self.socios_data)
        self.cerrar_bottomsheet()
        self.page.update()
    
    


class SociosTable:
    def __init__(self, socios_page, socios_data):
        self.socios_page = socios_page
        self.data_table = self.crear_tabla_socios(socios_data)

    def crear_tabla_socios(self, socios):
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
            rows=self.crear_filas(socios),
        )

    def crear_filas(self, socios):
        return [
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
                                ft.IconButton(ft.icons.EDIT, on_click=lambda _, s=socio: self.socios_page.mostrar_bottomsheet_editar(s)),
                                ft.IconButton(ft.icons.DELETE, on_click=lambda _, s=socio: self.socios_page.confirmar_eliminar_socio(s))
                            ]
                        )
                    )
                ],
            ) for socio in socios
        ]

    def actualizar_filas(self, socios):
        self.data_table.rows = self.crear_filas(socios)
        self.data_table.update()


class SociosForm:
    def __init__(self, socios_page, titulo, accion, socio=None):
        self.socios_page = socios_page
        self.formulario = self.crear_formulario_socio(titulo, accion, socio)

    def crear_formulario_socio(self, titulo, accion, socio=None):
        cedula = ft.TextField(label="Cédula", value=socio['cedula'] if socio else "")
        nombres = ft.TextField(label="Nombres", value=socio['nombres'] if socio else "")
        apellidos = ft.TextField(label="Apellidos", value=socio['apellidos'] if socio else "")
        direccion = ft.TextField(label="Dirección", value=socio['direccion'] if socio else "", multiline=True)
        telefono = ft.TextField(label="Teléfono", value=socio['numero_telefono'] if socio else "")
        control = ft.TextField(label="Control", value=socio['numero_control'] if socio else "")
        rif = ft.TextField(label="RIF", value=socio['rif'] if socio else "")
        fecha_nacimiento = ft.TextField(label="Fecha Nacimiento", hint_text="aaaa/dd/mm", value=socio['fecha_nacimiento'] if socio else "")

        formulario = ft.Container(
            ft.Column([
                ft.Row([cedula, nombres], spacing=10),
                ft.Row([apellidos, direccion], spacing=10),
                ft.Row([telefono, control], spacing=10),
                ft.Row([rif, fecha_nacimiento], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", on_click=lambda _: self.socios_page.cerrar_bottomsheet()),
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

        return formulario