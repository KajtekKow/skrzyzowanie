import math
import pygame

class Renderer:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 18)
        self.width = 1920
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.delivery_surface = self.create_car_surface((180, 180, 255))
        self.car_surface = self.create_car_surface((130, 130, 130))  
        self.bus_surface = self.create_bus_surface((200, 160, 60))   
        self.tram_surface = self.create_tram_surface((100, 200, 255))
        self.emergency_surface = self.create_car_surface((255, 255, 255))       
        self.cx = self.width // 2
        self.cy = self.height // 2
        self.buttons = {
            "pause": pygame.Rect(1500, 20, 80, 30),
            "x1":    pygame.Rect(1500, 60, 80, 30),
            "x5":    pygame.Rect(1500, 100, 80, 30),
            "x10":    pygame.Rect(1500, 140, 80, 30),
            "reset": pygame.Rect(1500, 180, 80, 30),
            "morning_peak": pygame.Rect(1500, 260, 100, 30),
            "evening_peak": pygame.Rect(1500, 300, 100, 30),
            "x20": pygame.Rect(1590, 20, 80, 30),
            "x1000": pygame.Rect(1590, 60, 80, 30),
        }
        self.paused = False
                
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
        self.draw_tram_lights(sim)
        self.draw_bus_stop_markings(sim)
        self.draw_info_panel(sim)
        self.handle_buttons(sim)
        self.draw_buttons(sim)

        for e in sim.entities:
            if hasattr(e, "x") and hasattr(e, "y"):

                if hasattr(e, "is_tram"):
                    base = self.tram_surface

                elif hasattr(e, "is_emergency"):
                    base = self.emergency_surface

                elif hasattr(e, "is_delivery"):
                    base = self.delivery_surface

                elif hasattr(e, "is_bus"):
                    base = self.bus_surface

                else:
                    base = self.car_surface

                shadow = pygame.Surface((30, 15), pygame.SRCALPHA)
                pygame.draw.rect(shadow, (0, 0, 0, 60), (0, 0, 30, 15), border_radius=4)

                rot_shadow = pygame.transform.rotate(shadow, e.angle)
                shadow_rect = rot_shadow.get_rect(center=(e.x + 2, e.y + 2))
                self.screen.blit(rot_shadow, shadow_rect.topleft)

                rotated = pygame.transform.rotate(base, e.angle)
                r = rotated.get_rect(center=(e.x, e.y))

                self.screen.blit(rotated, r.topleft)

                if hasattr(e, "is_emergency"):
                    blink = (pygame.time.get_ticks() // 200) % 2

                    light_color = (40, 120, 255) if blink == 0 else (255, 40, 40)

                    siren = pygame.Surface((14, 14), pygame.SRCALPHA)
                    pygame.draw.circle(siren, light_color, (7, 7), 5)
                    pygame.draw.circle(siren, (*light_color, 80), (7, 7), 7)

                    rot_siren = pygame.transform.rotate(siren, e.angle)
                    siren_rect = rot_siren.get_rect(center=(e.x, e.y - 10))

                    self.screen.blit(rot_siren, siren_rect.topleft)

        pygame.display.flip()
        self.clock.tick(0)

    def draw_bus_stop_markings(self, sim):
        if not hasattr(sim.intersection, "bus_stops"):
            return

        for stop in sim.intersection.bus_stops:
            x, y = stop["point"]

            lane_indexes = stop.get("lane_index", [])
            if not isinstance(lane_indexes, list):
                lane_indexes = [lane_indexes]

            main_lane = None
            for idx in lane_indexes:
                if 0 <= idx < len(sim.intersection.lanes):
                    main_lane = sim.intersection.lanes[idx]
                    break

            if main_lane is None:
                continue

            stop_len = 200   
            stop_thick = 65 
            point_gap = 12   

            if main_lane.direction == "horizontal":
                if y < self.cy:
                    rect_x = int(x - 10)
                    rect_y = int(self.cy - 200)
                else:
                    rect_x = int(x - stop_len + 10)
                    rect_y = int(self.cy + 135)

                rect = pygame.Rect(rect_x, rect_y, stop_len, stop_thick)

            else:
                if y < self.cy:
                    rect_y = int(y)
                else:
                    rect_y = int(y - stop_len - point_gap)

                rect_x = int(x - stop_thick // 2)
                rect = pygame.Rect(rect_x, rect_y, stop_thick, stop_len)

            stop_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

            pygame.draw.rect(
                stop_surface,
                (255, 210, 40, 55),
                (0, 0, rect.width, rect.height),
                border_radius=4
            )

            pygame.draw.rect(
                stop_surface,
                (255, 220, 60, 230),
                (0, 0, rect.width, rect.height),
                3,
                border_radius=4
            )

            label = self.font.render("BUS STOP", True, (255, 240, 120))
            
            if main_lane.direction == "vertical":
                label = pygame.transform.rotate(label, 90)

            label_rect = label.get_rect(center=(rect.width // 2, rect.height // 2))
            stop_surface.blit(label, label_rect)

            self.screen.blit(stop_surface, rect.topleft)

    def handle_buttons(self, sim):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if not mouse_pressed:
            return

        if self.buttons["pause"].collidepoint(mouse_pos):
            self.paused = not self.paused
            sim.time_scale = 0 if self.paused else 1.0

        elif self.buttons["x1"].collidepoint(mouse_pos):
            self.paused = False
            sim.time_scale = 1.0

        elif self.buttons["x5"].collidepoint(mouse_pos):
            self.paused = False
            sim.time_scale = 5

        elif self.buttons["x10"].collidepoint(mouse_pos):
            self.paused = False
            sim.time_scale = 10.0

        elif self.buttons["reset"].collidepoint(mouse_pos):
            sim.reset()
            self.paused = False
            sim.time_scale = 1.0    

        elif self.buttons["morning_peak"].collidepoint(mouse_pos):
            sim.time_of_day = 7.0
            sim.time_scale = 1.0
            self.paused = False

            sim.sim_time = 0

            spawn = next((s for s in sim.systems if hasattr(s, "spawn_interval")), None)
            if spawn:
                spawn.timer = 0
                spawn.spawned_total = 0
                for k in spawn.spawned_types:
                    spawn.spawned_types[k] = 0

        elif self.buttons["evening_peak"].collidepoint(mouse_pos):
            sim.time_of_day = 15.0
            sim.time_scale = 1.0
            self.paused = False

            sim.sim_time = 0

            spawn = next((s for s in sim.systems if hasattr(s, "spawn_interval")), None)
            if spawn:
                spawn.timer = 0
                spawn.spawned_total = 0
                for k in spawn.spawned_types:
                    spawn.spawned_types[k] = 0

        elif self.buttons["x20"].collidepoint(mouse_pos):
            self.paused = False
            sim.time_scale = 20.0

        elif self.buttons["x1000"].collidepoint(mouse_pos):
            self.paused = False
            sim.time_scale = 1000.0

    def draw_buttons(self, sim):
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (60, 60, 60), rect, border_radius=6)
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 2, border_radius=6)

            if name == "pause":
                label = "PLAY" if self.paused else "PAUSE"
            elif name == "morning_peak":
                label = "PEAK AM"
            elif name == "evening_peak":
                label = "PEAK PM"
            else:
                label = name.upper()

            txt = self.font.render(label, True, (255, 255, 255))
            txt_rect = txt.get_rect(center=rect.center)
            self.screen.blit(txt, txt_rect)

        speed_txt = self.font.render(f"x{sim.time_scale:.1f}", True, (255, 255, 255))
        self.screen.blit(speed_txt, (self.buttons["pause"].x, self.buttons["pause"].y - 20))  
    
    def draw_info_panel(self, sim):
        spawn_system = next((s for s in sim.systems if hasattr(s, "get_stats")), None)
        hour = int(sim.time_of_day)
        minute = int((sim.time_of_day - hour) * 60)
        time_str = f"{hour:02d}:{minute:02d}"

        if spawn_system is None:
            return  

        stats = spawn_system.get_stats()

        time_hours = sim.sim_time / 3600
        flow = spawn_system.spawned_total / max(0.001, time_hours)

        lines = [
                "Plac Jana Pawła II",
                f"Godzina: {time_str}", 
                "",
                f"Czas: {sim.sim_time:.1f} s",
                f"Pojazdy (łącznie): {spawn_system.spawned_total}",
                f"Natężenie: {flow:.0f} poj/h",
                "",
                "Struktura:",
                f"Car: {stats['car']:.1f}% ",
                f"Delivery: {stats['delivery']:.1f}% ",
                f"Bus: {stats['bus']:.1f}% ",
                f"Tram: {stats['tram']:.1f}% ",
            ]

        padding = 10
        line_h = 20
        width = 300
        height = padding*2 + line_h*len(lines)

        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((20, 20, 20, 180))

        for i, text in enumerate(lines):
            txt = self.font.render(text, True, (230, 230, 230))
            panel.blit(txt, (padding, padding + i*line_h))

        self.screen.blit(panel, (10, 10))
    
    def draw_tram_lights(self, sim):
        for light in sim.intersection.tram_lights:
            lx, ly = light.x, light.y

            pygame.draw.rect(self.screen, (20, 20, 20), (lx - 14, ly - 14, 28, 28), border_radius=4)

            state = getattr(light, "state", "STOP")

            if state == "STOP":
                pygame.draw.circle(self.screen, (200, 50, 50), (lx, ly), 6)

            elif state == "STRAIGHT":
                pygame.draw.line(self.screen, (50, 220, 100), (lx - 6, ly), (lx + 6, ly), 2)

            elif state == "RIGHT":
                pygame.draw.polygon(
                    self.screen,
                    (50, 220, 100),
                    [(lx, ly - 6), (lx + 6, ly), (lx, ly + 6)]
                )

            elif state == "LEFT":
                pygame.draw.polygon(
                    self.screen,
                    (50, 220, 100),
                    [(lx, ly - 6), (lx - 6, ly), (lx, ly + 6)]
                )

            elif state == "ALL":
                pygame.draw.circle(self.screen, (50, 220, 100), (lx, ly), 6)
                    
    def create_bus_surface(self, color):
        surf = pygame.Surface((50, 18), pygame.SRCALPHA)

        pygame.draw.rect(surf, color, (0, 0, 50, 18), border_radius=5)

        for i in range(4):
            pygame.draw.rect(surf, (180, 220, 255), (8 + i*10, 4, 8, 8), border_radius=2)

        pygame.draw.rect(surf, (240, 240, 240), (45, 4, 3, 3))
        pygame.draw.rect(surf, (240, 240, 240), (45, 11, 3, 3))

        pygame.draw.rect(surf, (200, 50, 50), (2, 4, 3, 3))
        pygame.draw.rect(surf, (200, 50, 50), (2, 11, 3, 3))

        return surf
    def create_tram_surface(self, color):
        surf = pygame.Surface((80, 20), pygame.SRCALPHA) 

        pygame.draw.rect(surf, color, (0, 0, 80, 20), border_radius=6)

        for i in range(4):
            pygame.draw.rect(surf, (180, 220, 255), (8 + i*16, 5, 10, 8), border_radius=2)

        pygame.draw.rect(surf, (240, 240, 240), (75, 5, 3, 3))
        pygame.draw.rect(surf, (240, 240, 240), (75, 12, 3, 3))

        pygame.draw.rect(surf, (200, 50, 50), (2, 5, 3, 3))
        pygame.draw.rect(surf, (200, 50, 50), (2, 12, 3, 3))

        return surf
    
    def create_car_surface(self, color):
        surf = pygame.Surface((30, 15), pygame.SRCALPHA)

        pygame.draw.rect(surf, color, (0, 0, 30, 15), border_radius=4)

        pygame.draw.rect(surf, (70, 70, 70), (6, 3, 18, 9), border_radius=3)

        pygame.draw.rect(surf, (140, 140, 150), (8, 4, 14, 7), border_radius=2)

        pygame.draw.rect(surf, (240, 240, 240), (26, 3, 2, 3), border_radius=1)
        pygame.draw.rect(surf, (240, 240, 240), (26, 9, 2, 3), border_radius=1)

        pygame.draw.rect(surf, (180, 40, 40), (2, 3, 2, 3), border_radius=1)
        pygame.draw.rect(surf, (180, 40, 40), (2, 9, 2, 3), border_radius=1)

        return surf
    
    def create_emergency_surface(self):
        surf = pygame.Surface((34, 16), pygame.SRCALPHA)

        pygame.draw.rect(surf, (245, 245, 245), (0, 0, 34, 16), border_radius=4)

        pygame.draw.rect(surf, (210, 30, 30), (14, 2, 6, 12), border_radius=1)
        pygame.draw.rect(surf, (210, 30, 30), (8, 6, 18, 4), border_radius=1)

        pygame.draw.rect(surf, (70, 70, 70), (5, 3, 8, 10), border_radius=2)
        pygame.draw.rect(surf, (70, 70, 70), (21, 3, 8, 10), border_radius=2)

        pygame.draw.rect(surf, (240, 240, 240), (30, 3, 2, 3), border_radius=1)
        pygame.draw.rect(surf, (240, 240, 240), (30, 10, 2, 3), border_radius=1)

        return surf
    
    def draw_layout(self):
        road_w = 400 
        split_w = 160 
        offset = 120 

        pygame.draw.rect(self.screen, self.C_ROAD, (0, self.cy - road_w//2, self.cx - 100, road_w))
        
        pygame.draw.rect(self.screen, self.C_ROAD, (self.cx - road_w//2, 0, road_w, self.height))

        pygame.draw.rect(self.screen, self.C_ROAD, (self.cx + 100, self.cy - 50, self.width, 100))

        pygame.draw.rect(self.screen, self.C_ROAD, (self.cx + 100, self.cy - offset - split_w//2, self.width, split_w))
        pygame.draw.rect(self.screen, self.C_ROAD, (self.cx + 100, self.cy + offset - split_w//2, self.width, split_w))

        pygame.draw.rect(self.screen, self.C_ROAD, (self.cx - road_w//2, self.cy - road_w//2, road_w + 200, road_w))
        pygame.draw.line(self.screen, self.C_ROAD, (650, 720), (800, 900), 80)
        pygame.draw.line(self.screen, self.C_ROAD, (650, 360), (800, 180), 80)
        pygame.draw.line(self.screen, self.C_ROAD, (1120, 900), (1270, 720), 80)
        pygame.draw.line(self.screen, self.C_ROAD, (1120, 180), (1270, 360), 80)

    def draw_lane_markings(self):
        for y in [self.cy - 135, self.cy - 85]: 
            for x in range(0, self.cx - 180, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x + 20, y), 1)
        for y in [self.cy + 60, self.cy + 110, self.cy + 160]: 
            for x in range(0, self.cx - 180, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x + 20, y), 1)

        for y in [self.cy - 160, self.cy - 110, self.cy - 60]:
            for x in range(self.cx + 180, self.width, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x + 20, y), 1)
        for y in [self.cy + 85, self.cy + 135]:
            for x in range(self.cx + 180, self.width, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x + 20, y), 1)

        for x in [self.cx - 120]: 
            for y in range(0, self.cy - 200, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x, y + 20), 1)
        x_in_north = self.cx + 120 
        for y in range(0, self.cy - 200, 40):
            pygame.draw.line(self.screen, self.C_LINE, (x_in_north, y), (x_in_north, y + 20), 1)

        x_in_south = self.cx - 120
        for y in range(self.cy + 200, self.height, 40):
            pygame.draw.line(self.screen, self.C_LINE, (x_in_south, y), (x_in_south, y + 20), 1)

        for x in [self.cx + 90, self.cx + 140]:
            for y in range(self.cy + 200, self.height, 40):
                pygame.draw.line(self.screen, self.C_LINE, (x, y), (x, y + 20), 1)

    def draw_tracks(self):
        t_bg_w = 50

        pygame.draw.rect(self.screen, (50, 50, 50), (0, self.cy - t_bg_w//2, self.width, t_bg_w))
        pygame.draw.rect(self.screen, (50, 50, 50), (self.cx - t_bg_w//2, 0, t_bg_w, self.height))

       
        pygame.draw.line(self.screen, self.C_TRACK, (0, self.cy - 12), (self.width, self.cy - 12), 3)
        pygame.draw.line(self.screen, self.C_TRACK, (0, self.cy + 12), (self.width, self.cy + 12), 3)
        pygame.draw.line(self.screen, self.C_TRACK, (self.cx - 12, 0), (self.cx - 12, self.height), 3)
        pygame.draw.line(self.screen, self.C_TRACK, (self.cx + 12, 0), (self.cx + 12, self.height), 3)

        pygame.draw.arc(self.screen, self.C_TRACK, (self.cx - 285, self.cy + 12, 275, 275), 0, 0.5 * math.pi, 3)
        pygame.draw.arc(self.screen, self.C_TRACK, (self.cx - 262, self.cy - 12, 275, 275), 0, 0.5 * math.pi, 3)

    def draw_traffic_lights(self, sim):
        drawn_lights = set()
        pygame.draw.line(self.screen, (255, 255, 255), (760, 738), (760, 565), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (1160, 515), (1160, 342), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (760, 338), (933, 338), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (1160, 738), (987, 738), 2)
        pygame.draw.line(self.screen, (255,255,255), (695, 820), (745, 790), 2)
        pygame.draw.line(self.screen, (255,255,255), (695, 260), (745, 290), 2)
        pygame.draw.line(self.screen, (255,255,255), (1175, 790), (1225, 820), 2)            
        pygame.draw.line(self.screen, (255,255,255), (1175, 290), (1225, 260), 2)

        for lane in sim.intersection.lanes:
            if lane.lane_type in ["tram", "bike", "emergency"]:
                continue

            light = lane.traffic_light

            if not hasattr(light, "state"):
                continue

            if light in drawn_lights:
                continue

            drawn_lights.add(light)

            lx, ly = light.x, light.y

            horizontal = lane.direction == "horizontal"

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
                body_w, body_h = 42, 16
                draw_y = ly + shift if y1 < y2 else ly - shift
                
                pygame.draw.rect(self.screen, (25, 25, 25), 
                                (lx - body_w//2, draw_y - body_h//2, body_w, body_h), border_radius=4)
                
                w, h, gap = 10, 6, 8
                pygame.draw.rect(self.screen, red,    (lx - gap - w, draw_y - h//2, w, h), border_radius=2)
                pygame.draw.rect(self.screen, yellow, (lx - w//2,     draw_y - h//2, w, h), border_radius=2)
                pygame.draw.rect(self.screen, green,  (lx + gap,      draw_y - h//2, w, h), border_radius=2)

            
