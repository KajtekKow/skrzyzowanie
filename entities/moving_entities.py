import numpy as np

class Entity:
    pass


class MovingEntity(Entity):
    def __init__(self, x, y, direction, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx 
        self.vy = vy
        self.desired_vx = vx 
        self.direction = direction
        self.is_stopped = False

class Vehicle(MovingEntity):
    def __init__(self, x, y, direction, vx=0, vy=0):
        super().__init__(x, y, direction, vx, vy)
        self.length = 4
        self.lane = None
        self.progress = 0


class Car(Vehicle):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction, vx = 280 + np.random.randint(-10, 10), vy=280 + np.random.randint(-10, 10))


class Bus(Vehicle):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction, vx=45, vy=45)
        self.length = 12
        self.is_bus = True


class Tram(MovingEntity):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction, vx=280, vy=280)
        self.length = 50
        self.turn = "STRAIGHT" 
        self.is_tram = True


class Pedestrian(MovingEntity):
    def __init__(self, x, y):
        super().__init__(x, y, vx=0, vy=20)

class EmergencyVehicle(Car):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)

        self.is_emergency = True
        self.length = 6
        self.priority_radius = 260

        self.max_speed = 170
        self.acceleration = 130
        self.brake_power = 260

        self.lateral_offset = 0       