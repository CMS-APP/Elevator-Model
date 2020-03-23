import random
import pygame

DisplayWidth = 1280
DisplayHeight = 720
White = (255, 255, 255)
Black = (0, 0, 0)


class Passenger:
    def __init__(self, name, source, destination):
        self.name = name
        self.source = source
        self.destination = destination


class Floor:
    def __init__(self, name, floor_type, x_value, y_value, spawn_rate, passengers):
        self.name = name
        self.floor_type = floor_type
        self.x = x_value
        self.y = y_value
        self.spawn_rate = spawn_rate
        self.passengers = passengers


class Elevator:
    def __init__(self, x_value, y_value, direction, speed, mode, capacity, passengers):
        self.x = x_value
        self.y = y_value
        self.direction = direction
        self.speed = speed
        self.mode = mode
        self.capacity = capacity
        self.passengers = passengers
        self.image = pygame.image.load('lift.png')
        self.image = pygame.transform.scale(self.image, (100, 100))

    def update_position(self):
        self.y += self.speed * self.direction


class ElevatorNetwork:
    def __init__(self, floors, elevator, passengers, time_limit, frame_rate, mode):
        self.floors = floors
        self.elevator = elevator
        self.passengers = passengers
        self.time_limit = time_limit
        self.frame_rate = frame_rate
        self.mode = mode
        self.modes = ['linear', 'first_come', 'point_system']
        self.game_display = pygame.display.set_mode((DisplayWidth, DisplayHeight))
        self.game_clock = pygame.time.Clock()
        self.animation = False
        self.real_time = 0
        self.time = 0
        self.all_passengers = []
        self.elevator.target_passenger = ""
        self.elevator.target = 'ground'
        self.elevator.second_target = ''

    def animation_init(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Elevator Simulation")
        self.animation = True
        self.simulation()

    def message_display(self, text, font_size, text_x, text_y, colour):  # Function to simplify displaying messages
        font = pygame.font.Font("freesansbold.ttf", font_size)  # uses font module to create a font
        display_text = font.render(str(text), True, colour)  # Creates the font with the text and the colour
        self.game_display.blit(display_text, [text_x, text_y])  # Places to the x and y locations

    def animation_update(self):
        self.game_display.fill(White)
        for floor in self.floors:
            pygame.draw.rect(self.game_display, Black, (floor.x - 100, floor.y + 90, 100, 10))
            self.message_display(floor.name, 20, floor.x - 75, floor.y + 70, Black)
            for passenger in range(len(floor.passengers)):
                pygame.draw.rect(self.game_display, Black, (floor.x - (passenger * 15) - 15, floor.y + 110, 10, 10))
        self.game_display.blit(self.elevator.image, (self.elevator.x, self.elevator.y))
        self.message_display(str(len(self.elevator.passengers)) + " / " + str(self.elevator.capacity), 20, self.elevator.x + 25, self.elevator.y - 20, Black)
        pygame.display.update()
        self.game_clock.tick(self.frame_rate)

    def new_passengers(self, passenger_num):
        for floor in self.floors:
            if random.random() < floor.spawn_rate:
                possible_destinations = [x for x in self.floors if x != floor]
                passenger_num += 1
                passenger = Passenger("Passenger " + str(passenger_num), floor.name, random.choice(possible_destinations).name)
                floor.passengers.append(passenger)
                self.all_passengers.append(passenger)
                print("(" + str(self.real_time) + " wait), " + passenger.name + ", " + floor.name + ", " + passenger.destination)
        return passenger_num

    def stationary_events(self, floor):
        all_elevator_alight = True
        all_elevator_board = True
        leaving_passengers = []

        for elevator_passenger in self.elevator.passengers:
            if elevator_passenger.destination == floor.name:
                leaving_passengers.append(elevator_passenger)

        if len(leaving_passengers) >= 1:
            all_elevator_alight = False
            for leaving_passenger in leaving_passengers:
                self.all_passengers.remove(leaving_passenger)
                self.elevator.passengers.remove(leaving_passenger)
                if leaving_passenger.name == self.elevator.target_passenger:
                    self.elevator.target_passenger = ''
                print("(" + str(self.real_time) + " alight), " + leaving_passenger.name + ", " + floor.name + ", " + leaving_passenger.destination)
                break

        if all_elevator_alight:
            for floor_passenger in floor.passengers:
                if len(self.elevator.passengers) < self.elevator.capacity:
                    all_elevator_board = False
                    self.elevator.passengers.append(floor_passenger)
                    floor.passengers.remove(floor_passenger)
                    print("(" + str(self.real_time) + " board), " + floor_passenger.name + ", " + floor.name + ", " + floor_passenger.destination)
                    break
                elif len(self.elevator.passengers) == self.elevator.capacity:
                    all_elevator_board = True

        if all_elevator_alight and all_elevator_board:
            self.elevator.speed, self.elevator.mode = 0, 'idle'

    def linear_simulation(self):
        """ A linear simulation of an elevator, moving up and down like a bus.

        The main part of the algorithm includes
        """
        if self.elevator.mode != 'leaving':
            for floor in self.floors:
                if floor.y == self.elevator.y:
                    if self.elevator.mode == 'moving':

                        if floor.floor_type == 'end':
                            self.elevator.direction *= -1
                            self.elevator.speed, self.elevator.mode = 0, 'turning'

                        for passenger in self.elevator.passengers:
                            if passenger.destination == floor.name:
                                self.elevator.speed, self.elevator.mode = 0, 'boarding'

                        if len(floor.passengers) != 0:
                            self.elevator.speed, self.elevator.mode = 0, 'boarding'

                    elif self.elevator.mode == 'boarding':
                        self.stationary_events(floor)
                        self.elevator.speed, self.elevator.mode = 10, 'moving'

                    elif self.elevator.mode == 'turning':
                        self.elevator.speed, self.elevator.mode = 10, 'leaving'
        else:
            self.elevator.mode = 'moving'

    def first_come(self):
        """
        First come first serve algorithm
        """
        target_reached = False

        for floor in self.floors:
            if self.elevator.y == floor.y and self.elevator.target == floor.name:
                self.elevator.speed, self.elevator.mode = 0, 'boarding'
                self.stationary_events(floor)
                if self.elevator.mode == 'idle':
                    target_reached = True
                    if self.elevator.second_target != '':
                        self.elevator.target = self.elevator.second_target
                        self.elevator.second_target = ''
                        target_reached = False

        if not target_reached:
            for floor in self.floors:
                if self.elevator.target == floor.name and self.elevator.y != floor.y:
                    displacement = floor.y - self.elevator.y
                    if displacement > 0:
                        self.elevator.direction = 1
                    elif displacement < 0:
                        self.elevator.direction = -1
                    self.elevator.speed = 10
                    self.elevator.mode = 'moving'

        elif target_reached and len(self.all_passengers) != 0:
            for passenger in self.all_passengers:
                self.elevator.target_passenger = passenger.name
                self.elevator.target = passenger.source
                self.elevator.second_target = passenger.destination
                break

        elif target_reached and len(self.all_passengers) == 0:
            self.elevator.target = 'ground'
            self.elevator.second_target = ''

    def simulation(self):
        passenger_num = 0
        while self.time <= 100 or self.animation:
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
                self.animation_update()
            self.elevator.update_position()

floor_0 = Floor('ground', 'end', 600, 350, 0.03, [])
floor_1 = Floor('1st', 'not_end', 600, 250, 0.01, [])
floor_2 = Floor('2nd', 'end', 600, 150, 0.01, [])
floor_3 = Floor('3rd', 'end', 600, 50, 0.01, [])
floors_1 = [floor_0, floor_1, floor_2, floor_3]

elevator_1 = Elevator(600, 350, -1, 10, 'leaving', 10, [])
# elevator.mode = ['leaving','moving','stationary','turning']

passengers_1 = []

Model_1 = ElevatorNetwork(floors_1, elevator_1, passengers_1, 100, 2, 'first_come')
# Model.mode = ['linear', 'first come', 'point system']

Model_1.animation_init()