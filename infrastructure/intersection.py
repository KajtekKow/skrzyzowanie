from infrastructure.lane import Lane
from infrastructure.traffic_light import TrafficLight
from infrastructure.tram_light import TramLight

class Intersection:
    def __init__(self):

        self.lights = [
            TrafficLight(1160, 450), # ruska -> legnicka prosto 0
            TrafficLight(1160, 400), # ruska -> legnicka prosto 1
            TrafficLight(1195, 270), # ruska -> podwale prawo 2 <------
            TrafficLight(1160, 500), # ruska -> podwale lewo 3
            TrafficLight(760, 580), # legnicka -> podwale lewo 4
            TrafficLight(760, 620), # legnicka -> ruska prosto 5
            TrafficLight(760, 670), # legnicka -> ruska prosto 6
            TrafficLight(725, 810), # legnicka -> podwale prawo 7 <-------
            TrafficLight(1020, 738), # podawle -> legnicka lewo 8
            TrafficLight(1075, 738), # podwale -> legnicka lewo/podwale prosto 9
            TrafficLight(1130, 738), # podwale -> podwale prosto 10
            TrafficLight(1195, 805), # podwale -> ruska prawo 11 <---------
            TrafficLight(720, 275), # podwale -> legnicka prawo 12 <--------
            TrafficLight(800, 338), # podwale -> podwale prosto 13
            TrafficLight(900, 338), #podwale -> podwale prosto 14
            TrafficLight(760, 720), #buspas legnicka -> ruska 15
            TrafficLight(1160, 350), #buspas ruska -> legnicka 16
            
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
            Lane([(1920, 350), (1290, 350),(1195, 270), (1100, 200 ), (1100, 0)], self.lights[2], "horizontal"),
            Lane([(1920, 500), (1100, 500), (1000, 550),(900, 650), (810, 720), (810, 1080)], self.lights[3], "horizontal", lane_type="MIXED"), #busy moge 3
            Lane([(1920, 500), (1100, 500), (1000, 550),(900, 650), (860, 720), (860, 1080)], self.lights[3], "horizontal"),
            Lane([(0, 580), (760, 580), (1100, 350), (1100, 0)], self.lights[4], "horizontal"),
            Lane([(0, 620),(760, 620), (1000, 615), (1100, 600), (1920, 600)], self.lights[5], "horizontal"),
            Lane([(0, 670),(760, 670), (1000, 650), (1100, 640), (1920, 640)], self.lights[6], "horizontal"),
            Lane([(0, 720), (650, 720), (725, 810), (800,900), (810, 1080)], self.lights[7], "horizontal"),
            Lane([(1020, 1080), (1020, 738), (1010, 600), (960, 540), (900, 480), (0, 480)], self.lights[8], "vertical"),
            Lane([(1075, 1080), (1075, 738), (1055, 480), (900, 450), (700, 430), (0, 430)], self.lights[9], "vertical"),
            Lane([(1075, 1080), (1075, 738), (1040, 580),(1040, 0)], self.lights[9], "vertical"),
            Lane([(1130, 1080), (1130, 738), (1100, 640), (1100, 0)], self.lights[10], "vertical", lane_type="MIXED"), # busy moga 12
            Lane([(1130, 1080), (1130, 920), (1195, 805), (1300, 700),(1400, 670), (1500, 640), (1920, 640)], self.lights[11], "vertical"),
            Lane([(800, 0), (800, 200), (720, 275), (695, 290), (670, 370), (650, 400), (600, 430), (0, 430)], self.lights[12], "vertical"),
            Lane([(800, 0), (800, 338), (810, 700), (810, 1080)], self.lights[13], "vertical", lane_type="MIXED"), # busy moga 15
            Lane([(900, 0), (900, 338), (860, 700), (860, 1080)], self.lights[14], "vertical"),
        ]

        lane = Lane([(0, 552), (1920, 552)], self.tram_lights[0], "horizontal", lane_type="tram") #17
        lane.turn = "STRAIGHT"
        self.lanes.append(lane)

        lane = Lane([(948, 0), (948, 1080)], self.tram_lights[1], "vertical", lane_type="tram") #18
        lane.turn = "STRAIGHT"
        self.lanes.append(lane)

        lane = Lane([(0, 552), (760, 552), (840, 552), (900, 575), (948, 670), (948, 1080)], #19
                    self.tram_lights[0], "horizontal", lane_type="tram")
        lane.turn = "RIGHT"
        self.lanes.append(lane)

        lane = Lane([(1920, 528), (1160, 528), (0, 528)], #20
                    self.tram_lights[3], "horizontal", lane_type="tram")
        lane.turn = "STRAIGHT"
        self.lanes.append(lane)

        lane = Lane([(972, 1080), (972, 738), (972, 0)], # 21
                    self.tram_lights[2], "vertical", lane_type="tram")
        lane.turn = "STRAIGHT"
        self.lanes.append(lane)

        lane = Lane([(972, 1080), (972, 738), (972, 620), (948, 575), (850 ,528), (0,528)], #22
                    self.tram_lights[2], "vertical", lane_type="tram")
        lane.turn = "LEFT"
        self.lanes.append(lane)

        lane = Lane([(0, 720), (760, 720),(900, 710), (1920, 700)], #23 - stop
                    self.lights[15], "horizontal", lane_type = "bus")
        self.lanes.append(lane)
        
        lane = Lane([(1920, 350), (1160, 360), (900, 370), (0, 370)], #24 - stop
                    self.lights[16], "horizontal", lane_type = "bus")
        self.lanes.append(lane)

        lane = Lane([(1130, 1080), (1130, 920), (1195, 805), (1300, 720), (1350, 700), (1920, 700)], #25 - stop
                    self.lights[11], "vertical", lane_type = "bus")
        self.lanes.append(lane)

        lane = Lane([(800, 0), (800, 200), (720, 275), (695, 290), (680, 360), (650, 370), (0, 370)], #26 - stop 
                    self.lights[12], "vertical", lane_type = "bus")
        self.lanes.append(lane)

        lane = Lane([(1075, 1080), (1075, 738), (1055, 480), (900, 400), (700, 370), (0, 370)], #27 - stop
                    self.lights[9], "vertical", lane_type = "bus")
        self.lanes.append(lane)

        lane = Lane(
            [(0, 580), (760, 580), (800, 560), (830, 520), (825, 480), (790, 430), (720, 390), (650, 370), (450, 370), (250, 370), (0, 370)],
            self.lights[4], "horizontal", lane_type="bus"
        )
        self.lanes.append(lane)
        

        lane = Lane(
            [(0, 690), (650, 690), (760, 690), (950, 670), (1200, 660), (1920, 650)],
            self.lights[5],
            "horizontal",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)

        lane = Lane(
            [(0, 670), (650, 670), (760, 670), (880, 630), (960, 540), (1010, 410), (1040, 250), (1060, 0)],
            self.lights[5],
            "horizontal",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)

        lane = Lane(
            [(0, 710), (650, 710), (760, 720), (820, 810), (845, 930), (850, 1080)],
            self.lights[5],
            "horizontal",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)

        lane = Lane(
            [(1920, 430), (1600, 430), (1300, 430), (1160, 435), (960, 440), (760, 445), (400, 445), (0, 450)],
            self.lights[0],
            "horizontal",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)     

        lane = Lane(
            [(1920, 430), (1600, 430), (1300, 430), (1160, 425), (1100, 390), (1070, 320), (1060, 220), (1065, 100), (1080, 0)],
            self.lights[0],
            "horizontal",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)

        lane = Lane(
            [(1920, 465), (1600, 465), (1300, 465), (1160, 475), (1040, 510), (940, 570), (870, 670), (835, 800), (825, 940), (825, 1080)],
            self.lights[0],
            "horizontal",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)

        lane = Lane(
            [(860, 0), (860, 180), (860, 338), (855, 520), (850, 700), (850, 900), (850, 1080)],
            self.lights[13],
            "vertical",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)

        lane = Lane(
            [(830, 0), (830, 180), (830, 300), (810, 360), (760, 405), (680, 430), (520, 435), (300, 435), (0, 435)],
            self.lights[13],
            "vertical",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)

        lane = Lane(
            [(870, 0), (870, 180), (870, 320), (885, 430), (940, 515), (1060, 585), (1250, 625), (1500, 635), (1920, 635)],
            self.lights[13],
            "vertical",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)

        lane = Lane(
            [(1050, 1080), (1050, 900), (1050, 760), (1055, 620), (1060, 480), (1060, 300), (1060, 120), (1060, 0)],
            self.lights[9],
            "vertical",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)

        lane = Lane(
            [(1025, 1080), (1025, 900), (1020, 760), (990, 640), (900, 535), (760, 475), (520, 455), (250, 455), (0, 455)],
            self.lights[8],
            "vertical",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)

        lane = Lane(
            [(1085, 1080), (1085, 900), (1090, 760), (1130, 665), (1230, 625), (1450, 640), (1700, 640), (1920, 640)],
            self.lights[10],
            "vertical",
            lane_type="emergency"
        )
        lane.approach = "EM"
        self.lanes.append(lane)
    
        self.bus_stops = [
            {
                "name": "Przystanek zachod-gora",
                "lane_index": [24, 26, 27, 28],
                "point": (250, 370),
                "zone_length": 180,
                "dwell_time": 5.0
            },
            {
                "name": "Przystanek wschod-dol",
                "lane_index": [23, 25],
                "point": (1680, 700),
                "zone_length": 180,
                "dwell_time": 5.0
            },
        ]

        def connect_neighbors(a, b):
            if self.lanes[b] not in self.lanes[a].neighbors:
                self.lanes[a].neighbors.append(self.lanes[b])
            if self.lanes[a] not in self.lanes[b].neighbors:
                self.lanes[b].neighbors.append(self.lanes[a])


        # ruska -> legnicka / podwale, pasy obok siebie z prawej strony
        connect_neighbors(0, 1)
        connect_neighbors(1, 2)
        connect_neighbors(3, 4)

        # legnicka -> ruska, kilka równoległych pasów
        connect_neighbors(5, 6)
        connect_neighbors(6, 7)
        connect_neighbors(7, 8)

        # podwale od dołu / pionowe pasy obok siebie
        connect_neighbors(9, 10)
        connect_neighbors(10, 11)
        connect_neighbors(11, 12)
        connect_neighbors(12, 13)

        # podwale od góry / pionowe pasy obok siebie
        connect_neighbors(14, 15)
        connect_neighbors(15, 16)

        # buspasy jako sąsiedzi odpowiednich zwykłych pasów
        connect_neighbors(8, 23)
        connect_neighbors(2, 24)
        connect_neighbors(13, 25)
        connect_neighbors(14, 26)
        connect_neighbors(10, 27)


        self.phases = [
            {"cars": [0,1,2,5,6,7,15,16], "trams": {0: "STRAIGHT", 1: "STOP", 2: "STOP", 3: "STRAIGHT"}},
            {"cars": [3,4],         "trams": {0: "STOP",    1: "STOP", 2: "STOP", 3: "STOP"}},
            {"cars": [8,9,10,11],   "trams": {0: "RIGHT",     1: "STOP", 2: "LEFT", 3: "STOP"}},
            {"cars": [12,13,14],    "trams": {0: "STOP",     1: "STRAIGHT", 2:"STRAIGHT", 3:"STOP"}},
        ]
        # self.phases = [
        #     {"cars": [0,1,2,5,6,7,15,16], "trams": {0: "STRAIGHT", 1: "STOP", 2: "STOP", 3: "STRAIGHT"}},
        #     {"cars": [2,7,11,12], "trams": {0: "STOP",     1: "STRAIGHT", 2:"STRAIGHT", 3:"STOP"}}, 
        #     {"cars": [3,4],         "trams": {0: "STOP",    1: "STOP", 2: "STOP", 3: "STOP"}},
        #     {"cars": [8,9,10,11],   "trams": {0: "RIGHT",     1: "STOP", 2: "LEFT", 3: "STOP"}},
        #     {"cars": [12,13,14],    "trams": {0: "STOP",     1: "STRAIGHT", 2:"STRAIGHT", 3:"STOP"}},
        # ]

        self.current_phase = 0
        self.phase_timer = 0
        self.green_time = 50
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

        has_vehicle = False

        for lane in self.lanes:

            if lane.traffic_light in [self.lights[i] for i in car_phase]:

                for v in lane.vehicles:

                    dx = lane.traffic_light.x - v.x
                    dy = lane.traffic_light.y - v.y
                    dist = (dx**2 + dy**2)**0.5

                    if dist < 180:
                        has_vehicle = True
                        break

        if not has_vehicle and self.phase_timer > self.green_time * 0.25:
            self.phase_timer += dt * 5

        if self.phase_timer > self.green_time + self.yellow_time:
            self.phase_timer = 0
            self.current_phase = (self.current_phase + 1) % len(self.phases)

        for light in self.tram_lights:
            light.state = "STOP"

        for idx, state in tram_phase.items():
            if idx < len(self.tram_lights):
                self.tram_lights[idx].state = state

