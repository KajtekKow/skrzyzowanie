class Simulation:
    def __init__(self):
        self.entities = []
        self.systems = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_system(self, system):
        self.systems.append(system)

    def update(self, dt):
        for system in self.systems:
            system.update(self, dt)
            
    def update_vehicles_green(self):
        for e in self.entities:
            e.is_stopped = False