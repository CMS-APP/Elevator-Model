import random

from elevator_sim.objects import Passenger


class ElevatorNetwork:
    def __init__(self, floors, elevator, passengers, frame_rate, mode):
        super().__init__()
        self.floors = floors
        self.elevator = elevator
        self.passengers = passengers
        self.frame_rate = frame_rate
        self.mode = mode
        self.modes = ['linear', 'first_come']
        self.animation = False
        self.real_time = 0
        self.time = 0
        self.all_passengers = []
        self.passenger_number = 0
        self.elevator.passenger_target = None
        self.elevator.target = None
        self.elevator.second_target = None

    def new_passengers(self):
        for floor in self.floors:
            if random.random() < floor.spawn_rate:
                self.passenger_number += 1
                possible_destinations = [x for x in self.floors if x != floor]
                passenger = Passenger(name="Passenger " + str(self.passenger_number), source=floor,
                                      destination=random.choice(possible_destinations))
                floor.passengers.append(passenger)
                self.all_passengers.append(passenger)
                print(f"( {self.real_time} wait), {passenger.name}, {floor.name}, {passenger.destination.name}")

    def stop_check(self, floor):
        if len(self.elevator.passengers) != 0:
            for passenger in self.elevator.passengers:
                if passenger.destination == floor:
                    return True

        if len(floor.passengers) != 0 and len(self.elevator.passengers) != self.elevator.capacity:
            return True

        return False

    def floor_action(self, floor):
        if len(self.elevator.passengers) != 0:
            for passenger in self.elevator.passengers:
                if passenger.destination == floor:
                    self.elevator.passengers.remove(passenger)
                    self.all_passengers.remove(passenger)
                    if self.elevator.passenger_target == passenger:
                        self.elevator.passenger_target = None
                    print(f'({self.real_time} leave), {passenger.name}, {floor.name}')
                    return

        if len(floor.passengers) != 0:
            passenger = floor.passengers[0]
            self.elevator.passengers.append(passenger)
            print(
                f'({self.real_time} board), {passenger.name}, {floor.name}, {passenger.destination.name}')
            floor.passengers.remove(floor.passengers[0])
            return

    def linear_simulation(self):
        for floor in self.floors:
            if self.elevator.y == floor.y:
                if floor.floor_type == 'end' and self.elevator.mode != 'leaving' and self.elevator.mode != 'idle':
                    self.elevator.direction *= -1
                    self.elevator.mode = 'turning'

                if self.stop_check(floor):
                    if self.elevator.mode == 'idle':
                        self.floor_action(floor)
                    else:
                        self.elevator.mode, self.elevator.speed = 'idle', 0

                elif not self.stop_check(floor):
                    self.elevator.mode, self.elevator.speed = 'leaving', 10

                if self.elevator.mode == 'leaving':
                    self.elevator.mode = 'moving'

    def first_come(self):
        if self.elevator.passenger_target is None and len(self.all_passengers) != 0:
            self.elevator.passenger_target = self.all_passengers[0]
            if self.all_passengers[0] not in self.elevator.passengers:
                self.elevator.target = self.all_passengers[0].source
                self.elevator.second_target = self.all_passengers[0].destination
            else:
                self.elevator.target, self.elevator.second_target = self.all_passengers[0].destination, None

        elif self.elevator.target is None and len(self.all_passengers) == 0:
            self.elevator.target = self.floors[0]
            if self.elevator.y == self.floors[0].y:
                self.elevator.target = None
            self.elevator.second_target = None

        for floor in self.floors:
            if self.elevator.y == floor.y:
                if floor.floor_type == 'end' and self.elevator.mode != 'leaving' and self.elevator.mode != 'idle':
                    self.elevator.direction *= -1
                    self.elevator.mode = 'turning'

                if self.stop_check(floor):
                    if self.elevator.mode == 'idle':
                        self.floor_action(floor)
                    else:
                        self.elevator.mode, self.elevator.speed = 'idle', 0

                elif not self.stop_check(floor):
                    if self.elevator.target == floor:
                        self.elevator.target, self.elevator.second_target = self.elevator.second_target, None
                    self.elevator.mode, self.elevator.speed = 'leaving', 10

                if self.elevator.mode == 'leaving':
                    self.elevator.mode = 'moving'
                    if self.elevator.target is not None:
                        displacement = self.elevator.target.y - self.elevator.y
                        if displacement > 0:
                            self.elevator.direction = 1
                        elif displacement < 0:
                            self.elevator.direction = -1
                    else:
                        self.elevator.mode, self.elevator.speed = 'idle', 0
