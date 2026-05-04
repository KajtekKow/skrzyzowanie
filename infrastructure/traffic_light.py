class TrafficLight:
    def __init__(self, x, y):
        self.state = "GREEN"
        self.timer = 0
        self.x = x
        self.y = y

    def update(self, dt, sim, index):
        self.timer += dt

        if self.state == "GREEN" and self.timer > 5:
            self.state = "RED"
            self.timer = 0

        elif self.state == "RED" and self.timer > 5:
            self.state = "GREEN"
            self.timer = 0
            sim.update_vehicles_green()