# controller/avances_controlador.py

from model.avances_modelo import AvancesModelo

class AvancesControlador:
    def __init__(self):
        self.modelo = AvancesModelo()

    def obtener_todos_avances(self):
        return self.modelo.obtener_todos_avances()

    def insertar_avance(self, numero_control, nombre, apellido, cedula_avance, fecha_nacimiento, rif):
        self.modelo.insertar_avance(numero_control, nombre, apellido, cedula_avance, fecha_nacimiento, rif)

    def actualizar_avance(self, ID_avance, numero_control, nombre, apellido, cedula_avance, fecha_nacimiento, rif):
        self.modelo.actualizar_avance(ID_avance, numero_control, nombre, apellido, cedula_avance, fecha_nacimiento, rif)

    def eliminar_avance(self, ID_avance):
        self.modelo.eliminar_avance(ID_avance)
