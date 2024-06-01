# modelos/modelo_vehiculo.py

from utils.db_config import ConfiguracionBaseDeDatos

class ModeloVehiculo:
    def __init__(self):
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    def obtener_todos_vehiculos(self):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM vehiculos"
        cursor.execute(query)
        vehiculos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return vehiculos

    def insertar_vehiculo(self, cedula, numero_control, marca, modelo, ano, placa):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        INSERT INTO vehiculos (cedula, numero_control, marca, modelo, ano, placa)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (cedula, numero_control, marca, modelo, ano, placa))
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar_vehiculo(self, id_vehiculo, cedula, numero_control, marca, modelo, ano, placa):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        UPDATE vehiculos 
        SET cedula = %s, numero_control = %s, marca = %s, modelo = %s, ano = %s, placa = %s
        WHERE id_vehiculo = %s
        """
        cursor.execute(query, (cedula, numero_control, marca, modelo, ano, placa, id_vehiculo))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar_vehiculo(self, id_vehiculo):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = "DELETE FROM vehiculos WHERE id_vehiculo = %s"
        cursor.execute(query, (id_vehiculo,))
        conexion.commit()
        cursor.close()
        conexion.close()
