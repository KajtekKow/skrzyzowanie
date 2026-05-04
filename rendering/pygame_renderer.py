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

        center_x = self.width // 2
        center_y = self.height // 2

        lane_width = 35
        lanes = 5
        road_half = lane_width * lanes + 20

        # # === DROGA POZIOMA ===
        # pygame.draw.rect(
        #     self.screen,
        #     (50, 50, 50),
        #     (0, center_y - road_half, self.width, road_half * 2)
        # )

        # # === DROGA PIONOWA ===
        # pygame.draw.rect(
        #     self.screen,
        #     (50, 50, 50),
        #     (center_x - road_half, 0, road_half * 2, self.height)
        # )

        # === LINIE PASÓW (POZIOME) ===
        for i in range(1, lanes):
            offset = i * lane_width

            # góra
            y = center_y - offset
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (self.width, y), 1)

            # dół
            y = center_y + offset
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (self.width, y), 1)

        # === LINIE PASÓW (PIONOWE) ===
        for i in range(1, lanes):
            offset = i * lane_width

            # lewo
            x = center_x - offset
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, self.height), 1)

            # prawo
            x = center_x + offset
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, self.height), 1)

        # === POJAZDY ===
        for e in sim.entities:
            if hasattr(e, "length"):

                # poziome auto
                if e.direction == 0:
                    width = e.length * 5
                    height = 10

                # pionowe auto
                else:
                    width = 10
                    height = e.length * 5

                pygame.draw.rect(
                    self.screen,
                    (0, 200, 0),
                    (e.x, e.y, width, height)
                )
                
        # === TRAFFIC LIGHTS ===
        for light in sim.traffic_lights:
            if light.state == "GREEN":
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)

            pygame.draw.circle(
                self.screen,
                color,
                (int(light.x), int(light.y)),
                10
            )
        pygame.display.flip()
        self.clock.tick(60)