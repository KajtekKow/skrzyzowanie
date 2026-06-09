from core.simulation import Simulation
from systems.movement_system import MovementSystem
from systems.traffic_control_system import TrafficControlSystem
from systems.spawn_system import SpawnSystem
from rendering.pygame_renderer import Renderer
from infrastructure.intersection import Intersection
from systems.stats_system import StatsSystem
import pygame


sim = Simulation()
renderer = Renderer()
stats = StatsSystem()


intersection = Intersection()
sim.add_intersection(intersection)

for light in intersection.lights:
    sim.add_traffic_light(light)

sim.add_system(stats)
sim.add_system(TrafficControlSystem())
sim.add_system(SpawnSystem(1.2))        
sim.add_system(MovementSystem())        

running = True

clock = pygame.time.Clock()
FIXED_DT = 1 / 60
accumulator = 0.0
MAX_SUBSTEPS = 5

while running:
    
    frame_dt = clock.tick(60) / 1000.0
    frame_dt = min(frame_dt, 0.10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if sim.sim_time >= 24 * 3600:
        print("Koniec symulacji (24h)")
        running = False
        break

    if sim.time_scale < 50:
        accumulator += frame_dt

        substeps = 0
        while accumulator >= FIXED_DT and substeps < MAX_SUBSTEPS:
            sim.update(FIXED_DT)
            accumulator -= FIXED_DT
            substeps += 1

        if substeps == MAX_SUBSTEPS:
            accumulator = 0.0

        renderer.draw(sim)

    else:
        if sim.time_scale >= 1000:
            steps = 120
        elif sim.time_scale >= 100:
            steps = 40
        else:
            steps = 4

        for _ in range(steps):
            sim.update(FIXED_DT)

pygame.quit()