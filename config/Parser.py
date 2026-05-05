from model.Hub import Hub
from model.Connection import Connection
from .Validator import Validator
from model.Map import Map


class Parser:

    def convertHub(self, toconvert: str) -> Hub:
        toconvert = toconvert.strip()
        parts = toconvert.split(" ", 3)
        name = parts[0]
        posx = int(parts[1])
        posy = int(parts[2])
        kwargs = {}

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
