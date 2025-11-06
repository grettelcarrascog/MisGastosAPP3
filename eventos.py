# EventBus para emitir y suscribir eventos - observador

class EventBus:
    def __init__(self):
        self._subs = {}

    def subscribe(self, event_name, callback):
        self._subs.setdefault(event_name, []).append(callback)

    def emit(self, event_name, payload):
        for cb in self._subs.get(event_name, []):
            try:
                cb(payload)
            except Exception as e:
                # No quiero que un error en un observer rompa la app
                print(f"Error en observer '{event_name}': {e}")