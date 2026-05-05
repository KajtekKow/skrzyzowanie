from infrastructure.lane import Lane
from infrastructure.traffic_light import TrafficLight
import numpy as np

class Intersection:
    def __init__(self):

        # --- ŚWIATŁA (pozycje mniej więcej na środku skrzyżowania) ---
        self.lights = [
            TrafficLight(1160, 450),  #prosto ruska -> legnicka
            TrafficLight(1160, 400),  #prosto ruska -> legnicka
            TrafficLight(1160, 350),  # prawo ruska -> podwale 338 738
            TrafficLight(1160, 500), # lewo ruska -> podwale
            TrafficLight(760, 575), # lewo legnicka -> podwale
            TrafficLight(760, 620), # prosto legnicka -> ruska
            TrafficLight(760, 670), # prosto legnicka -> ruska
            TrafficLight(760, 720), # prawo legnicka -> podwale
            TrafficLight(1010, 738),
            TrafficLight(1055, 738),
            TrafficLight(1100, 738),
            TrafficLight(1145, 738),
            TrafficLight(780, 338),
            TrafficLight(840, 338),
            TrafficLight(900, 338)
        ]

        # --- PASY ---
        self.lanes = [
            Lane(
                [(1920, 450), (960, 450),(900, 470), (0, 480)], #prosto ruska -> legnicka
                self.lights[0],
                "horizontal"
            ),

            Lane(
                [(1920, 400), (960, 400), (900, 420), (0, 430)], #prosto ruska -> legnicka
                self.lights[1],
                "horizontal"
            ),

            Lane(
                [(1920, 350), (1100, 350), (1100, 0)], # prawo ruska -> podwale (prawy pas)
                self.lights[2],
                "horizontal"
            ),

            Lane(
                [(1920, 500), (1100, 500), (1000, 550),(900, 650), (810, 720), (810, 1080)], # lewo ruska -> podwale (prawy pas)
                self.lights[3],
                "horizontal"
            ),

            Lane(
                [(1920, 500), (1100, 500), (1000, 550),(900, 650), (860, 720), (860, 1080)], # lewo ruska -> podwale (lewy pas)
                self.lights[3],
                "horizontal"
            ),

            Lane(
                [(0, 575), (760, 575), (1100, 350), (1100, 0)], # lewo legnicka -> podwale (prawy pas)
                self.lights[4],
                "horizontal"
            ),

            Lane(
                [(0, 620),(760, 620), (1000, 615), (1100, 600), (1920, 600)], # prosto legnicka -> ruska
                self.lights[5],
                "horizontal"
            ),

            Lane(
                [(0, 670),(760, 670), (1000, 650), (1100, 640), (1920, 640)], # prosto legnicka -> ruska
                self.lights[6],
                "horizontal"
            ),

            Lane(
                [(0, 720), (760, 720), (810, 720), (810, 1080)], # prawo legnicka -> podwale
                self.lights[7],
                "horizontal"
            ),

            Lane(
                [(1010, 1080), (1010, 738), (800, 480), (0, 480)], # lewo podwale -> legnicka (lewy pas)
                self.lights[8],
                "vertical"
            ),

            Lane(
                [(1055, 1080), (1055, 738), (900, 450), (700, 430), (0, 430)], # lewo podwale -> legnicka (prawy pas)
                self.lights[9],
                "vertical"
            ),

            Lane(
                [(1055, 1080), (1055, 738), (1040, 580),(1040, 0)], # prosto podwale -> podwale (lewy pas)
                self.lights[9],
                "vertical"
            ),

            Lane(
                [(1100, 1080), (1100, 738), (1100, 640), (1100, 0)], # prosto podwale -> podwale (prawy pas)
                self.lights[10],
                "vertical"
            ),

            Lane(
                [(1145, 1080), (1145, 738), (1200, 640), (1920, 640)], # prawo podwale -> ruska 
                self.lights[11],
                "vertical"
            ),

            Lane(
                [(780, 0), (780, 338), (780, 380), (700, 400), (650, 430), (0, 430)], # prawo podwale -> legnicka
                self.lights[12],
                "vertical"
            ),

            Lane(
                [(840, 0), (840, 338), (810, 700), (810, 1080)], # prosto podwale -> podwale (prawy pas)
                self.lights[13],
                "vertical"
            ),

            Lane(
                [(900, 0), (900, 338), (860, 700), (860, 1080)], # prosto podwale -> podwale (lewy pas)
                self.lights[14],
                "vertical"
            )
        ]

            # → z lewej do prawej (dolna droga)
            # Lane((0, 410), self.lights[3], (720, 410), (1440, 410), "horizontal"),
            # Lane((0, 440), self.lights[4], (720, 440), (1440, 440), "horizontal"),
            # Lane((0, 480), self.lights[5], (720, 480), (1440, 480), "horizontal"),

            # ↓ z góry w dół
            # Lane((590, 720), self.lights[6], (590, 360), (590, 0), "vertical"),
        
        self.phases = [
            [0, 1, 2, 5, 6, 7],        # poziome prosto
            [3, 4],      # skręty
            [8, 9, 10 , 11],
            [12, 13, 14]
        ]

        self.current_phase = 0
        self.phase_timer = 0

        self.green_time = 6
        self.yellow_time = 3.5

        
        self.lanes[3].neighbors.append(self.lanes[4])
        self.lanes[4].neighbors.append(self.lanes[3])
        self.lanes[10].neighbors.append(self.lanes[11])
        self.lanes[11].neighbors.append(self.lanes[10])

    def update_lights(self, dt):
        self.phase_timer += dt

        phase = self.phases[self.current_phase]

        # RESET wszystkich
        for i, light in enumerate(self.lights):
            if i in phase:
                if self.phase_timer < self.green_time:
                    light.state = "GREEN"
                elif self.phase_timer < self.green_time + self.yellow_time:
                    light.state = "YELLOW"
                else:
                    light.state = "RED"
            else:
                light.state = "RED"

        # zmiana fazy
        if self.phase_timer > self.green_time + self.yellow_time:
            self.phase_timer = 0
            self.current_phase = (self.current_phase + 1) % len(self.phases)
        
        