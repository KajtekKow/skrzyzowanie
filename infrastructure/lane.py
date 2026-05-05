import math

class Lane:
    def __init__(self, points, traffic_light, direction):
        self.points = points
        self.traffic_light = traffic_light
        self.direction = direction
        self.vehicles = []

        self.forward = 1
        self.stop_progress = 0.4
        self.neighbors = []

        # długość całej ścieżki
        self.length = 0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            self.length += math.hypot(x2 - x1, y2 - y1)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.lane = self
        vehicle.progress = 0