import flet as ft
from controller.sanciones_controlador import SancionControlador
from controller.auth_controlador import AuthControlador
import mysql.connector.errors
from fpdf import FPDF

class SancionesPage(ft.View):
    def __init__(self, page):
        super().__init__(route="/sanciones")
        self.page = page
        self.sancion_controlador = SancionControlador()
        self.sanciones_data = self.obtener_datos_sanciones()
        self.tabla_sanciones = SancionesTable(self, self.sanciones_data)
        
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
                title=ft.Text("Sanciones"),
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
                            controls=[self.tabla_sanciones.data_table],
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
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar la sanción con ID {sancion['ID_sancion']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda _: self.eliminar_sancion(sancion['ID_sancion']))
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

    def guardar_sancion(self, cedula, motivo_sancion, inicio_sancion, final_sancion, monto):
        try:
            if not cedula or not motivo_sancion or not inicio_sancion or not final_sancion or not monto:
                raise ValueError("Todos los campos son obligatorios.")
            self.sancion_controlador.insertar_sancion(cedula, motivo_sancion, inicio_sancion, final_sancion, monto)
            self.mostrar_snackbar("Sanción agregada correctamente")
            self.refrescar_datos()
        except ValueError as ve:
            self.mostrar_banner(f"Error de validación: {ve}")
        except mysql.connector.Error as err:
            self.mostrar_banner(f"Error de base de datos: {err}")

    def actualizar_sancion(self, ID_sancion, cedula, motivo_sancion, inicio_sancion, final_sancion, monto):
        try:
            if not ID_sancion or not cedula or not motivo_sancion or not inicio_sancion or not final_sancion or not monto:
                raise ValueError("Todos los campos son obligatorios.")
            self.sancion_controlador.actualizar_sancion(ID_sancion, cedula, motivo_sancion, inicio_sancion, final_sancion, monto)
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
        self.sanciones_data = self.obtener_datos_sanciones()
        self.tabla_sanciones.actualizar_filas(self.sanciones_data)
        self.cerrar_bottomsheet()
        self.page.update()

    def exportar_pdf(self, e):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="Reporte de Sanciones", ln=True, align='C')
        
        pdf.ln(10)  # Espacio debajo del título
        
        # Data rows
        for sancion in self.sanciones_data:
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt=f"ID Sanción: {sancion['ID_sancion']}", ln=True)
            pdf.set_font("Arial", 'B', size=10)
            pdf.cell(0, 10, txt=f"Cédula: {sancion['cedula']}", ln=True)
            pdf.cell(0, 10, txt=f"Motivo: {sancion['motivo_sancion']}", ln=True)
            pdf.cell(0, 10, txt=f"Fecha de Inicio: {sancion['inicio_sancion']}", ln=True)
            pdf.cell(0, 10, txt=f"Fecha de Final: {sancion['final_sancion']}", ln=True)
            pdf.cell(0, 10, txt=f"Monto: {sancion['monto']}", ln=True)
            
            pdf.ln(5)  # Espacio entre registros de sanciones
        
        pdf.output("reporte_sanciones.pdf")
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

class SancionesTable:
    def __init__(self, sanciones_page, sanciones_data):
        self.sanciones_page = sanciones_page
        self.data_table = self.crear_tabla_sanciones(sanciones_data)

    def crear_tabla_sanciones(self, sanciones):
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Cédula")),
                ft.DataColumn(ft.Text("Motivo")),
                ft.DataColumn(ft.Text("Fecha de Inicio")),
                ft.DataColumn(ft.Text("Fecha de Final")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=self.crear_filas(sanciones),
        )

    def crear_filas(self, sanciones):
        rol = AuthControlador.obtener_rol()  # Obtener el rol del usuario autenticado

        def obtener_acciones(sancion):
            acciones = []
            if rol in ["Admin", "Editor"]:
                acciones.append(ft.IconButton(ft.icons.EDIT, on_click=lambda _, s=sancion: self.sanciones_page.mostrar_bottomsheet_editar(s)))
            if rol == "Admin":
                acciones.append(ft.IconButton(ft.icons.DELETE, on_click=lambda _, s=sancion: self.sanciones_page.confirmar_eliminar_sancion(s)))
            return acciones

        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(sancion['ID_sancion']))),
                    ft.DataCell(ft.Text(sancion['cedula'])),
                    ft.DataCell(ft.Text(sancion['motivo_sancion'])),
                    ft.DataCell(ft.Text(str(sancion['inicio_sancion']))),
                    ft.DataCell(ft.Text(str(sancion['final_sancion']))),
                    ft.DataCell(ft.Text(str(sancion['monto']))),
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
        self.formulario = self.crear_formulario_sancion(titulo, accion, sancion)

    def crear_formulario_sancion(self, titulo, accion, sancion=None):
        cedula = ft.TextField(label="Cédula", value=sancion['cedula'] if sancion else "")
        motivo_sancion = ft.TextField(label="Motivo de Sanción", value=sancion['motivo_sancion'] if sancion else "")
        inicio_sancion = ft.TextField(label="Fecha de Inicio", value=sancion['inicio_sancion'] if sancion else "")
        final_sancion = ft.TextField(label="Fecha de Final", value=sancion['final_sancion'] if sancion else "")
        monto = ft.TextField(label="Monto", value=sancion['monto'] if sancion else "")

        formulario = ft.Container(
            ft.Column([
                ft.Row([cedula, motivo_sancion], spacing=10),
                ft.Row([inicio_sancion, final_sancion, monto], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", on_click=lambda _: self.sanciones_page.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", on_click=lambda _: accion(
                            sancion['ID_sancion'] if sancion else None,
                            cedula.value, motivo_sancion.value, inicio_sancion.value, final_sancion.value, monto.value
                        ) if sancion else self.sanciones_page.guardar_sancion(
                            cedula.value, motivo_sancion.value, inicio_sancion.value, final_sancion.value, monto.value
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
                ft.TextButton("SANCIONES", icon=ft.icons.REPORT, on_click=lambda _: page.go("/sanciones")),
                ft.TextButton("FINANZAS", icon=ft.icons.PAYMENTS_OUTLINED, on_click=lambda _: page.go("/finanzas")),
                ft.VerticalDivider(width=100),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

