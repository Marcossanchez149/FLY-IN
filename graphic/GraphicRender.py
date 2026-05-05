import pygame
from typing import List
from model.Map import Map
from model.Drone import Drone


class GraphicRender:
    def __init__(
        self,
        screen_width: int = 1200,
        screen_height: int = 800,
        margin: int = 100,
        fps: int = 60
    ) -> None:

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin = margin
        self.fps = fps

        self.bg = (30, 30, 30)
        self.conn_color = (100, 100, 100)
        self.drone_color = (255, 50, 50)
        self.drone_outline = (255, 255, 255)

        self.menu_height = 100
        self.menu_bg = (15, 15, 15)
        self.menu_text = (230, 230, 230)

    def _prepare_scaling(self, mapa: Map) -> None:
        hubs = mapa.getHubs() + [mapa.getStartHub(), mapa.getEndHub()]
        xs = [hub.getPosx() for hub in hubs]
        ys = [hub.getPosy() for hub in hubs]
        self.min_x, max_x = min(xs), max(xs)
        self.min_y, max_y = min(ys), max(ys)
        rango_x = max_x - self.min_x
        rango_y = max_y - self.min_y

        espacio_usable_w = self.screen_width - (self.margin * 2)
        espacio_usable_h = self.screen_height - self.menu_height - (
            self.margin * 2)
        escala_x = espacio_usable_w / rango_x if rango_x > 0 else float('inf')
        escala_y = espacio_usable_h / rango_y if rango_y > 0 else float('inf')
        self.scale = min(escala_x, escala_y)

        if self.scale == float('inf'):
            self.scale = 80

        mapa_ancho_real = rango_x * self.scale
        mapa_alto_real = rango_y * self.scale
        self.offset_x = (espacio_usable_w - mapa_ancho_real) / 2
        self.offset_y = (espacio_usable_h - mapa_alto_real) / 2

    def _get_px_coords(self, posx: int, posy: int) -> tuple[int, int]:
        x_px = self.margin + self.offset_x + ((posx - self.min_x) * self.scale)
        y_px = self.margin + self.offset_y + ((posy - self.min_y) * self.scale)
        return (int(x_px), int(y_px))

    def draw_network(self, mapa: Map, drones: List[Drone]) -> None:
        """
        Dibuja el mapa e inicia el bucle gráfico.
        Controles:
        - ESPACIO: Avanzar 1 turno.
        - R: Reiniciar simulación (Devuelve los drones al inicio).
        - ESC: Salir.
        """
        pygame.init()
        self._prepare_scaling(mapa)
        screen = pygame.display.set_mode((self.screen_width,
                                          self.screen_height))
        pygame.display.set_caption("Drone Network Simulator - Auto-Scaled")
        clock = pygame.time.Clock()
        clock = pygame.time.Clock()
        turno_actual = 0
        todos_en_meta = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_SPACE and not todos_en_meta:
                        movimientos_del_turno = []
                        todos_en_meta = True
                        for dron in drones:
                            if not dron.hasReachedGoal():
                                todos_en_meta = False
                                se_movio = dron.move_next_step()
                                if se_movio:
                                    id = dron.getId()
                                    destino = dron.getPosition()
                                    movimientos_del_turno.append(f"D"
                                                                 f"{id}"
                                                                 f"-{destino}")
                        if movimientos_del_turno:
                            print(" ".join(movimientos_del_turno))

                        if not todos_en_meta:
                            turno_actual += 1

                        if todos_en_meta:
                            print(f"Total number of simulation turns: "
                                  f"{turno_actual}")

                    if event.key == pygame.K_r:
                        turno_actual = 0
                        todos_en_meta = False
                        for dron in drones:
                            dron.reset()

            screen.fill(self.bg)

            self._draw_connections(screen, mapa)
            self._draw_hubs(screen, mapa)
            self._draw_drones(screen, drones, mapa)
            y_menu = self.screen_height - self.menu_height
            self._draw_menu(screen, self.screen_width, y_menu,
                            turno_actual, todos_en_meta)
            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()

    def _draw_connections(self, screen: pygame.Surface, mapa: Map) -> None:
        hubs_dict = {hub.getName(): hub for hub in mapa.getHubs()}
        hubs_dict[mapa.getStartHub().getName()] = mapa.getStartHub()
        hubs_dict[mapa.getEndHub().getName()] = mapa.getEndHub()

        for conn in mapa.getConnections():
            h1 = hubs_dict.get(conn.getHub1())
            h2 = hubs_dict.get(conn.getHub2())
            if h1 and h2:
                p1 = self._get_px_coords(h1.getPosx(), h1.getPosy())
                p2 = self._get_px_coords(h2.getPosx(), h2.getPosy())
                thickness = 2 if conn.getMaxLink() == -1 else 6
                pygame.draw.line(screen, self.conn_color, p1, p2, thickness)

    def _draw_hubs(self, screen: pygame.Surface, mapa: Map) -> None:
        hubs = mapa.getHubs() + [mapa.getStartHub(), mapa.getEndHub()]

        for hub in hubs:
            px, py = self._get_px_coords(hub.getPosx(), hub.getPosy())
            radius = 15
            try:
                color = pygame.Color(hub.getColor())
            except Exception:
                color = "White"

            pygame.draw.circle(screen, color, (px, py), radius)
            pygame.draw.circle(screen, (200, 200, 200), (px, py), radius, 2)

    def _draw_drones(self, screen: pygame.Surface, drones: List[Drone],
                     mapa: Map) -> None:
        hubs_dict = {hub.getName(): hub for hub in mapa.getHubs()}
        hubs_dict[mapa.getStartHub().getName()] = mapa.getStartHub()
        hubs_dict[mapa.getEndHub().getName()] = mapa.getEndHub()

        for dron in drones:
            hub_actual = hubs_dict.get(dron.getPosition())
            if hub_actual:
                px, py = self._get_px_coords(hub_actual.getPosx(),
                                             hub_actual.getPosy())

                offset_x = (dron.getId() * 6) % 18 - 9
                offset_y = (dron.getId() * 6) % 18 - 9

                rect = pygame.Rect(px - 6 + offset_x, py - 6 + offset_y,
                                   12, 12)
                pygame.draw.rect(screen, self.drone_color, rect)
                pygame.draw.rect(screen, self.drone_outline, rect, 1)

    def _draw_menu(self, screen: pygame.Surface, width: int, y_offset: int,
                   turno: int, finalizado: bool) -> None:
        menu_rect = pygame.Rect(0, y_offset, width, self.menu_height)
        pygame.draw.rect(screen, self.menu_bg, menu_rect)
        pygame.draw.line(screen, (100, 100, 100), (0, y_offset),
                         (width, y_offset), 3)

        font = pygame.font.SysFont(None, 26)

        text_controls = font.render("ESPACIO: Avanzar Turno   "
                                    "|   R: Reiniciar   |   ESC: Salir",
                                    True, self.menu_text)
        screen.blit(text_controls, (20, y_offset + 20))

        if finalizado:
            estado = f"¡TODOS LOS DRONES HAN LLEGADO! Total de turnos: {turno}"
        else:
            estado = f"Turno Actual: {turno}"
        color_estado = (0, 255, 0) if finalizado else (255, 255, 0)
        text_turno = font.render(estado, True, color_estado)
        screen.blit(text_turno, (20, y_offset + 55))
