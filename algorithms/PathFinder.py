from model.Map import Map
from model.Connection import Connection
from model.Drone import Drone


class Base:
    pass


class Sub(Base):
    pass


class Pathfinder:
    def __init__(self, map: Map) -> None:
        """
        Initializes the drone path planner.

        Sets up the required structures to manage:
        - Hub and connection reservations by turn.
        - A dictionary of hubs accessible by name.
        - Neighbor lists for each hub in the map.

        Args:
            map (Map): Map containing hubs, connections,
                start hub, and end hub.
        """
        self.map = map
        self.reservas_hubs: dict[tuple[str, int], int] = {}
        self.reservas_conexiones: dict[tuple[tuple[str, str], int], int] = {}

        self.hubs_dict = {hub.getName(): hub for hub in map.getHubs()}
        self.hubs_dict[map.getStartHub().getName()] = map.getStartHub()
        self.hubs_dict[map.getEndHub().getName()] = map.getEndHub()
        self.vecinos: dict[str, list[tuple[str, Connection]]] = {
            nombre: [] for nombre in self.hubs_dict.keys()}

        for conn in map.getConnections():
            h1 = conn.getHub1()
            h2 = conn.getHub2()
            self.vecinos[h1].append((h2, conn))
            self.vecinos[h2].append((h1, conn))

    def _get_cost(self, zone_type: str) -> float:
        """
        Returns the movement cost associated with a zone type.

        Costs are used to prioritize routes:
        - normal -> 1.0
        - priority -> 0.5
        - restricted -> 5.0
        - blocked -> infinity

        Args:
            zone_type (str): Zone type of the hub.

        Returns:
            float: Cost associated with the zone.
        """
        costes = {"normal": 1.0, "priority": 0.5, "restricted": 5.0,
                  "blocked": float('inf')}
        return costes.get(zone_type.lower(), 1.0)

    def _capacity_hub(self, hub_name: str, turno: int) -> bool:
        """
        Checks whether a hub has available capacity
        during a given turn.

        A hub with capacity -1 is considered unlimited.
        Start and end hubs are always available.

        Args:
            hub_name (str): Name of the hub.
            turno (int): Turn to check.

        Returns:
            bool: True if the hub can accept more drones,
                False otherwise.
        """
        hub = self.hubs_dict[hub_name]
        if (hub.getMaxDrones() == -1 or hub_name in
            [self.map.getStartHub().getName(),
             self.map.getEndHub().getName()]):
            return True
        return (self.reservas_hubs.get((hub_name,
                                        turno), 0) < hub.getMaxDrones())

    def _capacity_conex(self, conn: Connection, turno: int) -> bool:
        """
        Checks whether a connection has available capacity
        during a given turn.

        A connection with capacity -1 is considered unlimited.

        Args:
            conn (Connection): Connection between two hubs.
            turno (int): Turn to check.

        Returns:
            bool: True if the connection has available capacity,
                False otherwise.
        """
        if conn.getMaxLink() == -1:
            return True
        h1 = str(conn.getHub1())
        h2 = str(conn.getHub2())
        conn_pair: tuple[str, str] = (min(h1, h2), max(h1, h2))
        return self.reservas_conexiones.get(
            (conn_pair, turno), 0) < conn.getMaxLink()

    def search_route_for_dron(self) -> list[str]:
        """
        Finds a valid route for a drone while considering:
        - Zone movement costs.
        - Hub capacities.
        - Connection capacities.
        - Reservations made by previously planned drones.

        The algorithm explores routes based on accumulated cost
        and allows the drone to wait at a hub if necessary.

        Returns:
            list: List of hub names representing the route.
                Returns an empty list if no valid route exists.
        """
        line: list[tuple[float, int, str, list[str]]] = []
        nombre_inicio = self.map.getStartHub().getName()
        nombre_fin = self.map.getEndHub().getName()
        line.append((0, 0, nombre_inicio, [nombre_inicio]))
        visitados = set()

        def extraer_coste(elemento_cola:
                          tuple[float, int, str, list[str]]) -> tuple[int,
                                                                      float]:
            coste_acumulado = elemento_cola[0]
            turno_cola = elemento_cola[1]
            return (turno_cola, coste_acumulado)

        while line:
            line.sort(key=extraer_coste)
            coste, turno, actual, ruta = line.pop(0)

            if (turno >= 1000):
                break

            if actual == nombre_fin:
                return ruta

            estado = (actual, turno)
            if estado in visitados:
                continue
            visitados.add(estado)

            if self._capacity_hub(actual, turno + 1):
                nueva_ruta = list(ruta)
                nueva_ruta.append(actual)
                line.append((coste + 1, turno + 1, actual, nueva_ruta))

            for nombre_vecino, conexion in self.vecinos[actual]:
                hub_vecino = self.hubs_dict[nombre_vecino]
                coste_mov = self._get_cost(hub_vecino.getZone())

                if coste_mov == float('inf'):
                    continue

                if (self._capacity_hub(nombre_vecino, turno + 1)
                   and self._capacity_conex(conexion, turno + 1)):

                    nueva_ruta = list(ruta)
                    nueva_ruta.append(nombre_vecino)
                    line.append((coste + coste_mov, turno + 1,
                                 nombre_vecino, nueva_ruta))

        return []

    def plan_fleet(self) -> list[Drone]:
        """
        Generates and plans routes for the entire drone fleet.

        For each drone:
        - Finds a valid route.
        - Creates a drone instance.
        - Reserves hubs and connections used at each turn.

        Args:
            clase_dron (Type[Base]): Class used to instantiate
                drone objects.

        Returns:
            list[Drone]: List of drones with assigned routes.
        """
        flota_drones: list[Drone] = []

        for id_dron in range(self.map.getNbDrones()):
            ruta_dron = self.search_route_for_dron()

            if not ruta_dron:
                print(f"ERROR:Imposible find path for Dron {id_dron}")
                break

            nuevo_dron = Drone(id_dron, ruta_dron)
            flota_drones.append(nuevo_dron)

            for turno in range(len(ruta_dron)):
                hub_actual = ruta_dron[turno]
                self.reservas_hubs[(hub_actual, turno)] = \
                    self.reservas_hubs.get((hub_actual, turno), 0) + 1
                if turno > 0:
                    hub_anterior = ruta_dron[turno - 1]
                    if hub_anterior != hub_actual:
                        conn_pair: tuple[str, str] = \
                         (min(hub_anterior, hub_actual),
                          max(hub_anterior, hub_actual))
                        self.reservas_conexiones[(conn_pair, turno)] = \
                            self.reservas_conexiones.get((conn_pair, turno),
                                                         0) + 1

        return flota_drones
