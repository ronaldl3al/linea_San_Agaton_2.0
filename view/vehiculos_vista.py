import flet as ft
from controller.vehiculo_controlador import VehiculoControlador
from view.common.common import Common
import mysql.connector.errors
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Vehículos', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def cell_with_multiline(self, w, h, text, border=0, ln=0, align='', fill=False):
        lines = self.multi_cell(w, h, text, border=0, ln=0, align='', fill=False, split_only=True)
        for line in lines:
            self.cell(w, h, line, border=border, ln=2, align=align, fill=fill)
            border = 0  # Only border the first line
        if ln > 0:
            self.ln(h)


class VehiculosPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/vehiculos")
        self.page = page
        self.vehiculo_controlador = VehiculoControlador()
        self.vehiculos_data = self.obtener_datos_vehiculos()
        self.tabla_vehiculos = VehiculosTable(self, self.vehiculos_data)
        
        self.controls = [
            ft.AppBar(
                title=ft.Text("Vehículos"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu")),
                actions=[
                    Common.crear_botones_navegacion(self.page),
                    ft.IconButton(icon=ft.icons.PICTURE_AS_PDF, on_click=self.exportar_pdf)
                ]
            ),
            ft.Container(
                content=ft.ListView(
                    controls=[self.tabla_vehiculos.data_table],
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

    def obtener_datos_vehiculos(self):
        return self.vehiculo_controlador.obtener_todos_vehiculos()

    def mostrar_bottomsheet_agregar(self, e):
        self.bottom_sheet.content = VehiculosForm(self, "Agregar Vehículo", self.guardar_vehiculo).formulario
        self.bottom_sheet.open = True
        self.page.update()

    def mostrar_bottomsheet_editar(self, vehiculo):
        self.bottom_sheet.content = VehiculosForm(self, "Editar Vehículo", self.actualizar_vehiculo, vehiculo).formulario
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
        except ValueError as ve:
            self.mostrar_snackbar(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_snackbar(f"Error de base de datos: {err}")

    def actualizar_vehiculo(self, id_vehiculo, cedula, numero_control, marca, modelo, ano, placa):
        try:
            if not id_vehiculo or not cedula or not numero_control or not marca or not modelo or not ano or not placa:
                raise ValueError("Todos los campos son obligatorios.")
            self.vehiculo_controlador.actualizar_vehiculo(id_vehiculo, cedula, numero_control, marca, modelo, ano, placa)
            self.mostrar_snackbar("Vehículo actualizado correctamente")
            self.refrescar_datos()
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
        self.tabla_vehiculos.actualizar_filas(self.vehiculos_data)
        self.cerrar_bottomsheet()
        self.page.update()

    def exportar_pdf(self, e):
        pdf = PDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="Reporte de Vehículos", ln=True, align='C')
        
        pdf.ln(10)  # Espacio debajo del título
        
        # Data rows
        for vehiculo in self.vehiculos_data:
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt=f"ID Vehículo: {vehiculo['ID_vehiculo']}", ln=True)
            pdf.set_font("Arial", 'B', size=10)
            pdf.cell(0, 10, txt=f"Cédula: {vehiculo['cedula']}", ln=True)
            pdf.cell(0, 10, txt=f"Número de Control: {vehiculo['numero_control']}", ln=True)
            pdf.cell(0, 10, txt=f"Marca: {vehiculo['marca']}", ln=True)
            pdf.cell(0, 10, txt=f"Modelo: {vehiculo['modelo']}", ln=True)
            pdf.cell(0, 10, txt=f"Año: {vehiculo['ano']}", ln=True)
            pdf.cell(0, 10, txt=f"Placa: {vehiculo['Placa']}", ln=True)
            
            pdf.ln(5)  # Espacio entre registros de vehículos
        
        pdf.output("reporte_vehiculos.pdf")
        self.mostrar_snackbar("PDF generado correctamente")

class VehiculosTable:
    def __init__(self, vehiculos_page, vehiculos_data):
        self.vehiculos_page = vehiculos_page
        self.data_table = self.crear_tabla_vehiculos(vehiculos_data)

    def crear_tabla_vehiculos(self, vehiculos):
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
            rows=self.crear_filas(vehiculos),
        )

    def crear_filas(self, vehiculos):
        return [
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
                                ft.IconButton(ft.icons.EDIT, on_click=lambda _, v=vehiculo: self.vehiculos_page.mostrar_bottomsheet_editar(v)),
                                ft.IconButton(ft.icons.DELETE, on_click=lambda _, v=vehiculo: self.vehiculos_page.confirmar_eliminar_vehiculo(v))
                            ]
                        )
                    )
                ],
            ) for vehiculo in vehiculos
        ]

    def actualizar_filas(self, vehiculos):
        self.data_table.rows = self.crear_filas(vehiculos)
        self.data_table.update()


class VehiculosForm:
    def __init__(self, vehiculos_page, titulo, accion, vehiculo=None):
        self.vehiculos_page = vehiculos_page
        self.formulario = self.crear_formulario_vehiculo(titulo, accion, vehiculo)

    def crear_formulario_vehiculo(self, titulo, accion, vehiculo=None):
        cedula = ft.TextField(label="Cédula", value=vehiculo['cedula'] if vehiculo else "")
        numero_control = ft.TextField(label="Número de Control", value=vehiculo['numero_control'] if vehiculo else "")
        marca = ft.TextField(label="Marca", value=vehiculo['marca'] if vehiculo else "")
        modelo = ft.TextField(label="Modelo", value=vehiculo['modelo'] if vehiculo else "")
        ano = ft.TextField(label="Año", value=vehiculo['ano'] if vehiculo else "")
        placa = ft.TextField(label="Placa", value=vehiculo['Placa'] if vehiculo else "")

        formulario = ft.Container(
            ft.Column([
                ft.Row([cedula, numero_control], spacing=10),
                ft.Row([marca, modelo], spacing=10),
                ft.Row([ano, placa], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", on_click=lambda _: self.vehiculos_page.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", on_click=lambda _: accion(
                            vehiculo['ID_vehiculo'] if vehiculo else None,
                            cedula.value, numero_control.value, marca.value, modelo.value, ano.value, placa.value
                        ) if vehiculo else self.vehiculos_page.guardar_vehiculo(
                            cedula.value, numero_control.value, marca.value, modelo.value, ano.value, placa.value
                        ))
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ]),
            padding=20,
            border_radius=15,
        )

        return formulario
