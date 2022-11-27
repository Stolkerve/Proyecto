from dataclasses import asdict
import requests
import json

from models import *
from utils import Colors

JSON_TEMPLATE = "{\"tickets\": [], \"bills\": []}"
SAVE_FILENAME = "save.json"

MAX_PRODUCTOS = 10

# Estado del programa
db = DB([], [], [], [], {}, {}, {}, [], [])

def fetch_data() -> bool:
    # Peticion a la api de los equipos
    res = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json")
    if res.status_code != 200:
        return False
    for e in res.json():
        db.teams.append(Team(int(e["id"]), e["name"], e["flag"], e["fifa_code"], e["group"]))

    # Peticion a la api de los estadios
    res = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json")
    if res.status_code != 200:
        return False

    # Es mas facil guardar si el alcohol en el tipo
    is_alcoholic = lambda p: "alcoholic" if p["adicional"] == "alcoholic" else p["type"]
    for e in res.json():
        stadium = Stadium(
            e["id"],
            e["name"],
            e["capacity"],
            e["location"],
        )
        for r in e["restaurants"]:
            db.restaurants.append(Restaurant(stadium.id, r["name"], [Product(p["name"], p["price"], is_alcoholic(p), p["adicional"], MAX_PRODUCTOS, 0) for p in r["products"]]))
        db.stadiums.append(stadium)

    # Peticion a la api de los partidos
    res = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json")
    if res.status_code != 200:
        return False
    for m in res.json():
        db.matches.append(Match(int(m["id"]), m["home_team"], m["away_team"], m["date"], m["stadium_id"]))

    #No hubo error, ahora computar los filtros
    for m in db.matches:
        for t in db.teams:
            if m.away_team == t.name or m.home_team == t.name:
                try:
                    db.partidos_por_pais[t.name].append(m)
                except:
                    db.partidos_por_pais[t.name] = [m]

    for m in db.matches:
        for s in db.stadiums:
            if m.stadium_id == s.id:
                try:
                    db.partidos_por_estadio[s.name].append(m)
                except:
                    db.partidos_por_estadio[s.name] = [m]

    for m in db.matches:
        try:
            db.partidos_por_fecha[m.date].append(m)
        except:
            db.partidos_por_fecha[m.date] = [m]
    
    return True

def load_save_file():
    # Si no existe crearlo
    try:
        f = open(SAVE_FILENAME, "x")
        j = json.loads(JSON_TEMPLATE)
        json.dump(j, f, indent=2)
        f.close()
    except:
        read_save_file()

def read_save_file():
    f = open(SAVE_FILENAME, "r+") # Si ya existe cargamos sus datos

    # Tratar de cargar el json
    try:
        j = json.load(f)
        for t in j["tickets"]:
            db.tickets.append(Ticket(t["id"], t["client_name"], t["client_id"], t["client_age"], t["match_id"], t["stadium_id"], t["type"], t["burnend"], t["seat"], t["spents"]))

        for b in j["bills"]:
            db.res_bills.append(Bill(b["client_id"], b["stadium_id"], b["restaurant"], b["product"], b["spents"]))
            for r in db.restaurants:
                if r.stadium_id == b["stadium_id"] and r.name == b["restaurant"]:
                    for p in r.products:
                        if p.name == b["product"]:
                            p.sold = p.sold + 1 if p.sold != 10 else p.sold
    except:
        print(f"{Colors.RED}El archivo de guardado se modifico de manera incorrecta. No se puede leer, se va eliminar sus datos y volver a crearlo{Colors.END}")

        f.seek(0)
        f.truncate()

        j = json.loads(JSON_TEMPLATE)
        json.dump(j, f, indent=2)
    finally:
        f.close()

# Se va a sobreescribir con todos los tickets en db
def write_save_file():
    f = open(SAVE_FILENAME, "w")
    tickets = [asdict(t) for t in db.tickets]
    bills = [asdict(b) for b in db.res_bills]
    json.dump({"tickets": tickets, "bills": bills}, f, indent=2)
    f.close()
