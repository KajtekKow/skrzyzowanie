class MovementSystem:
    def update(self, sim, dt):
        n = sim.entities
        t_x, t_y = sim.traffic_light.x, sim.traffic_light.y
        
        for i in range(n):
            e = sim.entities[i]
            
            if hasattr(e, "lane") and e.lane is not None:
                
                if sim.traffic_light.state == "RED":
                    distance = ((t_x - e.x)**2 + (t_y - e.y)**2)**(1/2)
                    stop_threshold = (e.length * 5) * (i + 1) + 5
                                        
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
                x1, y1 = e.lane.start
                x2, y2 = e.lane.end

                e.x = x1 + (x2 - x1) * e.progress
                e.y = y1 + (y2 - y1) * e.progress