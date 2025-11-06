import re

def descripcion_valida(texto):
    patron = r'^[A-Za-zÁÉÍÓÚáéíóúñÑ0-9\s.,#-]+$'
    return re.match(patron, texto)

def monto_valido(valor):
    patron = r'^\d+(\.\d{1,2})?$'
    return re.match(patron, valor)