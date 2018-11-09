import sys
import time
import random
import pygame
import copy


class Building():
    
    def __init__(self, elevators, riders, env, screen, display, image, event):

        self.elevators = elevators
        self.riders = riders
        self.env = env
        self.screen = screen
        self.display = display
        self.image = image
        self.event = event

        for elevator in elevators:
            elevator_img = image.load("elevator.bmp")
            ele_rect = elevator_img.get_rect()
            ele_rect.y = 750
            ele_rect.x = 100 * elevators.index(elevator)
            elevator.rect = ele_rect
            elevator.img = elevator_img

        count = 0
        for rider in riders:
            rider_img = image.load("stick_"+str(count%4)+".bmp")
            rider_rect = rider_img.get_rect()
            rider.rect = rider_rect
            rider.img = rider_img
            count += 1

    def run(self):

        while True:

            for event in self.event.get():
                if event.type == pygame.QUIT: sys.exit()

            color_fill = 200, 255, 255
            self.screen.fill(color_fill)


            for ele in self.elevators:

                self._move_riders_into_elevator(ele)

                self._draw_elevator_with_riders(ele)

                message = '{} at {} with stops {} has riders: {}'.format(ele.name, ele.current_floor, ele.stop_list, [str(rider) for rider in ele.riders])
                print(message)

            for rider in self.riders:

                if not rider.request_elevator and not rider.chosen_elevator and rider.current_floor != rider.desired_floor:

                    rider.request_elevator = True

                    best_elevator = self._choose_best_elevator(rider)
                    best_elevator.add_stop(rider.current_floor)
                    rider.chosen_elevator = best_elevator

                    rider.rect.x = rider.chosen_elevator.rect.x


                elif rider.chosen_elevator and rider.current_floor == rider.desired_floor:

                    rider.chosen_elevator.riders.remove(rider)
                    rider.chosen_elevator.stop_list.remove(rider.current_floor)
                    rider.chosen_elevator = None

                elif rider.chosen_elevator and rider.current_floor != rider.desired_floor:# and rider.request_elevator :
                    self.screen.blit(rider.img, rider.rect)

                print(rider.name, "at", rider.current_floor, rider.request_elevator, "wants to go to", rider.desired_floor)
                    # elevator is choosen and picks up the next rider

            self.display.flip()
            yield self.env.timeout(1)



    def _draw_elevator_with_riders(self, ele):

        if ele.still:
            pass
            ## ele.rect = ele.rect.move([0, 0])

        elif ele.going_up:
            ele.rect = ele.rect.move([ele.speed[0], ele.speed[1] * -1])

        elif not ele.going_up:
            ele.rect = ele.rect.move([ele.speed[0], ele.speed[1]])

        for rider in ele.riders:
            rider.rect.x = ele.rect.x
            rider.rect.y = ele.rect.y + 25

        self.screen.blit(ele.img, ele.rect)


    def _move_riders_into_elevator(self, ele):

        for rider in self.riders:

            if rider.chosen_elevator == ele and ele.current_floor == rider.current_floor and rider.request_elevator:
                # Rider enter to the elevator and push floor button

                rider.request_elevator = False
                ele.add_rider(rider)
                ele.remove_stop(rider.current_floor)
                ele.add_stop(rider.desired_floor)






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

            ele_score -= abs(elevator.current_floor - rider.desired_floor)

            print('ele_score: ', elevator.name, ele_score)

            if ele_score > best_score:
                best = elevator
                best_score = ele_score
                print('best_elevator: ', best.name)

        return best

