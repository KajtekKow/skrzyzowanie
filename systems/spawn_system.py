import random
from entities.moving_entities import Car, Bus, Tram, EmergencyVehicle


class SpawnSystem:
    def __init__(self, spawn_interval=1.2):
        self.timer = 0
        self.spawn_interval = spawn_interval

        self.spawned_total = 0
        self.spawned_types = {
            "car": 0,
            "delivery": 0,
            "bus": 0,
            "tram": 0,
            "emergency": 0
        }

        self.approach_weights = {
            "A": 0.35,
            "B": 0.30,
            "C": 0.20,
            "D": 0.15
        }

    def choose_vehicle_type(self):
        weights = {
            "car": 87.5,
            "delivery": 6.9,
            "tram": 2.0,
            "bus": 2.6,
            "emergency": 1.0
        }

        total = sum(weights.values())

        for k in weights:
            weights[k] /= total

        r = random.random()
        cumulative = 0

        for k, v in weights.items():
            cumulative += v
            if r < cumulative:
                return k

    def get_time_multiplier(self, hour):
        if 0 <= hour < 5:
            return 0.2
        elif 5 <= hour < 7:
            return 0.8
        elif 7 <= hour < 9:
            return 2.5
        elif 9 <= hour < 14:
            return 1.2
        elif 14 <= hour < 18:
            return 2.8
        elif 18 <= hour < 22:
            return 1.0
        else:
            return 0.3

    def update(self, sim, dt, index):
        self.timer += dt
        mult = max(0.05, self.get_time_multiplier(sim.time_of_day))
        effective_interval = self.spawn_interval / mult

        max_entities = 150 if sim.time_scale > 50 else 300 
        
        if len(sim.entities) < max_entities:
            if self.timer >= effective_interval:
                self.timer = 0
                self.spawn_vehicle(sim)
                
    def spawn_vehicle(self, sim):
        lanes = sim.intersection.lanes
        if len(sim.entities) > 300:
            return

        vehicle_type = self.choose_vehicle_type()

        if 0 <= sim.time_of_day < 5 and vehicle_type == "tram":
            return

        possible_lanes = []

        for l in lanes:
            if vehicle_type == "tram" and l.lane_type == "tram":
                possible_lanes.append(l)

            elif vehicle_type == "bus" and l.lane_type in ["bus", "MIXED"]:
                possible_lanes.append(l)

            elif vehicle_type in ["car", "delivery"] and l.lane_type in ["car", "MIXED"]:
                possible_lanes.append(l)

            elif vehicle_type == "emergency" and l.lane_type == "emergency":
                possible_lanes.append(l)

        if not possible_lanes:
            return

        weights = []

        for l in possible_lanes:
            base = self.approach_weights.get(getattr(l, "approach", "A"), 0.25)

            if vehicle_type == "tram":
                base *= 1.0   

                if hasattr(l, "approach"):
                    if l.approach == "A":   
                        base *= 0.7
                    elif l.approach == "B":
                        base *= 1.0
                    elif l.approach == "C":
                        base *= 1.2
                    elif l.approach == "D":
                        base *= 1.2

            weights.append(base)

        lane = random.choices(possible_lanes, weights=weights)[0]

        if lane.vehicles:
            first = min(lane.vehicles, key=lambda v: v.progress)
            gap = first.progress * lane.length
            if gap < 50:
                return

        direction = 0 if lane.direction == "horizontal" else 1

        v = None

        if vehicle_type == "tram":
            v = Tram(0, 0, direction)
            v.max_speed = 165
            v.acceleration = random.uniform(25, 55)
            v.brake_power = random.uniform(120, 220)

        elif vehicle_type == "bus":
            v = Bus(0, 0, direction)

        elif vehicle_type == "delivery":
            v = Car(0, 0, direction)
            v.is_delivery = True

        elif vehicle_type == "emergency":
            v = EmergencyVehicle(0, 0, direction)

        else:
            v = Car(0, 0, direction)

        if v is None:
            return

        if hasattr(v, "is_emergency"):
            v.acceleration = random.uniform(200, 250)
            v.brake_power = random.uniform(180, 280)
            v.max_speed = random.uniform(180, 250)
        else:
            v.acceleration = random.uniform(100, 160)
            v.brake_power = random.uniform(120, 220)
            v.max_speed = random.uniform(130, 180)

        if hasattr(v, "is_delivery"):
            v.max_speed *= 0.85

        v.current_speed = v.max_speed * 0.85

        if lane.direction == "horizontal":
            v.vx = v.max_speed
            v.vy = 0
        else:
            v.vx = 0
            v.vy = v.max_speed

        lane.add_vehicle(v)
        sim.add_entity(v)

        self.spawned_total += 1

        if hasattr(v, "is_tram"):
            self.spawned_types["tram"] += 1
        elif hasattr(v, "is_emergency"):
            self.spawned_types["emergency"] += 1
        elif hasattr(v, "is_bus"):
            self.spawned_types["bus"] += 1
        elif hasattr(v, "is_delivery"):
            self.spawned_types["delivery"] += 1
        else:
            self.spawned_types["car"] += 1

        stats = next((s for s in sim.systems if hasattr(s, "register_vehicle")), None)
        if stats:
            stats.register_vehicle(v, sim)

    def get_stats(self):
        total = max(1, self.spawned_total)

        return {
            "car": self.spawned_types["car"] / total * 100,
            "delivery": self.spawned_types["delivery"] / total * 100,
            "bus": self.spawned_types["bus"] / total * 100,
            "tram": self.spawned_types["tram"] / total * 100,
        }