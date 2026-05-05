from model.Map import Map
from model.Connection import Connection
from model.Drone import Drone
from typing import Type


class Base:
    pass


class Sub(Base):
    pass


class Pathfinder:
    def __init__(self, mapa: Map) -> None:
        self.mapa = mapa
        self.reservas_hubs = {}
        self.reservas_conexiones = {}

        self.hubs_dict = {hub.getName(): hub for hub in mapa.getHubs()}
        self.hubs_dict[mapa.getStartHub().getName()] = mapa.getStartHub()
        self.hubs_dict[mapa.getEndHub().getName()] = mapa.getEndHub()
        self.vecinos = {nombre: [] for nombre in self.hubs_dict.keys()}

        for conn in mapa.getConnections():
            h1 = conn.getHub1()
            h2 = conn.getHub2()
            self.vecinos[h1].append((h2, conn))
            self.vecinos[h2].append((h1, conn))

    def _obtener_coste_zona(self, zone_type: str) -> float:
        costes = {"normal": 1.0, "priority": 0.5, "restricted": 5.0,
                  "blocked": float('inf')}
        return costes.get(zone_type.lower(), 1.0)

    def _capacidad_hub_disponible(self, hub_name: str, turno: int) -> bool:
        hub = self.hubs_dict[hub_name]
        if (hub.getMaxDrones() == -1 or hub_name in
            [self.mapa.getStartHub().getName(),
             self.mapa.getEndHub().getName()]):
            return True
        return (self.reservas_hubs.get((hub_name,
                                        turno), 0) < hub.getMaxDrones())

    def _capacidad_conexion_disponible(self, conn: Connection,
                                       turno: int) -> bool:
        if conn.getMaxLink() == -1:
            return True
        conn_pair = tuple(sorted([conn.getHub1(), conn.getHub2()]))
        return self.reservas_conexiones.get(
            (conn_pair, turno), 0) < conn.getMaxLink()

    def buscar_ruta_para_un_dron(self) -> list:
        cola = []
        nombre_inicio = self.mapa.getStartHub().getName()
        nombre_fin = self.mapa.getEndHub().getName()
        cola.append((0, 0, nombre_inicio, [nombre_inicio]))
        visitados = set()

        def extraer_coste(elemento_cola):
            coste_acumulado = elemento_cola[0]
            return coste_acumulado

        while cola:
            cola.sort(key=extraer_coste)
            coste, turno, actual, ruta = cola.pop(0)

            if actual == nombre_fin:
                return ruta

            estado = (actual, turno)
            if estado in visitados:
                continue
            visitados.add(estado)

            if self._capacidad_hub_disponible(actual, turno + 1):
                nueva_ruta = list(ruta)
                nueva_ruta.append(actual)
                cola.append((coste + 1, turno + 1, actual, nueva_ruta))

            for nombre_vecino, conexion in self.vecinos[actual]:
                hub_vecino = self.hubs_dict[nombre_vecino]
                coste_mov = self._obtener_coste_zona(hub_vecino.getZone())

                if coste_mov == float('inf'):
                    continue

                if (self._capacidad_hub_disponible(nombre_vecino, turno + 1)
                    and self._capacidad_conexion_disponible(conexion,
                                                            turno + 1)):

                    nueva_ruta = list(ruta)
                    nueva_ruta.append(nombre_vecino)
                    cola.append((coste + coste_mov, turno + 1,
                                 nombre_vecino, nueva_ruta))

        return []

    def planificar_flota(self, clase_dron: Type[Base]) -> list[Drone]:
        flota_drones = []

        for id_dron in range(self.mapa.getNbDrones()):
            ruta_dron = self.buscar_ruta_para_un_dron()

            if not ruta_dron:
                print(f"ERROR:Imposible encontrar ruta para el Dron {id_dron}")
                break

            nuevo_dron = clase_dron(id_dron, ruta_dron)
            flota_drones.append(nuevo_dron)

            for turno in range(len(ruta_dron)):
                hub_actual = ruta_dron[turno]
                self.reservas_hubs[(hub_actual, turno)] = \
                    self.reservas_hubs.get((hub_actual, turno), 0) + 1
                if turno > 0:
                    hub_anterior = ruta_dron[turno - 1]
                    if hub_anterior != hub_actual:
                        conn_pair = tuple(sorted([hub_anterior, hub_actual]))
                        self.reservas_conexiones[(conn_pair, turno)] = \
                            self.reservas_conexiones.get((conn_pair,
                                                          turno), 0) + 1

        return flota_drones
