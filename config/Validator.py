from model import Hub, Connection
from model.Map import Map


class Validator:

    def __init__(self):
        self.nb_drones = None
        self.start_hub = None
        self.end_hub = None
        self.hubs_dict = {}
        self.connections = []
        self.seen_connections = set()

    VALID_ZONES = {"normal", "blocked", "restricted", "priority"}

    def set_nb_drones(self, value: int, line_num: int) -> None:
        if self.nb_drones is not None:
            raise ValueError(f"Line {line_num}: 'nb_drones' defined "
                             f"multiple times.")
        if value <= 0:
            raise ValueError(f"Line {line_num}: 'nb_drones' must be "
                             f"a positive integer.")
        self.nb_drones = value

    def add_hub(self, hub: Hub, hub_type: str, line_num: int) -> None:
        if "-" in hub.getName() or " " in hub.getName():
            raise ValueError(f"Line {line_num}: Invalid zone "
                             f"name '{hub.getName()}'. Dashes and spaces "
                             f"are not allowed.")
        if hub.getZone().lower() not in self.VALID_ZONES:
            raise ValueError(f"Line {line_num}: Invalid zone "
                             f"type '{hub.getZone()}'.")
        if hub.getMaxDrones() != -1 and hub.getMaxDrones() <= 0:
            raise ValueError(f"Line {line_num}: max_drones must be"
                             f" a positive integer.")

        if hub.getName() in self.hubs_dict:
            raise ValueError(f"Line {line_num}: Duplicate "
                             f"zone name '{hub.getName()}'.")

        if hub_type == "start_hub":
            if self.start_hub is not None:
                raise ValueError(f"Line {line_num}: "
                                 f"Multiple start_hubs defined.")
            self.start_hub = hub
        elif hub_type == "end_hub":
            if self.end_hub is not None:
                raise ValueError(f"Line {line_num}: Multiple "
                                 f"end_hubs defined.")
            self.end_hub = hub

        self.hubs_dict[hub.getName()] = hub

    def add_connection(self, conn: Connection, line_num: int) -> None:
        if conn.getMaxLink() != -1 and conn.getMaxLink() <= 0:
            raise ValueError(f"Line {line_num}: max_link_capacity"
                             f" must be a positive integer.")

        if conn.getHub1() not in self.hubs_dict:
            raise ValueError(f"Line {line_num}: Connection links"
                             f"undefined zone '{conn.getHub1()}'.")
        if conn.getHub2() not in self.hubs_dict:
            raise ValueError(f"Line {line_num}: Connection links"
                             f" undefined zone '{conn.getHub2()}'.")

        conn_pair = tuple(sorted([conn.getHub1(), conn.getHub2()]))
        if conn_pair in self.seen_connections:
            raise ValueError(f"Line {line_num}: Duplicate connection"
                             f" between '{conn.getHub1()}' "
                             f"and '{conn.getHub2()}'.")

        self.seen_connections.add(conn_pair)
        self.connections.append(conn)

    def finalize_network(self) -> dict:
        if self.nb_drones is None:
            raise ValueError("File Error: 'nb_drones' was never defined.")
        if self.start_hub is None:
            raise ValueError("File Error: Expected exactly 1 "
                             "start_hub, found 0.")
        if self.end_hub is None:
            raise ValueError("File Error: Expected exactly "
                             "1 end_hub, found 0.")

        return Map(self.nb_drones, self.start_hub, self.end_hub,
                   list(self.hubs_dict.values()), self.connections)
