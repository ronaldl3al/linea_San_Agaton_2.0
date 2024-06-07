import flet as ft
from controller.finanza_controlador import FinanzaControlador
from controller.auth_controlador import AuthControlador
import mysql.connector.errors
from fpdf import FPDF

class FinanzasPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/finanzas")
        self.page = page
        self.finanza_controlador = FinanzaControlador()
        self.finanzas_data = self.obtener_datos_finanzas()
        self.tabla_finanzas = FinanzasTable(self, self.finanzas_data)
        
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
                title=ft.Text("Finanzas"),
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
                            controls=[self.tabla_finanzas.data_table],
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
                bgcolor="#111111",
                border_radius=20,
                image_src="image\LOGO_SAN_AGATON_REMASTER1.png",
            ),
        ]

        self.bottom_sheet = ft.BottomSheet(
            ft.Container(),
            open=False,
            on_dismiss=self.cerrar_bottomsheet
        )
        self.page.overlay.append(self.bottom_sheet)

    def obtener_datos_finanzas(self):
        return self.finanza_controlador.obtener_todas_finanzas()

    def mostrar_bottomsheet_agregar(self, e):
        self.bottom_sheet.content = FinanzasForm(self, "Agregar Finanzas", self.guardar_finanza).formulario
        self.bottom_sheet.open = True
        self.page.update()

    def mostrar_bottomsheet_editar(self, finanza):
        self.bottom_sheet.content = FinanzasForm(self, "Editar Finanzas", self.actualizar_finanza, finanza).formulario
        self.bottom_sheet.open = True
        self.page.update()

    def confirmar_eliminar_finanza(self, finanza):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar las finanzas con ID {finanza['ID_finanzas']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda _: self.eliminar_finanza(finanza['ID_finanzas']))
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

    def guardar_finanza(self, cedula, pagos_mensuales, impuestos_anuales, fecha_pago):
        try:
            if not cedula or not pagos_mensuales or not impuestos_anuales or not fecha_pago:
                raise ValueError("Todos los campos son obligatorios.")
            self.finanza_controlador.insertar_finanza(cedula, pagos_mensuales, impuestos_anuales, fecha_pago)
            self.mostrar_snackbar("Finanzas agregadas correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def actualizar_finanza(self, ID_finanza, cedula, pagos_mensuales, impuestos_anuales, fecha_pago):
        try:
            if not ID_finanza or not cedula or not pagos_mensuales or not impuestos_anuales or not fecha_pago:
                raise ValueError("Todos los campos son obligatorios.")
            self.finanza_controlador.actualizar_finanza(ID_finanza, cedula, pagos_mensuales, impuestos_anuales, fecha_pago)
            self.mostrar_snackbar("Finanzas actualizadas correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def eliminar_finanza(self, ID_finanza):
        try:
            self.finanza_controlador.eliminar_finanza(ID_finanza)
            self.mostrar_snackbar("Finanza eliminada correctamente")
        except mysql.connector.errors.IntegrityError:
            self.mostrar_banner("No puedes eliminar esta finanza.")
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
        self.finanzas_data = self.obtener_datos_finanzas()
        self.tabla_finanzas.actualizar_filas(self.finanzas_data)
        self.cerrar_bottomsheet()
        self.page.update()

    def exportar_pdf(self, e):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="Reporte de Finanzas", ln=True, align='C')
        
        pdf.ln(10)  # Espacio debajo del título
        
        # Data rows
        for finanza in self.finanzas_data:
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt=f"ID Finanzas: {finanza['ID_finanzas']}", ln=True)
            pdf.set_font("Arial", 'B', size=10)
            pdf.cell(0, 10, txt=f"Cédula: {finanza['cedula']}", ln=True)
            pdf.cell(0, 10, txt=f"Pagos Mensuales: {finanza['pagos_mensuales']}", ln=True)
            pdf.cell(0, 10, txt=f"Impuestos Anuales: {finanza['impuestos_anuales']}", ln=True)
            pdf.cell(0, 10, txt=f"Fecha de Pago: {finanza['fecha_pago']}", ln=True)
            
            pdf.ln(5)  # Espacio entre registros de finanzas
        
        pdf.output("reporte_finanzas.pdf")
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

class FinanzasTable:
    def __init__(self, finanzas_page, finanzas_data):
        self.finanzas_page = finanzas_page
        self.data_table = self.crear_tabla_finanzas(finanzas_data)

    def crear_tabla_finanzas(self, finanzas):
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Cédula")),
                ft.DataColumn(ft.Text("Pagos Mensuales")),
                ft.DataColumn(ft.Text("Impuestos Anuales")),
                ft.DataColumn(ft.Text("Fecha de Pago")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=self.crear_filas(finanzas),
        )

    def crear_filas(self, finanzas):
        rol = AuthControlador.obtener_rol()  # Obtener el rol del usuario autenticado

        def obtener_acciones(finanza):
            acciones = []
            if rol in ["Admin", "Editor"]:
                acciones.append(ft.IconButton(ft.icons.EDIT, on_click=lambda _, f=finanza: self.finanzas_page.mostrar_bottomsheet_editar(f)))
            if rol == "Admin":
                acciones.append(ft.IconButton(ft.icons.DELETE, on_click=lambda _, f=finanza: self.finanzas_page.confirmar_eliminar_finanza(f)))
            return acciones

        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(finanza['ID_finanzas']))),
                    ft.DataCell(ft.Text(finanza['cedula'])),
                    ft.DataCell(ft.Text(str(finanza['pagos_mensuales']))),
                    ft.DataCell(ft.Text(str(finanza['impuestos_anuales']))),
                    ft.DataCell(ft.Text(str(finanza['fecha_pago']))),
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
        self.formulario = self.crear_formulario_finanza(titulo, accion, finanza)

    def crear_formulario_finanza(self, titulo, accion, finanza=None):
        cedula = ft.TextField(label="Cédula", value=finanza['cedula'] if finanza else "")
        pagos_mensuales = ft.TextField(label="Pagos Mensuales", value=finanza['pagos_mensuales'] if finanza else "")
        impuestos_anuales = ft.TextField(label="Impuestos Anuales", value=finanza['impuestos_anuales'] if finanza else "")
        fecha_pago = ft.TextField(label="Fecha de Pago", value=finanza['fecha_pago'] if finanza else "", hint_text="aaaa/mm/dd")

        formulario = ft.Container(
            ft.Column([
                ft.Row([cedula, pagos_mensuales], spacing=10),
                ft.Row([impuestos_anuales, fecha_pago], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", on_click=lambda _: self.finanzas_page.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", on_click=lambda _: accion(
                            finanza['ID_finanzas'] if finanza else None,
                            cedula.value, pagos_mensuales.value, impuestos_anuales.value, fecha_pago.value
                        ) if finanza else self.finanzas_page.guardar_finanza(
                            cedula.value, pagos_mensuales.value, impuestos_anuales.value, fecha_pago.value
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
                ft.TextButton("AVANCES", icon=ft.icons.WORK_OUTLINE, on_click=lambda _: page.go("/avances")),
                ft.TextButton("SANCIONES", icon=ft.icons.REPORT_OUTLINED, on_click=lambda _: page.go("/sanciones")),
                ft.TextButton("FINANZAS", icon=ft.icons.PAYMENTS, on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=100),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
