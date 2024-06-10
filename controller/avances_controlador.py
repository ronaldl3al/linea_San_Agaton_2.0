# controladores/avances_controlador.py

from model.modelo_avance import ModeloAvance

class AvanceControlador:
    def __init__(self):
        self.modelo_avance = ModeloAvance()

    def obtener_todos_avances(self):
        return self.modelo_avance.obtener_todos_avances()

    def insertar_avance(self, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf):
        self.modelo_avance.insertar_avance(numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf)

    def actualizar_avance(self, ID_avance, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf):
        self.modelo_avance.actualizar_avance(ID_avance, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf)

    def eliminar_avance(self, ID_avance):
        self.modelo_avance.eliminar_avance(ID_avance)
