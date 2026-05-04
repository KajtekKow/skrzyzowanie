# === BASE ===
import numpy as np

class Entity:
    pass


class MovingEntity(Entity):
    def __init__(self, x, y, direction, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx 
        self.vy = vy
        self.desired_vx = vx  # 👈 globalnie dla wszystkich
        self.direction = direction
        self.is_stopped = False


# === VEHICLES ===

class Vehicle(MovingEntity):
    def __init__(self, x, y, direction, vx=0, vy=0):
        super().__init__(x, y, direction, vx, vy)
        self.length = 4
        self.lane = None
        self.progress = 0


class Car(Vehicle):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction, vx = 120 + np.random.randint(-10, 10), vy=40)


class Bus(Vehicle):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction, vx=45, vy=45)
        self.length = 12


class Tram(MovingEntity):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction, vx=45, vy=45)
        self.length = 30


# === PEDESTRIAN ===

class Pedestrian(MovingEntity):
    def __init__(self, x, y):
        super().__init__(x, y, vx=0, vy=20)