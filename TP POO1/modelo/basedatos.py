import sqlite3
import os

class BaseDeDatos:

    def __init__ (self, nombre_db):
        ruta = os.path.join(os.path.dirname(__file__), nombre_db)
        self.db=sqlite3.connect(ruta)
        self.cursor=self.db.cursor()

    def ejecutar(self, sql, params=()):
        cursor = self.db.cursor()
        cursor.execute(sql, params)

        if not sql.strip().upper().startswith("SELECT"):
            self.db.commit()

        return cursor

        
    def fetchone(self,sql,params=()):
        self.cursor.execute(sql,params)
        return self.cursor.fetchone()
    
    def fetchall(self, sql,params=()):
        self.cursor.execute(sql,params)
        return self.cursor.fetchall()
