# Servidor que guarda lo que recibe en server.log.

import socket
import threading

HOST = "0.0.0.0"
PORT = 5050

def handle_client(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode("utf-8").strip()
            # Guardo lo recibido con el origen del cliente
            try:
                with open("server.log", "a", encoding="utf-8") as f:
                    f.write(f"{addr} | {msg}\n")
            except Exception as e:
                print(f"Error escribiendo server.log: {e}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor de logs en {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()