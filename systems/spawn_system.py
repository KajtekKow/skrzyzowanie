import random
from entities.moving_entities import Car, Bus

class SpawnSystem:
    def __init__(self, spawn_interval=1.5):
        self.timer = 0
        self.spawn_interval = spawn_interval

    def update(self, sim, dt, index):
        self.timer += dt

        if self.timer < self.spawn_interval:
            return

        self.timer = 0

        lane = random.choice(sim.intersection.lanes)

        # =========================
        # 🚫 BLOKADA SPAWNU
        # =========================
        if lane.vehicles:
            first = min(lane.vehicles, key=lambda v: v.progress)

            # jeśli ktoś jest blisko startu → nie spawnuj
            gap = first.progress * lane.length
            if gap < 60:
                return

        # =========================
        # 🎯 POPRAWNY DIRECTION
        # =========================
        direction = 0 if lane.direction == "horizontal" else 1

        # =========================
        # 🚗 SPAWN
        # =========================
        if random.random() < 0.7:
            v = Car(0, 0, direction)
        else:
            v = Bus(0, 0, direction)

        # 🚀 PRĘDKOŚĆ
        v.current_speed = 0

        v.acceleration = random.uniform(120, 220)
        v.brake_power = random.uniform(250, 400)
        v.reaction_time = random.uniform(0.2, 0.8)

        v.wait_timer = 0

        base_speed = 280
        variation = random.randint(-30, 30)
        v.max_speed = base_speed + variation

        if lane.direction == "horizontal":
            v.vx = v.max_speed
            v.vy = 0
        else:
            v.vx = 0
            v.vy = v.max_speed

        lane.add_vehicle(v)
        sim.add_entity(v)