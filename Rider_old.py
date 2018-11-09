import random

class Rider():

    def __init__(self, name, env):
        self.name = name
        self.env = env

        self.wait = random.randint(1, 5)
        self.chosen_elevator = None
        self.current_floor = 0
        self.desired_floor = random.randint(1, 7)
        self.request_elevator = False
        self.waiting = True

        self.rect = None
        self.img = None


    def run(self):

        while True:

            if not self.waiting:

                if (not self._rider_in_desired_floor()) or self.request_elevator:

                    ## Understand why this code, because in any case do the same
                    # if self.request_elevator:
                    #     yield self.env.timeout(1)
                    #
                    # elif self._rider_in_desired_floor() and not self.request_elevator and not self.chosen_elevator:
                    #     yield self.env.timeout(1)

                    yield self.env.timeout(1)

                elif self._rider_in_desired_floor():

                    # Spend some time in the floor and decide where to go next
                    time_in_floor, next_floor_to_go = self._rider_behaviour()

                    yield self.env.timeout(time_in_floor)
                    self.desired_floor = next_floor_to_go

            else:
                yield self.env.timeout(1)
                self.waiting = False


    def _rider_in_desired_floor(self):
        return self.current_floor == self.desired_floor


    def _rider_behaviour(self):
        """ Rider logic. How many time spend in the floor, and where does he go next"""

        time_in_floor = random.randint(10, 15)
        next_floor = random.randint(1, 10)

        if self.env.now > 50:
            next_floor = 0

        return time_in_floor, next_floor


    def __repr__(self):
        return str(self.name)
