from peewee import SqliteDatabase, Model, CharField, fn
import os

# Configurar la base de datos
db = SqliteDatabase(os.path.join(os.path.dirname(__file__), "linea_produccion.db"))

class MotoOk(Model):
    num_moto = CharField(primary_key=True)
    num_motor = CharField()
    
    class Meta:
        database = db
        table_name = 'motos_ok'

class MotoNoOk(Model):
    num_moto = CharField(primary_key=True)
    num_motor = CharField()
    defecto = CharField()
    
    class Meta:
        database = db
        table_name = 'motos_no_ok'

class Moto:

    defectos = [
        "Defectos pieza origen",
        "Defecto montaje",
        "Otros"
    ]
    
    def __init__(self):
        db.create_tables([MotoOk, MotoNoOk], safe=True)

    def alta(self, moto, motor):
        if not moto or not motor:
            return False
        
        try:
            MotoOk.replace(num_moto=moto, num_motor=motor).execute()
            MotoNoOk.delete().where(MotoNoOk.num_moto == moto).execute()
            return True
        except:
            return False

    def baja(self, moto, motor, defecto):
        try:
            prueba = int(defecto) - 1
            if prueba < 0 or prueba >= len(self.defectos):
                return False
            
            defecto = self.defectos[prueba]
            MotoNoOk.replace(num_moto=moto, num_motor=motor, defecto=defecto).execute()
            return True
        except ValueError:
            return False

    def mover_a_ok(self, moto):
        try:
            moto_no_ok = MotoNoOk.get(MotoNoOk.num_moto == moto)
            MotoNoOk.delete().where(MotoNoOk.num_moto == moto).execute()
            MotoOk.replace(num_moto=moto_no_ok.num_moto, num_motor=moto_no_ok.num_motor).execute()
            return True
        except:
            return False
    
    def buscar(self, moto):
        try:
            MotoOk.get(MotoOk.num_moto == moto)
            return "Moto OK"
        except:
            pass
        
        try:
            moto_no_ok = MotoNoOk.get(MotoNoOk.num_moto == moto)
            return f"Moto NO OK - Defecto: {moto_no_ok.defecto}"
        except:
            return "Moto no encontrada"
    
    def listar_ok(self):
        return [(m.num_moto, m.num_motor) for m in MotoOk.select()]
    
    def listar_no_ok(self):
        return [(m.num_moto, m.num_motor, m.defecto) for m in MotoNoOk.select()]
    
    def final_dia(self):
        contador_ok = MotoOk.select(fn.COUNT('*')).scalar()
        contador_no_ok = MotoNoOk.select(fn.COUNT('*')).scalar()
        return contador_ok, contador_no_ok