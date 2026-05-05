from core.simulation import Simulation
from systems.movement_system import MovementSystem
from systems.traffic_control_system import TrafficControlSystem
from systems.spawn_system import SpawnSystem
from rendering.pygame_renderer import Renderer
from infrastructure.intersection import Intersection
import pygame


sim = Simulation()
renderer = Renderer()

intersection = Intersection()
sim.add_intersection(intersection)

for light in intersection.lights:
    sim.add_traffic_light(light)

sim.add_system(TrafficControlSystem())
sim.add_system(SpawnSystem(1.2))        
sim.add_system(MovementSystem())        

running = True

while running:
    steps = 1
    if sim.time_scale > 20: steps = 4  
    if sim.time_scale > 500: steps = 10 
    
    sub_dt = 0.016 / steps
    for _ in range(steps):
        sim.update(sub_dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    renderer.draw(sim)

pygame.quit()