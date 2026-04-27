class TrafficControlSystem:
    def __init__(self, traffic_light):
        self.traffic_light = traffic_light
        self.stop_x = 720  # 👈 punkt zatrzymania (środek skrzyżowania)

    def update(self, sim, dt):
        self.traffic_light.update(dt)

        for e in sim.entities:
            if hasattr(e, "vx") and hasattr(e, "length"):

                front_x = e.x + e.length * 5
                distance = self.stop_x - front_x

                if self.traffic_light.state == "RED":

                    if distance > 0:
                        # im bliżej, tym wolniej
                        slow_factor = min(distance / 50, 1)

                        e.vx = e.desired_vx * slow_factor

                        # bardzo blisko → zatrzymaj dokładnie
                        if distance < 5:
                            e.vx = 0

                elif self.traffic_light.state == "GREEN":
                    e.vx = e.desired_vx