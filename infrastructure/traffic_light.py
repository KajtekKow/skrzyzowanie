class TrafficLight:
    def __init__(self):
        self.state = "GREEN"
        self.timer = 0

    def update(self, dt):
        self.timer += dt

        if self.state == "GREEN" and self.timer > 5:
            self.state = "RED"
            self.timer = 0

        elif self.state == "RED" and self.timer > 5:
            self.state = "GREEN"
            self.timer = 0