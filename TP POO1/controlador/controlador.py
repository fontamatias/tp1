from modelo.usuario import Usuario
from modelo.moto import Moto
from vista.sistemavista import Sistema

class Controlador:

    def __init__(self):
        self.usuario_model = Usuario()
        self.moto_model = Moto()

    def login(self, usuario, password, ventana):
        error = self.usuario_model.login(usuario, password)
        if error:
            return error

        ventana.destroy()
        Sistema(self, usuario)
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
    
    def resumen(self):
        return self.moto_model.final_dia()
