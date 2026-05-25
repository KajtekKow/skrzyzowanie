class TrafficControlSystem:
    def update(self, sim, dt, index):

        total_queue = 0

        for lane in sim.intersection.lanes:

            light = lane.traffic_light

            for v in lane.vehicles:

                dx = light.x - v.x
                dy = light.y - v.y
                dist = (dx**2 + dy**2)**0.5

                if getattr(v, "is_stopped", False) and dist < 120:
                    total_queue += 1

        if total_queue > 30:
            sim.intersection.green_time = 50

        elif total_queue > 20:
            sim.intersection.green_time = 42

        elif total_queue > 10:
            sim.intersection.green_time = 35

        else:
            sim.intersection.green_time = 25

        sim.intersection.update_lights(dt)