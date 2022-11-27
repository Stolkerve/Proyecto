from dataclasses import dataclass

@dataclass
class Team:
    id: int
    name: str
    flag: str
    fifa_code: str
    group: str

@dataclass
class Product:
    name: str
    price: int
    type: str
    adicional: str
    quantity: int # cantidad maxima de productos
    sold: int # cantidad vendida de productos

@dataclass
class Restaurant:
    stadium_id: int
    name: str
    products: list[Product]

@dataclass
class Stadium:
    id: int
    name: str
    capacity: tuple[int, int]
    location: str

@dataclass
class Match:
    id: int
    home_team: str
    away_team: str
    date: str
    stadium_id: int

@dataclass
class Ticket:
    id: str
    client_name: str
    client_id: int
    client_age: int
    match_id: int
    stadium_id: int
    type: bool # False para entrada general y True para la vip
    burnend: bool # False si ya se utilizo
    seat: str
    spents: float

@dataclass
class Bill:
    client_id: int
    stadium_id: int
    restaurant: str
    product: str
    spents: float

@dataclass
class DB:
    teams: list[Team]
    stadiums: list[Stadium]
    restaurants: list[Restaurant]
    matches: list[Match]

    # filtros
    partidos_por_pais: dict[str, list[Match]]
    partidos_por_estadio: dict[str, list[Match]]
    partidos_por_fecha: dict[str, list[Match]]

    # Datos de guardado
    tickets: list[Ticket]
    res_bills: list[Bill]
