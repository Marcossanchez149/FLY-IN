from model.Hub import Hub
from model.Connection import Connection
from .Validator import Validator
from model.Map import Map
from typing import Any


class Parser:
    """
    Parses a network configuration file and converts its content into
    Hub, Connection, and Map objects.

    This class provides helper methods to parse hub and connection
    definitions from strings, as well as a main parser method to read
    and validate an entire configuration file.
    """

    def convertHub(self, toconvert: str) -> Hub:
        """
        Convert a string representation of a hub into a Hub object.

        Expected format:
            "<name> <posx> <posy> [key=value ...]"

        Supported optional attributes:
            - color
            - zone
            - max_drones

        Args:
            toconvert (str):
                String containing the hub definition.

        Returns:
            Hub:
                A Hub instance created from the parsed data.
        """
        toconvert = toconvert.strip()
        parts = toconvert.split(" ", 3)
        name = parts[0]
        posx = int(parts[1])
        posy = int(parts[2])
        kwargs: dict[str, Any] = {}

        if len(parts) == 4:
            variables_str = parts[3].strip()
            if variables_str.startswith("[") and variables_str.endswith("]"):
                variables_str = variables_str[1:-1]

            variables_list = variables_str.split()
            for var in variables_list:
                key, value = var.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key == "color":
                    kwargs["color"] = value
                elif key == "zone":
                    kwargs["zone"] = value
                elif key == "max_drones":
                    kwargs["max_drones"] = int(value)
        return Hub(name, posx, posy, **kwargs)

    def convertConnection(self, toconvert: str) -> Connection:
        """
        Convert a string representation of a connection into
        a Connection object.

        Expected format:
            "<hub1>-<hub2> [key=value ...]"

        Supported optional attributes:
            - max_link_capacity

        Args:
            toconvert (str):
                String containing the connection definition.

        Returns:
            Connection:
                A Connection instance created from the parsed data.
        """
        toconvert = toconvert.strip()
        parts = toconvert.split(" ", 1)
        nombres_hubs = parts[0]
        hub1, hub2 = nombres_hubs.split("-", 1)
        kwargs = {}

        if len(parts) == 2:
            variables_str = parts[1].strip()
            if variables_str.startswith("[") and variables_str.endswith("]"):
                variables_str = variables_str[1:-1]
            variables_list = variables_str.split()
            for var in variables_list:
                key, value = var.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key == "max_link_capacity":
                    kwargs["max_link_capacity"] = int(value)
        return Connection(hub1, hub2, **kwargs)

    def parse(self, path: str) -> Map:
        """
        Parse a configuration file and build a validated network map.

        The parser processes the file line by line, ignoring empty lines
        and comments. Each valid line must follow the format:

            <key>: <value>

        Supported keys:
            - nb_drones
            - start_hub
            - end_hub
            - hub
            - connection

        Validation is delegated to the Validator class.

        Args:
            path (str):
                Path to the configuration file.

        Returns:
            Map:
                A validated Map object representing the network.

        Raises:
            ValueError:
                If a line contains invalid syntax or an unknown key.
        """
        validator = Validator()

        with open(path, "r") as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if ":" not in line:
                    raise ValueError(f"Line {line_num}: Invalid "
                                     f"syntax. Missing ':'.")

                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()

                if key == "nb_drones":
                    validator.set_nb_drones(int(value), line_num)

                elif key in ["start_hub", "end_hub", "hub"]:
                    hub = self.convertHub(value)
                    validator.add_hub(hub, key, line_num)

                elif key == "connection":
                    conn = self.convertConnection(value)
                    validator.add_connection(conn, line_num)

                else:
                    raise ValueError(f"Line {line_num}: Unknown key '{key}'.")

        return validator.finalize_network()
