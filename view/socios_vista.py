import flet as ft
from controller.socios_controlador import SocioControlador
import mysql.connector.errors
from fpdf import FPDF
from controller.auth_controlador import AuthControlador
import re
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos de Socios', 0, 1, 'C')

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

class SociosPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/socios")
        self.page = page
        self.bgcolor = "#F4F9FA"
        self.socio_controlador = SocioControlador()
        self.socios_data = self.obtener_datos_socios()
        self.tabla_socios = SociosTable(self, self.socios_data)
        
        # Obtener el rol del usuario autenticado
        self.rol = AuthControlador.obtener_rol()

        # Definir el botón de agregar en una variable dependiendo del rol
        btn_agregar = None
        if self.rol in ["Admin", "Editor"]:  # Asumiendo roles en mayúsculas como en la base de datos
            btn_agregar = ft.IconButton(icon=ft.icons.ADD, on_click=self.mostrar_bottomsheet_agregar, icon_size=40)
        elif self.rol == "Viewer":
            btn_agregar = ft.IconButton(icon=ft.icons.ADD, on_click=None, icon_size=40)  # Deshabilitar botón

        # 
        

        self.controls = [
            ft.Container(
                bgcolor="#111111",
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.center_right,
                    colors=["#0D1223", "#182241"]
                ),
                border_radius=20,
                content = ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "SOCIOS",
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
                            controls=[self.tabla_socios.data_table],
                            expand=True,
                            spacing=10,
                            padding=20,
                            auto_scroll=True
                        ),
                        ft.Row(
                            [btn_agregar] if btn_agregar else [],  # Utilizar la variable del botón aquí
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
            bgcolor="#0D1223",
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar al socio {socio['nombres']} {socio['apellidos']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda _: self.eliminar_y_cerrar_dialogo(socio['cedula']), style=ft.ButtonStyle(color="red"))
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def eliminar_y_cerrar_dialogo(self, cedula):
        self.eliminar_socio(cedula)
        self.cerrar_dialogo()

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
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def actualizar_socio(self, cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento):
        try:
            if not cedula or not apellidos or not nombres:
                raise ValueError("Los campos 'Cédula', 'Nombres' y 'Apellidos' son obligatorios.")
            self.socio_controlador.actualizar_socio(cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento)
            self.mostrar_snackbar("Socio actualizado correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def eliminar_socio(self, cedula):
        try:
            self.socio_controlador.eliminar_socio(cedula)
            self.mostrar_snackbar("Socio eliminado correctamente")
        except mysql.connector.errors.IntegrityError:
            self.mostrar_banner("No puedes eliminar este socio sin primero eliminar los vehículos asociados.")
        self.refrescar_datos()

    def mostrar_snackbar(self, mensaje):
        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor="#F4F9FA")
        self.page.snack_bar.open = True
        self.page.update()

    def mostrar_banner(self, mensaje):
        self.page.banner = ft.AlertDialog(
            content=ft.Text(mensaje, color=ft.colors.WHITE),
            bgcolor="#eb3936",  # Color rojo pastel
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
        self.socios_data = self.obtener_datos_socios()
        self.tabla_socios.actualizar_filas(self.socios_data)
        self.cerrar_bottomsheet()
        self.page.update()

    def exportar_pdf(self, e):
        pdf = PDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="Reporte de Socios", ln=True, align='C')
        
        pdf.ln(10)  # Espacio debajo del título
        
        # Data rows
        for socio in self.socios_data:
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt=f"Control: {socio['numero_control']}", ln=True)
            pdf.set_font("Arial", 'B', size=10)
            pdf.cell(0, 10, txt=f"Cédula: {socio['cedula']}", ln=True)
            pdf.cell(0, 10, txt=f"Nombres: {socio['nombres']}", ln=True)
            pdf.cell(0, 10, txt=f"Apellidos: {socio['apellidos']}", ln=True)
            pdf.cell(0, 10, txt=f"Dirección: {socio['direccion']}", ln=True)
            pdf.cell(0, 10, txt=f"Teléfono: {socio['numero_telefono']}", ln=True)
            pdf.cell(0, 10, txt=f"RIF: {socio['rif']}", ln=True)
            pdf.cell(0, 10, txt=f"Fecha Nacimiento: {socio['fecha_nacimiento']}", ln=True)
            
            pdf.ln(5)  # Espacio entre registros de socios
            pdf.ln(5)  # Espacio entre registros de socios
        
        pdf.output("reporte_socios.pdf")
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

class SociosTable:
    def __init__(self, socios_page, socios_data):
        self.socios_page = socios_page
        self.data_table = self.crear_tabla_socios(socios_data)

    def crear_tabla_socios(self, socios):
        return ft.DataTable(
            bgcolor="#40404040",
            border_radius=20,
            columns=[
                ft.DataColumn(ft.Text("Control", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Nombres", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Apellidos", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Cédula", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Teléfono", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Dirección", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("RIF", weight="w700", size=16, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Fecha Nac.", weight="w800", size=19, font_family="Arial Black italic")),
                ft.DataColumn(ft.Text("Acciones", weight="w800", size=19, font_family="Arial Black italic"))
            ],
            rows=self.crear_filas(socios),
        )

    def crear_filas(self, socios):
        rol = AuthControlador.obtener_rol()  # Obtener el rol del usuario autenticado

        def obtener_acciones(socio):
            acciones = []
            if rol in ["Admin", "Editor"]:
                acciones.append(ft.IconButton(ft.icons.EDIT, icon_color="#F4F9FA", on_click=lambda _, s=socio: self.socios_page.mostrar_bottomsheet_editar(s)))
            if rol == "Admin":
                acciones.append(ft.IconButton(ft.icons.DELETE_OUTLINE, icon_color="#eb3936", on_click=lambda _, s=socio: self.socios_page.confirmar_eliminar_socio(s)))
            return acciones

        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(socio['numero_control'])),
                    ft.DataCell(ft.Text(socio['nombres'])),
                    ft.DataCell(ft.Text(socio['apellidos'])),
                    ft.DataCell(ft.Text(socio['cedula'])),
                    ft.DataCell(ft.Text(socio['numero_telefono'])),
                    ft.DataCell(ft.Text(socio['direccion'])),
                    ft.DataCell(ft.Text(socio['rif'])),
                    ft.DataCell(ft.Text(socio['fecha_nacimiento'])),
                    ft.DataCell(
                        ft.Row(
                            obtener_acciones(socio)
                        )
                    )
                ],
            ) for socio in socios
        ]

    def actualizar_filas(self, socios):
        self.data_table.rows = self.crear_filas(socios)
        self.data_table.update()
#region botones navegacion
class Botones_nav:
    @staticmethod
    def crear_botones_navegacion(page):
        return ft.Row(
            [
                ft.TextButton("INICIO", scale=1.2,icon=ft.icons.HOME_OUTLINED,   on_click=lambda _: page.go("/menu"), ),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("SOCIOS", scale=1.2,icon=ft.icons.PEOPLE,style=ft.ButtonStyle(color="#F4F9FA"),  on_click=lambda _: page.go("/socios")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("VEHICULOS", scale=1.2,icon=ft.icons.LOCAL_TAXI_OUTLINED, on_click=lambda _: page.go("/vehiculos")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("AVANCES", scale=1.2,icon=ft.icons.WORK_OUTLINE, on_click=lambda _: page.go("/avances")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("SANCIONES", scale=1.2,icon=ft.icons.REPORT_OUTLINED, on_click=lambda _: page.go("/sanciones")),
                ft.VerticalDivider(width=2.5,),
                ft.TextButton("FINANZAS", scale=1.2,icon=ft.icons.PAYMENTS_OUTLINED, on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=40,),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )


#region validacion


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

    @staticmethod
    def validar_rif(rif):
        patron = r'^[VEJPG]\d{7,10}$'
        return re.match(patron, rif) is not None

class SociosForm:
    def __init__(self, socios_page, titulo, accion, socio=None):
        self.socios_page = socios_page
        self.accion = accion
        self.formulario = self.crear_formulario_socio(titulo, accion, socio)

    def crear_formulario_socio(self, titulo, accion, socio=None):
        control = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="Control", max_length=2, width=85, input_filter=ft.NumbersOnlyInputFilter(), value=socio['numero_control'] if socio else "")
        nombres = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Nombres", 
            max_length=30, 
            value=socio['nombres'] if socio else "",
            on_change=self.validar_texto
        )
        apellidos = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Apellidos", 
            max_length=30, 
            value=socio['apellidos'] if socio else "",
            on_change=self.validar_texto
        )
        cedula = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Cédula", 
            max_length=11, 
            width=180, 
            hint_text="V-/E-", 
            value=socio['cedula'] if socio else "",
            on_change=self.validar_cedula
        )
        telefono = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="Teléfono", max_length=15, width=175, prefix_text="+58 ", input_filter=ft.NumbersOnlyInputFilter(), hint_text="414 1234567", value=socio['numero_telefono'] if socio else "")
        direccion = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="Dirección", width=420, value=socio['direccion'] if socio else "", max_length=255, hint_text="municipio/urb/sector/calle/casa", multiline=True)
        rif = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="RIF", 
            width=180, 
            max_length=15, 
            value=socio['rif'] if socio else "",
            on_change=self.validar_rif
        )
        fecha_nacimiento = ft.TextField(
            border_radius=13, 
            border_color="#F4F9FA", 
            focused_border_color="#06F58E", 
            label="Fecha Nacimiento", 
            max_length=10, 
            width=140, 
            hint_text="AA/MM/DD", 
            value=socio['fecha_nacimiento'] if socio else "",
            on_change=self.validar_fecha_nacimiento
        )

        formulario = ft.Container(
            ft.Column([
                ft.Row([nombres, apellidos], spacing=10),
                ft.Row([control, cedula, fecha_nacimiento, telefono], spacing=10),
                ft.Row([direccion, rif], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", icon=ft.icons.CANCEL, style=ft.ButtonStyle(color="#eb3936"), on_click=lambda _: self.socios_page.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", icon=ft.icons.SAVE, style=ft.ButtonStyle(color="#06F58E"), on_click=lambda _: self.guardar_socio(
                            cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento
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
            e.control.error_text = "AA/MM/DD"
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

    def guardar_socio(self, cedula, nombres, apellidos, direccion, telefono, control, rif, fecha_nacimiento):
        fecha_str = fecha_nacimiento.value if isinstance(fecha_nacimiento.value, str) else fecha_nacimiento.value.strftime('%Y-%m-%d')
        if (Validacion.validar_fecha(fecha_str) and
            Validacion.validar_cedula(cedula.value) and
            Validacion.validar_texto(nombres.value) and
            Validacion.validar_texto(apellidos.value) and
            Validacion.validar_rif(rif.value)):
            # Si la fecha y la cédula son válidas, proceder con la acción
            self.accion(cedula.value, nombres.value, apellidos.value, direccion.value, telefono.value, control.value, rif.value, fecha_str)
        else:
            # Mostrar un banner de error si alguna validación falla
            if not Validacion.validar_fecha(fecha_str):
                self.socios_page.mostrar_banner("La fecha de nacimiento no es válida. Debe estar en el formato 'aaaa-mm-dd'.")
            if not Validacion.validar_cedula(cedula.value):
                self.socios_page.mostrar_banner("La cédula no es válida. Debe ser 'V-' o 'E-' seguido de 7 a 9 dígitos.")
            if not Validacion.validar_texto(nombres.value):
                self.socios_page.mostrar_banner("El nombre no es válido. Solo se permiten letras y espacios.")
            if not Validacion.validar_texto(apellidos.value):
                self.socios_page.mostrar_banner("El apellido no es válido. Solo se permiten letras y espacios.")
            if not Validacion.validar_rif(rif.value):
                self.socios_page.mostrar_banner("El RIF no es válido. Debe empezar por 'V', 'E', 'J', 'P', 'G' seguido de 7 a 10 dígitos.")
