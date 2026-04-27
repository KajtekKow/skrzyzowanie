# === BASE ===
import numpy as np

class Entity:
    pass


class MovingEntity(Entity):
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx 
        self.vy = vy
        self.desired_vx = vx  # 👈 globalnie dla wszystkich


# === VEHICLES ===

class Vehicle(MovingEntity):
    def __init__(self, x, y, vx=0, vy=0):
        super().__init__(x, y, vx + np.random.randint(-10, 10), vy)
        self.length = 4


class Car(Vehicle):
    def __init__(self, x, y):
        super().__init__(x, y, vx=50 + np.random.randint(-5, 5), vy=0)


class Bus(Vehicle):
    def __init__(self, x, y):
        super().__init__(x, y, vx=45, vy=0)
        self.length = 12


class Tram(MovingEntity):
    def __init__(self, x, y):
        super().__init__(x, y, vx=45, vy=0)
        self.length = 30


# === PEDESTRIAN ===

class Pedestrian(MovingEntity):
    def __init__(self, x, y):
        super().__init__(x, y, vx=0, vy=20)