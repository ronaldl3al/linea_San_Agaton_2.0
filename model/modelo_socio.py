# modelos/modelo_socio.py

from utils.db_config import ConfiguracionBaseDeDatos

class ModeloSocio:
    def __init__(self):
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    def obtener_todos_socios(self):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM socio  ORDER BY numero_control ASC "
        cursor.execute(query)
        socios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return socios

    def insertar_socio(self, cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        INSERT INTO socio (cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento))
        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar_socio(self, cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = """
        UPDATE socio 
        SET nombres = %s, apellidos = %s, direccion = %s, 
            numero_telefono = %s, numero_control = %s, rif = %s, fecha_nacimiento = %s
        WHERE cedula = %s
        """
        cursor.execute(query, (nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento, cedula))
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar_socio(self, cedula):
        conexion = self.configuracion_bd.conectar()
        cursor = conexion.cursor()
        query = "DELETE FROM socio WHERE cedula = %s"
        cursor.execute(query, (cedula,))
        conexion.commit()
        cursor.close()
        conexion.close()
