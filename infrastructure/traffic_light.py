class TrafficLight:
    def __init__(self, x, y):
        self.state = "GREEN"
        self.timer = 0

        self.green_time = 5
        self.yellow_time = 2
        self.red_time = 5

        self.x = x
        self.y = y

    def update(self, dt, sim, index):
        self.timer += dt

        if self.state == "GREEN" and self.timer > self.green_time:
            self.state = "YELLOW"
            self.timer = 0

        elif self.state == "YELLOW" and self.timer > self.yellow_time:
            self.state = "RED"
            self.timer = 0

        elif self.state == "RED" and self.timer > self.red_time:
            self.state = "GREEN"
            self.timer = 0
            sim.update_vehicles_green()