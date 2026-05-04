class Simulation:
    def __init__(self):
        self.entities = []
        self.systems = []
        self.traffic_lights = []
        self.intersection = None
    
    def add_intersection(self, intersection):
        self.intersection = intersection

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_system(self, system):
        self.systems.append(system)

    def add_traffic_light(self, traffic_lights):
        self.traffic_lights.append(traffic_lights)

    def update(self, dt):
        for system in self.systems:
            system.update(self, dt, 0)
            
    def update_vehicles_green(self):
        for e in self.entities:
            e.is_stopped = False