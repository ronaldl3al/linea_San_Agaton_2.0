# modelos/modelo_socio.py

from utils.db_config import ConfiguracionBaseDeDatos

#region ModeloSocio Class
# Modelo de datos para los socios
class ModeloSocio:
    def __init__(self):
        # Inicializa la configuración de la base de datos
        self.configuracion_bd = ConfiguracionBaseDeDatos()
    
    # Metodo para obtener todos los socios
    def obtener_todos_socios(self):
        conexion = self.configuracion_bd.conectar()  # Conectar a la base de datos
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM socio ORDER BY numero_control ASC"
        cursor.execute(query)
        socios = cursor.fetchall()  # Obtener todos los registros
        cursor.close()
        conexion.close()
        return socios

    # Metodo para insertar un nuevo socio
    def insertar_socio(self, cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento):
        conexion = self.configuracion_bd.conectar()  # Conectar a la base de datos
        cursor = conexion.cursor()
        query = """
        INSERT INTO socio (cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento))
        conexion.commit()  # Confirmar la transacción
        cursor.close()
        conexion.close()

    # Metodo para actualizar un socio existente
    def actualizar_socio(self, cedula, nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento):
        conexion = self.configuracion_bd.conectar()  # Conectar a la base de datos
        cursor = conexion.cursor()
        query = """
        UPDATE socio 
        SET nombres = %s, apellidos = %s, direccion = %s, 
            numero_telefono = %s, numero_control = %s, rif = %s, fecha_nacimiento = %s
        WHERE cedula = %s
        """
        cursor.execute(query, (nombres, apellidos, direccion, numero_telefono, numero_control, rif, fecha_nacimiento, cedula))
        conexion.commit()  # Confirmar la transacción
        cursor.close()
        conexion.close()

    # Metodo para eliminar un socio
    def eliminar_socio(self, cedula):
        conexion = self.configuracion_bd.conectar()  # Conectar a la base de datos
        cursor = conexion.cursor()
        query = "DELETE FROM socio WHERE cedula = %s"
        cursor.execute(query, (cedula,))
        conexion.commit()  # Confirmar la transacción
        cursor.close()
        conexion.close()
# endregion
