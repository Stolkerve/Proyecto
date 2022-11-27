from collections.abc import Callable
from dataclasses import dataclass

from db import db, write_save_file
from utils import ask_value, is_in_range, is_int, clear_screen, pause_cin

MENU_MSG = "Ingrese una opcion. Ver partidos por pais (0), partidos por estadio (1), partidos por fecha (2): "

@dataclass
class AsistenciaMenu():
    # ticket:  Ticket
    def main(self, main_menu: Callable):
        clear_screen()

        ask_value("Ingrese el id de su ticket: ", "Su ticket no existe o ya fue usado, intentelo de nuevo: ", self.check_id)

        write_save_file()

        match = list(filter(lambda m: m.id == self.ticket.match_id, db.matches))[0]

        print(f"Gracias por asistir {self.ticket.client_name} al partido {match.home_team} VS {match.away_team}")

        pause_cin()

        main_menu()

    def check_id(self, v: str):
        for t in db.tickets:
            if t.id == v and t.burnend != True:
                self.ticket = t
                t.burnend = True
                return True

        return False
