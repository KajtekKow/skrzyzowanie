from core.simulation import Simulation
from systems.movement_system import MovementSystem
from systems.traffic_control_system import TrafficControlSystem
from systems.spawn_system import SpawnSystem
from rendering.pygame_renderer import Renderer
from infrastructure.intersection import Intersection
import pygame

# --- INIT ---
sim = Simulation()
renderer = Renderer()

# --- INTERSECTION + LIGHTS ---
intersection = Intersection()
sim.add_intersection(intersection)

# dodanie WSZYSTKICH świateł z lane’ów
for light in intersection.lights:
    sim.add_traffic_light(light)

# --- SYSTEMS (kolejność ma znaczenie!) ---
sim.add_system(TrafficControlSystem())  # tylko update świateł
sim.add_system(SpawnSystem(0.1))        # spawn co ~1.2s
sim.add_system(MovementSystem())        # ruch

# --- LOOP ---
running = True
while running:
    sim.update(0.016)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    renderer.draw(sim)

pygame.quit()