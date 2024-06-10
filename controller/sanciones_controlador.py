# controladores/sancion_controlador.py

from model.modelo_sancion import ModeloSancion

class SancionControlador:
    def __init__(self):
        self.modelo_sancion = ModeloSancion()

    def obtener_todas_sanciones(self):
        return self.modelo_sancion.obtener_todas_sanciones()

    def insertar_sancion(self, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido):
        self.modelo_sancion.insertar_sancion(cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido)

    def actualizar_sancion(self, ID_sancion, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido):
        self.modelo_sancion.actualizar_sancion(ID_sancion, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido)

    def eliminar_sancion(self, ID_sancion):
        self.modelo_sancion.eliminar_sancion(ID_sancion)
