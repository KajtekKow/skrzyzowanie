import pygame

class Renderer:
    def __init__(self):
        pygame.init()
        self.width = 1440
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.clock = pygame.time.Clock()

    def draw(self, sim):
        self.screen.fill((30, 30, 30))
        # === PARAMETRY ===
        center_y = self.height // 2
        lane_width = 35
        lanes = 2

        road_half = lane_width * lanes + 30

        # === ASFALT ===
        pygame.draw.rect(
            self.screen,
            (50, 50, 50),
            (0, center_y - road_half, self.width, road_half * 2)
        )

        # === TOR TRAMWAJOWY (środek) ===
        track_offset = 10

        pygame.draw.line(
            self.screen,
            (180, 180, 180),
            (0, center_y - track_offset),
            (self.width, center_y - track_offset),
            3
        )

        pygame.draw.line(
            self.screen,
            (180, 180, 180),
            (0, center_y + track_offset),
            (self.width, center_y + track_offset),
            3
        )

        # === LINIA ŚRODKOWA (przerywana) ===
        for x in range(0, self.width, 40):
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (x, center_y),
                (x + 20, center_y),
                2
            )

        # === PASY (przerywane) ===
        for i in range(1, lanes):
            offset = i * lane_width

            # góra
            y = center_y - offset
            for x in range(0, self.width, 40):
                pygame.draw.line(self.screen, (200, 200, 200), (x, y), (x + 20, y), 1)

            # dół
            y = center_y + offset
            for x in range(0, self.width, 40):
                pygame.draw.line(self.screen, (200, 200, 200), (x, y), (x + 20, y), 1)

        # === LINIE KRAWĘDZI DROGI ===
        pygame.draw.line(self.screen, (255, 255, 255),
                        (0, center_y - road_half), (self.width, center_y - road_half), 2)

        pygame.draw.line(self.screen, (255, 255, 255),
                        (0, center_y + road_half), (self.width, center_y + road_half), 2)

        for e in sim.entities:
            # POJAZDY (mają length)
            if hasattr(e, "length"):
                pygame.draw.rect(
                    self.screen,
                    (0, 200, 0),
                    (e.x, e.y, e.length * 5, 10)
                )

            # PIESI (nie mają length)
            else:
                pygame.draw.circle(
                    self.screen,
                    (255, 255, 0),
                    (int(e.x), int(e.y)),
                    5
                )
        # rysuj światło
        color = (0, 255, 0) if sim.systems[0].traffic_light.state == "GREEN" else (255, 0, 0)

        pygame.draw.circle(self.screen, color, (50, 50), 15)
        
        pygame.draw.line(self.screen, (255, 255, 255), (720, 0), (720, self.height), 2)

        pygame.display.flip()
        self.clock.tick(60)