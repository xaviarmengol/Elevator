import sys
import time
import random
import pygame
import copy

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

class Building():
    
    def __init__(self, elevators, riders, riders_in_landing, riders_in_floor, env, screen, display, image, event):

        self.elevators = elevators
        self.riders = riders
        self._riders_in_landing = riders_in_landing
        self._riders_in_floor = riders_in_floor
        self.env = env
        self.screen = screen
        self._screen_x, self._screen_y = screen.get_size()
        self.display = display
        self.image = image
        self.event = event


        for elevator in elevators:
            elevator_img = image.load("elevator.bmp")
            ele_rect = elevator_img.get_rect()
            ele_rect.y = self._screen_y - 100
            ele_rect.x = 100 * elevators.index(elevator)
            elevator.rect = ele_rect
            elevator.img = elevator_img

        self.riders_x_start_location = 100 * (len(elevators) + 0.5)

        #colors = [(random.randint(0,155),random.randint(0,155),random.randint(0,155)) for _ in range(len(self.riders))]
        colors = [(0,0,255), (0,255,255), (255,0,0), (0,255,0), (255,0,255)]
        for count, rider in enumerate(riders):
            #rider_img = image.load("stick_"+str(count % 4)+".bmp")
            rider_img = image.load("stick_1.bmp")
            rider_img = colorize(rider_img, colors[count%5])
            rider_rect = rider_img.get_rect()
            rider.rect = rider_rect
            rider.rect.y = self._screen_y - 80
            rider.img = rider_img

    def run(self):

        while True:

            for event in self.event.get():
                if event.type == pygame.QUIT: sys.exit()

            color_fill = 255, 255, 255
            self.screen.fill(color_fill)


            for ele in self.elevators:

                self._move_riders_into_elevator(ele)

                self._move_elevator_and_his_riders(ele)

                self.screen.blit(ele.img, ele.rect)

                message = '{} at {} with stops {} has riders: {}'.format(ele.name, ele.current_floor, ele.stop_list, [str(rider) for rider in ele.riders])
                print(message)

            for rider in self.riders:


                if not rider.request_elevator and not rider.chosen_elevator and rider.current_floor != rider.desired_floor:
                    # In landing and has not chosen elevator

                    rider.request_elevator = True

                    best_elevator = self._choose_best_elevator(rider)
                    best_elevator.add_stop(rider.current_floor)
                    rider.chosen_elevator = best_elevator

                    if rider in self._riders_in_floor[rider.current_floor]:
                        self._riders_in_floor[rider.current_floor].remove(rider)
                        self._riders_in_landing[rider.current_floor].append(rider)


                elif rider.request_elevator and rider.chosen_elevator and rider.current_floor != rider.desired_floor:
                    # In landing waiting for the elevator

                    rider.rect.x = self.riders_x_start_location + self._riders_in_landing[rider.current_floor].index(rider) * 30
                    self.screen.blit(rider.img, rider.rect)

                elif not rider.request_elevator and not rider.chosen_elevator and rider.current_floor == rider.desired_floor:
                    # In plant, doing something

                    rider.rect.x = self.riders_x_start_location + 200 + self._riders_in_floor[rider.current_floor].index(rider) * 30
                    #rider.rect.x = self.riders_x_start_location + self._riders_in_floor[rider.current_floor].index(rider) * 20
                    self.screen.blit(rider.img, rider.rect)


                elif rider.chosen_elevator and rider.current_floor == rider.desired_floor:
                    # Just arrived to the plant

                    rider.chosen_elevator.riders.remove(rider)
                    rider.chosen_elevator.remove_stop(rider.current_floor)
                    rider.chosen_elevator = None
                    self._riders_in_floor[rider.current_floor].append(rider)


                elif rider.chosen_elevator and rider.current_floor != rider.desired_floor:# and rider.request_elevator :
                    # In the elevator
                    self.screen.blit(rider.img, rider.rect)

                    pass

                else:
                    assert False

                #print(rider.name, "at", rider.current_floor, 'request elev', rider.request_elevator, "wants to go to", rider.desired_floor)


            self.display.flip()
            yield self.env.timeout(1)


    def _move_riders_into_elevator(self, ele):

        for rider in self.riders:

            if rider.chosen_elevator == ele and ele.current_floor == rider.current_floor and rider.request_elevator:
                # Rider enter to the elevator and push floor button

                ele.remove_stop(rider.current_floor)

                if len(ele.riders) < ele.max:

                    rider.request_elevator = False
                    ele.add_rider(rider)
                    ele.add_stop(rider.desired_floor)

                    self._riders_in_landing[rider.current_floor].remove(rider)

                else:
                    print(ele.name, 'Can not take', rider.name)
                    rider.request_elevator = False
                    rider.chosen_elevator = None
                    #best_elevator = random.choice(self.elevators)#self._choose_best_elevator(rider)
                    #best_elevator.add_stop(rider.current_floor)
                    #rider.chosen_elevator = best_elevator


    def _move_elevator_and_his_riders(self, ele):

        if ele.still:
            pass
            ## ele.rect = ele.rect.move([0, 0])

        elif ele.going_up:
            ele.rect = ele.rect.move([ele.speed[0], ele.speed[1] * -1])

        elif not ele.going_up:
            ele.rect = ele.rect.move([ele.speed[0], ele.speed[1]])

        for rider in ele.riders:
            rider.rect.x = ele.rect.x + ele.riders.index(rider)*10
            rider.rect.y = ele.rect.y + 25


    def _choose_best_elevator(self, rider):

        best = copy.copy(self.elevators[0])
        best_score = -10000

        for elevator in self.elevators:

            ele_score = 0
            if ((elevator.going_up and elevator.current_floor <= rider.current_floor and elevator.current_floor < rider.desired_floor) or
            (not elevator.going_up and elevator.current_floor >= rider.current_floor and elevator.current_floor > rider.desired_floor)):
                ele_score += 200

            if len(elevator.stop_list):
                ele_score -= (len(elevator.stop_list) * 4)

            ele_score -= abs(elevator.current_floor - rider.desired_floor)*10

            #print('ele_score: ', elevator.name, ele_score)

            if ele_score > best_score:
                best = elevator
                best_score = ele_score
                #print('best_elevator: ', best.name)

        return best



def colorize(image, new_color):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(new_color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image