import random

import simpy
import pygame
from Rider import Rider
from Elevator import Elevator
from Building import Building

RANDOM_SEED = 42
NUM_OF_ELEVATORS = 10
NUM_OF_RIDERS = 60

env = simpy.RealtimeEnvironment(initial_time=0, factor=0.3, strict=False)

elevators = []
riders = []
random.seed(RANDOM_SEED)

pygame.init()

size = width, height = 1000, 850

screen = pygame.display.set_mode(size)
display = pygame.display
image = pygame.image
event = pygame.event

for elevator_num in range(NUM_OF_ELEVATORS):
	new_elevator = Elevator('E-' + str(elevator_num), env)
	elevators.append(new_elevator)

for rider_number in range(NUM_OF_RIDERS):
	new_rider = Rider(chr(65 + rider_number), env)
	riders.append(new_rider)

new_building = Building(elevators, riders, env, screen, display, image, event)

for new_rider in riders:
	env.process(new_rider.run())

for elevator in elevators:
	env.process(elevator.run())

env.process(new_building.run())

env.run(until=10000)
