# controladores/socio_controlador.py

from model.modelo_socio import ModeloSocio

class SocioControlador:
    def __init__(self):
        self.modelo_socio = ModeloSocio()

    def obtener_todos_socios(self):
        return self.modelo_socio.obtener_todos_socios()

    def insertar_socio(self, cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento):
        self.modelo_socio.insertar_socio(cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento)

    def actualizar_socio(self, cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento):
        self.modelo_socio.actualizar_socio(cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento)

    def eliminar_socio(self, cedula):
        self.modelo_socio.eliminar_socio(cedula)
