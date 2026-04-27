from core.simulation import Simulation
from systems.movement_system import MovementSystem
from systems.traffic_control_system import TrafficControlSystem
from infrastructure.traffic_light import TrafficLight
from entities.moving_entities import Car, Bus, Tram, Pedestrian
from rendering.pygame_renderer import Renderer
import pygame

# --- INIT ---
sim = Simulation()
renderer = Renderer()

# --- TRAFFIC LIGHT ---
traffic_light = TrafficLight()

# --- SYSTEMS (kolejność ma znaczenie!) ---
sim.add_system(TrafficControlSystem(traffic_light))
sim.add_system(MovementSystem())

# --- ENTITIES ---
sim.add_entity(Car(100, 280))
sim.add_entity(Car(100, 300))
sim.add_entity(Bus(50, 320))
sim.add_entity(Tram(0, 350))
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