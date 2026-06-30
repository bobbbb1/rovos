import inspect

def _get_node_name():
    """Mencari tahu nama node yang sedang memanggil log ini secara otomatis"""
    try:
        frame = inspect.currentframe().f_back.f_back
        local_self = frame.f_locals.get('self', None)
        if local_self and hasattr(local_self, 'name'):
            return local_self.name
    except Exception:
        pass
    return "ROVOS"

def log(msg: str):
    WHITE = "\033[0m"
    RESET = "\033[0m"
    print(f"{WHITE}[LOG][{_get_node_name()}] {msg}{RESET}")

def info(msg: str):
    GREY = "\033[90m"
    RESET = "\033[0m"
    print(f"[{GREY}INFO{RESET}][{_get_node_name()}] {msg}")

def success(msg: str):
    GREEN = "\033[92m"
    RESET = "\033[0m"
    print(f"[{GREEN}SUCCESS{RESET}][{_get_node_name()}] {msg}")

def warn(msg: str):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"[{YELLOW}WARN{RESET}][{_get_node_name()}] {msg}")

def error(msg: str):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"[{RED}ERROR{RESET}][{_get_node_name()}] {msg}")