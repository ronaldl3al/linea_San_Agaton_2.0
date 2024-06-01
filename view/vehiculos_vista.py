# vistas/vehiculos_vista.py

import flet as ft
from controller.vehiculo_controlador import VehiculoControlador
from view.common.common import Common
import mysql.connector.errors

class VehiculosPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/vehiculos")
        self.page = page
        self.vehiculo_controlador = VehiculoControlador()
        self.vehiculos_data = self.obtener_datos_vehiculos()
        self.tabla_vehiculos = self.crear_tabla_vehiculos()

        self.controls = [
            ft.AppBar(
                title=ft.Text("Vehículos"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu")),
                actions=[Common.crear_botones_navegacion(self.page)]
            ),
            ft.Column(
                [
                    ft.Row(
                        [self.tabla_vehiculos],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.mostrar_bottomsheet_agregar)
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.START
            )
        ]

        self.bottom_sheet = ft.BottomSheet(
            ft.Container(),
            open=False,
            on_dismiss=self.cerrar_bottomsheet
        )
        self.page.overlay.append(self.bottom_sheet)

    def obtener_datos_vehiculos(self):
        return self.vehiculo_controlador.obtener_todos_vehiculos()

    def crear_tabla_vehiculos(self):
        vehiculos = self.obtener_datos_vehiculos()
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Cédula")),
                ft.DataColumn(ft.Text("Número de Control")),
                ft.DataColumn(ft.Text("Marca")),
                ft.DataColumn(ft.Text("Modelo")),
                ft.DataColumn(ft.Text("Año")),
                ft.DataColumn(ft.Text("Placa")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(vehiculo['cedula'])),
                        ft.DataCell(ft.Text(vehiculo['numero_control'])),
                        ft.DataCell(ft.Text(vehiculo['marca'])),
                        ft.DataCell(ft.Text(vehiculo['modelo'])),
                        ft.DataCell(ft.Text(vehiculo['ano'])),
                        ft.DataCell(ft.Text(vehiculo['Placa'])),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(ft.icons.EDIT, on_click=lambda _, v=vehiculo: self.mostrar_bottomsheet_editar(v)),
                                    ft.IconButton(ft.icons.DELETE, on_click=lambda _, v=vehiculo: self.confirmar_eliminar_vehiculo(v))
                                ]
                            )
                        )
                    ],
                ) for vehiculo in vehiculos
            ],
        )

    def mostrar_bottomsheet_agregar(self, e):
        self.bottom_sheet.content = self.crear_formulario_vehiculo("Agregar Vehículo", self.guardar_vehiculo)
        self.bottom_sheet.open = True
        self.page.update()

    def mostrar_bottomsheet_editar(self, vehiculo):
        self.bottom_sheet.content = self.crear_formulario_vehiculo("Editar Vehículo", self.actualizar_vehiculo, vehiculo)
        self.bottom_sheet.open = True
        self.page.update()

    def confirmar_eliminar_vehiculo(self, vehiculo):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar el vehículo con ID {vehiculo['ID_vehiculo']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda _: self.eliminar_vehiculo(vehiculo['ID_vehiculo']))
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

    def guardar_vehiculo(self, cedula, numero_control, marca, modelo, ano, placa):
        try:
            if not cedula or not numero_control or not marca or not modelo or not ano or not placa:
                raise ValueError("Todos los campos son obligatorios.")
            self.vehiculo_controlador.insertar_vehiculo(cedula, numero_control, marca, modelo, ano, placa)
            self.mostrar_snackbar("Vehículo agregado correctamente")
            self.refrescar_datos()
            self.cerrar_bottomsheet()
        except ValueError as ve:
            self.mostrar_snackbar(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_snackbar(f"Error de base de datos: {err}")

    def actualizar_vehiculo(self, id_vehiculo, cedula, numero_control, marca, modelo, ano, placa):
        try:
            if not cedula or not numero_control or not marca or not modelo or not ano or not placa:
                raise ValueError("Todos los campos son obligatorios.")
            self.vehiculo_controlador.actualizar_vehiculo(id_vehiculo, cedula, numero_control, marca, modelo, ano, placa)
            self.mostrar_snackbar("Vehículo actualizado correctamente")
            self.refrescar_datos()
            self.cerrar_bottomsheet()
        except ValueError as ve:
            self.mostrar_snackbar(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_snackbar(f"Error de base de datos: {err}")

    def eliminar_vehiculo(self, id_vehiculo):
        try:
            self.vehiculo_controlador.eliminar_vehiculo(id_vehiculo)
            self.mostrar_snackbar("Vehículo eliminado correctamente")
        except mysql.connector.errors.IntegrityError:
            self.mostrar_snackbar("No puedes eliminar este vehículo sin primero eliminar los datos asociados.")
        self.refrescar_datos()

    def mostrar_snackbar(self, mensaje):
        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje))
        self.page.snack_bar.open = True
        self.page.update()

    def refrescar_datos(self):
        self.vehiculos_data = self.obtener_datos_vehiculos()
        self.tabla_vehiculos.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(vehiculo['ID_vehiculo']))),
                    ft.DataCell(ft.Text(vehiculo['cedula'])),
                    ft.DataCell(ft.Text(vehiculo['numero_control'])),
                    ft.DataCell(ft.Text(vehiculo['marca'])),
                    ft.DataCell(ft.Text(vehiculo['modelo'])),
                    ft.DataCell(ft.Text(vehiculo['ano'])),
                    ft.DataCell(ft.Text(vehiculo['Placa'])),
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.EDIT, on_click=lambda _, v=vehiculo: self.mostrar_bottomsheet_editar(v)),
                                ft.IconButton(ft.icons.DELETE, on_click=lambda _, v=vehiculo: self.confirmar_eliminar_vehiculo(v))
                            ]
                        )
                    )
                ],
            ) for vehiculo in self.vehiculos_data
        ]
        self.tabla_vehiculos.update()
        self.cerrar_bottomsheet()
        self.page.update()

    def crear_formulario_vehiculo(self, titulo, accion, vehiculo=None):
        height = 40  # Ajustar la altura según sea necesario

        cedula = ft.TextField(label="Cédula", value=vehiculo['cedula'] if vehiculo else "", height=height)
        numero_control = ft.TextField(label="Número de Control", value=vehiculo['numero_control'] if vehiculo else "", height=height)
        marca = ft.TextField(label="Marca", value=vehiculo['marca'] if vehiculo else "", height=height)
        modelo = ft.TextField(label="Modelo", value=vehiculo['modelo'] if vehiculo else "", height=height)
        ano = ft.TextField(label="Año", value=vehiculo['ano'] if vehiculo else "", height=height)
        placa = ft.TextField(label="Placa", value=vehiculo['Placa'] if vehiculo else "", height=height)

        return ft.Container(
            ft.Column([
                ft.Row([cedula, numero_control], spacing=10),
                ft.Row([marca, modelo], spacing=10),
                ft.Row([ano, placa], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", on_click=lambda _: accion(
                            cedula.value, numero_control.value, marca.value, modelo.value, ano.value, placa.value
                        ))
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ]),
            padding=20,
            border_radius=15,
        )
