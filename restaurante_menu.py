from collections.abc import Callable
from dataclasses import dataclass

from db import MAX_PRODUCTOS, Bill, Restaurant, Ticket, db, write_save_file
from utils import ask_value, is_in_range, is_int, clear_screen, is_perfect_num, pause_cin, yes_or_not

MENU_MSG = "Buscar por nombre (0),\n" + \
        "ver platos (1),\n" + \
        "ver bebidas (2),\n" + \
        "ver bebidas alcoholicas (3),\n" + \
        "cancelar (4),\n" + \
        "finalizar orden (5)\n" + \
        "Ingrese una opcion: "

@dataclass
class RestauranteMenu():
    # is_legal: bool
    # restaurant: Restaurand
    # tickets: list[Ticket]
    tickets: list[Ticket]
    order: list[str]
    def main(self, main_menu: Callable):
        self.main_menu = main_menu
        ask_value("Ingrese su cédula: ", "Usted no posee ningun ticket V.I.P, intente de nuevo: ", self.check_id)

        # Ir directamente al unico restaurante
        if len(self.tickets) == 1:
            for t in self.tickets:
                self.restaurant = list(filter(lambda r: r.stadium_id == t.stadium_id, db.restaurants))[0]
            self.show_restaurant_menu()
        else:
            self.show_restaurants()

    def show_restaurants(self):
        clear_screen()
        print("Usted posee acceder a los restaurantes:")
        restaurantes: list[Restaurant] = []
        for t in self.tickets:
            for r in db.restaurants:
                if t.stadium_id == r.stadium_id:
                        restaurantes.append(r)
        for i, r in enumerate(restaurantes):
            print(f"\t{r.name} ({i})")

        i = int(ask_value("Ingrese el restaurante: ", "Ingrese un restaurante valida: ", lambda v: is_in_range(v, len(restaurantes) - 1)))

        self.restaurant = restaurantes[i]
        self.show_restaurant_menu()

    def show_restaurant_menu(self):
        clear_screen()
        print(f"Bienvenido al restaurante {self.restaurant.name}")
        if len(self.order):
            print(f"Su order es: ")
            for o in self.order:
                print(f"\t{o}")

        o = int(ask_value(MENU_MSG, MENU_MSG, lambda v: is_in_range(v, 5)))

        if o == 0:
            self.search_by_name()
        elif o == 1:
            self.search_product("comida", "food", False)
        elif o == 2:
            self.search_product("bebida", "beverages", False)
        elif o == 3:
            self.search_product("bebida alcoholica", "alcoholic", True)
        elif o == 4:
            for o in self.order:
                name = o[:o.index("(") - 1]
                for p in self.restaurant.products:
                     if p.name == name:
                         p.sold -= 1
            pause_cin()
            self.main_menu()
        elif o == 5:
            if len(self.order):
                price = 0.0
                final_price = 0.0
                products = []
                for o in self.order:
                    name = o[:o.index("(") - 1]
                    price = int(o[o.index("$")+1:o.index(")")])
                    products.append((name, price))
                    final_price += price

                is_perfect = is_perfect_num(self.tickets[0].client_id)

                print("Factura: ")
                print(f"\tSubtotal: {final_price}")
                print(f"\t16% IVA: {final_price * 0.16}")
                if is_perfect:
                    print(f"\t15% de descuento por que su cédula es un numero perfecto")
                    final_price -= price * 0.15
                final_price += price * 0.16
                print(f"Total: {final_price}")

                v = ask_value("Quiere finalizar su compra? (si, no): ", "Quiere finalizar su compra? (si, no): ", yes_or_not)
                if v == "si":
                    for (name, p) in products:
                        f_price = p
                        if is_perfect:
                            f_price -= p * 0.15
                        f_price += p * 0.16
                        db.res_bills.append(Bill(self.tickets[0].client_id, self.tickets[0].stadium_id, self.restaurant.name, name, f_price))
                    write_save_file()
                    print("Gracias por su compra!")
                    pause_cin()
                    self.main_menu()
                else:
                    self.main_menu()
            else:
                print("Usted no posee ninguna orden")
            pause_cin()
            self.show_restaurant_menu()

    def search_by_name(self):
        name = input("Nombre: ")

        match = None
        for p in self.restaurant.products:
            if p.name == name:
                match = p

        if match:
            if match.type == "alcoholic" and self.tickets[0].client_age < 18:
                print("Usted no puede comprar bebidas alcoholicas")
                pause_cin()
                self.show_restaurant_menu()
            if match.sold != MAX_PRODUCTOS:
                o = ask_value(f"Añadir {match.name} a la order (si o no): ", f"Añadir {match.name} a la order (si o no): ", yes_or_not)
                if o == "si":
                    self.order.append(f"{match.name} (${match.price})")
                    match.sold += 1
                    pause_cin()
                    self.show_restaurant_menu()
                else:
                    print(f"Cancelando la orden de {match.name}")
                    pause_cin()
                    self.show_restaurant_menu()
            else:
                print(f"No hay mas {match.name} disponible")
                pause_cin()
                self.show_restaurant_menu()
        else:
            print("No se encontro el producto")
            pause_cin()
            self.show_restaurant_menu()

    def search_product(self, name: str, type: str, plus_18: bool):
        if self.tickets[0].client_age < 18 and plus_18:
            print("Usted no puede comprar bebidas alcoholicas")
            pause_cin()
            self.show_restaurant_menu()

        filter = self.price_order()
        msg = f"Ingrese la {name} que desee ordenar: "

        products = []
        for p in self.restaurant.products:
            if p.type == type:
                if p.sold != MAX_PRODUCTOS:
                    products.append(p)
                else:
                    print(f"Se acabo {p.name}")
        if filter:
            products.sort(reverse=True, key=lambda p: p.price)
        else:
            products.sort(key=lambda p: p.price)

        print(f"{name.title()}s: ")
        if len(products):
            for i, p in enumerate(products):
                print(f"\t{p.name} ${p.price} ({i})")
        else:
            print(f"Se acabaron todos los {name}s")
            pause_cin()
            self.show_restaurant_menu()

        i = int(ask_value(msg, msg, lambda v: is_in_range(v, len(products) - 1)))
        p = products[i]
        self.order.append(f"{p.name} (${p.price})")
        p.sold += 1

        self.show_restaurant_menu()
  
    def price_order(self) -> bool:
        msg = "Buscar por menor precio (0) o mayor precio (1): "
        o = int(ask_value(msg, msg, lambda v: is_in_range(v, 1)))
        return o == 1

    def check_id(self, v: str):
        if is_int(v):
            id = int(v)
            for t in db.tickets:
                if t.client_id == id and t.type:
                    self.tickets.append(t)
            if len(self.tickets) >= 1:
                return True
        return False
