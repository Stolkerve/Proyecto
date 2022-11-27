from threading import Thread

from main_menu import main_menu
from utils import enable_ansi_color, Colors, waiting_animation, clear_screen
from db import fetch_data, load_save_file

def setup_data():
    # Hacemos las peticiones http a la api para inicializar la db
    if not fetch_data():
        print(f"{Colors.RED}Hubo un error con los endpoints de la api. No se puede proseguir con la app{Colors.END}")
        exit()

    # Creamos un archivo de guardado si no existe, sino lo cargamos

    # y guardamos en db todos los datos
    load_save_file()

def main():
    clear_screen()

    t = Thread(target=setup_data)
    t.start()

    enable_ansi_color()

    waiting_animation(t)

    main_menu()

if __name__ == "__main__":
    main()
