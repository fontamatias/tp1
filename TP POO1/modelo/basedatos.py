from peewee import SqliteDatabase
import os

class BaseDeDatos:

    def __init__(self, nombre_db):
        ruta = os.path.join(os.path.dirname(__file__), nombre_db)
        self.db = SqliteDatabase(ruta)

    def ejecutar(self, sql, params=()):
        """Ejecuta una query SQL directa"""
        return self.db.execute_sql(sql, params)

    def fetchone(self, sql, params=()):
        """Obtiene una fila"""
        cursor = self.db.execute_sql(sql, params)
        return cursor.fetchone()
    
    def fetchall(self, sql, params=()):
        """Obtiene todas las filas"""
        cursor = self.db.execute_sql(sql, params)
        return cursor.fetchall()