import math

class Lane:
    def __init__(self, points, traffic_light, direction, lane_type="car"):
        self.points = points
        self.traffic_light = traffic_light
        self.direction = direction
        self.lane_type = lane_type
        self.vehicles = []
        self.id = None
        self.forward = 1
        self.stop_progress = 0.4
        self.neighbors = []

        self.length = 0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            self.length += math.hypot(x2 - x1, y2 - y1)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.lane = self
        vehicle.progress = 0

        vehicle.x = self.points[0][0]
        vehicle.y = self.points[0][1]

        vehicle.position_initialized = True
        
        if hasattr(vehicle, "is_tram") and hasattr(self, "turn"):
            vehicle.turn = self.turn