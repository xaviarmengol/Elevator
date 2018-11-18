MAX_EVEVATOR_SIZE = 4


class Elevator():

    def __init__(self, name, env):
        self.max = MAX_EVEVATOR_SIZE

        self.name = name
        self.env = env

        self.current_floor = 0
        self.destination_floor = 0
        self.riders = []
        self.stop_list = set()
        self.going_up = True
        self.still = True
        self.time_per_floor = 1
        self.time_open_doors = 1
        self.speed = [0, 100]#/ self.time_per_floor]

        self.rect = None
        self.img = None


    def add_rider(self, rider):
        self.riders.append(rider)

    def add_stop(self, stop):
        self.stop_list.add(stop) #append(stop)

    def remove_stop(self, stop):
        try:
            self.stop_list.discard(stop) #remove(stop)
        except:
            pass


    def run(self):

        while True:

            if self._there_is_stops_to_process():

                self._elevator_control()
                step = self._move_elevator()

                print(self.name, self.destination_floor, self.going_up)

                yield self.env.timeout(self.time_per_floor)

                self.current_floor += step
                self._move_riders_in_elevator()



                #yield self.env.timeout(self.time_open_doors)

            else:
                self.still = True
                yield self.env.timeout(1)


    def _there_is_stops_to_process(self):
        return self.stop_list


    def _elevator_control(self):
        """Decision logic for new destination"""

        if self.going_up:
            destination_floor = max(self.stop_list)
        else:
            destination_floor = min(self.stop_list)

        self.destination_floor = destination_floor


    def _move_elevator(self):
        """ Moving elevator up, down or not moving"""

        if self.destination_floor > self.current_floor:
            self.going_up = True
            step = +1
            self.still = False

        elif self.destination_floor < self.current_floor:
            self.going_up = False
            step = -1
            self.still = False

        else:
            self.still = True
            step = 0

        return step



    def _move_riders_in_elevator(self):

        for rider in self.riders:
            rider.current_floor = self.current_floor

