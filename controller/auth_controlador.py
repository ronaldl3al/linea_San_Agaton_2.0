# controladores/auth_controlador.py

from model.usuario_modelo import UsuarioModelo

class AuthControlador:
    def __init__(self):
        self.usuario_modelo = UsuarioModelo()

    def autenticar(self, nombre_usuario, contrasena):
        usuario = self.usuario_modelo.obtener_usuario(nombre_usuario, contrasena)
        if usuario:
            return usuario['rol']
        return None
