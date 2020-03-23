from elevator_sim.objects import Passenger, Floor, Elevator
from elevator_sim.animations import animation_init, animation_update
from elevator_sim.elevator_network import ElevatorNetwork
import pygame


class ElevatorSim(ElevatorNetwork):
    def __init__(self, floors, elevator, passengers, time_limit, frame_rate, mode):
        super().__init__(floors, elevator, passengers, time_limit, frame_rate, mode)

    def py_animation(self):
        animation_init(self)

    def simulation(self):
        """
        """
        passenger_num = 0
        while self.time <= 1000 or self.animation:

            if self.animation:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

            passenger_num = self.new_passengers(passenger_num)

            if self.mode in self.modes:
                if self.mode == 'linear':
                    self.linear_simulation()
                elif self.mode == 'first_come':
                    self.first_come()
                else:
                    quit()
            else:
                quit()

            self.time += self.frame_rate
            self.real_time = self.time/self.frame_rate
            if self.animation:
                animation_update(self)
            self.elevator.update_position()


floor_0 = Floor('ground', 'end', 600, 350, 0.03, [])
floor_1 = Floor('1st', 'not_end', 600, 250, 0.01, [])
floor_2 = Floor('2nd', 'not-end', 600, 150, 0.01, [])
floor_3 = Floor('3rd', 'end', 600, 50, 0.01, [])
floors_1 = [floor_0, floor_1, floor_2, floor_3]

elevator_1 = Elevator(600, 350, -1, 10, 'leaving', 10, [])
# elevator.mode = ['idle','leaving','moving','turning',]

passengers_1 = []

Model_1 = ElevatorSim(floors_1, elevator_1, passengers_1, 100, 2, 'linear')
# Model.mode = ['linear', 'first come', 'point system']

Model_1.py_animation()