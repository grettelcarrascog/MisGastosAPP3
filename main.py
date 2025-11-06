import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv

from modelo import Gasto, inicializar_db
from gastos_controller import GastosController
from validaciones import descripcion_valida, monto_valido
from eventos import EventBus
from log_observer import LogObserver

# Inicializo la base al arrancar
inicializar_db()

# Clase principal de la app - Vista
class AppGastos:
    def __init__(self, root, controller, event_bus):
        self.root = root
        self.root.title("Registro de Gastos Personales")
        self.root.geometry("720x600")
        self.root.configure(bg="misty rose")

        self.controller = controller
        self.event_bus = event_bus

        # Variables para los campos
        self.entrada_descripcion = tk.StringVar()
        self.entrada_monto = tk.StringVar()
        self.entrada_categoria = tk.StringVar()
        self.mensaje = tk.StringVar()

        # Categorías disponibles
        self.categorias = ["Alimentación", "Transporte", "Vivienda", "Salud",
                           "Educación", "Ocio", "Compras", "Servicios", "Deudas", "Otros"]

        # Armo la interfaz
        self.crear_interfaz()
        self.actualizar_tabla()

        # Suscribo la vista a eventos simples para refrescar tabla - observador 
        self.event_bus.subscribe("gasto_creado", lambda _: self.actualizar_tabla())
        self.event_bus.subscribe("gasto_modificado", lambda _: self.actualizar_tabla())
        self.event_bus.subscribe("gasto_eliminado", lambda _: self.actualizar_tabla())

    # Armo todos los elementos visuales
    def crear_interfaz(self):
        font_label = ("Courier New", 10, "bold")
        tk.Label(self.root, text="Detalle de tus gastos", bg="misty rose",
                 font=("Courier New", 12, "bold")).pack(pady=(10, 5))

        frame_entrada = tk.Frame(self.root, bg="misty rose")
        frame_entrada.pack(pady=5)

        tk.Label(frame_entrada, text="Descripción:", bg="misty rose", font=font_label)\
            .grid(row=0, column=0, padx=5, sticky="e")
        tk.Entry(frame_entrada, textvariable=self.entrada_descripcion, width=30)\
            .grid(row=0, column=1, padx=5)

        tk.Label(frame_entrada, text="Monto:", bg="misty rose", font=font_label)\
            .grid(row=1, column=0, padx=5, sticky="e")
        tk.Entry(frame_entrada, textvariable=self.entrada_monto, width=30)\
            .grid(row=1, column=1, padx=5)

        tk.Label(frame_entrada, text="Categoría:", bg="misty rose", font=font_label)\
            .grid(row=2, column=0, padx=5, sticky="e")
        self.combo_categoria = ttk.Combobox(frame_entrada, textvariable=self.entrada_categoria,
                                            values=self.categorias, state="readonly", width=28)
        self.combo_categoria.grid(row=2, column=1, padx=5)
        self.combo_categoria.set("")

        frame_botones = tk.Frame(self.root, bg="misty rose")
        frame_botones.pack(pady=5)

        tk.Button(frame_botones, text="Agregar", command=self.agregar_gasto, bg="lavender")\
            .grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Modificar", command=self.modificar, bg="bisque")\
            .grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar, bg="salmon")\
            .grid(row=0, column=2, padx=5)
        tk.Button(frame_botones, text="Exportar", command=self.exportar_csv, bg="light green")\
            .grid(row=0, column=3, padx=5)

        tk.Label(self.root, textvariable=self.mensaje, fg="purple", bg="misty rose",
                 font=font_label).pack(pady=5)

        columnas = ("ID", "Descripción", "Monto", "Categoría", "Fecha")
        self.tabla = ttk.Treeview(self.root, columns=columnas, show="headings", height=12)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor=tk.CENTER, width=130 if col != "Descripción" else 160)
        self.tabla.pack(pady=5)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

        self.total_label = tk.Label(self.root, text="Total gastado: $0.00", bg="misty rose", font=font_label)
        self.total_label.pack(pady=10)

    # Agrego un nuevo gasto usando el controlador 
    def agregar_gasto(self):
        descripcion = self.entrada_descripcion.get()
        monto = self.entrada_monto.get()
        categoria = self.entrada_categoria.get()
        fecha = datetime.now().strftime("%d/%m/%Y")

        # Validaciones 
        if not descripcion_valida(descripcion):
            self.mensaje.set("Descripción inválida.")
            return
        if not monto_valido(monto):
            self.mensaje.set("Monto inválido.")
            return
        if not categoria:
            self.mensaje.set("Seleccioná una categoría.")
            return

        try:
            gasto = Gasto(descripcion, float(monto), categoria, fecha)
            self.controller.agregar_gasto(gasto)  # el controlador maneja DB y emite eventos
            self.mensaje.set("Gasto registrado.")
            self.actualizar_tabla()
            self.limpiar()
        except Exception as e:
            self.mensaje.set(f"Error: {e}")

    # Elimino el gasto seleccionado
    def eliminar(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion)
            id_gasto = item["values"][0]
            try:
                self.controller.eliminar_gasto(id_gasto)
                self.mensaje.set("Gasto eliminado.")
                self.actualizar_tabla()
                self.limpiar()
            except Exception as e:
                self.mensaje.set(f"Error: {e}")

    # Modifico el gasto seleccionado
    def modificar(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion)
            id_gasto = item["values"][0]

            descripcion = self.entrada_descripcion.get()
            monto = self.entrada_monto.get()
            categoria = self.entrada_categoria.get()
            fecha = datetime.now().strftime("%d/%m/%Y")

            if not descripcion_valida(descripcion) or not monto_valido(monto):
                self.mensaje.set("Datos inválidos.")
                return
            if not categoria:
                self.mensaje.set("Seleccioná una categoría.")
                return

            try:
                gasto = Gasto(descripcion, float(monto), categoria, fecha)
                self.controller.modificar_gasto(id_gasto, gasto)
                self.mensaje.set("Gasto modificado.")
                self.actualizar_tabla()
                self.limpiar()
            except Exception as e:
                self.mensaje.set(f"Error: {e}")

    # Actualizo la tabla con los datos actuales
    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        registros = self.controller.obtener_gastos()
        total = 0
        for id_gasto, descripcion, monto, categoria, fecha in registros:
            self.tabla.insert("", tk.END, values=(id_gasto, descripcion, f"${monto:.2f}", categoria, fecha))
            total += monto

        self.total_label.config(text=f"Total gastado: ${total:.2f}")

    # Cargo los datos al seleccionar una fila
    def seleccionar(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion)
            valores = item["values"]
            self.entrada_descripcion.set(valores[1])
            self.entrada_monto.set(valores[2].replace("$", ""))
            self.entrada_categoria.set(valores[3])

    # Limpia los campos de entrada
    def limpiar(self):
        # Borras los datos ingresados para arrancar limpio
        self.entrada_descripcion.set("")
        self.entrada_monto.set("")
        self.combo_categoria.set("")

    # Exporta todo a CSV
    def exportar_csv(self):
        try:
            registros = self.controller.obtener_gastos()
            with open("gastos_exportados.csv", mode="w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(["ID", "Descripción", "Monto", "Categoría", "Fecha"])
                for fila in registros:
                    escritor.writerow(fila)
            self.mensaje.set("Exportación exitosa.")
            # emito un evento de log informativo
            self.event_bus.emit("log", {"level": "INFO", "message": "Exportación CSV realizada"})
        except Exception as e:
            self.mensaje.set("Error al exportar.")
            self.event_bus.emit("log", {"level": "ERROR", "message": f"Error exportar CSV: {e}"})

# Ejecuto la app
if __name__ == "__main__":
    bus = EventBus()
    # Observador que guarda logs
    from remoto import enviar_remoto
    observer = LogObserver(enviar_remoto=enviar_remoto)
    bus.subscribe("log", observer.on_log)

    root = tk.Tk()
    controller = GastosController(event_bus=bus)
    app = AppGastos(root, controller, bus)
    root.mainloop()