from controlador.controlador_distribucion import ControladorDistribucion
from vista.login_distribucion import LoginDistribucion

if __name__ == "__main__":
    controlador = ControladorDistribucion()
    LoginDistribucion(controlador)