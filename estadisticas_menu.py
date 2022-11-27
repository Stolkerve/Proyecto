import numpy as np
from matplotlib import pyplot as plt
from tabulate import tabulate
from collections.abc import Callable
from dataclasses import dataclass

from db import db
from utils import Colors, ask_value, is_in_range, clear_screen, pause_cin

MENU_MSG = "Promedio de gasto de un cliente VIP (0),\n" + \
    "Tabla de asistencias de los partidos (1),\n" + \
    "Partido con mayor asistencia (2),\n" + \
    "Partido con mayor boletos vendidos (3),\n" + \
    "Top 3 productos más vendidos de los restaurantes (4),\n" + \
    "Top 3 de clientes con más boletos (5),\n" + \
    "Volver a menu pricipal (6),\n" + \
    "Ingrese una opcion: "

@dataclass
class EstadisticasMenu():
    def main(self, main_menu: Callable):
        self.main_menu = main_menu
        clear_screen()
        option = int(ask_value(MENU_MSG, MENU_MSG, lambda v: is_in_range(v, 6)))
        if option == 0:
            clear_screen()
            self.show_spents_avarege()
        elif option == 1:
            clear_screen()
            self.show_assistance_table()
        elif option == 2:
            clear_screen()
            self.most_attended_match()
        elif option == 3:
            clear_screen()
            self.most_sold_match_ticket()
        elif option == 4:
            clear_screen()
            self.top_most_sold_products()
        elif option == 5:
            clear_screen()
            self.top_clients()
        elif option == 6:
            self.main_menu()

    def check_tickets(self):
        if not len(db.tickets):
            print(f"{Colors.RED}No hay data para computar estadisticas{Colors.END}")
            pause_cin()
            self.main_menu()

    def show_spents_avarege(self):
        self.check_tickets()
        spents = []
        for t in db.tickets:
            if t.type:
                amount = t.spents
                for b in db.res_bills:
                    if t.client_id == b.client_id:
                        amount += b.spents
                spents.append(int(amount))

        plt.scatter(spents, spents, color="red", label="Gastos (restaurante + V.I.P) por cliente")
        avg = np.average(spents)
        plt.axhline(y=int(avg), linestyle='--', label="Promedio gastos (restaurante + V.I.P)")
        plt.legend()
        plt.show()
        pause_cin()
        try: plt.close()
        except: pass
        self.main(self.main_menu)

    def show_assistance_table(self):
        clear_screen()
        columns_labels = ["Partido", "Estadio", "Boletos vendidos", "Personas que asistieron", "Asistencia/ventas"]
        cells = []

        for m in db.matches:
            solds = 0
            assistance = []
            for t in db.tickets:
                if t.match_id == m.id:
                    solds += 1
                    if t.burnend:
                        assistance.append(t.client_name)
            stadium = list(filter(lambda s: s.id == m.stadium_id, db.stadiums))[0]
            people = ""
            for i, a in enumerate(assistance):
                if i == len(assistance) - 1:
                    people += a
                else:
                    people += f"{a}, "

            assistance_solds = "0"
            if solds != 0 and len(assistance) != 0:
                ratio = (len(assistance) / solds).as_integer_ratio()
                assistance_solds = f"{ratio[0]}/{ratio[1]}"

            cells.append([f"{m.home_team} VS {m.away_team}", stadium.name, solds, people, assistance_solds])

        print(tabulate(cells, headers=columns_labels))
        pause_cin()
        self.main(self.main_menu)

    def most_attended_match(self):
        self.check_tickets()
        matches: dict[str, int] = {}
        for t in db.tickets:
            for m in db.matches:
                if t.match_id == m.id and t.burnend:
                    print(f"{m.home_team} VS {m.away_team}")
                    try:
                        matches[f"{m.home_team} VS {m.away_team}"] = matches[f"{m.home_team} VS {m.away_team}"] + 1
                    except:
                        matches[f"{m.home_team} VS {m.away_team}"] = 1

        print(matches)
        max = 0
        match = ""
        for k in matches:
            if max <= matches[k]:
                max = matches[k]
                match = k

        print(f"El partido con mayor asistencia es {match}, con {max} asientos ocupados")

        _ = plt.figure(figsize = (10, 5))
        plt.bar(list(matches.keys()), list(matches.values()))
        plt.xlabel("Partidos")
        plt.ylabel("Asistencia")
        plt.title("Asistencia en los partidos con boletos comprados")
        plt.show()
        pause_cin()
        try: plt.close()
        except: pass
        self.main(self.main_menu)
    
    def most_sold_match_ticket(self):
        self.check_tickets()
        matches: dict[str, int] = {}
        for t in db.tickets:
            for m in db.matches:
                if t.match_id == m.id:
                    try:
                        matches[f"{m.home_team} VS {m.away_team}"] = matches[f"{m.home_team} VS {m.away_team}"] + 1
                    except:
                        matches[f"{m.home_team} VS {m.away_team}"] = 1

        max = 0
        match = ""
        for k in matches:
            if max <= matches[k]:
                max = matches[k]
                match = k

        print(f"El partido con más ventas es {match}, con {max} boletos vendidos")

        _ = plt.figure(figsize = (10, 5))
        plt.bar(list(matches.keys()), list(matches.values()))
        plt.xlabel("Partidos")
        plt.ylabel("Boletos vendidos")
        plt.title("Venta de boletos de partidos")
        plt.show()
        pause_cin()
        try: plt.close()
        except: pass
        self.main(self.main_menu)
        self.check_tickets()

    def top_most_sold_products(self):
        if not len(db.res_bills):
            print(f"{Colors.RED}No hay data para computar estadisticas{Colors.END}")
            pause_cin()
            self.main_menu()

        res_products: dict[str, list[str]] = {}
        for b in db.res_bills:
            for r in db.restaurants:
                if r.name == b.restaurant:
                    try:
                        res_products[r.name].append(b.product)
                    except:
                        res_products[r.name] = [b.product]

        res_group_products: dict[str, dict[str, int]] = {}
        for r in res_products:
            products = res_products[r]
            res_group_products[r] = {}
            for p in set(products):
                res_group_products[r][p] = products.count(p)
            sorted_values = sorted(res_group_products[r].items(), reverse=True, key=lambda x: x[1])
            res_group_products[r].clear()
            c = 0
            for (p, i) in sorted_values:
                if c == 3:
                    break
                res_group_products[r][p] = i
                c += 1

        print("Restaurantes: ")
        restaurantes = list(res_group_products.keys())
        for i, r in enumerate(restaurantes):
            print(f"\t{r} ({i})")

        i = int(ask_value("Ingrese el restaurante: ", "Ingrese el restaurante: ", lambda v: is_in_range(v, len(restaurantes) - 1)))

        restaurante = restaurantes[i]
        data = res_group_products[restaurante]

        _ = plt.figure(figsize = (10, 5))
        plt.bar(list(data.keys()), list(data.values()), width = 0.4)

        plt.xlabel("Productos")
        plt.ylabel("Cantidad")
        plt.title(f"Top 3 productos más vendidos en el restaurante {restaurante}")
        plt.show()
        pause_cin()
        try: plt.close()
        except: pass
        self.main(self.main_menu)
        self.check_tickets()


    def top_clients(self):
        self.check_tickets()

        clients: list[str] = []
        for client_id  in set(map(lambda t: t.client_id, db.tickets)):
            for t in db.tickets:
                if client_id == t.client_id:
                    clients.append(f"{t.client_name}. C.I: {client_id}")

        clients_set = list(set(clients))

        client_tickets: dict[str, int] = {}
        for c in clients_set:
            client_tickets[c] = clients.count(c)

        data: dict[str, int] = {}
        e = 0
        for (c, i) in sorted(client_tickets.items(), reverse=True, key=lambda x: x[1]):
            if e == 3:
                break
            e += 1
            data[c] = i

        _ = plt.figure(figsize = (10, 5))
        plt.bar(list(data.keys()), list(data.values()), width = 0.4)

        plt.xlabel("Clientes")
        plt.ylabel("Cantidad")
        plt.title("Top 3 de clientes con más boletos")
        plt.show()
        pause_cin()
        try: plt.close()
        except: pass
        self.main(self.main_menu)
        self.check_tickets()
