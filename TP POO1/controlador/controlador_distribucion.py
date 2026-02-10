from modelo.usuario_distribucion import UsuarioDistribucion
from modelo.venta import Venta

class ControladorDistribucion:

    def __init__(self):
        self.usuario_model = UsuarioDistribucion()
        self.venta_model = Venta()

    def login(self, usuario, password, ventana):
        error = self.usuario_model.login(usuario, password)
        if error:
            return error

        ventana.destroy()
        # la vista de distribución será la que muestre el stock y permita vender
        from vista.distribucionvista import DistribucionVista
        DistribucionVista(self, usuario)
        return None

    def listar_stock(self):
        return self.venta_model.listar_stock()

    def crear_pedido(self, num_moto, num_chasis, cantidad, comprador, darsena):
        return self.venta_model.crear_pedido(num_moto, num_chasis, cantidad, comprador, darsena)

    def listar_ventas(self):
        return self.venta_model.listar_ventas()