import flet as ft

def main(page: ft.Page):
    page.title = "Ejemplo de FilledTonalButton"
    
    filled_tonal_button = ft.FilledTonalButton(
        content=ft.Text(
            "Go To Search",
            weight="w700",
        ),
        width=180,
        height=40,
        on_click=lambda _: page.go("/main")
    )
    
    # Agregar el botón a la página
    page.add(filled_tonal_button)

ft.app(target=main)



class SociosForm:
    def __init__(self, socios_page, titulo, accion, socio=None):
        self.socios_page = socios_page
        self.formulario = self.crear_formulario_socio(titulo, accion, socio)

    def validar_fecha(self, e):
        error_text = Validations.validar_fecha(e.control.value)
        e.control.error_text = error_text
        e.control.update()

    def validar_cedula(self, e):
        error_text = Validations.validar_cedula(e.control.value)
        e.control.error_text = error_text
        e.control.update()

    def validar_rif(self, e):
        error_text = Validations.validar_rif(e.control.value)
        e.control.error_text = error_text
        e.control.update()

    def validar_nombre_apellido(self, e):
        error_text = Validations.validar_nombre_apellido(e.control.value)
        e.control.error_text = error_text
        e.control.update()

    def validar_campos(self, campos):
        errores = []
        for campo, validador in campos.items():
            error = validador(campo.value)
            if error:
                campo.error_text = error
                campo.update()
                errores.append(error)
        return errores

    def crear_formulario_socio(self, titulo, accion, socio=None):
        control = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="Control", max_length=2, width=85, input_filter=ft.NumbersOnlyInputFilter(), value=socio['numero_control'] if socio else "")
        nombres = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="Nombres", max_length=30, input_filter=ft.TextOnlyInputFilter(), on_change=self.validar_nombre_apellido, value=socio['nombres'] if socio else "")
        apellidos = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="Apellidos", max_length=30, input_filter=ft.TextOnlyInputFilter(), on_change=self.validar_nombre_apellido, value=socio['apellidos'] if socio else "")
        cedula = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="Cédula", max_length=11, width=180, hint_text="V-/E-", on_change=self.validar_cedula, value=socio['cedula'] if socio else "")
        telefono = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="Teléfono", max_length=15, width=175, prefix_text="+58", input_filter=ft.NumbersOnlyInputFilter(), hint_text="414 1234567", value=socio['numero_telefono'] if socio else "")
        direccion = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="Dirección", width=420, value=socio['direccion'] if socio else "", max_length=255, hint_text="municipio/urb/sector/calle/casa", multiline=True)
        rif = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="RIF", width=180, max_length=15, on_change=self.validar_rif, value=socio['rif'] if socio else "")
        fecha_nacimiento = ft.TextField(border_radius=13, border_color="#F4F9FA", focused_border_color="#06F58E", label="Fecha Nacimiento", max_length=10, width=140, on_change=self.validar_fecha, hint_text="aaaa-mm-dd", value=socio['fecha_nacimiento'] if socio else "")

        def guardar():
            campos = {
                cedula: Validations.validar_cedula,
                nombres: Validations.validar_nombre_apellido,
                apellidos: Validations.validar_nombre_apellido,
                telefono: lambda x: None if x else "El teléfono no puede estar vacío",
                direccion: lambda x: None if x else "La dirección no puede estar vacía",
                rif: Validations.validar_rif,
                fecha_nacimiento: Validations.validar_fecha
            }
            errores = self.validar_campos(campos)
            if not errores:
                accion(cedula.value, nombres.value, apellidos.value, direccion.value, telefono.value, control.value, rif.value, fecha_nacimiento.value)

        formulario = ft.Container(
            ft.Column([
                ft.Row([nombres, apellidos], spacing=10),
                ft.Row([control, cedula, fecha_nacimiento, telefono], spacing=10),
                ft.Row([direccion, rif], spacing=10),
                ft.Row(
                    [
                        ft.TextButton("Cancelar", icon=ft.icons.CANCEL, style=ft.ButtonStyle(color="#eb3936"), on_click=lambda _: self.socios_page.cerrar_bottomsheet()),
                        ft.TextButton("Guardar", icon=ft.icons.SAVE, style=ft.ButtonStyle(color="#06F58E"), on_click=lambda _: guardar())
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ]),
            padding=20,
            border_radius=15,
        )

        return formulario