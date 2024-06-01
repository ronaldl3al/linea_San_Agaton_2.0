# controladores/vehiculo_controlador.py

from model.modelo_vehiculo import ModeloVehiculo

class VehiculoControlador:
    def __init__(self):
        self.modelo_vehiculo = ModeloVehiculo()

    def obtener_todos_vehiculos(self):
        return self.modelo_vehiculo.obtener_todos_vehiculos()

    def insertar_vehiculo(self, cedula, numero_control, marca, modelo, ano, placa):
        self.modelo_vehiculo.insertar_vehiculo(cedula, numero_control, marca, modelo, ano, placa)

    def actualizar_vehiculo(self, id_vehiculo, cedula, numero_control, marca, modelo, ano, placa):
        self.modelo_vehiculo.actualizar_vehiculo(id_vehiculo, cedula, numero_control, marca, modelo, ano, placa)

    def eliminar_vehiculo(self, id_vehiculo):
        self.modelo_vehiculo.eliminar_vehiculo(id_vehiculo)
