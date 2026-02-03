from modelo.basedatos import BaseDeDatos

class Moto(BaseDeDatos):

    defectos = [
        "Defectos pieza origen",
        "Defecto montaje",
        "Otros"
    ]
    
    def __init__(self):
        super().__init__("linea_produccion.db")

        self.ejecutar("""
                      CREATE TABLE IF NOT EXISTS motos_ok(
                      num_moto TEXT PRIMARY KEY,
                      num_motor TEXT
                      )
                      """)
        
        self.ejecutar("""
                      CREATE TABLE IF NOT EXISTS motos_no_ok(
                      num_moto TEXT PRIMARY KEY,
                      num_motor TEXT,
                      defecto TEXT
                      )
                      """)
        
    def alta(self, moto, motor):
        if not moto or not motor:
                return False
            
        self.ejecutar(
                "INSERT OR REPLACE INTO motos_ok VALUES (?,?)",
                (moto, motor)
            )
        self.ejecutar(
                "DELETE FROM motos_no_ok WHERE num_moto=?",
                (moto,)
            )
        return True

    def baja (self, moto, motor, defecto):
        try:
            prueba = int(defecto)-1
            if prueba<0 or prueba>=len(self.defectos):
                 return False
            
            defecto = self.defectos[prueba]

            self.ejecutar(
                 "INSERT OR REPLACE INTO motos_no_ok VALUES (?,?,?)",
                 (moto,motor,defecto)
            )
            return True
        except ValueError:
             return False

    def mover_a_ok(self, moto):
         fila = self.fetchone(
              "SELECT num_moto, num_moto FROM motos_no_ok WHERE num_moto=?",
              (moto,)
         )
         if fila:
              self.ejecutar("DELETE FROM motos_no_ok WHERE num_moto=?",(moto,))
              self.ejecutar("INSERT OR REPLACE INTO motos_ok VALUES (?,?)",fila)
              return True
         return False
    
    def buscar(self,moto):
         if self.fetchone("SELECT 1 FROM motos_ok WHERE num_moto=?",(moto,)):
              return "Moto OK"
         
         res=self.fetchone(
              "SELECT defecto FROM motos_no_ok WHERE num_moto=?",
              (moto,)
         )
         if res:
              return f"moto no encontrada"
    
    def listar_ok(self):
         return self.fetchall("SELECT * FROM motos_ok")
    
    def listar_no_ok(self):
         return self.fetchall("SELECT * FROM motos_no_ok")
    
    def final_dia(self):
         cursor=self.ejecutar(
              "SELECT COUNT(*)FROM motos_ok"
         )
         contador_ok=cursor.fetchone()[0]

         cursor=self.ejecutar(
              "SELECT COUNT(*)FROM motos_no_ok"
         )
         contador_no_ok=cursor.fetchone()[0]

         return contador_ok, contador_no_ok
