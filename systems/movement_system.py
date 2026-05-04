class MovementSystem:
    def update(self, sim, dt, index):
        m = len(sim.intersection.lanes)
        t_x, t_y = sim.traffic_lights[0].x, sim.traffic_lights[0].y
        
        for l in range(m):
            n = len(sim.intersection.lanes[l].vehicles)
            for v in range(n):
                e = sim.intersection.lanes[l].vehicles[v]
                
                if hasattr(e, "lane") and e.lane is not None:
                    
                    if sim.traffic_lights[0].state == "RED":
                        distance = ((t_x - e.x)**2 + (t_y - e.y)**2)**(1/2)
                        stop_threshold = (e.length * 5) * (v + 1) + 10
                                            
                        if distance <= stop_threshold:
                            e.is_stopped = True
                            continue
                            
                    e.is_stopped = False
                    # zwiększamy progres
                    speed = abs(e.vx) if e.lane.direction == "horizontal" else abs(e.vy)
                    e.progress += speed * dt / 500  # skalowanie

                    # clamp
                    e.progress = min(e.progress, 1)

                    # interpolacja pozycji
                    if e.progress < 0.5:
                        # etap 1: start -> checkpoint
                        t = e.progress * 2  # skalowanie 0–0.5 → 0–1
                        x1, y1 = e.lane.start
                        x2, y2 = e.lane.checkpoint
                    else:
                        # etap 2: checkpoint -> end
                        t = (e.progress - 0.5) * 2  # skalowanie 0.5–1 → 0–1
                        x1, y1 = e.lane.checkpoint
                        x2, y2 = e.lane.end

                    e.x = x1 + (x2 - x1) * t
                    e.y = y1 + (y2 - y1) * t