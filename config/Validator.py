from typing import Optional
from model import Hub, Connection
from model.Map import Map


class Validator:
    """
    Validates hubs, connections, and global network settings while
    constructing a Map object.

    This class ensures that:
        - Required fields are defined exactly once.
        - Hub and connection definitions are valid.
        - Duplicate hubs and connections are rejected.
        - Connections only reference existing hubs.
        - Network constraints are respected before creating the final map.
    """

    def __init__(self) -> None:
        """
        Initialize the validator with empty network data structures.

        Attributes:
            nb_drones (Optional[int]):
                Total number of drones in the network.

            start_hub (Optional[Hub]):
                The designated starting hub.

            end_hub (Optional[Hub]):
                The designated ending hub.

            hubs_dict (dict[str, Hub]):
                Dictionary mapping hub names to Hub objects.

            connections (list[Connection]):
                List of all validated connections.

            seen_connections (set[tuple[str, str]]):
                Set used to detect duplicate connections.

            Valid_zones (set[str]):
                Allowed zone types for hubs.
        """
        self.nb_drones: Optional[int] = None
        self.start_hub: Optional[Hub] = None
        self.end_hub: Optional[Hub] = None
        self.hubs_dict: dict[str, Hub] = {}
        self.connections: list[Connection] = []
        self.seen_connections: set[tuple[str, str]] = set()
        self.Valid_zones = {"normal", "blocked", "restricted", "priority"}

    def set_nb_drones(self, value: int, line_num: int) -> None:
        """
        Validate and set the number of drones.

        Ensures that:
            - 'nb_drones' is defined only once.
            - The value is a positive integer.

        Args:
            value (int):
                Number of drones.

            line_num (int):
                Line number in the configuration file for error reporting.

        Raises:
            ValueError:
                If 'nb_drones' is duplicated or invalid.
        """
        if self.nb_drones is not None:
            raise ValueError(f"Line {line_num}: 'nb_drones' defined "
                             f"multiple times.")
        if value <= 0:
            raise ValueError(f"Line {line_num}: 'nb_drones' must be "
                             f"a positive integer.")
        self.nb_drones = value

    def add_hub(self, hub: Hub, hub_type: str, line_num: int) -> None:
        """
        Validate and add a hub to the network.

        Validation rules:
            - Hub names cannot contain spaces or dashes.
            - Zone types must be valid.
            - max_drones must be positive if specified.
            - Hub names must be unique.
            - Only one start_hub and one end_hub are allowed.

        Args:
            hub (Hub):
                The hub object to validate and add.

            hub_type (str):
                Type of hub definition:
                    - "hub"
                    - "start_hub"
                    - "end_hub"

            line_num (int):
                Line number in the configuration file for error reporting.

        Raises:
            ValueError:
                If any validation rule is violated.
        """
        if "-" in hub.getName() or " " in hub.getName():
            raise ValueError(f"Line {line_num}: Invalid zone "
                             f"name '{hub.getName()}'. Dashes and spaces "
                             f"are not allowed.")
        if hub.getZone().lower() not in self.Valid_zones:
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
        """
        Validate and add a connection between two hubs.

        Validation rules:
            - max_link_capacity must be positive if specified.
            - Both hubs in the connection must already exist.
            - Duplicate connections are not allowed.

        Args:
            conn (Connection):
                The connection object to validate and add.

            line_num (int):
                Line number in the configuration file for error reporting.

        Raises:
            ValueError:
                If the connection is invalid or duplicated.
        """
        if conn.getMaxLink() != -1 and conn.getMaxLink() <= 0:
            raise ValueError(f"Line {line_num}: max_link_capacity"
                             f" must be a positive integer.")

        h1 = str(conn.getHub1())
        h2 = str(conn.getHub2())

        if h1 not in self.hubs_dict:
            raise ValueError(f"Line {line_num}: Connection links "
                             f"undefined zone '{h1}'.")
        if h2 not in self.hubs_dict:
            raise ValueError(f"Line {line_num}: Connection links "
                             f"undefined zone '{h2}'.")

        conn_pair: tuple[str, str] = (min(h1, h2), max(h1, h2))

        if conn_pair in self.seen_connections:
            raise ValueError(f"Line {line_num}: Duplicate connection "
                             f"between '{h1}' and '{h2}'.")

        self.seen_connections.add(conn_pair)
        self.connections.append(conn)

    def finalize_network(self) -> Map:
        """
        Finalize validation and create the network map.

        Ensures that:
            - nb_drones is defined.
            - Exactly one start_hub exists.
            - Exactly one end_hub exists.

        Returns:
            Map:
                A fully validated Map object containing all hubs
                and connections.

        Raises:
            ValueError:
                If required network components are missing.
        """
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
