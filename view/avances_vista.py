import flet as ft
from controller.avances_controlador import AvancesControlador
import mysql.connector.errors
from fpdf import FPDF
from controller.auth_controlador import AuthControlador

class AvancesPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/avances")
        self.page = page
        self.avances_controlador = AvancesControlador()
        self.avances_data = self.obtener_datos_avances()
        self.tabla_avances = AvancesTable(self, self.avances_data)
        
        # Obtener el rol del usuario autenticado
        self.rol = AuthControlador.obtener_rol()

        # Definir el botón de agregar en una variable dependiendo del rol
        btn_agregar = None
        if self.rol in ["Admin", "Editor"]:  # Asumiendo roles en mayúsculas como en la base de datos
            btn_agregar = ft.IconButton(icon=ft.icons.ADD, on_click=self.mostrar_bottomsheet_agregar, icon_size=40)
        elif self.rol == "Viewer":
            btn_agregar = ft.IconButton(icon=ft.icons.ADD, on_click=None, icon_size=40)  # Deshabilitar botón

        # Añadir controles
        self.controls = [
            ft.AppBar(
                title=ft.Text("Avances"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                    Botones_nav.crear_botones_navegacion(self.page),
                    ft.PopupMenuButton(
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
                ]
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
                            [btn_agregar] if btn_agregar else [],  # Utilizar la variable del botón aquí
                            alignment=ft.MainAxisAlignment.END,
                            spacing=10,
                        ),
                    ],
                    expand=True,
                    spacing=10
                ),
                expand=True,
                bgcolor="#333333",
                border_radius=20,
            ),
        ]

        self.bottom_sheet = ft.BottomSheet(
            ft.Container(),
            open=False,
            on_dismiss=self.cerrar_bottomsheet
        )
        self.page.overlay.append(self.bottom_sheet)

    def obtener_datos_avances(self):
        return self.avances_controlador.obtener_todos_avances()

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
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar el avance de {avance['nombre']} {avance['apellido']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda _: self.eliminar_avance(avance['ID_avance']))
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

    def guardar_avance(self, numero_control, nombre, apellido, cedula_avance, fecha_nacimiento, rif):
        try:
            if not numero_control or not nombre or not apellido:
                raise ValueError("Los campos 'Número de Control', 'Nombre' y 'Apellido' son obligatorios.")
            self.avances_controlador.insertar_avance(numero_control, nombre, apellido, cedula_avance, fecha_nacimiento, rif)
            self.mostrar_snackbar("Avance agregado correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def actualizar_avance(self, ID_avance, numero_control, nombre, apellido, cedula_avance, fecha_nacimiento, rif):
        try:
            if not numero_control or not nombre or not apellido:
                raise ValueError("Los campos 'Número de Control', 'Nombre' y 'Apellido' son obligatorios.")
            self.avances_controlador.actualizar_avance(ID_avance, numero_control, nombre, apellido, cedula_avance, fecha_nacimiento, rif)
            self.mostrar_snackbar("Avance actualizado correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def eliminar_avance(self, ID_avance):
        try:
            self.avances_controlador.eliminar_avance(ID_avance)
            self.mostrar_snackbar("Avance eliminado correctamente")
        except mysql.connector.errors.IntegrityError:
            self.mostrar_banner("No puedes eliminar este avance.")
        self.refrescar_datos()

    def mostrar_snackbar(self, mensaje):
        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje))
        self.page.snack_bar.open = True
        self.page.update()

    def mostrar_banner(self, mensaje):
        self.page.banner = ft.Banner(
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
        self.avances_data = self.obtener_datos_avances()
        self.tabla_avances.actualizar_filas(self.avances_data)
        self.cerrar_bottomsheet()
        self.page.update()

    def exportar_pdf(self, e):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="Reporte de Avances", ln=True, align='C')
        
        pdf.ln(10)  # Espacio debajo del título
        
        # Data rows
        for avance in self.avances_data:
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt=f"ID Avance: {avance['ID_avance']}", ln=True)
            pdf.set_font("Arial", 'B', size=10)
            pdf.cell(0, 10, txt=f"Nombre: {avance['nombre']}", ln=True)
            pdf.cell(0, 10, txt=f"Apellido: {avance['apellido']}", ln=True)
            pdf.cell(0, 10, txt=f"Cédula: {avance['cedula_avance']}", ln=True)
            pdf.cell(0, 10, txt=f"Fecha de Nacimiento: {avance['fecha_nacimiento']}", ln=True)
            pdf.cell(0, 10, txt=f"RIF: {avance['rif']}", ln=True)
            
            pdf.ln(5)  # Espacio entre registros de avances
        
        pdf.output("reporte_avances.pdf")
        self.mostrar_snackbar("PDF generado correctamente")

    def show_logout_popup(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Cierre de Sesión"),
            content=ft.Text("¿Está seguro de que desea cerrar sesión?"),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog, style=ft.ButtonStyle(color="red")),
                ft.TextButton("Cerrar Sesión", on_click=self.logout),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
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
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Número de Control")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Cédula")),
                ft.DataColumn(ft.Text("Fecha Nacimiento")),
                ft.DataColumn(ft.Text("RIF")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=self.crear_filas(avances),
        )

    def crear_filas(self, avances):
        rol = AuthControlador.obtener_rol()  # Obtener el rol del usuario autenticado

        def obtener_acciones(avance):
            acciones = []
            if rol in ["Admin", "Editor"]:
                acciones.append(ft.IconButton(ft.icons.EDIT, on_click=lambda _, a=avance: self.avances_page.mostrar_bottomsheet_editar(a)))
            if rol == "Admin":
                acciones.append(ft.IconButton(ft.icons.DELETE, on_click=lambda _, a=avance: self.avances_page.confirmar_eliminar_avance(a)))
            return acciones

        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(avance['ID_avance']))),
                    ft.DataCell(ft.Text(avance['numero_control'])),
                    ft.DataCell(ft.Text(avance['nombre'])),
                    ft.DataCell(ft.Text(avance['apellido'])),
                    ft.DataCell(ft.Text(avance['cedula_avance'])),
                    ft.DataCell(ft.Text(avance['fecha_nacimiento'])),
                    ft.DataCell(ft.Text(avance['rif'])),
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
        self.formulario = self.crear_formulario_avance(titulo, accion, avance)

    def crear_formulario_avance(self, titulo, accion, avance=None):
        numero_control = ft.TextField(label="Número de Control", value=avance['numero_control'] if avance else "")
        nombre = ft.TextField(label="Nombre", value=avance['nombre'] if avance else "")
        apellido = ft.TextField(label="Apellido", value=avance['apellido'] if avance else "")
        cedula_avance = ft.TextField(label="Cédula", value=avance['cedula_avance'] if avance else "")
        fecha_nacimiento = ft.TextField(label="Fecha de Nacimiento", value=avance['fecha_nacimiento'] if avance else "", hint_text="aaaa/dd/mm")
        rif = ft.TextField(label="RIF", value=avance['rif'] if avance else "")

        formulario = ft.Container(
            ft.Column([
                ft.Row([numero_control, nombre], spacing=10),
                ft.Row([apellido, cedula_avance], spacing=10),
                ft.Row([fecha_nacimiento, rif], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", on_click=lambda _: self.avances_page.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", on_click=lambda _: accion(
                            numero_control.value, nombre.value, apellido.value, cedula_avance.value, fecha_nacimiento.value, rif.value
                        ))
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ]),
            padding=20,
            border_radius=15,
        )

        return formulario

class Botones_nav:
    def crear_botones_navegacion(page):
        return ft.Row(
            [
                ft.TextButton("INICIO", icon=ft.icons.HOME_OUTLINED, on_click=lambda _: page.go("/menu")),
                ft.TextButton("SOCIOS", icon=ft.icons.PEOPLE_OUTLINE, on_click=lambda _: page.go("/socios")),
                ft.TextButton("VEHICULOS", icon=ft.icons.LOCAL_TAXI_OUTLINED, on_click=lambda _: page.go("/vehiculos")),
                ft.TextButton("AVANCES", icon=ft.icons.WORK, on_click=lambda _: page.go("/avances")),
                ft.TextButton("SANCIONES", icon=ft.icons.REPORT_OUTLINED, on_click=lambda _: page.go("/sanciones")),
                ft.TextButton("FINANZAS", icon=ft.icons.PAYMENTS_OUTLINED, on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=100),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
