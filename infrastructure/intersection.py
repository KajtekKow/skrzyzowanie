from infrastructure.lane import Lane
from infrastructure.traffic_light import TrafficLight
from infrastructure.tram_light import TramLight

class Intersection:
    def __init__(self):

        self.lights = [
            TrafficLight(1160, 450), # ruska -> legnicka prosto
            TrafficLight(1160, 400), # ruska -> legnicka prosto
            TrafficLight(1160, 350), # ruska -> podwale prawo
            TrafficLight(1160, 500), # ruska -> podwale lewo
            TrafficLight(760, 580), # legnicka -> podwale lewo
            TrafficLight(760, 620), # legnicka -> ruska prosto
            TrafficLight(760, 670), # legnicka -> ruska prosto
            TrafficLight(760, 720), # legnicka -> podwale prawo
            TrafficLight(1010, 738), # podawle -> legnicka lewo
            TrafficLight(1055, 738), # podwale -> legnicka lewo/podwale prosto
            TrafficLight(1100, 738), # podwale -> podwale prosto
            TrafficLight(1145, 738), # podwale -> ruska prawo
            TrafficLight(780, 338), # podwale -> legnicka prawo
            TrafficLight(840, 338), # podwale -> podwale prosto
            TrafficLight(900, 338) #podwale -> podwale prosto
        ]

        self.tram_lights = [
            TramLight(760, 552),   
            TramLight(948, 338),    
            TramLight(972, 738),
            TramLight(1160, 528)
        ]

        self.lanes = [
            Lane([(1920, 450), (960, 450),(900, 470), (0, 480)], self.lights[0], "horizontal"), 
            Lane([(1920, 400), (960, 400), (900, 420), (0, 430)], self.lights[1], "horizontal"),
            Lane([(1920, 350), (1100, 350), (1100, 0)], self.lights[2], "horizontal"),
            Lane([(1920, 500), (1100, 500), (1000, 550),(900, 650), (810, 720), (810, 1080)], self.lights[3], "horizontal", lane_type="MIXED"), #busy moge 3
            Lane([(1920, 500), (1100, 500), (1000, 550),(900, 650), (860, 720), (860, 1080)], self.lights[3], "horizontal"),
            Lane([(0, 580), (760, 580), (1100, 350), (1100, 0)], self.lights[4], "horizontal"),
            Lane([(0, 620),(760, 620), (1000, 615), (1100, 600), (1920, 600)], self.lights[5], "horizontal"),
            Lane([(0, 670),(760, 670), (1000, 650), (1100, 640), (1920, 640)], self.lights[6], "horizontal"),
            Lane([(0, 720), (760, 720), (810, 720), (810, 1080)], self.lights[7], "horizontal"),
            Lane([(1010, 1080), (1010, 738), (1010, 600), (960, 540), (900, 480), (0, 480)], self.lights[8], "vertical"),
            Lane([(1055, 1080), (1055, 738), (1055, 480), (900, 450), (700, 430), (0, 430)], self.lights[9], "vertical"),
            Lane([(1055, 1080), (1055, 738), (1040, 580),(1040, 0)], self.lights[9], "vertical"),
            Lane([(1100, 1080), (1100, 738), (1100, 640), (1100, 0)], self.lights[10], "vertical", lane_type="MIXED"), # busy moga 12
            Lane([(1145, 1080), (1145, 738), (1200, 640), (1920, 640)], self.lights[11], "vertical"),
            Lane([(780, 0), (780, 338), (780, 380), (700, 400), (650, 430), (0, 430)], self.lights[12], "vertical"),
            Lane([(840, 0), (840, 338), (810, 700), (810, 1080)], self.lights[13], "vertical", lane_type="MIXED"), # busy moga 15
            Lane([(900, 0), (900, 338), (860, 700), (860, 1080)], self.lights[14], "vertical"),
        ]

        lane = Lane([(0, 552), (1920, 552)], self.tram_lights[0], "horizontal", lane_type="tram")
        lane.turn = "STRAIGHT"
        self.lanes.append(lane)

        lane = Lane([(948, 0), (948, 1080)], self.tram_lights[1], "vertical", lane_type="tram")
        lane.turn = "STRAIGHT"
        self.lanes.append(lane)

        lane = Lane([(0, 552), (760, 552), (840, 552), (900, 575), (948, 670), (948, 1080)],
                    self.tram_lights[0], "horizontal", lane_type="tram")
        lane.turn = "RIGHT"
        self.lanes.append(lane)

        lane = Lane([(1920, 528), (1160, 528), (0, 528)],
                    self.tram_lights[3], "horizontal", lane_type="tram")
        lane.turn = "STRAIGHT"
        self.lanes.append(lane)

        lane = Lane([(972, 1080), (972, 738), (972, 0)],
                    self.tram_lights[2], "vertical", lane_type="tram")
        lane.turn = "STRAIGHT"
        self.lanes.append(lane)

        lane = Lane([(972, 1080), (972, 738), (972, 620), (948, 575), (850 ,528), (0,528)],
                    self.tram_lights[2], "vertical", lane_type="tram")
        lane.turn = "LEFT"
        self.lanes.append(lane)

        lane = Lane([(0, 720), (760, 720),(900, 710), (1920, 700)],
                    self.lights[7], "horizontal", lane_type = "bus")
        self.lanes.append(lane)
        
        lane = Lane([(1920, 350), (1160, 360), (900, 370), (0, 370)],
                    self.lights[2], "horizontal", lane_type = "bus")
        self.lanes.append(lane)

        lane = Lane([(1145, 1080), (1145, 738), (1200, 720), (1250, 700), (1920, 700)],
                    self.lights[11], "vertical", lane_type = "bus")
        self.lanes.append(lane)

        lane = Lane([(780, 0), (780, 338), (700, 360), (650, 370), (0, 370)],
                    self.lights[12], "vertical", lane_type = "bus")
        self.lanes.append(lane)

        lane = Lane([(1055, 1080), (1055, 738), (1055, 480), (900, 400), (700, 370), (0, 370)],
                    self.lights[9], "vertical", lane_type = "bus")
        self.lanes.append(lane)


        self.lanes[3].neighbors.append(self.lanes[4])
        self.lanes[4].neighbors.append(self.lanes[3])
        self.lanes[10].neighbors.append(self.lanes[11])
        self.lanes[11].neighbors.append(self.lanes[10])
        self.lanes[19].neighbors.append(self.lanes[17])
        self.lanes[19].neighbors.append(self.lanes[17])


        self.phases = [
            {"cars": [0,1,2,5,6,7], "trams": {0: "STRAIGHT", 1: "STOP", 2: "STOP", 3: "STRAIGHT"}},
            {"cars": [3,4],         "trams": {0: "STOP",    1: "STOP", 2: "STOP", 3: "STOP"}},
            {"cars": [8,9,10,11],   "trams": {0: "RIGHT",     1: "STOP", 2: "LEFT", 3: "STOP"}},
            {"cars": [12,13,14],    "trams": {0: "STOP",     1: "STRAIGHT", 2:"STRAIGHT", 3:"STOP"}},
        ]

        self.current_phase = 0
        self.phase_timer = 0
        self.green_time = 35
        self.yellow_time = 5

        # zachód (A)
        self.lanes[0].approach = "A"
        self.lanes[1].approach = "A"
        self.lanes[2].approach = "A"
        self.lanes[3].approach = "A"
        self.lanes[4].approach = "A"

        # wschód (B)
        self.lanes[5].approach = "B"
        self.lanes[6].approach = "B"
        self.lanes[7].approach = "B"
        self.lanes[8].approach = "B"

        # północ (C)
        self.lanes[9].approach = "C"
        self.lanes[10].approach = "C"
        self.lanes[11].approach = "C"
        self.lanes[12].approach = "C"
        self.lanes[13].approach = "C"

        # południe (D)
        self.lanes[14].approach = "D"
        self.lanes[15].approach = "D"
        self.lanes[16].approach = "D"

        

    def update_lights(self, dt):
        self.phase_timer += dt

        phase = self.phases[self.current_phase]
        car_phase = phase["cars"]
        tram_phase = phase["trams"]

        for i, light in enumerate(self.lights):
            if i in car_phase:
                if self.phase_timer < self.green_time:
                    light.state = "GREEN"
                elif self.phase_timer < self.green_time + self.yellow_time:
                    light.state = "YELLOW"
                else:
                    light.state = "RED"
            else:
                light.state = "RED"

        if self.phase_timer > self.green_time + self.yellow_time:
            self.phase_timer = 0
            self.current_phase = (self.current_phase + 1) % len(self.phases)

        for light in self.tram_lights:
            light.state = "STOP"

        for idx, state in tram_phase.items():
            if idx < len(self.tram_lights):
                self.tram_lights[idx].state = state

