# Decorador para registrar acciones con timestamp.

import functools
from datetime import datetime

def log_action(action_name):
    """
    Uso:
    @log_action("agregar_gasto")
    def funcion(...):
        ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ts = datetime.now().isoformat(timespec='seconds')
            try:
                result = func(*args, **kwargs)
                msg = f"{ts} | OK | {action_name}"
            except Exception as e:
                msg = f"{ts} | ERROR | {action_name} | {e}"
                _write_log(msg)
                raise
            _write_log(msg)
            return result
        return wrapper
    return decorator

def _write_log(message):
    # Log local en app.log
    try:
        with open("app.log", "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except Exception as e:
        # Si falla escribir, no rompo la app
        print(f"Error escribiendo log: {e}")