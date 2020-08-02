import pygame

from elevator_sim.animations import animation_init, animation_update
from elevator_sim.elevator_network import ElevatorNetwork
from elevator_sim.objects import Floor, Elevator


class ElevatorSim(ElevatorNetwork):
    def __init__(self, sim_floors, sim_elevator, sim_passengers, frame_rate, mode):
        super().__init__(sim_floors, sim_elevator, sim_passengers, frame_rate, mode)

    def py_animation(self):
        # If animation is enabled then initiate pygame
        animation_init(self)

    def simulation(self):
        while self.time <= 1000 or self.animation:
            if self.animation:
                for event in pygame.event.get():
                    # Checks if the user quits the application
                    if event.type == pygame.QUIT:
                        quit()

            self.new_passengers()
            # Spawns new passengers

            if self.mode == 'linear':
                self.linear_simulation()
            elif self.mode == 'first_come':
                self.first_come()
            else:
                quit()

            self.time += self.frame_rate
            self.real_time = self.time / self.frame_rate
            if self.animation:
                animation_update(self)
            self.elevator.update_position()


floor_0 = Floor('ground', 'end', 600, 350, 0.03, [])
floor_1 = Floor('1st', 'not_end', 600, 250, 0.02, [])
floor_2 = Floor('2nd', 'not-end', 600, 150, 0.02, [])
floor_3 = Floor('3rd', 'end', 600, 50, 0.02, [])
floors = [floor_0, floor_1, floor_2, floor_3]

elevator = Elevator(600, 350, -1, 10, 'leaving', 10, [])
# Elevator modes: 'idle', 'leaving', 'moving', 'turning'

passengers = []

# Example: ElevatorSim(floors, elevator, passengers, 2, 'linear').py_animation()
# Example: ElevatorSim(floors, elevator, passengers, 2, 'linear').simulation()

ElevatorSim(floors, elevator, passengers, 2, 'first_come').py_animation()
# Model modes: 'linear', 'first_come', 'point_system'
