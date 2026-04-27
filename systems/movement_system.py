class MovementSystem:
    def update(self, sim, dt):
        for e in sim.entities:
            if hasattr(e, "vx"):
                e.x += e.vx * dt
                e.y += e.vy * dt