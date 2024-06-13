# controladores/socio_controlador.py

from model.modelo_socio import ModeloSocio

#region SocioControlador Class

#controla las operaciones relacionadas con los socios
class SocioControlador:
    def __init__(self):
        # Inicializa la instancia del modelo de socio
        self.modelo_socio = ModeloSocio()

    # Método para obtener todos los socios
    def obtener_todos_socios(self):
        return self.modelo_socio.obtener_todos_socios()

    # Método para insertar un nuevo socio
    def insertar_socio(self, cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento):
        self.modelo_socio.insertar_socio(cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento)

    # Método para actualizar un socio existente
    def actualizar_socio(self, cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento):
        self.modelo_socio.actualizar_socio(cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento)

    # Método para eliminar un socio
    def eliminar_socio(self, cedula):
        self.modelo_socio.eliminar_socio(cedula)
# endregion
