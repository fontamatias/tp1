from modelo.basedatos import BaseDeDatos
from datetime import date
from peewee import *

class Venta(BaseDeDatos):
    def __init__(self):
        # usa la misma base de datos de producción para leer motos en stock
        super().__init__("linea_produccion.db")
        # tabla de ventas (se crea si no existe)
        self.ejecutar("""
            CREATE TABLE IF NOT EXISTS ventas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_num TEXT,
                num_moto TEXT,
                num_chasis TEXT,
                cantidad INTEGER,
                comprador TEXT,
                darsena TEXT,
                fecha TEXT
            )
        """)

    def listar_stock(self):
        # lista las motos actuales en stock (motos_ok)
        return self.fetchall("SELECT * FROM motos_ok")

    def generar_num_pedido(self):
        # genera un número de pedido simple: YYYYMMDD-<contador del día>
        hoy = date.today().isoformat().replace("-", "")
        cursor = self.ejecutar("SELECT COUNT(*) FROM ventas WHERE fecha=?", (date.today().isoformat(),))
        contador = cursor.fetchone()[0] or 0
        return f"{hoy}-{contador+1}"

    def crear_pedido(self, num_moto, num_chasis, cantidad, comprador, darsena):
        # verifica que la moto exista en stock
        if not num_moto:
            return False, "Falta número de moto"

        existencia = self.fetchone("SELECT 1 FROM motos_ok WHERE num_moto=?", (num_moto,))
        if not existencia:
            return False, "La moto no está en stock"

        # En el esquema actual cada moto es una unidad única.
        # Si se quiere vender más de 1 unidad del mismo num_moto, esto no es posible sin cambiar el modelo.
        if cantidad is None or int(cantidad) < 1:
            return False, "Cantidad inválida"
        if int(cantidad) != 1:
            return False, "En este esquema cada moto es una unidad; la cantidad debe ser 1"

        pedido_num = self.generar_num_pedido()
        fecha = date.today().isoformat()

        self.ejecutar(
            "INSERT INTO ventas (pedido_num, num_moto, num_chasis, cantidad, comprador, darsena, fecha) VALUES (?,?,?,?,?,?,?)",
            (pedido_num, num_moto, num_chasis, int(cantidad), comprador, darsena, fecha)
        )

        # quitar la moto del stock (se considera vendida)
        self.ejecutar("DELETE FROM motos_ok WHERE num_moto=?", (num_moto,))

        return True, pedido_num

    def listar_ventas(self):
        return self.fetchall("SELECT * FROM ventas ORDER BY fecha DESC, id DESC")