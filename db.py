import sqlite3
from modelo import Gasto

# Inserta un gasto en la base de datos
def insertar_gasto(gasto):
    try:
        assert isinstance(gasto.monto, float), "El monto debe ser numérico"
        with sqlite3.connect("gastos.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO gastos (descripcion, monto, categoria, fecha) VALUES (?, ?, ?, ?)",
                           (gasto.descripcion, gasto.monto, gasto.categoria, gasto.fecha))
            conexion.commit()
    except AssertionError as error:
        raise ValueError(f"Error de validación: {error}")
    except Exception as e:
        print(f"Error al insertar gasto: {e}")
        raise

# Trae todos los gastos registrados
def obtener_gastos():
    try:
        with sqlite3.connect("gastos.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, descripcion, monto, categoria, fecha FROM gastos")
            registros = cursor.fetchall()
            return registros
    except Exception as e:
        print(f"Error al obtener gastos: {e}")
        return []

# Elimina un gasto por ID
def eliminar_gasto(id_gasto):
    try:
        with sqlite3.connect("gastos.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM gastos WHERE id = ?", (id_gasto,))
            conexion.commit()
    except Exception as e:
        print(f"Error al eliminar gasto: {e}")
        raise

# Modifica un gasto existente
def modificar_gasto(id_gasto, gasto):
    try:
        with sqlite3.connect("gastos.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("UPDATE gastos SET descripcion = ?, monto = ?, categoria = ?, fecha = ? WHERE id = ?",
                           (gasto.descripcion, gasto.monto, gasto.categoria, gasto.fecha, id_gasto))
            conexion.commit()
    except Exception as e:
        print(f"Error al modificar gasto: {e}")
        raise