class Simulation:
    def __init__(self):
        self.entities = []
        self.systems = []
        self.traffic_lights = []
        self.intersection = None

        self.sim_time = 0        
        self.time_scale = 1.0    

        self.time_of_day = 6.0   

    def add_intersection(self, intersection):
        self.intersection = intersection

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_system(self, system):
        self.systems.append(system)

    def add_traffic_light(self, traffic_lights):
        self.traffic_lights.append(traffic_lights)

    def update(self, dt):
        dt *= self.time_scale

        dt = min(dt, 0.1)

        self.sim_time += dt

        self.time_of_day += dt / 3600
        self.time_of_day %= 24

        for system in self.systems:
            system.update(self, dt, 0)
    
    def reset(self):
        self.entities.clear()
        self.sim_time = 0
        self.time_of_day = 6.0

        for s in self.systems:
            if hasattr(s, "spawned_total"):
                s.spawned_total = 0
            if hasattr(s, "spawned_types"):
                for k in s.spawned_types:
                    s.spawned_types[k] = 0
            if hasattr(s, "timer"):
                s.timer = 0

        if self.intersection:
            self.intersection.current_phase = 0
            self.intersection.phase_timer = 0

    def update_vehicles_green(self):
        for e in self.entities:
            e.is_stopped = False