import flet as ft
from controller.vehiculo_controlador import VehiculoControlador
import mysql.connector.errors
from fpdf import FPDF
from controller.auth_controlador import AuthControlador
import re
from datetime import datetime


class VehiculosPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/vehiculos")
        self.page = page
        self.bgcolor = "#F4F9FA"
        self.vehiculo_controlador = VehiculoControlador()
        self.vehiculos_data = self.obtener_datos_vehiculos()
        self.tabla_vehiculos = VehiculosTable(self, self.vehiculos_data)
        self.page.title = "VEHICULOS"
        
        self.rol = AuthControlador.obtener_rol()

        btn_agregar = None
        if self.rol in ["Admin", "Editor"]:
            btn_agregar = ft.IconButton(icon=ft.icons.ADD, on_click=self.mostrar_bottomsheet_agregar, icon_size=40, style=ft.ButtonStyle(color="#06F58E"))
        elif self.rol == "Viewer":
            btn_agregar = ""  

        self.controls = [
            ft.Container(
                bgcolor="#111111",
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.center_right,
                    colors=["#0D1223", "#182241"]
                ),
                border_radius=20,
                content=ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "VEHÍCULOS",
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
                                Botones_nav.crear_botones_navegacion(self.page),
                                ft.PopupMenuButton(
                                    bgcolor="#1E2A4A",
                                    items=[
                                        ft.PopupMenuItem(
                                            text="Exportar PDF",
                                            icon=ft.icons.PICTURE_AS_PDF,
                                            on_click=self.exportar_pdf,
                                        ),
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
                        ft.ListView(
                            controls=[self.tabla_vehiculos.data_table],
                            expand=True,
                            spacing=10,
                            padding=20,
                            auto_scroll=True
                        ),
                        ft.Row(
                            [btn_agregar] if btn_agregar else [],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    expand=True,
                    spacing=10
                ),
                expand=True,
                bgcolor="#111111",
                border_radius=20,
                image_src="image\LOGO_SAN_AGATON_REMASTER1.png",
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.center_right,
                    colors=["#0D1223", "#182241"]
                ),
            ),
        ]

        self.bottom_sheet = ft.BottomSheet(
            ft.Container(),
            open=False,
            bgcolor="#0D1223",
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
            bgcolor="#0D1223",
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar el vehículo asociado al control {vehiculo['numero_control']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda _: self.eliminar_y_cerrar_dialogo(vehiculo['ID_vehiculo']), style=ft.ButtonStyle(color="red"))
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def eliminar_y_cerrar_dialogo(self, id_vehiculo):
        self.eliminar_vehiculo(id_vehiculo)
        self.cerrar_dialogo()

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
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def actualizar_vehiculo(self, id_vehiculo, cedula, numero_control, marca, modelo, ano, placa):
        try:
            if not id_vehiculo or not cedula or not numero_control or not marca or not modelo or not ano or not placa:
                raise ValueError("Todos los campos son obligatorios.")
            self.vehiculo_controlador.actualizar_vehiculo(id_vehiculo, cedula, numero_control, marca, modelo, ano, placa)
            self.mostrar_snackbar("Vehículo actualizado correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def eliminar_vehiculo(self, id_vehiculo):
        try:
            self.vehiculo_controlador.eliminar_vehiculo(id_vehiculo)
            self.mostrar_snackbar("Vehículo eliminado correctamente")
        except mysql.connector.errors.IntegrityError:
            self.mostrar_banner("No puedes eliminar este vehículo sin primero eliminar los datos asociados.")
        self.refrescar_datos()

    def mostrar_snackbar(self, mensaje):
        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor="#F4F9FA")
        self.page.snack_bar.open = True
        self.page.update()

    def mostrar_banner(self, mensaje):
        self.page.banner = ft.AlertDialog(
            content=ft.Text(mensaje, color=ft.colors.WHITE),
            bgcolor="#eb3936",
            actions=[
                ft.TextButton("CERRAR", on_click=lambda _: self.cerrar_banner(), style=ft.ButtonStyle(color=ft.colors.WHITE))
            ]
        )
        self.page.banner.open = True
        self.page.update()

    def cerrar_banner(self):
        self.page.banner.open = False
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
        
        pdf.ln(10)
        
        for vehiculo in self.vehiculos_data:
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt=f"Control: {vehiculo['numero_control']}", ln=True)
            pdf.set_font("Arial", 'B', size=10)
            pdf.cell(0, 10, txt=f"Cédula: {vehiculo['cedula']}", ln=True)
    
            pdf.cell(0, 10, txt=f"Marca: {vehiculo['marca']}", ln=True)
            pdf.cell(0, 10, txt=f"Modelo: {vehiculo['modelo']}", ln=True)
            pdf.cell(0, 10, txt=f"Año: {vehiculo['ano']}", ln=True)
            pdf.cell(0, 10, txt=f"Placa: {vehiculo['Placa']}", ln=True)
            
            pdf.ln(5)
        
        pdf.output("reporte_vehiculos.pdf")
        self.mostrar_snackbar("PDF generado correctamente")

    def show_logout_popup(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Cierre de Sesión"),
            content=ft.Text("¿Está seguro de que desea cerrar sesión?"),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog, style=ft.ButtonStyle(color="#eb3936")),
                ft.TextButton("Cerrar Sesión", on_click=self.logout),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#0D1223"
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

class VehiculosTable:
    def __init__(self, vehiculos_page, vehiculos_data):
        self.vehiculos_page = vehiculos_page
        self.data_table = self.crear_tabla_vehiculos(vehiculos_data)

    def crear_tabla_vehiculos(self, vehiculos):
        return ft.DataTable(
            bgcolor="#35353535",
            border_radius=20,
            columns=[
                ft.DataColumn(ft.Text("Control", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Cédula", weight="w700", size=16, font_family="Arial Black italic")),
                
                ft.DataColumn(ft.Text("Marca", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Modelo", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Año", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Placa", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Acciones", weight="w800", size=19, font_family="Arial Black italic"))
            ],
            rows=self.crear_filas(vehiculos),
        )

    def crear_filas(self, vehiculos):
        rol = AuthControlador.obtener_rol()

        def obtener_acciones(vehiculo):
            acciones = []
            if rol in ["Admin", "Editor"]:
                acciones.append(ft.IconButton(ft.icons.EDIT, icon_color="#F4F9FA", on_click=lambda _, v=vehiculo: self.vehiculos_page.mostrar_bottomsheet_editar(v)))
            if rol == "Admin":
                acciones.append(ft.IconButton(ft.icons.DELETE_OUTLINE, icon_color="#eb3936", on_click=lambda _, v=vehiculo: self.vehiculos_page.confirmar_eliminar_vehiculo(v)))
            return acciones

        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(vehiculo['numero_control'])),
                    ft.DataCell(ft.Text(vehiculo['cedula'])),
                    
                    ft.DataCell(ft.Text(vehiculo['marca'])),
                    ft.DataCell(ft.Text(vehiculo['modelo'])),
                    ft.DataCell(ft.Text(vehiculo['ano'])),
                    ft.DataCell(ft.Text(vehiculo['Placa'])),
                    ft.DataCell(
                        ft.Row(
                            obtener_acciones(vehiculo)
                        )
                    )
                ],
            ) for vehiculo in vehiculos
        ]

    def actualizar_filas(self, vehiculos):
        self.data_table.rows = self.crear_filas(vehiculos)
        self.data_table.update()

class Validacion:
    @staticmethod
    def validar_ano(ano):
        patron = r'^\d{4}$'
        return re.match(patron, ano) is not None

    @staticmethod
    def validar_cedula(cedula):
        patron = r'^[VE]-\d{7,9}$'
        return re.match(patron, cedula) is not None

    @staticmethod
    def validar_texto(texto):
        patron = r'^[a-zA-Z\s]+$'
        return re.match(patron, texto) is not None

    @staticmethod
    def validar_placa(placa):
        patron = r'^[A-Z0-9]{6,10}$'
        return re.match(patron, placa) is not None

class VehiculosForm:
    def __init__(self, vehiculos_page, titulo, accion, vehiculo=None):
        self.vehiculos_page = vehiculos_page
        self.accion = accion
        self.vehiculo = vehiculo
        self.formulario = self.crear_formulario_vehiculo(titulo, accion, vehiculo)

    def crear_formulario_vehiculo(self, titulo, accion, vehiculo=None):
        cedula = ft.TextField(
            border_radius=13,
            border_color="#F4F9FA",
            focused_border_color="#06F58E",
            label="Cédula del Socio",
            max_length=11,
            width=180,
            hint_text="V-/E-",
            value=vehiculo['cedula'] if vehiculo else "",
            on_change=self.validar_cedula
        )
        numero_control = ft.TextField(
            border_radius=13,
            border_color="#F4F9FA",
            focused_border_color="#06F58E",
            label="Control",
            max_length=2,
            width=100,
            input_filter=ft.NumbersOnlyInputFilter(),
            value=vehiculo['numero_control'] if vehiculo else ""
        )
        marca = ft.TextField(
            border_radius=13,
            border_color="#F4F9FA",
            focused_border_color="#06F58E",
            label="Marca",
            max_length=30,
            width=280,
            value=vehiculo['marca'] if vehiculo else ""
        )
        modelo = ft.TextField(
            border_radius=13,
            border_color="#F4F9FA",
            focused_border_color="#06F58E",
            label="Modelo",
            width=280,
            max_length=30,
            value=vehiculo['modelo'] if vehiculo else ""
        )
        ano = ft.TextField(
            border_radius=13,
            border_color="#F4F9FA",
            focused_border_color="#06F58E",
            label="Año",
            max_length=4,
            width=120,
            input_filter=ft.NumbersOnlyInputFilter(),
            value=str(vehiculo['ano']) if vehiculo else "",
            on_change=self.validar_ano
        )
        placa = ft.TextField(
            border_radius=13,
            border_color="#F4F9FA",
            focused_border_color="#06F58E",
            label="Placa",
            max_length=8,
            width=160,
            value=vehiculo['Placa'] if vehiculo else "",
            on_change=self.validar_placa
        )

        formulario = ft.Container(
            ft.Column([
                ft.Row([numero_control, cedula, marca ], spacing=10),
                ft.Row([modelo,ano, placa], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", icon=ft.icons.CANCEL, style=ft.ButtonStyle(color="#eb3936"), on_click=lambda _: self.vehiculos_page.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", icon=ft.icons.SAVE, style=ft.ButtonStyle(color="#06F58E"), on_click=lambda _: self.guardar_vehiculo(
                            vehiculo['ID_vehiculo'] if vehiculo else None,
                            cedula, numero_control, marca, modelo, ano, placa
                        ))
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ]),
            padding=20,
            border_radius=15,
        )

        return formulario

    def validar_cedula(self, e):
        if Validacion.validar_cedula(e.control.value):
            e.control.error_text = None
            e.control.update()
        else:
            e.control.error_text = "'V-' o 'E-'"
            e.control.update()

    def validar_texto(self, e):
        if Validacion.validar_texto(e.control.value):
            e.control.error_text = None
            e.control.update()
        else:
            e.control.error_text = "Solo se permiten letras"
            e.control.update()

    def validar_ano(self, e):
        if Validacion.validar_ano(e.control.value):
            e.control.error_text = None
            e.control.update()
        else:
            e.control.error_text = "Año inválido"
            e.control.update()

    def validar_placa(self, e):
        if Validacion.validar_placa(e.control.value):
            e.control.error_text = None
            e.control.update()
        else:
            e.control.error_text = "Placa inválida"
            e.control.update()

    def guardar_vehiculo(self, id_vehiculo, cedula, numero_control, marca, modelo, ano, placa):
        if (Validacion.validar_cedula(cedula.value) and
            Validacion.validar_ano(ano.value) and
            Validacion.validar_placa(placa.value)):
            if id_vehiculo is not None:
                self.accion(id_vehiculo, cedula.value, numero_control.value, marca.value, modelo.value, ano.value, placa.value)
            else:
                self.accion(cedula.value, numero_control.value, marca.value, modelo.value, ano.value, placa.value)
        else:
            if not Validacion.validar_cedula(cedula.value):
                self.vehiculos_page.mostrar_banner("La cédula no es válida. Debe ser 'V-' o 'E-' seguido de 7 a 9 dígitos.")
            if not Validacion.validar_ano(ano.value):
                self.vehiculos_page.mostrar_banner("El año no es válido. Debe ser un año de 4 dígitos.")
            if not Validacion.validar_placa(placa.value):
                self.vehiculos_page.mostrar_banner("La placa no es válida.")

class Botones_nav:
    @staticmethod
    def crear_botones_navegacion(page):
        return ft.Row(
            [
                ft.TextButton("INICIO", scale=1.2, icon=ft.icons.HOME_OUTLINED, on_click=lambda _: page.go("/menu")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("SOCIOS", scale=1.2, icon=ft.icons.PEOPLE_OUTLINE , on_click=lambda _: page.go("/socios")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("VEHICULOS", scale=1.2, icon=ft.icons.LOCAL_TAXI,style=ft.ButtonStyle(color="#F4F9FA"), on_click=lambda _: page.go("/vehiculos")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("AVANCES", scale=1.2, icon=ft.icons.WORK_OUTLINE, on_click=lambda _: page.go("/avances")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("SANCIONES", scale=1.2, icon=ft.icons.REPORT_OUTLINED, on_click=lambda _: page.go("/sanciones")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("FINANZAS", scale=1.2, icon=ft.icons.PAYMENTS_OUTLINED, on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=40,),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Vehículos', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def celda_multiple(self, w, h, text, border=0, ln=0, align='', fill=False):
        lines = self.multi_cell(w, h, text, border=0, ln=0, align='', fill=False, split_only=True)
        for line in lines:
            self.cell(w, h, line, border=border, ln=2, align=align, fill=fill)
            border = 0
        if ln > 0:
            self.ln(h)