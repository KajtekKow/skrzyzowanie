class Lane:
    def __init__(self, start, end, direction):
        self.start = start  # (x, y)
        self.end = end      # (x, y)
        self.direction = direction  # "horizontal" / "vertical"
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.lane = self
        vehicle.progress = 0  # 👈 ile przejechał po pasie (0 → 1)