#!/usr/bin/env python3
import sys
from config import Parser
from algorithms import Pathfinder
from graphic.GraphicRender import GraphicRender


def main() -> None:
    """
    Main entry point of the Fly-in drone network simulator.

    This function:
        - Validates command-line arguments.
        - Parses the map configuration file.
        - Computes drone paths using the Pathfinder.
        - Launches the graphical simulation if the map is valid.

    Workflow:
        1. Read the map file path from command-line arguments.
        2. Parse and validate the map configuration.
        3. Generate drone routes.
        4. Start the graphical renderer.

    Raises:
        Exception:
            Any unexpected exception is caught and displayed
            to the user.
    """
    print("Fly-in")
    try:
        if not (len(sys.argv) > 1):
            print("Invalid arguments, example -> "
                  "python3 fly_in.py map.txt")
            return

        parser = Parser()
        mapa = parser.parse(sys.argv[1])

        print("Calculating paths...")
        pathfinder = Pathfinder(mapa)
        flota_drones = pathfinder.plan_fleet()
        if (not flota_drones):
            print("The map is not valid")
        else:
            print("Iniciating graphic...")
            renderer = GraphicRender()
            renderer.draw_network(mapa, flota_drones)
    except Exception as e:
        print(f"Exception: {e}")
    return


if __name__ == "__main__":
    main()
