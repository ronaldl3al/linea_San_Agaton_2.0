# modelos/usuario_modelo.py

from utils.db_config import ConfiguracionBaseDeDatos

class UsuarioModelo:
    def __init__(self):
        self.db_config = ConfiguracionBaseDeDatos()

    def obtener_usuario(self, nombre_usuario, contrasena):
        conexion = self.db_config.conectar()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
        cursor.execute(query, (nombre_usuario, contrasena))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario
