import flet as ft
from controller.sanciones_controlador import SancionControlador
import mysql.connector.errors
from fpdf import FPDF
from controller.auth_controlador import AuthControlador
import re
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Sanciones', 0, 1, 'C')

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

class SancionesPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/sanciones")
        self.page = page
        self.bgcolor = "#F4F9FA"
        self.sancion_controlador = SancionControlador()
        self.sanciones_data = self.obtener_datos_sanciones()
        self.tabla_sanciones = SancionesTable(self, self.sanciones_data)

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
                                    "SANCIONES",
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
                            controls=[self.tabla_sanciones.data_table],
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

    def obtener_datos_sanciones(self):
        return self.sancion_controlador.obtener_todas_sanciones()

    def mostrar_bottomsheet_agregar(self, e):
        self.bottom_sheet.content = SancionesForm(self, "Agregar Sanción", self.guardar_sancion).formulario
        self.bottom_sheet.open = True
        self.page.update()

    def mostrar_bottomsheet_editar(self, sancion):
        self.bottom_sheet.content = SancionesForm(self, "Editar Sanción", self.actualizar_sancion, sancion).formulario
        self.bottom_sheet.open = True
        self.page.update()

    def confirmar_eliminar_sancion(self, sancion):
        self.page.dialog = ft.AlertDialog(
            bgcolor="#0D1223",
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar la sanción {sancion['motivo_sancion']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda _: self.eliminar_y_cerrar_dialogo(sancion['ID_sancion']), style=ft.ButtonStyle(color="red"))
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def eliminar_y_cerrar_dialogo(self, ID_sancion):
        self.eliminar_sancion(ID_sancion)
        self.cerrar_dialogo()

    def cerrar_dialogo(self):
        self.page.dialog.open = False
        self.page.update()

    def cerrar_bottomsheet(self, e=None):
        self.bottom_sheet.open = False
        self.page.update()

    def guardar_sancion(self, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido):
        try:
            if not cedula or not motivo_sancion or not nombre or not apellido:
                raise ValueError("Los campos 'Cédula', 'Motivo de Sanción', 'Nombre' y 'Apellido' son obligatorios.")
            self.sancion_controlador.insertar_sancion(cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido)
            self.mostrar_snackbar("Sanción agregada correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def actualizar_sancion(self, ID_sancion, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido):
        try:
            if not ID_sancion or not motivo_sancion or not nombre or not apellido:
                raise ValueError("Los campos 'ID de Sanción', 'Motivo de Sanción', 'Nombre' y 'Apellido' son obligatorios.")
            self.sancion_controlador.actualizar_sancion(ID_sancion, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido)
            self.mostrar_snackbar("Sanción actualizada correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def eliminar_sancion(self, ID_sancion):
        try:
            self.sancion_controlador.eliminar_sancion(ID_sancion)
            self.mostrar_snackbar("Sanción eliminada correctamente")
        except mysql.connector.errors.IntegrityError:
            self.mostrar_banner("No puedes eliminar esta sanción.")
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
        self.sanciones_data = self.obtener_datos_sanciones()
        self.tabla_sanciones.actualizar_filas(self.sanciones_data)
        self.cerrar_bottomsheet()
        self.page.update()

    def exportar_pdf(self, e):
        pdf = PDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="Reporte de Sanciones", ln=True, align='C')
        
        pdf.ln(10)

        for sancion in self.sanciones_data:
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt=f"ID Sanción: {sancion['ID_sancion']}", ln=True)
            pdf.set_font("Arial", 'B', size=10)
            pdf.cell(0, 10, txt=f"Cédula: {sancion['cedula']}", ln=True)
            pdf.cell(0, 10, txt=f"Motivo de Sanción: {sancion['motivo_sancion']}", ln=True)
            pdf.cell(0, 10, txt=f"Monto: {sancion['monto']}", ln=True)
            pdf.cell(0, 10, txt=f"Inicio de Sanción: {sancion['inicio_sancion']}", ln=True)
            pdf.cell(0, 10, txt=f"Final de Sanción: {sancion['final_sancion']}", ln=True)
            pdf.cell(0, 10, txt=f"Nombre: {sancion['nombre']}", ln=True)
            pdf.cell(0, 10, txt=f"Apellido: {sancion['apellido']}", ln=True)
            
            pdf.ln(5)
        
        pdf.output("reporte_sanciones.pdf")
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

class SancionesTable:
    def __init__(self, sanciones_page, sanciones_data):
        self.sanciones_page = sanciones_page
        self.data_table = self.crear_tabla_sanciones(sanciones_data)

    def crear_tabla_sanciones(self, sanciones):
        return ft.DataTable(
            bgcolor="#35353535",
            border_radius=20,
            columns=[
                ft.DataColumn(ft.Text("Cédula del Socio", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Nombre", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Apellido", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Inicio de Sanción", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Final de Sanción", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Monto", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Motivo de Sanción", weight="w700", size=16, font_family="Arial Black italic")),
                
                
                ft.DataColumn(ft.Text("Acciones", weight="w800", size=19, font_family="Arial Black italic")),
            ],
            rows=self.crear_filas(sanciones),
        )

    def crear_filas(self, sanciones):
        rol = AuthControlador.obtener_rol()

        def obtener_acciones(sancion):
            acciones = []
            if rol in ["Admin", "Editor"]:
                acciones.append(ft.IconButton(ft.icons.EDIT, icon_color="#F4F9FA", on_click=lambda _, s=sancion: self.sanciones_page.mostrar_bottomsheet_editar(s)))
            if rol == "Admin":
                acciones.append(ft.IconButton(ft.icons.DELETE_OUTLINE, icon_color="#eb3936", on_click=lambda _, s=sancion: self.sanciones_page.confirmar_eliminar_sancion(s)))
            return acciones

        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(sancion['cedula'])),
                    ft.DataCell(ft.Text(sancion['nombre'])),
                    ft.DataCell(ft.Text(sancion['apellido'])),
                    
                    ft.DataCell(ft.Text(sancion['inicio_sancion'])),
                    ft.DataCell(ft.Text(sancion['final_sancion'])),
                    ft.DataCell(ft.Text(sancion['monto'])),
                    ft.DataCell(ft.Text(sancion['motivo_sancion'])),
                    
                    ft.DataCell(
                        ft.Row(
                            obtener_acciones(sancion)
                        )
                    )
                ],
            ) for sancion in sanciones
        ]

    def actualizar_filas(self, sanciones):
        self.data_table.rows = self.crear_filas(sanciones)
        self.data_table.update()

class SancionesForm:
    def __init__(self, sanciones_page, titulo, accion, sancion=None):
        self.sanciones_page = sanciones_page
        self.accion = accion
        self.sancion = sancion
        self.formulario = self.crear_formulario_sancion(titulo, accion, sancion)

    def crear_formulario_sancion(self, titulo, accion, sancion=None):
        cedula = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Cédula del Socio", 
            max_length=16, 
            width=180, 
            value=sancion['cedula'] if sancion and 'cedula' in sancion else "",
            on_change=self.validar_cedula
        )
        motivo_sancion = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Motivo de Sanción", 
            max_length=30, 
            width=600, 
            multiline= True,
            value=sancion['motivo_sancion'] if sancion and 'motivo_sancion' in sancion else "",
            on_change=self.validar_texto
        )
        monto = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Monto", 
            max_length=10, 
            width=110, 
            value=sancion['monto'] if sancion and 'monto' in sancion else "",
            input_filter=ft.NumbersOnlyInputFilter()
        )
        inicio_sancion = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Inicio de Sanción", 
            max_length=10, 
            width=140, 
            hint_text="AAAA-MM-DD", 
            value=sancion['inicio_sancion'] if sancion and 'inicio_sancion' in sancion else "",
            on_change=self.validar_fecha
        )
        final_sancion = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Final de Sanción", 
            max_length=10, 
            width=140, 
            hint_text="AAAA-MM-DD", 
            value=sancion['final_sancion'] if sancion and 'final_sancion' in sancion else "",
            on_change=self.validar_fecha
        )
        nombre = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Nombre",
            width=295,
            max_length=60, 
            value=sancion['nombre'] if sancion and 'nombre' in sancion else "",
            on_change=self.validar_texto
        )
        apellido = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Apellido", 
            width=295,
            max_length=60, 
            value=sancion['apellido'] if sancion and 'apellido' in sancion else "",
            on_change=self.validar_texto
        )

        formulario = ft.Container(
            ft.Column([
                ft.Row([nombre, apellido ], spacing=10),
                ft.Row([cedula, monto, inicio_sancion, final_sancion], spacing=10),
                ft.Row([motivo_sancion], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", icon=ft.icons.CANCEL, style=ft.ButtonStyle(color="#eb3936"), on_click=lambda _: self.sanciones_page.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", icon=ft.icons.SAVE, style=ft.ButtonStyle(color="#06F58E"), on_click=lambda _: self.guardar_sancion(
                            sancion['ID_sancion'] if sancion else None, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido
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

    def guardar_sancion(self, ID_sancion, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido):
        fecha_inicio_str = inicio_sancion.value if isinstance(inicio_sancion.value, str) else inicio_sancion.value.strftime('%Y-%m-%d')
        fecha_final_str = final_sancion.value if isinstance(final_sancion.value, str) else final_sancion.value.strftime('%Y-%m-%d')
        if (Validacion.validar_fecha(fecha_inicio_str) and
            Validacion.validar_fecha(fecha_final_str) and
            Validacion.validar_cedula(cedula.value) and
            Validacion.validar_texto(motivo_sancion.value) and
            Validacion.validar_texto(nombre.value) and
            Validacion.validar_texto(apellido.value)):
            if ID_sancion:
                self.accion(ID_sancion, cedula.value, motivo_sancion.value, monto.value, fecha_inicio_str, fecha_final_str, nombre.value, apellido.value)
            else:
                self.accion(cedula.value, motivo_sancion.value, monto.value, fecha_inicio_str, fecha_final_str, nombre.value, apellido.value)
        else:
            if not Validacion.validar_fecha(fecha_inicio_str) or not Validacion.validar_fecha(fecha_final_str):
                self.sanciones_page.mostrar_banner("Las fechas no son válidas. Deben estar en el formato 'AAAA-MM-DD'.")
            if not Validacion.validar_cedula(cedula.value):
                self.sanciones_page.mostrar_banner("La cédula no es válida. Debe ser 'V-' o 'E-' seguido de 7 a 9 dígitos.")
            if not Validacion.validar_texto(motivo_sancion.value):
                self.sanciones_page.mostrar_banner("El motivo de sanción no es válido. Solo se permiten letras y espacios.")
            if not Validacion.validar_texto(nombre.value):
                self.sanciones_page.mostrar_banner("El nombre no es válido. Solo se permiten letras y espacios.")
            if not Validacion.validar_texto(apellido.value):
                self.sanciones_page.mostrar_banner("El apellido no es válido. Solo se permiten letras y espacios.")

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
        patron = r'^[a-zA-Z\s]+$'
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
                ft.TextButton("SANCIONES", scale=1.2, icon=ft.icons.REPORT, style=ft.ButtonStyle(color="#F4F9FA"), on_click=lambda _: page.go("/sanciones")),
                ft.VerticalDivider(width=2.5),
                ft.TextButton("FINANZAS", scale=1.2, icon=ft.icons.PAYMENTS_OUTLINED, on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=40),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
