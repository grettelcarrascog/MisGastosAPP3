# Cliente simple para enviar un log como JSON al servidor de logs.

import socket
import json

def enviar_remoto(payload, host="127.0.0.1", port=5050):
    """
    payload: dict con {"level": "...", "message": "..."}
    """
    try:
        data = (json.dumps(payload) + "\n").encode("utf-8")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(data)
    except Exception as e:
        # Si el server no está, no rompo la app
        print(f"No se pudo enviar log remoto: {e}")