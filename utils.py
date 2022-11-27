import threading
import time
from collections.abc import Callable
from os import system, name
from itertools import permutations

class Colors():
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

def ask_value(msg: str, err_msg: str, cmp_fun: Callable) -> str:
    v = input(msg)
    while not cmp_fun(v):
        v = input(err_msg)
    return v

def is_int(v: str):
    try:
        int(v)
        return True
    except Exception:
        return False

def is_in_range(v: str, max: int):
    if is_int(v):
        o = int(v)
        if o > max:
            return False
        return True
    return False

def clear_screen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def pause_cin():
    input("[Precione enter para continuar]\n")

def yes_or_not(v: str):
    return v.lower() == "si" or v.lower() == "no"

def is_perfect_num(n: int) -> bool:
    count = 0
    for i in range(1, n):
        if n % i == 0:
            count = count + i
    return count == n

def is_vampire(n: int) -> bool:
    n_str = str(n)

    # si no es par, no cumple para ser vampiro
    if len(n_str) % 2 == 1:
        return False

    # todas las posibles combinaciones gracias a permutations
    fang1 = permutations(n_str[:int(len(n_str)/2)]) # la mitad izquirda del numero

    for f1 in fang1:
        v1 = "".join(f1)
        for f2 in permutations(n_str[int(len(n_str)/2):]): # la mitad derecha del numero
            v2 = "".join(f2)
            if int(v1) * int(v2) == int(n):
                return True
    return False

def waiting_animation(t: threading.Thread):
    animation = "|/-\\"
    idx = 0
    while t.is_alive():
        print(f"Cargando datos {animation[idx % len(animation)]}", end="\r")
        idx += 1
        time.sleep(0.1)

def enable_ansi_color():
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        # set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32
