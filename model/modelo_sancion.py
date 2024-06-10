# modelos/modelo_sancion.py

from utils.db_config import ConfiguracionBaseDeDatos

class ModeloSancion:
    def __init__(self):
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    def obtener_todas_sanciones(self):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM sanciones ORDER BY ID_sancion ASC"
        cursor.execute(query)
        sanciones = cursor.fetchall()
        cursor.close()
        conexion.close()
        return sanciones

    def insertar_sancion(self, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        INSERT INTO sanciones (cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido))
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar_sancion(self, ID_sancion, cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        UPDATE sanciones 
        SET cedula = %s, motivo_sancion = %s, monto = %s, inicio_sancion = %s, final_sancion = %s, nombre = %s, apellido = %s
        WHERE ID_sancion = %s
        """
        cursor.execute(query, (cedula, motivo_sancion, monto, inicio_sancion, final_sancion, nombre, apellido, ID_sancion))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar_sancion(self, ID_sancion):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = "DELETE FROM sanciones WHERE ID_sancion = %s"
        cursor.execute(query, (ID_sancion,))
        conexion.commit()
        cursor.close()
        conexion.close()
