# controladores/auth_controlador.py

from model.usuario_modelo import UsuarioModelo

class AuthControlador:
    # Variable de clase para almacenar la información del usuario autenticado
    user_info = {}

    def __init__(self):
        self.usuario_modelo = UsuarioModelo()

    def autenticar(self, nombre_usuario, contrasena):
        usuario = self.usuario_modelo.obtener_usuario(nombre_usuario, contrasena)
        if usuario:
            AuthControlador.user_info = {"nombre_usuario": nombre_usuario, "rol": usuario['rol']}
            return usuario['rol']
        return None

    @staticmethod
    def obtener_rol():
        return AuthControlador.user_info.get("rol", None)