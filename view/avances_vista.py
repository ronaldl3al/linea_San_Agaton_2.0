import flet as ft
from controller.avances_controlador import AvanceControlador
import mysql.connector.errors
from fpdf import FPDF
from controller.auth_controlador import AuthControlador
import re
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Avances', 0, 1, 'C')

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

class AvancesPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/avances")
        self.page = page
        self.bgcolor = "#F4F9FA"
        self.avance_controlador = AvanceControlador()
        self.avances_data = self.obtener_datos_avances()
        self.tabla_avances = AvancesTable(self, self.avances_data)
        self.page.title = "AVANCES"

        self.rol = AuthControlador.obtener_rol()
        btn_agregar = None
        if self.rol in ["Admin", "Editor"]:
            btn_agregar = ft.IconButton(icon=ft.icons.ADD, on_click=self.mostrar_bottomsheet_agregar, icon_size=40)
        elif self.rol == "Viewer":
            btn_agregar = ft.IconButton(icon=ft.icons.ADD, on_click=None, icon_size=40)

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
                                    "AVANCES",
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
                            controls=[self.tabla_avances.data_table],
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

    def obtener_datos_avances(self):
        return self.avance_controlador.obtener_todos_avances()

    def mostrar_bottomsheet_agregar(self, e):
        self.bottom_sheet.content = AvancesForm(self, "Agregar Avance", self.guardar_avance).formulario
        self.bottom_sheet.open = True
        self.page.update()

    def mostrar_bottomsheet_editar(self, avance):
        self.bottom_sheet.content = AvancesForm(self, "Editar Avance", self.actualizar_avance, avance).formulario
        self.bottom_sheet.open = True
        self.page.update()


    def confirmar_eliminar_avance(self, avance):
        self.page.dialog = ft.AlertDialog(
            bgcolor="#0D1223",
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar el avance {avance['nombre']} {avance['apellido']}?"),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda _: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda _: self.eliminar_y_cerrar_dialogo(avance['ID_avance']), style=ft.ButtonStyle(color="red"))
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def eliminar_y_cerrar_dialogo(self, ID_avance):
        self.eliminar_avance(ID_avance)
        self.cerrar_dialogo()

    def cerrar_dialogo(self):
        self.page.dialog.open = False
        self.page.update()

    def cerrar_bottomsheet(self, e=None):
        self.bottom_sheet.open = False
        self.page.update()

    def guardar_avance(self, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf):
        try:
            if not numero_control or not nombre or not apellido:
                raise ValueError("Los campos 'Control', 'Nombre' y 'Apellido' son obligatorios.")
            self.avance_controlador.insertar_avance(numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf)
            self.mostrar_snackbar("Avance agregado correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def actualizar_avance(self, ID_avance, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf):
        try:
            if not ID_avance or not nombre or not apellido:
                raise ValueError("Los campos 'ID de Avance', 'Nombre' y 'Apellido' son obligatorios.")
            self.avance_controlador.actualizar_avance(ID_avance, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf)
            self.mostrar_snackbar("Avance actualizado correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def eliminar_avance(self, ID_avance):
        try:
            self.avance_controlador.eliminar_avance(ID_avance)
            self.mostrar_snackbar("Avance eliminado correctamente")
        except mysql.connector.errors.IntegrityError:
            self.mostrar_banner("No puedes eliminar este avance.")
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
        self.avances_data = self.obtener_datos_avances()
        self.tabla_avances.actualizar_filas(self.avances_data)
        self.cerrar_bottomsheet()
        self.page.update()

    def exportar_pdf(self, e):
        pdf = PDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="Reporte de Avances", ln=True, align='C')
        
        pdf.ln(10)

        for avance in self.avances_data:
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt=f"ID Avance: {avance['ID_avance']}", ln=True)
            pdf.set_font("Arial", 'B', size=10)
            pdf.cell(0, 10, txt=f"Nombre: {avance['nombre']}", ln=True)
            pdf.cell(0, 10, txt=f"Apellido: {avance['apellido']}", ln=True)
            pdf.cell(0, 10, txt=f"Control: {avance['numero_control']}", ln=True)
            pdf.cell(0, 10, txt=f"Fecha de Nacimiento: {avance['fecha_nacimiento']}", ln=True)
            pdf.cell(0, 10, txt=f"RIF: {avance['rif']}", ln=True)
            pdf.cell(0, 10, txt=f"Cédula Avance: {avance['cedula_avance']}", ln=True)
            pdf.cell(0, 10, txt=f"Teléfono: {avance['numero_telf']}", ln=True)
            
            pdf.ln(5)
        
        pdf.output("reporte_avances.pdf")
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

class AvancesTable:
    def __init__(self, avances_page, avances_data):
        self.avances_page = avances_page
        self.data_table = self.crear_tabla_avances(avances_data)

    def crear_tabla_avances(self, avances):
        return ft.DataTable(
            bgcolor="#35353535",
            border_radius=20,
            columns=[
                ft.DataColumn(ft.Text("Control", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Nombre", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Apellido", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Cédula Avance", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Teléfono", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("RIF", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Fecha de Nac.", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Acciones", weight="w800", size=16, font_family="Arial Black italic")),
            ],
            rows=self.crear_filas(avances),
        )

    def crear_filas(self, avances):
        rol = AuthControlador.obtener_rol()

        def obtener_acciones(avance):
            acciones = []
            if rol in ["Admin", "Editor"]:
                acciones.append(ft.IconButton(ft.icons.EDIT, icon_color="#F4F9FA", on_click=lambda _, a=avance: self.avances_page.mostrar_bottomsheet_editar(a)))
            if rol == "Admin":
                acciones.append(ft.IconButton(ft.icons.DELETE_OUTLINE, icon_color="#eb3936", on_click=lambda _, a=avance: self.avances_page.confirmar_eliminar_avance(a)))
            return acciones

        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(avance['numero_control'])),
                    ft.DataCell(ft.Text(avance['nombre'])),
                    ft.DataCell(ft.Text(avance['apellido'])),
                    ft.DataCell(ft.Text(avance['cedula_avance'])),
                    ft.DataCell(ft.Text(avance['numero_telf'])),
                    ft.DataCell(ft.Text(avance['rif'])),
                    ft.DataCell(ft.Text(avance['fecha_nacimiento'])),

                    
                    
                    ft.DataCell(
                        ft.Row(
                            obtener_acciones(avance)
                        )
                    )
                ],
            ) for avance in avances
        ]

    def actualizar_filas(self, avances):
        self.data_table.rows = self.crear_filas(avances)
        self.data_table.update()

class AvancesForm:
    def __init__(self, avances_page, titulo, accion, avance=None):
        self.avances_page = avances_page
        self.accion = accion
        self.avance = avance
        self.formulario = self.crear_formulario_avance(titulo, accion, avance)

    def crear_formulario_avance(self, titulo, accion, avance=None):
        numero_control = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Control", 
            max_length=2, 
            width=85, 
            input_filter=ft.NumbersOnlyInputFilter(), 
            value=avance['numero_control'] if avance and 'numero_control' in avance else ""
        )
        nombre = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Nombre", 
            max_length=30, 
            width=250,
            value=avance['nombre'] if avance and 'nombre' in avance else "",
            on_change=self.validar_texto
        )
        apellido = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Apellido", 
            width=250,
            max_length=30, 
            value=avance['apellido'] if avance and 'apellido' in avance else "",
            on_change=self.validar_texto
        )
        cedula_avance = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Cédula Avance", 
            max_length=11, 
            width=130, 
            hint_text="V-/E-", 
            value=avance['cedula_avance'] if avance and 'cedula_avance' in avance else "",
            on_change=self.validar_cedula
        )
        numero_telf = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Teléfono", 
            max_length=11, 
            width=170, 
            prefix_text="+58 ", 
            input_filter=ft.NumbersOnlyInputFilter(), 
            hint_text="414 1234567", 
            value=avance['numero_telf'] if avance and 'numero_telf' in avance else ""
        )
        rif = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="RIF", 
            width=140, 
            max_length=15, 
            value=avance['rif'] if avance and 'rif' in avance else "",
            on_change=self.validar_rif,
            hint_text="V121233211",
        )
        fecha_nacimiento = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Fecha Nacimiento", 
            max_length=10, 
            width=135, 
            hint_text="AAAA-MM-DD", 
            value=avance['fecha_nacimiento'] if avance and 'fecha_nacimiento' in avance else "",
            on_change=self.validar_fecha_nacimiento
        )

        formulario = ft.Container(
            ft.Column([
                ft.Row([numero_control, nombre, apellido], spacing=10),
                ft.Row([ cedula_avance, fecha_nacimiento, numero_telf, rif], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", icon=ft.icons.CANCEL, style=ft.ButtonStyle(color="#eb3936"), on_click=lambda _: self.avances_page.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", icon=ft.icons.SAVE, style=ft.ButtonStyle(color="#06F58E"), on_click=lambda _: self.guardar_avance(
                            avance['ID_avance'] if avance else None, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf
                        ))
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ]),
            padding=20,
            border_radius=15,
        )

        return formulario


    def validar_fecha_nacimiento(self, e):
        if Validacion.validar_fecha(e.control.value):
            e.control.error_text = None
            e.control.update()
        else:
            e.control.error_text = "AAAA-MM-DD"
            e.control.update()

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

    def validar_rif(self, e):
        if Validacion.validar_rif(e.control.value):
            e.control.error_text = None
            e.control.update()
        else:
            e.control.error_text = "Formato RIF inválido"
            e.control.update()

    def guardar_avance(self, ID_avance, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf):
            fecha_str = fecha_nacimiento.value if isinstance(fecha_nacimiento.value, str) else fecha_nacimiento.value.strftime('%Y-%m-%d')
            if (Validacion.validar_fecha(fecha_str) and
                Validacion.validar_cedula(cedula_avance.value) and
                Validacion.validar_texto(nombre.value) and
                Validacion.validar_texto(apellido.value) and
                Validacion.validar_rif(rif.value)):
                if ID_avance:
                    self.accion(ID_avance, numero_control.value, nombre.value, apellido.value, fecha_str, rif.value, cedula_avance.value, numero_telf.value)
                else:
                    self.accion(numero_control.value, nombre.value, apellido.value, fecha_str, rif.value, cedula_avance.value, numero_telf.value)
            else:
                if not Validacion.validar_fecha(fecha_str):
                    self.avances_page.mostrar_banner("La fecha de nacimiento no es válida. Debe estar en el formato 'AAAA-MM-DD'.")
                if not Validacion.validar_cedula(cedula_avance.value):
                    self.avances_page.mostrar_banner("La cédula no es válida. Debe ser 'V-' o 'E-' seguido de 7 a 9 dígitos.")
                if not Validacion.validar_texto(nombre.value):
                    self.avances_page.mostrar_banner("El nombre no es válido. Solo se permiten letras y espacios.")
                if not Validacion.validar_texto(apellido.value):
                    self.avances_page.mostrar_banner("El apellido no es válido. Solo se permiten letras y espacios.")
                if not Validacion.validar_rif(rif.value):
                    self.avances_page.mostrar_banner("El RIF no es válido. Debe empezar por 'V', 'E', 'J', 'P', 'G' seguido de 7 a 10 dígitos.")

class Validacion:
    @staticmethod
    def validar_fecha(fecha):
        if isinstance(fecha, datetime):
            fecha = fecha.strftime('%Y-%m-%d')
        patron = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(patron, fecha) is not None

    @staticmethod
    def validar_cedula(cedula):
        patron = r'^[VE]-\d{7,9}$'
        return re.match(patron, cedula) is not None

    @staticmethod
    def validar_texto(texto):
        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
        return re.match(patron, texto) is not None

    @staticmethod
    def validar_rif(rif):
        patron = r'^[VEJPG]\d{7,10}$'
        return re.match(patron, rif) is not None

class Botones_nav:
    @staticmethod
    def crear_botones_navegacion(page):
        return ft.Row(
            [
                ft.TextButton("INICIO", scale=1.2, icon=ft.icons.HOME_OUTLINED, on_click=lambda _: page.go("/menu")),
                ft.VerticalDivider(width=2.5),
                ft.TextButton("SOCIOS", scale=1.2, icon=ft.icons.PEOPLE_OUTLINE, on_click=lambda _: page.go("/socios")),
                ft.VerticalDivider(width=2.5),
                ft.TextButton("VEHICULOS", scale=1.2, icon=ft.icons.LOCAL_TAXI_OUTLINED, on_click=lambda _: page.go("/vehiculos")),
                ft.VerticalDivider(width=2.5),
                ft.TextButton("AVANCES", scale=1.2, icon=ft.icons.WORK, style=ft.ButtonStyle(color="#F4F9FA"), on_click=lambda _: page.go("/avances")),
                ft.VerticalDivider(width=2.5),
                ft.TextButton("SANCIONES", scale=1.2, icon=ft.icons.REPORT_OUTLINED, on_click=lambda _: page.go("/sanciones")),
                ft.VerticalDivider(width=2.5),
                ft.TextButton("FINANZAS", scale=1.2, icon=ft.icons.PAYMENTS_OUTLINED, on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=40),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
