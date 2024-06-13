import flet as ft
from controller.finanza_controlador import FinanzaControlador
import mysql.connector.errors
from fpdf import FPDF
from controller.auth_controlador import AuthControlador
import re
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Finanzas', 0, 1, 'C')

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

class FinanzasPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/finanzas")
        self.page = page
        self.bgcolor = "#F4F9FA"
        self.finanza_controlador = FinanzaControlador()
        self.finanzas_data = self.obtener_datos_finanzas()
        self.tabla_finanzas = FinanzasTable(self, self.finanzas_data)
        self.page.title = "FINANZAS"

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
                                    "FINANZAS",
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
                            controls=[self.tabla_finanzas.data_table],
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

    def obtener_datos_finanzas(self):
        return self.finanza_controlador.obtener_todas_finanzas()

    def mostrar_bottomsheet_agregar(self, e):
        self.bottom_sheet.content = FinanzasForm(self, "Agregar Finanza", self.guardar_finanza).formulario
        self.bottom_sheet.open = True
        self.page.update()

    def mostrar_bottomsheet_editar(self, finanza):
        self.bottom_sheet.content = FinanzasForm(self, "Editar Finanza", self.actualizar_finanza, finanza).formulario
        self.bottom_sheet.open = True
        self.page.update()

    def confirmar_eliminar_finanza(self, finanza):
        self.page.dialog = ft.AlertDialog(
            bgcolor="#0D1223",
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar la finanza con ID {finanza['ID_finanzas']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda _: self.eliminar_y_cerrar_dialogo(finanza['ID_finanzas']), style=ft.ButtonStyle(color="red"))
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def eliminar_y_cerrar_dialogo(self, ID_finanzas):
        self.eliminar_finanza(ID_finanzas)
        self.cerrar_dialogo()

    def cerrar_dialogo(self):
        self.page.dialog.open = False
        self.page.update()

    def cerrar_bottomsheet(self, e=None):
        self.bottom_sheet.open = False
        self.page.update()

    def guardar_finanza(self, cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr):
        try:
            if not cedula or not pagos_mensuales or not impuestos_anuales:
                raise ValueError("Los campos 'Cédula', 'Pagos Mensuales' e 'Impuestos Anuales' son obligatorios.")
            self.finanza_controlador.insertar_finanza(cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr)
            self.mostrar_snackbar("Finanza agregada correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def actualizar_finanza(self, ID_finanzas, cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr):
        try:
            if not ID_finanzas or not cedula or not pagos_mensuales or not impuestos_anuales:
                raise ValueError("Los campos 'ID de Finanzas', 'Cédula', 'Pagos Mensuales' e 'Impuestos Anuales' son obligatorios.")
            self.finanza_controlador.actualizar_finanza(ID_finanzas, cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr)
            self.mostrar_snackbar("Finanza actualizada correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def eliminar_finanza(self, ID_finanzas):
        try:
            self.finanza_controlador.eliminar_finanza(ID_finanzas)
            self.mostrar_snackbar("Finanza eliminada correctamente")
        except mysql.connector.errors.IntegrityError:
            self.mostrar_banner("No puedes eliminar esta finanza.")
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
        self.finanzas_data = self.obtener_datos_finanzas()
        self.tabla_finanzas.actualizar_filas(self.finanzas_data)
        self.cerrar_bottomsheet()
        self.page.update()

    def exportar_pdf(self, e):
        pdf = PDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="Reporte de Finanzas", ln=True, align='C')
        
        pdf.ln(10)

        for finanza in self.finanzas_data:
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt=f"ID Finanzas: {finanza['ID_finanzas']}", ln=True)
            pdf.set_font("Arial", 'B', size=10)
            pdf.cell(0, 10, txt=f"Cédula: {finanza['cedula']}", ln=True)
            pdf.cell(0, 10, txt=f"Pagos Mensuales: {finanza['pagos_mensuales']}", ln=True)
            pdf.cell(0, 10, txt=f"Impuestos Anuales: {finanza['impuestos_anuales']}", ln=True)
            pdf.cell(0, 10, txt=f"Fecha de Pago: {finanza['fecha_pago']}", ln=True)
            pdf.cell(0, 10, txt=f"Número de Control: {finanza['numero_contr']}", ln=True)
            
            pdf.ln(5)
        
        pdf.output("reporte_finanzas.pdf")
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

class FinanzasTable:
    def __init__(self, finanzas_page, finanzas_data):
        self.finanzas_page = finanzas_page
        self.data_table = self.crear_tabla_finanzas(finanzas_data)

    def crear_tabla_finanzas(self, finanzas):
        return ft.DataTable(
            bgcolor="#35353535",
            border_radius=20,
            columns=[
                ft.DataColumn(ft.Text("Número de Control", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Cédula", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Pagos Mensuales", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Impuestos Anuales", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Fecha de Pago", weight="w700", size=16, font_family="Arial Black italic")),
                
                ft.DataColumn(ft.Text("Acciones", weight="w800", size=19, font_family="Arial Black italic")),
            ],
            rows=self.crear_filas(finanzas),
        )

    def crear_filas(self, finanzas):
        rol = AuthControlador.obtener_rol()

        def obtener_acciones(finanza):
            acciones = []
            if rol in ["Admin", "Editor"]:
                acciones.append(ft.IconButton(ft.icons.EDIT, icon_color="#F4F9FA", on_click=lambda _, f=finanza: self.finanzas_page.mostrar_bottomsheet_editar(f)))
            if rol == "Admin":
                acciones.append(ft.IconButton(ft.icons.DELETE_OUTLINE, icon_color="#eb3936", on_click=lambda _, f=finanza: self.finanzas_page.confirmar_eliminar_finanza(f)))
            return acciones

        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(finanza['numero_contr'])),
                    ft.DataCell(ft.Text(finanza['cedula'])),
                    ft.DataCell(ft.Text(finanza['pagos_mensuales'])),
                    ft.DataCell(ft.Text(finanza['impuestos_anuales'])),
                    ft.DataCell(ft.Text(finanza['fecha_pago'])),
                    
                    ft.DataCell(
                        ft.Row(
                            obtener_acciones(finanza)
                        )
                    )
                ],
            ) for finanza in finanzas
        ]

    def actualizar_filas(self, finanzas):
        self.data_table.rows = self.crear_filas(finanzas)
        self.data_table.update()

class FinanzasForm:
    def __init__(self, finanzas_page, titulo, accion, finanza=None):
        self.finanzas_page = finanzas_page
        self.accion = accion
        self.finanza = finanza
        self.formulario = self.crear_formulario_finanza(titulo, accion, finanza)

    def crear_formulario_finanza(self, titulo, accion, finanza=None):
        cedula = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Cédula", 
            max_length=16, 
            width=180, 
            value=finanza['cedula'] if finanza and 'cedula' in finanza else "",
            on_change=self.validar_cedula,
            hint_text="V-/E-", 
        )
        pagos_mensuales = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Pagos Mensuales", 
            max_length=10, 
            width=120, 
            value=finanza['pagos_mensuales'] if finanza and 'pagos_mensuales' in finanza else "",
            input_filter=ft.NumbersOnlyInputFilter()
        )
        impuestos_anuales = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Impuestos Anuales", 
            max_length=10, 
            width=120, 
            value=finanza['impuestos_anuales'] if finanza and 'impuestos_anuales' in finanza else "",
            input_filter=ft.NumbersOnlyInputFilter()
        )
        fecha_pago = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Fecha de Pago", 
            max_length=10, 
            width=140, 
            hint_text="AAAA-MM-DD", 
            value=finanza['fecha_pago'] if finanza and 'fecha_pago' in finanza else "",
            on_change=self.validar_fecha
        )
        numero_contr = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Control", 
            max_length=2, 
            width=100, 
            value=finanza['numero_contr'] if finanza and 'numero_contr' in finanza else "",
            input_filter=ft.NumbersOnlyInputFilter()
        )

        formulario = ft.Container(
            ft.Column([
                ft.Row([cedula, pagos_mensuales, impuestos_anuales, fecha_pago], spacing=10),
                ft.Row([ numero_contr], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", icon=ft.icons.CANCEL, style=ft.ButtonStyle(color="#eb3936"), on_click=lambda _: self.finanzas_page.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", icon=ft.icons.SAVE, style=ft.ButtonStyle(color="#06F58E"), on_click=lambda _: self.guardar_finanza(
                            finanza['ID_finanzas'] if finanza else None, cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr
                        ))
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ]),
            padding=20,
            border_radius=15,
        )

        return formulario

    def validar_fecha(self, e):
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

    def guardar_finanza(self, ID_finanzas, cedula, pagos_mensuales, impuestos_anuales, fecha_pago, numero_contr):
        fecha_str = fecha_pago.value if isinstance(fecha_pago.value, str) else fecha_pago.value.strftime('%Y-%m-%d')
        if (Validacion.validar_fecha(fecha_str) and
            Validacion.validar_cedula(cedula.value)):
            if ID_finanzas:
                self.accion(ID_finanzas, cedula.value, pagos_mensuales.value, impuestos_anuales.value, fecha_str, numero_contr.value)
            else:
                self.accion(cedula.value, pagos_mensuales.value, impuestos_anuales.value, fecha_str, numero_contr.value)
        else:
            if not Validacion.validar_fecha(fecha_str):
                self.finanzas_page.mostrar_banner("La fecha de pago no es válida. Debe estar en el formato 'AAAA-MM-DD'.")
            if not Validacion.validar_cedula(cedula.value):
                self.finanzas_page.mostrar_banner("La cédula no es válida. Debe ser 'V-' o 'E-' seguido de 7 a 9 dígitos.")
            if not Validacion.validar_texto(pagos_mensuales.value):
                self.finanzas_page.mostrar_banner("El valor de los pagos mensuales no es válido. Solo se permiten letras y espacios.")
            if not Validacion.validar_texto(impuestos_anuales.value):
                self.finanzas_page.mostrar_banner("El valor de los impuestos anuales no es válido. Solo se permiten letras y espacios.")

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
                ft.TextButton("AVANCES", scale=1.2, icon=ft.icons.WORK_OUTLINE, on_click=lambda _: page.go("/avances")),
                ft.VerticalDivider(width=2.5),
                ft.TextButton("SANCIONES", scale=1.2, icon=ft.icons.REPORT_OUTLINED, on_click=lambda _: page.go("/sanciones")),
                ft.VerticalDivider(width=2.5),
                ft.TextButton("FINANZAS", scale=1.2, icon=ft.icons.PAYMENTS, style=ft.ButtonStyle(color="#F4F9FA"), on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=40),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
