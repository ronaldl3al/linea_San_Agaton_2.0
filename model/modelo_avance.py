# modelos/modelo_avance.py

from utils.db_config import ConfiguracionBaseDeDatos

class ModeloAvance:
    def __init__(self):
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    def obtener_todos_avances(self):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM avances ORDER BY ID_avance ASC"
        cursor.execute(query)
        avances = cursor.fetchall()
        cursor.close()
        conexion.close()
        return avances

    def insertar_avance(self, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        INSERT INTO avances (numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf))
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar_avance(self, ID_avance, numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        UPDATE avances 
        SET numero_control = %s, nombre = %s, apellido = %s, fecha_nacimiento = %s, rif = %s, cedula_avance = %s, numero_telf = %s
        WHERE ID_avance = %s
        """
        cursor.execute(query, (numero_control, nombre, apellido, fecha_nacimiento, rif, cedula_avance, numero_telf, ID_avance))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar_avance(self, ID_avance):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = "DELETE FROM avances WHERE ID_avance = %s"
        cursor.execute(query, (ID_avance,))
        conexion.commit()
        cursor.close()
        conexion.close()
