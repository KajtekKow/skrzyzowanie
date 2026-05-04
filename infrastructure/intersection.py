from infrastructure.lane import Lane
from entities.moving_entities import Car, Bus

class Intersection:
    def __init__(self):
        self.lanes = [
            Lane((1440, 300), (720, 300) ,(720, 300), (0, 300), "horizontal"),
            Lane((1440, 270), (0,0), (0, 270), (0, 270),  "horizontal"),
            Lane((1440, 240), (0,0), (0, 240), (0, 240),"horizotnal"),
            Lane((0, 410), (0,0), (1440, 410), (1440, 410), "horizotnal"),
            Lane((0, 440), (0,0), (1440, 440), (1440, 440), "horizotnal"),
            Lane((0, 480), (0,0), (1440, 480), (1440, 480),"horizotnal"),
            Lane((590, 720), (0,0), (590, 0), (590, 0), "vertical"),
        ]

    def spawn(self, sim):
        car1 = Car(0, 0, 0)
        self.lanes[0].add_vehicle(car1)
        sim.add_entity(car1)

        car2 = Car(0, 0, 0)
        self.vx = 50
        self.lanes[0].add_vehicle(car2)
        sim.add_entity(car2)

        car3 = Car(0, 0, 0)
        self.lanes[3].add_vehicle(car3)
        sim.add_entity(car3)

        car4 = Bus(0, 0, 1)
        self.lanes[6].add_vehicle(car4)
        sim.add_entity(car4)

        car5 = Car(0, 0, 0)
        self.lanes[5].add_vehicle(car5)
        sim.add_entity(car5)