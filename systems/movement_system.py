import math

class MovementSystem:
    def update(self, sim, dt, index):
        for lane in sim.intersection.lanes:

            lane.vehicles.sort(key=lambda v: v.progress * lane.forward)
            to_remove = []

            for e in lane.vehicles:
                if not hasattr(e, "lane") or e.lane is None:
                    continue

                # =========================
                # INIT
                # =========================
                if not hasattr(e, "initialized"):
                    e.initialized = True

                    e.current_speed = 0
                    e.max_speed = max(abs(e.vx), abs(e.vy))

                    e.acceleration = 320      # 🔥 szybciej rusza
                    e.brake_power = 500

                    e.reaction_time = 0.4
                    e.wait_timer = 0
                    e.was_waiting_at_light = False

                e.is_stopped = False
                speed_factor = 1.0

                # =========================
                # KIERUNEK (segment)
                # =========================
                target_dist = e.progress * lane.length
                dist_acc = 0
                dx, dy = 1, 0

                for j in range(len(lane.points) - 1):
                    x1, y1 = lane.points[j]
                    x2, y2 = lane.points[j + 1]

                    seg_len = math.hypot(x2 - x1, y2 - y1)

                    if dist_acc + seg_len >= target_dist:
                        dx = x2 - x1
                        dy = y2 - y1
                        break

                    dist_acc += seg_len

                length = math.hypot(dx, dy)
                vx = dx / length if length else 1
                vy = dy / length if length else 0

                # =========================
                # 🚦 ŚWIATŁO
                # =========================
                light = lane.traffic_light
                dx_l = light.x - e.x
                dy_l = light.y - e.y

                distance_to_light = math.hypot(dx_l, dy_l)
                approaching = (dx_l * vx + dy_l * vy) > 0

                if light.state in ["RED", "YELLOW"] and approaching:

                    if distance_to_light < 80:
                        speed_factor = min(speed_factor, distance_to_light / 80)

                    if distance_to_light < 30:
                        e.is_stopped = True
                        speed_factor = 0.0
                        e.was_waiting_at_light = True

                # =========================
                # 🚗 AUTO PRZED (FIXED)
                # =========================
                candidates = lane.vehicles[:]
                for n in lane.neighbors:
                    candidates.extend(n.vehicles)

                ahead = None
                min_gap = float("inf")

                for other in candidates:
                    if other is e:
                        continue

                    dx_o = other.x - e.x
                    dy_o = other.y - e.y
                    dist = math.hypot(dx_o, dy_o)

                    dot = dx_o * vx + dy_o * vy

                    # 🔥 KLUCZ: tylko auta w tej samej linii
                    lateral = abs(dx_o * -vy + dy_o * vx)

                    if dot > 0 and dist < min_gap and lateral < 25:
                        min_gap = dist
                        ahead = other

                if ahead:
                    gap = min_gap

                    speed_self = e.current_speed
                    speed_ahead = getattr(ahead, "current_speed", 0)

                    min_gap_safe = 20 + e.length * 4

                    # 🔥 dużo mniejszy reaction gap
                    reaction_gap = min_gap_safe + speed_self * 0.3

                    if gap < reaction_gap:
                        speed_factor = min(speed_factor, gap / reaction_gap)

                        if gap < min_gap_safe:
                            e.is_stopped = True
                            speed_factor = 0.0
                    else:
                        speed_factor = 1.0

                # =========================
                # 🚀 PRZYSPIESZENIE
                # =========================
                if e.is_stopped:
                    e.current_speed -= e.brake_power * dt
                else:
                    if e.was_waiting_at_light:
                        e.wait_timer += dt

                        if e.wait_timer >= e.reaction_time:
                            e.current_speed += e.acceleration * dt

                        if e.current_speed > 5:
                            e.was_waiting_at_light = False
                            e.wait_timer = 0
                    else:
                        e.current_speed += e.acceleration * dt

                e.current_speed = max(0, min(e.current_speed, e.max_speed))

                # =========================
                # 🏃 RUCH
                # =========================
                if not e.is_stopped:
                    e.progress += (e.current_speed * dt / lane.length) * speed_factor
                    e.progress = min(e.progress, 1)

                # =========================
                # 📍 POZYCJA
                # =========================
                target_dist = e.progress * lane.length
                dist_acc = 0

                for j in range(len(lane.points) - 1):
                    x1, y1 = lane.points[j]
                    x2, y2 = lane.points[j + 1]

                    seg_len = math.hypot(x2 - x1, y2 - y1)
                    if seg_len == 0:
                        continue

                    if dist_acc + seg_len >= target_dist:
                        t = (target_dist - dist_acc) / seg_len

                        e.x = x1 + (x2 - x1) * t
                        e.y = y1 + (y2 - y1) * t

                        dx = x2 - x1
                        dy = y2 - y1

                        e.angle = math.degrees(math.atan2(-dy, dx))
                        break

                    dist_acc += seg_len
                else:
                    e.x, e.y = lane.points[-1]

                # =========================
                # CLEANUP
                # =========================
                if e.progress >= 1:
                    to_remove.append(e)

            for e in to_remove:
                if e in lane.vehicles:
                    lane.vehicles.remove(e)
                if e in sim.entities:
                    sim.entities.remove(e)