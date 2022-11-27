from partidos_menu import PartidosMenu
from entrada_menu import EntradaMenu
from asistencia_menu import AsistenciaMenu
from restaurante_menu import RestauranteMenu
from estadisticas_menu import EstadisticasMenu
from utils import ask_value, is_in_range, clear_screen

MENU_MSG = "Ver partidos (0),\n" + \
    "comprar entrada (1),\n" + \
    "asistir a partido (2),\n" + \
    "entrar a los restaurante (3),\n" + \
    "estadisticas (4),\n" + \
    "salir (5)\n" + \
    "Ingrese que menu quiere ingresar: "


def main_menu():
    clear_screen()
    option = int(ask_value(MENU_MSG, MENU_MSG, lambda v: is_in_range(v, 5)))

    if option == 0:
        PartidosMenu().main(main_menu)
    elif option == 1:
        EntradaMenu().main(main_menu)
    elif option == 2:
        AsistenciaMenu().main(main_menu)
    elif option == 3:
        RestauranteMenu([], []).main(main_menu)
    elif option == 4:
        EstadisticasMenu().main(main_menu)
    else:
        exit()
