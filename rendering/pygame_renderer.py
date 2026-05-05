import pygame

class Renderer:
    def __init__(self):
        pygame.init()
        self.width = 1920
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.car_surface = self.create_car_surface((130, 130, 130))  # szare auto
        self.bus_surface = self.create_car_surface((200, 160, 60))   # bus

        self.cx = self.width // 2
        self.cy = self.height // 2
        
        # Kolory
        self.C_ROAD = (40, 40, 42)
        self.C_TRACK = (0, 110, 220)
        self.C_BG = (15, 20, 15)
        self.C_LINE = (200, 200, 200)

    def draw(self, sim):
        self.screen.fill(self.C_BG)

        self.draw_layout()
        self.draw_lane_markings()
        self.draw_tracks()
        self.draw_traffic_lights(sim)

        # Auta (Twoje dane)
        for e in sim.entities:
            if hasattr(e, "x") and hasattr(e, "y"):

                base = self.bus_surface if hasattr(e, 'is_bus') else self.car_surface

                # cień (opcjonalnie, ale polecam)
                shadow = pygame.Surface((30, 15), pygame.SRCALPHA)
                pygame.draw.rect(shadow, (0, 0, 0, 60), (0, 0, 30, 15), border_radius=4)

                rot_shadow = pygame.transform.rotate(shadow, e.angle)
                shadow_rect = rot_shadow.get_rect(center=(e.x + 2, e.y + 2))
                self.screen.blit(rot_shadow, shadow_rect.topleft)

                # auto
                rotated = pygame.transform.rotate(base, e.angle)
                r = rotated.get_rect(center=(e.x, e.y))

                self.screen.blit(rotated, r.topleft)
        pygame.display.flip()
        self.clock.tick(60)

    def create_car_surface(self, color):
        surf = pygame.Surface((30, 15), pygame.SRCALPHA)

        # karoseria
        pygame.draw.rect(surf, color, (0, 0, 30, 15), border_radius=4)

        # dach (ciemny szary)
        pygame.draw.rect(surf, (70, 70, 70), (6, 3, 18, 9), border_radius=3)

        # szyby
        pygame.draw.rect(surf, (140, 140, 150), (8, 4, 14, 7), border_radius=2)

        # ===== PRZÓD (białe światła) =====
        pygame.draw.rect(surf, (240, 240, 240), (26, 3, 2, 3), border_radius=1)
        pygame.draw.rect(surf, (240, 240, 240), (26, 9, 2, 3), border_radius=1)

        # ===== TYŁ (czerwone światła) =====
        pygame.draw.rect(surf, (180, 40, 40), (2, 3, 2, 3), border_radius=1)
        pygame.draw.rect(surf, (180, 40, 40), (2, 9, 2, 3), border_radius=1)

        return surf
    
    def draw_layout(self):
        road_w = 400 
        split_w = 160 
        offset = 120 

        # 1. Zachód (Legnicka)
        pygame.draw.rect(self.screen, self.C_ROAD, (0, self.cy - road_w//2, self.cx - 100, road_w))
        
        # 2. Pion (Podwale)
        pygame.draw.rect(self.screen, self.C_ROAD, (self.cx - road_w//2, 0, road_w, self.height))
        
        # 3. WSCHÓD - DODANA DROGA POD TORAMI (Łącznik)
        # To wypełnia lukę, o którą prosiłeś w image_47138b.png
        pygame.draw.rect(self.screen, self.C_ROAD, (self.cx + 100, self.cy - 50, self.width, 100))
        
        # 4. Wschód (Ruska/Mikołaja) - dwie zewnętrzne nitki
        pygame.draw.rect(self.screen, self.C_ROAD, (self.cx + 100, self.cy - offset - split_w//2, self.width, split_w))
        pygame.draw.rect(self.screen, self.C_ROAD, (self.cx + 100, self.cy + offset - split_w//2, self.width, split_w))
        
        # 5. Środek skrzyżowania
        pygame.draw.rect(self.screen, self.C_ROAD, (self.cx - road_w//2, self.cy - road_w//2, road_w + 200, road_w))

    def draw_lane_markings(self):
        # --- POZIOME (Zgodnie z ostatnią prośbą: Wloty 4 pasy, Wyloty 3 pasy) ---
        # Zachód
        for y in [self.cy - 135, self.cy - 85]: # Wylot (3 pasy)
            for x in range(0, self.cx - 180, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x + 20, y), 1)
        for y in [self.cy + 60, self.cy + 110, self.cy + 160]: # Wlot (4 pasy)
            for x in range(0, self.cx - 180, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x + 20, y), 1)

        # Wschód
        for y in [self.cy - 160, self.cy - 110, self.cy - 60]: # Wlot (4 pasy)
            for x in range(self.cx + 180, self.width, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x + 20, y), 1)
        for y in [self.cy + 85, self.cy + 135]: # Wylot (3 pasy)
            for x in range(self.cx + 180, self.width, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x + 20, y), 1)

        # --- PIONOWE (WYRÓWNANE) ---
        # Ustawiamy linie wylotowe co 40px: 80, 120, 160 od środka
        # Ustawiamy linię wlotową na 120px od środka (środkowy pas wlotu)

        # Północ (Góra)
        # Wylot (lewa strona): 3 linie
        for x in [self.cx - 150, self.cx - 90]: 
            for y in range(0, self.cy - 200, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x, y + 20), 1)
        # Wlot (prawa strona): 1 linia (na pozycji środkowej linii wylotu dla symetrii)
        x_in_north = self.cx + 120 
        for y in range(0, self.cy - 200, 40):
            pygame.draw.line(self.screen, self.C_LINE, (x_in_north, y), (x_in_north, y + 20), 1)

        # Południe (Dół)
        # Wlot (lewa strona): 1 linia
        x_in_south = self.cx - 120
        for y in range(self.cy + 200, self.height, 40):
            pygame.draw.line(self.screen, self.C_LINE, (x_in_south, y), (x_in_south, y + 20), 1)
        # Wylot (prawa strona): 3 linie
        for x in [self.cx + 80, self.cx + 120, self.cx + 160]:
            for y in range(self.cy + 200, self.height, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x, y + 20), 1)

    def draw_tracks(self):
        import math
        t_bg_w = 50
        # Przywrócone tło torów (Podkłady) - teraz leżą na drodze z punktu 3.
        pygame.draw.rect(self.screen, (50, 50, 50), (0, self.cy - t_bg_w//2, self.width, t_bg_w))
        pygame.draw.rect(self.screen, (50, 50, 50), (self.cx - t_bg_w//2, 0, t_bg_w, self.height))

        # Szyny (bez zmian)
        pygame.draw.line(self.screen, self.C_TRACK, (0, self.cy - 12), (self.width, self.cy - 12), 3)
        pygame.draw.line(self.screen, self.C_TRACK, (0, self.cy + 12), (self.width, self.cy + 12), 3)
        pygame.draw.line(self.screen, self.C_TRACK, (self.cx - 12, 0), (self.cx - 12, self.height), 3)
        pygame.draw.line(self.screen, self.C_TRACK, (self.cx + 12, 0), (self.cx + 12, self.height), 3)

        pygame.draw.arc(self.screen, self.C_TRACK, (self.cx - 285, self.cy + 12, 275, 275), 0, 0.5 * math.pi, 3)
        pygame.draw.arc(self.screen, self.C_TRACK, (self.cx - 262, self.cy - 12, 275, 275), 0, 0.5 * math.pi, 3)

    def draw_traffic_lights(self, sim):
        drawn_lights = set()

        for lane in sim.intersection.lanes:
            light = lane.traffic_light
            if light in drawn_lights:
                continue
            
            drawn_lights.add(light)
            lx, ly = light.x, light.y

            # UŻYWAMY ZMIENNEJ DIRECTION Z KLASY LANE ZAMIAST OBLICZEŃ
            horizontal = lane.direction == "horizontal"
            
            # Pobieramy punkty do ustalenia strony przesunięcia (shift)
            x1, y1 = lane.points[0]
            x2, y2 = lane.points[-1]
            
            shift = 15 

            red    = (220, 50, 50)  if light.state == "RED"    else (60, 20, 20)
            yellow = (220, 180, 50) if light.state == "YELLOW" else (60, 50, 20)
            green  = (50, 220, 100) if light.state == "GREEN"  else (20, 60, 30)

            if horizontal:
                body_w, body_h = 16, 42
                draw_x = lx + shift if x1 < x2 else lx - shift
                
                pygame.draw.rect(self.screen, (25, 25, 25), 
                                (draw_x - body_w//2, ly - body_h//2, body_w, body_h), border_radius=4)
                
                w, h, gap = 10, 6, 8
                pygame.draw.rect(self.screen, red,    (draw_x - w//2, ly - gap - h, w, h), border_radius=2)
                pygame.draw.rect(self.screen, yellow, (draw_x - w//2, ly - h//2,     w, h), border_radius=2)
                pygame.draw.rect(self.screen, green,  (draw_x - w//2, ly + gap,     w, h), border_radius=2)
            else:
                # DLA PIONOWYCH (vertical) - ZAWSZE POZIOMY BOX
                body_w, body_h = 42, 16
                draw_y = ly + shift if y1 < y2 else ly - shift
                
                pygame.draw.rect(self.screen, (25, 25, 25), 
                                (lx - body_w//2, draw_y - body_h//2, body_w, body_h), border_radius=4)
                
                w, h, gap = 10, 6, 8
                pygame.draw.rect(self.screen, red,    (lx - gap - w, draw_y - h//2, w, h), border_radius=2)
                pygame.draw.rect(self.screen, yellow, (lx - w//2,     draw_y - h//2, w, h), border_radius=2)
                pygame.draw.rect(self.screen, green,  (lx + gap,      draw_y - h//2, w, h), border_radius=2)

            pygame.draw.line(self.screen, (255, 255, 255), (760, 738), (760, 565), 2)
            pygame.draw.line(self.screen, (255, 255, 255), (1160, 515), (1160, 342), 2)
            pygame.draw.line(self.screen, (255, 255, 255), (760, 338), (933, 338), 2)
            pygame.draw.line(self.screen, (255, 255, 255), (1160, 738), (987, 738), 2)