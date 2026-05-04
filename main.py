from core.simulation import Simulation
from systems.movement_system import MovementSystem
from systems.traffic_control_system import TrafficControlSystem
from infrastructure.traffic_light import TrafficLight
from entities.moving_entities import Car, Bus, Tram, Pedestrian
from rendering.pygame_renderer import Renderer
from infrastructure.intersection import Intersection
import pygame

# --- INIT ---
sim = Simulation()
renderer = Renderer()

# --- TRAFFIC LIGHT ---
traffic_light = TrafficLight()

# --- SYSTEMS (kolejność ma znaczenie!) ---
sim.add_system(TrafficControlSystem(traffic_light, 0))
sim.add_system(MovementSystem())

# --- ENTITIES ---
intersection = Intersection()
intersection.spawn(sim)

# sim.add_entity(Pedestrian(850, 260))

# --- LOOP ---
running = True
while running:
    sim.update(0.016)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    renderer.draw(sim)

pygame.quit()