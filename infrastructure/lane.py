class Lane:
    def __init__(self, start, checkpoint, end, direction):
        self.start = start  # (x, y)
        self.checkpoint = checkpoint
        self.end = end      # (x, y)
        self.direction = direction  # 0/1
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.lane = self
        vehicle.progress = 0  # 👈 ile przejechał po pasie (0 → 1)