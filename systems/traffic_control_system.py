class TrafficControlSystem:
    def update(self, sim, dt, index):
        sim.intersection.update_lights(dt)