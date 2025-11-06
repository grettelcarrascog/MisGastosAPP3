# Controlador que coordina la capa de datos y la vista.
# Aplico decorador de logging y emito eventos.

from logging_decorator import log_action
from db import insertar_gasto, obtener_gastos, eliminar_gasto, modificar_gasto

class GastosController:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    @log_action("agregar_gasto")
    def agregar_gasto(self, gasto):
        insertar_gasto(gasto)
        # emito un evento para que la vista refresque y para el sistema de logs
        self.event_bus.emit("gasto_creado", {"gasto": gasto})
        self.event_bus.emit("log", {"level": "INFO", "message": "Gasto agregado en DB"})

    @log_action("modificar_gasto")
    def modificar_gasto(self, id_gasto, gasto):
        modificar_gasto(id_gasto, gasto)
        self.event_bus.emit("gasto_modificado", {"id": id_gasto, "gasto": gasto})
        self.event_bus.emit("log", {"level": "INFO", "message": f"Gasto {id_gasto} modificado"})

    @log_action("eliminar_gasto")
    def eliminar_gasto(self, id_gasto):
        eliminar_gasto(id_gasto)
        self.event_bus.emit("gasto_eliminado", {"id": id_gasto})
        self.event_bus.emit("log", {"level": "INFO", "message": f"Gasto {id_gasto} eliminado"})

    # listar no necesita decorador
    def obtener_gastos(self):
        return obtener_gastos()