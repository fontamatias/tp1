from modelo.usuario import UsuarioModel
from modelo.moto import MotoModel
from vista.login_view import LoginView
from vista.sistema_view import SistemaView

class Controlador:

    def __init__(self):
        self.usuario_model = UsuarioModel()
        self.moto_model = MotoModel()
        LoginView(self)

    def login(self, usuario, password, ventana):
        error = self.usuario_model.login(usuario, password)
        if error:
            return error

        ventana.destroy()
        SistemaView(self, usuario)
        return None

    def alta(self, moto, motor):
        return self.moto_model.alta(moto, motor)

    def baja(self, moto, motor, defecto):
        return self.moto_model.baja(moto, motor, defecto)

    def mover_a_ok(self, moto):
        return self.moto_model.mover_a_ok(moto)

    def buscar(self, moto):
        return self.moto_model.buscar(moto)

    def listar_ok(self):
        return self.moto_model.listar_ok()

    def listar_no_ok(self):
        return self.moto_model.listar_no_ok()
