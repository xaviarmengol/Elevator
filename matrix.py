import random

import simpy
import pygame
from Rider import Rider
from Elevator import Elevator
from Building import Building

RANDOM_SEED = 42
NUM_OF_ELEVATORS = 4
NUM_OF_RIDERS = 100
NUM_OF_FLOORS = 8

env = simpy.RealtimeEnvironment(initial_time=0, factor=0.4, strict=False)

elevators = []
riders = []
riders_in_landing = {floor: list() for floor in range(NUM_OF_FLOORS)}
riders_in_floor = {floor: list() for floor in range(NUM_OF_FLOORS)}

random.seed(RANDOM_SEED)

pygame.init()

size = width, height = (NUM_OF_ELEVATORS + 1) * 100 + 900, (NUM_OF_FLOORS + 1) * 85 + 100

screen = pygame.display.set_mode(size)
display = pygame.display
image = pygame.image
event = pygame.event

for elevator_num in range(NUM_OF_ELEVATORS):
    new_elevator = Elevator('E-' + str(elevator_num), env)
    elevators.append(new_elevator)

for rider_number in range(NUM_OF_RIDERS):
    new_rider = Rider(str(rider_number), NUM_OF_FLOORS, env)
    riders.append(new_rider)
    riders_in_floor[0].append(new_rider)

new_building = Building(elevators, riders, riders_in_landing, riders_in_floor, env, screen, display, image, event)

for new_rider in riders:
    env.process(new_rider.run())

for elevator in elevators:
    env.process(elevator.run())

env.process(new_building.run())

env.run(until=10000)

