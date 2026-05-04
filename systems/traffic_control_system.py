class TrafficControlSystem:
    def __init__(self, traffic_light, stop_x):
        self.traffic_light = traffic_light
        self.stop_x = stop_x

    def update(self, sim, dt):
        self.traffic_light.update(dt)

        for e in sim.entities:
            if not (hasattr(e, "vx") and hasattr(e, "length")):
                continue

            # --- START ---
            target_vx = e.desired_vx

            front_x = e.x + e.length * 5
            distance = self.stop_x - front_x

            # --- ŚWIATŁA ---
            if self.traffic_light.state == "RED":
                if distance > 0:
                    slow_factor = min(distance / 50, 1)
                    target_vx = e.desired_vx * slow_factor

                    if distance < 5:
                        target_vx = 0
                        e.x = self.stop_x - e.length * 5

            # --- INNE POJAZDY ---
            for other in sim.entities:
                if other is e:
                    continue

                if not hasattr(other, "length"):
                    continue

                # 👇 TU JUŻ POWINNO BYĆ lane_id (następny krok)
                if hasattr(other, "lane_id") and other.lane_id == e.lane_id:
                    if other.x > e.x:
                        gap = other.x - (e.x + e.length * 5)

                    if gap < 20:
                        gap = max(gap, 0)

                        factor = gap / 20
                        target_vx = min(target_vx, other.vx * factor)

            # --- FINAL ---
            e.vx = max(target_vx, 0)