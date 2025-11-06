# Observador que escucha eventos y los guarda en observer.log.

class LogObserver:
    def __init__(self, enviar_remoto=None):
        self.enviar_remoto = enviar_remoto  # función para enviar logs a servidor remoto

    def on_log(self, payload):
        # payload: {"level": "INFO"/"ERROR", "message": "texto"}
        line = f"{payload.get('level', 'INFO')} | {payload.get('message', '')}"
        try:
            with open("observer.log", "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception as e:
            print(f"Error escribiendo observer.log: {e}")

        # Si tengo cliente, intento enviar al server
        if self.enviar_remoto:
            try:
                self.enviar_remoto(payload)
            except Exception as e:
                print(f"Error enviando log remoto: {e}")