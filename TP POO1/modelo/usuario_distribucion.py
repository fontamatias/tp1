from modelo.basedatos import BaseDeDatos
import re
from peewee import *

class UsuarioDistribucion(BaseDeDatos):

    regex_usuario = r"^[A-Za-z]{3,20}$"
    regex_password = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$"

    def __init__(self):
        # DB separada para usuarios de distribución
        super().__init__("distribucion_usuarios.db")
        self.ejecutar("""
            CREATE TABLE IF NOT EXISTS usuarios(
                usuario TEXT PRIMARY KEY,
                password TEXT
            )
        """)

    def validar_usuario(self, usuario):
        if not re.match(self.regex_usuario, usuario):
            return "Nombre inválido. Debe contener solo letras y entre 3 y 20 caracteres"
        return None

    def validar_password(self, password):
        if not re.match(self.regex_password, password):
            return (
                "Contraseña inválida.\n"
                "Debe tener:\n"
                "- Mayúscula\n"
                "- Minúscula\n"
                "- Número\n"
                "- Símbolo\n"
                "- Mínimo 8 caracteres"
            )
        return None

    def obtener(self, usuario):
        return self.fetchone("SELECT password FROM usuarios WHERE usuario=?", (usuario,))

    def crear(self, usuario, password):
        self.ejecutar("INSERT OR REPLACE INTO usuarios VALUES (?,?)", (usuario, password))

    def login(self, usuario, password):
        error = self.validar_usuario(usuario)
        if error:
            return error

        error = self.validar_password(password)
        if error:
            return error

        user = self.obtener(usuario)
        if user and user[0] != password:
            return "Contraseña incorrecta"

        if not user:
            self.crear(usuario, password)

        return None