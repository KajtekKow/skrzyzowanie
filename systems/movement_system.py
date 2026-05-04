class MovementSystem:
    def update(self, sim, dt):
        for e in sim.entities:
            if hasattr(e, "lane") and e.lane is not None:

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