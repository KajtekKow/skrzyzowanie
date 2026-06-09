import math
import random

class MovementSystem:

    def get_progress_at_point(self, lane, point):
        px, py = point

        best_dist = float("inf")
        best_along = 0
        dist_acc = 0

        for i in range(len(lane.points) - 1):
            ax, ay = lane.points[i]
            bx, by = lane.points[i + 1]

            abx = bx - ax
            aby = by - ay
            seg_len_sq = abx * abx + aby * aby

            if seg_len_sq == 0:
                continue

            apx = px - ax
            apy = py - ay

            t = (apx * abx + apy * aby) / seg_len_sq
            t = max(0, min(1, t))

            closest_x = ax + abx * t
            closest_y = ay + aby * t

            d = math.hypot(px - closest_x, py - closest_y)

            if d < best_dist:
                best_dist = d
                best_along = dist_acc + math.sqrt(seg_len_sq) * t

            dist_acc += math.sqrt(seg_len_sq)

        return best_along / max(1, lane.length)


    def update(self, sim, dt, index):
        for lane in sim.intersection.lanes:

            lane.vehicles.sort(key=lambda v: v.progress * lane.forward)
            to_remove = []

            for e in lane.vehicles:
                if not hasattr(e, "lane") or e.lane is None:
                    continue

                if not hasattr(e, "initialized"):
                    e.initialized = True

                    e.max_speed = max(abs(e.vx), abs(e.vy))
                    
                    if not hasattr(e, "current_speed"):
                        e.current_speed = e.max_speed * 0.85
                    else:
                        e.current_speed = max(e.current_speed, e.max_speed * 0.85)

                    e.acceleration = 70
                    e.brake_power = 400

                    e.reaction_time = random.uniform(0.9, 1.4)

                    if random.random() < 0.01:
                        e.reaction_time += random.uniform(1.0, 3.0)
                    e.wait_timer = 0
                    e.was_waiting_at_light = False

                    if not hasattr(e, "total_wait_time"):
                        e.total_wait_time = 0

                e.is_stopped = False
                speed_factor = 1.0

                if not hasattr(e, "yield_offset"):
                    e.yield_offset = 0

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

                is_turning_segment = abs(vx) > 0.25 and abs(vy) > 0.25

                if hasattr(e, "is_emergency"):
                    if not hasattr(e, "turn_safety_timer"):
                        e.turn_safety_timer = 0

                    if is_turning_segment:
                        e.turn_safety_timer = 1.2
                    else:
                        e.turn_safety_timer = max(0, e.turn_safety_timer - dt)

                emergency_cautious = hasattr(e, "is_emergency") and (
                    is_turning_segment or getattr(e, "turn_safety_timer", 0) > 0
)

                near_emergency = None

                if not hasattr(e, "is_emergency") and lane.lane_type != "tram":
                    for other in sim.entities:
                        if not hasattr(other, "is_emergency"):
                            continue

                        emergency_lane = getattr(other, "lane", None)

                        dx_e = other.x - e.x
                        dy_e = other.y - e.y
                        dist = math.hypot(dx_e, dy_e)

                        if dist > getattr(other, "priority_radius", 260):
                            continue

                        emergency_forward = dx_e * vx + dy_e * vy
                        emergency_lateral = abs(dx_e * -vy + dy_e * vx)

                        same_or_neighbor_lane = (
                            emergency_lane is lane or
                            emergency_lane in lane.neighbors
                        )

                        close_emergency_lane = (
                            emergency_lane is not None and
                            getattr(emergency_lane, "lane_type", None) == "emergency" and
                            emergency_lateral < 180
                        )

                        if not same_or_neighbor_lane and not close_emergency_lane:
                            continue

                        if emergency_forward < 90:
                            near_emergency = other
                            break

                        chain_yield_vehicle = None

                        for other_vehicle in lane.vehicles:
                            if other_vehicle is e:
                                continue

                            if not getattr(other_vehicle, "yielding_to_emergency", False):
                                continue

                            dx_o = other_vehicle.x - e.x
                            dy_o = other_vehicle.y - e.y

                            behind = (dx_o * vx + dy_o * vy) < 0
                            dist_o = math.hypot(dx_o, dy_o)

                            if behind and dist_o < 160:
                                chain_yield_vehicle = other_vehicle
                                break

                        if chain_yield_vehicle:
                            near_emergency = chain_yield_vehicle
                            break

                if near_emergency:
                    if not hasattr(e, "yield_side"):
                        emergency_lane = getattr(near_emergency, "lane", None)

                        if not hasattr(e, "yield_side"):
                            emergency_lane = getattr(near_emergency, "lane", None)

                            if emergency_lane is lane:
                                dx_e = near_emergency.x - e.x
                                dy_e = near_emergency.y - e.y

                                emergency_lateral = dx_e * -vy + dy_e * vx

                                if emergency_lateral >= 0:
                                    e.yield_side = -1
                                else:
                                    e.yield_side = 1

                            else:
                                ex, ey = emergency_lane.points[0]
                                lx, ly = lane.points[0]

                                side_to_emergency_lane = (ex - lx) * -vy + (ey - ly) * vx

                                if side_to_emergency_lane >= 0:
                                    e.yield_side = -1
                                else:
                                    e.yield_side = 1

                        else:
                            ex, ey = emergency_lane.points[0]
                            lx, ly = lane.points[0]

                            side_to_emergency_lane = (ex - lx) * -vy + (ey - ly) * vx

                            if side_to_emergency_lane >= 0:
                                e.yield_side = -1
                            else:
                                e.yield_side = 1

                    if hasattr(e, "is_bus"):
                        target_offset = e.yield_side * 32
                    else:
                        target_offset = e.yield_side * 22

                    max_step = 0.12
                    diff = target_offset - e.yield_offset

                    if diff > max_step:
                        diff = max_step
                    elif diff < -max_step:
                        diff = -max_step

                    side_free = True

                    test_offset = e.yield_offset + diff

                    test_x = e.x + (-vy * diff)
                    test_y = e.y + (vx * diff)

                    if not hasattr(e, "is_emergency") and lane.lane_type != "tram":
                        for tram_lane in sim.intersection.lanes:
                            if tram_lane.lane_type != "tram":
                                continue

                            for k in range(len(tram_lane.points) - 1):
                                ax, ay = tram_lane.points[k]
                                bx, by = tram_lane.points[k + 1]

                                abx = bx - ax
                                aby = by - ay
                                apx = test_x - ax
                                apy = test_y - ay

                                ab_len_sq = abx * abx + aby * aby

                                if ab_len_sq == 0:
                                    dist_to_track = math.hypot(test_x - ax, test_y - ay)
                                else:
                                    t_track = (apx * abx + apy * aby) / ab_len_sq
                                    t_track = max(0, min(1, t_track))

                                    closest_x = ax + abx * t_track
                                    closest_y = ay + aby * t_track

                                    dist_to_track = math.hypot(test_x - closest_x, test_y - closest_y)

                                if dist_to_track < 34:
                                    side_free = False
                                    break

                            if not side_free:
                                break

                    for other in sim.entities:
                        if other is e:
                            continue

                        if not hasattr(e, "is_emergency") and not hasattr(e, "is_tram") and hasattr(other, "is_tram"):
                            continue

                        dist_side = math.hypot(other.x - test_x, other.y - test_y)

                        min_side_dist = 26

                        if hasattr(e, "is_bus") or hasattr(other, "is_bus"):
                            min_side_dist = 36

                        if hasattr(e, "is_emergency") or hasattr(other, "is_emergency"):
                            min_side_dist = 24

                        if dist_side < min_side_dist:
                            side_free = False
                            break


                    if side_free:
                        e.yield_offset += diff
                        speed_factor = min(speed_factor, 0.75)
                        e.yielding_to_emergency = True
                    else:
                        speed_factor = min(speed_factor, 0.20)

                else:
                    e.yielding_to_emergency = False

                    target_offset = 0

                    max_step = 0.15
                    diff = target_offset - e.yield_offset

                    if diff > max_step:
                        diff = max_step
                    elif diff < -max_step:
                        diff = -max_step

                    e.yield_offset += diff

                    if abs(e.yield_offset) < 0.5:
                        e.yield_offset = 0

                        if hasattr(e, "yield_side"):
                            del e.yield_side

                if not hasattr(e, "is_emergency") and lane.lane_type != "tram":
                    for amb in sim.entities:
                        if not hasattr(amb, "is_emergency"):
                            continue

                        dx_a = amb.x - e.x
                        dy_a = amb.y - e.y

                        dist_to_amb = math.hypot(dx_a, dy_a)

                        if dist_to_amb > 150:
                            continue

                        amb_forward = dx_a * vx + dy_a * vy
                        amb_lateral = abs(dx_a * -vy + dy_a * vx)

                        if 0 < amb_forward < 140 and amb_lateral < 32:
                            speed_factor = min(speed_factor, 0.05)

                            if dist_to_amb < 95:
                                e.is_stopped = True
                                e.current_speed = 0

                            break

                light = lane.traffic_light

                if hasattr(e, "is_bus") and hasattr(sim.intersection, "bus_stops"):
                    if not hasattr(e, "visited_bus_stops"):
                        e.visited_bus_stops = set()

                    if not hasattr(e, "serving_bus_stop"):
                        e.serving_bus_stop = None

                    if not hasattr(e, "bus_stop_timer"):
                        e.bus_stop_timer = 0

                    if e.serving_bus_stop is not None:
                        e.bus_stop_timer -= dt
                        e.is_stopped = True
                        e.current_speed = 0
                        speed_factor = 0.0

                        if e.bus_stop_timer <= 0:
                            e.visited_bus_stops.add(e.serving_bus_stop)
                            e.serving_bus_stop = None

                    else:
                        for stop_id, stop in enumerate(sim.intersection.bus_stops):
                            if stop_id in e.visited_bus_stops:
                                continue

                            lane_indexes = stop.get("lane_index", [])

                            if not isinstance(lane_indexes, list):
                                lane_indexes = [lane_indexes]

                            valid_for_lane = False

                            for idx in lane_indexes:
                                if 0 <= idx < len(sim.intersection.lanes):
                                    if sim.intersection.lanes[idx] is lane:
                                        valid_for_lane = True
                                        break

                            if not valid_for_lane:
                                continue

                            sx, sy = stop["point"]

                            dx_s = sx - e.x
                            dy_s = sy - e.y

                            forward_to_stop = dx_s * vx + dy_s * vy
                            lateral_to_stop = abs(dx_s * -vy + dy_s * vx)

                            if 0 < forward_to_stop < 120 and lateral_to_stop < 45:
                                speed_factor = min(speed_factor, max(0.12, forward_to_stop / 120))

                            if 0 < forward_to_stop < 18 and lateral_to_stop < 45:
                                e.serving_bus_stop = stop_id
                                e.bus_stop_timer = stop.get("dwell_time", 5.0)
                                e.is_stopped = True
                                e.current_speed = 0
                                speed_factor = 0.0
                                break

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
                    if light.state in ["RED", "YELLOW"] and approaching and not hasattr(e, "is_emergency"):

                        if distance_to_light < 180:
                            speed_factor = min(speed_factor, distance_to_light / 180)

                        if distance_to_light < 60:
                            e.is_stopped = True
                            speed_factor = 0.0
                            e.was_waiting_at_light = True

                candidates = []

                for entity in sim.entities:
                    if entity is e:
                        continue

                    e_is_tram = hasattr(e, "is_tram")
                    e_is_emergency = hasattr(e, "is_emergency")

                    other_is_tram = hasattr(entity, "is_tram")
                    other_is_emergency = hasattr(entity, "is_emergency")

                    
                    if e_is_emergency and not other_is_tram and not other_is_emergency:
                        dx_o = entity.x - e.x
                        dy_o = entity.y - e.y

                        forward = dx_o * vx + dy_o * vy
                        lateral = abs(dx_o * -vy + dy_o * vx)
                        other_offset = abs(getattr(entity, "yield_offset", 0))

                        if emergency_cautious:
                            pass
                        elif other_offset > 16 and lateral > 18:
                            continue 
                                                    
                    if not e_is_emergency and not e_is_tram and other_is_tram:
                        continue

                    if e_is_tram and not other_is_tram and not other_is_emergency:
                        continue

                    dist_approx = abs(entity.x - e.x) + abs(entity.y - e.y)

                    if dist_approx < 300:
                        candidates.append(entity)
                            
                ahead = None
                min_gap = float("inf")

                for other in candidates:
                    dx_o = other.x - e.x
                    dy_o = other.y - e.y
                    dist = math.hypot(dx_o, dy_o)

                    dot = dx_o * vx + dy_o * vy
                    lateral = abs(dx_o * -vy + dy_o * vx)

                    if hasattr(e, "is_emergency") and not hasattr(other, "is_tram"):
                        if lateral > 24:
                            continue

                    if hasattr(e, "is_tram") and hasattr(other, "is_emergency"):
                        lateral_limit = 28
                    elif hasattr(e, "is_emergency") and hasattr(other, "is_tram"):
                        lateral_limit = 28
                    elif hasattr(e, "is_tram"):
                        lateral_limit = 12
                    elif hasattr(e, "is_emergency"):
                        lateral_limit = 8
                    else:
                        lateral_limit = 22

                    
                    if dot > 0 and lateral < lateral_limit:
                        if dist < min_gap:
                            safe_distance = 60

                            if hasattr(e, "is_emergency") and not hasattr(other, "is_tram"):
                                safe_distance = 15

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
                    elif hasattr(e, "is_emergency"):
                        min_gap_safe = 10  
                    else:
                        min_gap_safe = 40 + e.length * 2
                    if hasattr(e, "is_emergency"):
                        reaction_gap = min_gap_safe + speed_self * 0.25
                    else:
                        reaction_gap = min_gap_safe + speed_self * 0.8

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

                if hasattr(e, "is_emergency"):
                    emergency_blocked = False

                    for other in sim.entities:
                        if other is e:
                            continue

                        if hasattr(other, "is_tram"):
                            continue

                        dx_o = other.x - e.x
                        dy_o = other.y - e.y

                        forward = dx_o * vx + dy_o * vy
                        lateral = abs(dx_o * -vy + dy_o * vx)
                        other_offset = abs(getattr(other, "yield_offset", 0))

                        if forward > 0 and (lateral > 20 or other_offset > 10):
                            continue

                        if is_turning_segment:
                            danger_forward = 110
                            danger_lateral = 34
                        else:
                            danger_forward = 70
                            danger_lateral = 18

                        if abs(getattr(e, "emergency_offset", 0)) > 18 and lateral > 18:
                            continue

                        if 0 < forward < danger_forward and lateral < danger_lateral:
                            emergency_blocked = True
                            break

                    if emergency_blocked:
                        if is_turning_segment:
                            speed_factor = min(speed_factor, 0.12)
                        else:
                            speed_factor = min(speed_factor, 0.25)

                front_gap = float("inf")
                front_vehicle = None

                for other in lane.vehicles:
                    if other is e:
                        continue

                    if hasattr(e, "is_emergency") and not hasattr(other, "is_tram") and not hasattr(other, "is_emergency"):
                        dx_o = other.x - e.x
                        dy_o = other.y - e.y

                        other_forward = dx_o * vx + dy_o * vy
                        other_lateral = abs(dx_o * -vy + dy_o * vx)

                        if other_forward > 0 and other_lateral > 24:
                            continue

                    if other.progress <= e.progress:
                        continue

                    gap = (other.progress - e.progress) * lane.length

                    if gap < front_gap:
                        front_gap = gap
                        front_vehicle = other

                min_lane_gap = 35

                if hasattr(e, "is_bus") or (front_vehicle and hasattr(front_vehicle, "is_bus")):
                    min_lane_gap = 55

                if hasattr(e, "is_tram") or (front_vehicle and hasattr(front_vehicle, "is_tram")):
                    min_lane_gap = 90

                if hasattr(e, "is_emergency"):
                    min_lane_gap = 22

                if front_vehicle and front_gap < min_lane_gap:
                    e.is_stopped = True
                    e.current_speed = 0
                    speed_factor = 0.0


                if not e.is_stopped:
                    effective_speed = e.current_speed * speed_factor

                    e.progress += (effective_speed * dt / lane.length)
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

                        base_x = x1 + (x2 - x1) * t
                        base_y = y1 + (y2 - y1) * t

                        offset = getattr(e, "yield_offset", 0)

                        if hasattr(e, "is_emergency"):
                            if not hasattr(e, "emergency_offset"):
                                e.emergency_offset = 0

                            target_emergency_offset = 0

                            closest_blocker = None
                            closest_forward = float("inf")
                            blocker_lateral = 0

                            for other in sim.entities:
                                if other is e:
                                    continue

                                if hasattr(other, "is_tram"):
                                    continue

                                dx_o = other.x - e.x
                                dy_o = other.y - e.y

                                forward = dx_o * vx + dy_o * vy
                                lateral_signed = dx_o * -vy + dy_o * vx
                                lateral_abs = abs(lateral_signed)

                                if 0 < forward < 135 and lateral_abs < 42:
                                    if forward < closest_forward:
                                        closest_forward = forward
                                        closest_blocker = other
                                        blocker_lateral = lateral_signed

                            if closest_blocker is not None:
                                if blocker_lateral >= 0:
                                    target_emergency_offset = -26
                                else:
                                    target_emergency_offset = 26

                            else:
                                if lane.neighbors and not emergency_cautious:
                                    neighbor = lane.neighbors[0]

                                    nx, ny = neighbor.points[0]
                                    lx, ly = lane.points[0]

                                    side_to_neighbor = (nx - lx) * -vy + (ny - ly) * vx

                                    if side_to_neighbor >= 0:
                                        target_emergency_offset = 16
                                    else:
                                        target_emergency_offset = -16

                            max_emergency_step = 0.45
                            diff = target_emergency_offset - e.emergency_offset

                            if diff > max_emergency_step:
                                diff = max_emergency_step
                            elif diff < -max_emergency_step:
                                diff = -max_emergency_step

                            e.emergency_offset += diff

                            new_x = base_x + -vy * e.emergency_offset
                            new_y = base_y + vx * e.emergency_offset

                        else:
                            new_x = base_x + -vy * offset
                            new_y = base_y + vx * offset

                        e.x = new_x
                        e.y = new_y

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