#!/usr/bin/env python3
import sys
from config import Parser
from model import Drone
from algorithms import Pathfinder
from graphic.GraphicRender import GraphicRender


def main():
    print("Fly-in")
    try:
        if not (len(sys.argv) > 1):
            print("Invalid arguments, example -> "
                  "python3 fly_in.py map.txt")
            return

        parser = Parser()
        mapa = parser.parse(sys.argv[1])

        print("Calculando rutas...")
        pathfinder = Pathfinder(mapa)
        flota_drones = pathfinder.planificar_flota(Drone)

        print("Iniciando entorno gráfico...")
        renderer = GraphicRender()
        renderer.draw_network(mapa, flota_drones)
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
