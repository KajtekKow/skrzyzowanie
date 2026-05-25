import math
import random

class MovementSystem:
    def update(self, sim, dt, index):
        for lane in sim.intersection.lanes:

            lane.vehicles.sort(key=lambda v: v.progress * lane.forward)
            to_remove = []

            for e in lane.vehicles:
                if not hasattr(e, "lane") or e.lane is None:
                    continue

                if not hasattr(e, "initialized"):
                    e.initialized = True

                    e.current_speed = 0
                    e.max_speed = max(abs(e.vx), abs(e.vy))

                    e.acceleration = 320
                    e.brake_power = 500

                    e.reaction_time = random.uniform(0.7, 1.4)

                    # 1% kierowcow zamulonych
                    if random.random() < 0.01:
                        e.reaction_time += random.uniform(1.0, 3.0)
                    e.wait_timer = 0
                    e.was_waiting_at_light = False

                    if not hasattr(e, "total_wait_time"):
                        e.total_wait_time = 0

                e.is_stopped = False
                speed_factor = 1.0

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

                light = lane.traffic_light

                dx_l = light.x - e.x
                dy_l = light.y - e.y

                distance_to_light = math.hypot(dx_l, dy_l)
                approaching = (dx_l * vx + dy_l * vy) > 0

                if lane.lane_type == "tram":
                    state = getattr(light, "state", "STOP")

                    allowed = (
                        state == "ALL" or
                        state == lane.turn
                    )

                    if not allowed and approaching:
                        braking_zone = 150

                        if distance_to_light < braking_zone:
                            speed_factor = min(speed_factor, distance_to_light / braking_zone)

                        if distance_to_light < 80 + e.length:
                            e.is_stopped = True
                            speed_factor = 0.0

                else:
                    if light.state in ["RED", "YELLOW"] and approaching:

                        if distance_to_light < 80:
                            speed_factor = min(speed_factor, distance_to_light / 80)

                        if distance_to_light < 30:
                            e.is_stopped = True
                            speed_factor = 0.0
                            e.was_waiting_at_light = True

                candidates = []
                for entity in sim.entities:
                    if entity is e: 
                        continue
                    
                    dist_approx = abs(entity.x - e.x) + abs(entity.y - e.y)
                    if dist_approx < 400:
                        candidates.append(entity)
            
                ahead = None
                min_gap = float("inf")

                for other in candidates:
                    dx_o = other.x - e.x
                    dy_o = other.y - e.y
                    dist = math.hypot(dx_o, dy_o)

                    dot = dx_o * vx + dy_o * vy
                    lateral = abs(dx_o * -vy + dy_o * vx)

                    if hasattr(e, "is_tram"):
                        lateral_limit = 12 
                    else:
                        lateral_limit = 25 

                    
                    if dot > 0 and lateral < lateral_limit:
                        if dist < min_gap:
                            safe_distance = 60
                            if hasattr(other, "is_tram"):
                                safe_distance = 100 
                            
                            if dist < safe_distance + (e.current_speed * 0.2):
                                min_gap = dist
                                ahead = other
                if ahead:
                    gap = min_gap

                    speed_self = e.current_speed
                    if hasattr(e, "is_tram"):
                        min_gap_safe = 100  
                    else:
                        min_gap_safe = 40 + e.length * 2
                    reaction_gap = min_gap_safe + speed_self * 0.3

                    if gap < reaction_gap:
                        speed_factor = min(speed_factor, gap / reaction_gap)

                        if gap < min_gap_safe:
                            e.is_stopped = True
                            speed_factor = 0.0

                if e.is_stopped:
                    e.current_speed -= e.brake_power * dt
                    e.total_wait_time += dt   
                else:
                    if e.was_waiting_at_light:
                        e.wait_timer += dt

                        if e.wait_timer >= e.reaction_time:
                            e.current_speed += e.acceleration * dt

                        if e.current_speed > 20:
                            e.was_waiting_at_light = False
                            e.wait_timer = 0
                    else:
                        e.current_speed += e.acceleration * dt

                e.current_speed = max(0, min(e.current_speed, e.max_speed))

                if not e.is_stopped:
                    e.progress += (e.current_speed * dt / lane.length) * speed_factor
                    e.progress = min(e.progress, 1)

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

                if e.progress >= 1:
                    to_remove.append(e)

                    stats = next((s for s in sim.systems if hasattr(s, "register_wait_time")), None)
                    if stats:
                        stats.register_wait_time(e, getattr(e, "total_wait_time", 0))

            for e in to_remove:
                if e in lane.vehicles:
                    lane.vehicles.remove(e)
                if e in sim.entities:
                    sim.entities.remove(e)