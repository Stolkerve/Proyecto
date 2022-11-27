from collections.abc import Callable
from dataclasses import dataclass

from db import db
from utils import ask_value, is_in_range, clear_screen, pause_cin

MENU_MSG = "Ingrese una opcion. Ver partidos por pais (0), partidos por estadio (1), partidos por fecha (2): "

@dataclass
class PartidosMenu():
    def main(self, main_menu: Callable):
        self.main_menu = main_menu
        clear_screen()
        option = int(ask_value(MENU_MSG, MENU_MSG, lambda v: is_in_range(v, 2)))
        if option == 0:
            self.match_per_country()
        elif option == 1:
            self.match_per_stadium()
        elif option == 2:
            self.match_per_date()

    def match_per_country(self):
        clear_screen()
        msg = "Ingrese el pais: "
        msg_err = "Ingrese un pais existente: "

        print(f"Paises: ")
        for p in db.partidos_por_pais.keys():
            print(f"\t{p}")
        print()
        p = ask_value(msg, msg_err, lambda v: v in db.partidos_por_pais.keys())
        for m in db.partidos_por_pais[p]:
            print(f"\t{m.home_team} VS {m.away_team}")

        pause_cin()
        self.main_menu()

    def match_per_stadium(self):
        clear_screen()
        msg = "Ingrese un estadio: "
        msg_err = "Ingrese un estadio existente: "

        print(f"Paises: ")
        for s in db.partidos_por_estadio.keys():
            print(f"\t {s}")
        print()
        p = ask_value(msg, msg_err, lambda v: v in db.partidos_por_estadio.keys())
        for m in db.partidos_por_estadio[p]:
            print(f"\t{m.home_team} VS {m.away_team}")

        pause_cin()
        self.main_menu()

    def match_per_date(self):
        clear_screen()
        msg = "Ingrese una fecha: "
        msg_err = "Ingrese una fecha existente: "

        print(f"Paises: ")
        for d in db.partidos_por_fecha.keys():
            print(f"\t {d}")
        print()
        p = ask_value(msg, msg_err, lambda v: v in db.partidos_por_fecha.keys())
        for m in db.partidos_por_fecha[p]:
            print(f"\t{m.home_team} VS {m.away_team}")

        pause_cin()
        self.main_menu()
