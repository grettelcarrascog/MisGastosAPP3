import sqlite3

class Gasto:
    """
    Clase que representa un gasto personal.
    Contiene descripción, monto, categoría y fecha.
    """
    def __init__(self, descripcion, monto, categoria, fecha):
        self.descripcion = descripcion
        self.monto = monto
        self.categoria = categoria
        self.fecha = fecha

def inicializar_db():
    """
    Crea la base de datos y la tabla si no existen.
    """
    try:
        conexion = sqlite3.connect("gastos.db")
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                monto REAL NOT NULL,
                categoria TEXT,
                fecha TEXT
            )
        ''')
        conexion.commit()
        conexion.close()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")