from collections.abc import Callable
from dataclasses import dataclass
import re
import random

from db import db, Ticket, write_save_file
from utils import Colors, ask_value, is_in_range, is_int, clear_screen, pause_cin, yes_or_not, is_vampire

MAX_COLUMNS = 10

@dataclass
class EntradaMenu():
    # client_name: str
    # client_id: int
    # client_age: int
    # match: Match
    # stadium: Stadium
    # seats: [str]
    # seats_vip: int
    # seats_occupated: [str]
    # seat_type: bool

    def main(self, main_menu: Callable):
        clear_screen()
        self.main_menu = main_menu

        self.show_matches()
        ask_value("Ingrese el partido: ", "Ingrese un partido valido: ", self.check_match) # seteo dentro del callback

        self.show_map()
        ask_value("Ingrese el asiento: ", "Ingrese un asiento valido: ", self.check_seat) # lo mismo

        ask_value("Ingrese su edad: ", "Ingrese una edad valida: ", self.check_age) # lo mismo
        ask_value("Ingrese su nombre: ", "Ingrese un nombre valido: ", self.check_name) # lo mismo
        ask_value("Ingrese su cédula: ", "Ingrese una cédula valida: ", self.check_id) # lo mismo

        clear_screen()

        to_price = lambda v: 120 if v else 50
        total = to_price(self.seat_type)

        print("Factura: ")
        print("\tEntrada general: 50$" if not self.seat_type else "\tEntrada V.I.P: 120$")
        print(f"\t16% IVA: {total * 0.16}")
        is_vamp = is_vampire(int(self.client_id))
        if (is_vamp):
            print("\t50% de descuento por que su cédula es un numero vampiro!")
            total -= total * 0.5

        total += total * 0.16
        print(f"Total: {total}")

        v = ask_value("Quiere finalizar su compra? (si, no): ", "Quiere finalizar su compra? (si, no): ", yes_or_not)
        if (v == "si"):
            id = ""
            for _ in range(4):
                id += str(int.from_bytes(random.randbytes(1), byteorder="little"))
            ticket = Ticket(id, self.client_name, self.client_id, self.client_age, self.match.id, self.stadium.id, self.seat_type, False, self.seat, total)
            db.tickets.append(ticket)

            write_save_file()
            
            print(f"Gracias por su compra! Su ticket es f{id}")

            pause_cin()

            self.main_menu()
        else:
            self.main_menu()
    
    def show_matches(self):
        print("Partidos")
        for i, m in enumerate(db.matches):
            print(f"\t{m.home_team} VS {m.away_team} ({i})")

    def check_match(self, v: str) -> bool:
        if is_int(v):
            i = int(v)
            try:
                self.match = db.matches[i]
            except:
                return False

            return True
        return False

    def show_map(self):
        self.stadium =  list(filter(lambda s: s.id == self.match.stadium_id, db.stadiums))[0]
        (general, vip) = self.stadium.capacity

        self.seats = []
        self.seats_vip = general # posicion

        self.seats_occupated = list(map(lambda t: t.seat, filter(lambda t: t.stadium_id == self.stadium.id, db.tickets)))

        if len(self.seats_occupated) + 1 == (general + vip):
            print(f"{Colors.RED}Todos los asientos estan ocupados{Colors.END}")
            pause_cin()
            self.main_menu()

        print("Asientos generales (50$)")
        count = 0
        for r in range(int((general + vip) / MAX_COLUMNS)):
            print("\t|", end="")
            for c in range(MAX_COLUMNS):
                seat = f"{r}-{c}"
                if seat in self.seats_occupated:
                    print(f" {Colors.RED}{seat}{Colors.END} |", end="")
                elif count >= self.seats_vip:
                    print(f" {Colors.YELLOW}{seat}{Colors.END} |", end="")
                else:
                    print(f" {Colors.BLUE}{seat}{Colors.END} |", end="")
                self.seats.append(f"{seat}")
                count += 1
            if count == self.seats_vip:
                print("\nAsientos V.I.P (120$)")
            else:
                print()

    def check_seat(self, v: str) -> bool:
        if v in self.seats:
            if v in self.seats_occupated:
                print(f"El asiento ya esta ocupado")
                return False
            self.seat = v
            if self.seats.index(self.seat) >= self.seats_vip:
                self.seat_type = True
            else:
                self.seat_type = False
            return True
        return False

    def check_age(self, v: str) -> bool:
        if is_in_range(v, 100):
            self.client_age = int(v)
            return True
        return False

    def check_name(self, v: str) -> bool:
        if re.match("^[a-zA-Z ,.'-]+$", v):
            self.client_name = v.capitalize()
            return True
        return False

    def check_id(self, v: str) -> bool:
        if is_int(v):
            id = int(v)
            for t in db.tickets:
                if t.client_id == id and t.match_id == self.match.id:
                    print("Ya usted compro un ticket para este partido")
                    return False
                if t.client_id == id and t.client_age != self.client_age:
                    print("Su edad no coincide con los datos que ingreso anteriormente")
                    return False
                if t.client_id == id and t.client_name != self.client_name:
                    print("Su nombre no coincide con los datos que ingreso anteriormente")
                    return False
            self.client_id = id
            return True
        return False
