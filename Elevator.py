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
    def __init__(self, floors, elevator, passengers, time_limit, frame_rate):
        self.floors = floors
        self.elevator = elevator
        self.passengers = passengers
        self.time_limit = time_limit
        self.game_display = pygame.display.set_mode((DisplayWidth, DisplayHeight))
        self.game_clock = pygame.time.Clock()
        self.frame_rate = frame_rate
        self.animation = False
        self.time = 0

    def new_passengers(self, passenger_num):
        for floor in self.floors:
            if random.random() < floor.spawn_rate:
                possible_destinations = [x for x in self.floors if x != floor]
                passenger_num += 1
                passenger = Passenger("Passenger " + str(passenger_num), floor.name, random.choice(possible_destinations).name)
                floor.passengers.append(passenger)
                print("(" + str(self.time) + " wait), " + passenger.name + ", " + floor.name + ", " + passenger.destination)
        return passenger_num

    def message_display(self, text, font_size, text_x, text_y, colour):  # Function to simplify displaying messages
        font = pygame.font.Font("freesansbold.ttf", font_size)  # uses font module to create a font
        display_text = font.render(str(text), True, colour)  # Creates the font with the text and the colour
        self.game_display.blit(display_text, [text_x, text_y])  # Places to the x and y locations

    def animation_init(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Elevator Simulation")
        self.animation = True
        self.simulation()

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

    def simulation(self):
        passenger_num = 0
        while self.time <= 100 or self.animation:
            if self.animation:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
            passenger_num = self.new_passengers(passenger_num)
            if self.elevator.mode != 'leaving':
                for floor in self.floors:
                    if floor.y == self.elevator.y:
                        if self.elevator.mode == 'moving':

                            if floor.floor_type == 'end':

                                self.elevator.direction *= -1
                                self.elevator.speed, self.elevator.mode = 0, 'turning'

                            for passenger in self.elevator.passengers:
                                if passenger.destination == floor.name:
                                    self.elevator.speed, self.elevator.mode = 0, 'stationary'

                            if len(floor.passengers) != 0:
                                self.elevator.speed, self.elevator.mode = 0, 'stationary'

                        elif self.elevator.mode == 'stationary':
                            all_elevator_alight = True
                            all_elevator_board = True
                            leaving_passengers = []

                            for elevator_passenger in self.elevator.passengers:
                                if elevator_passenger.destination == floor.name:
                                    leaving_passengers.append(elevator_passenger)

                            if len(leaving_passengers) >= 1:
                                all_elevator_alight = False
                                for leaving_passenger in leaving_passengers:
                                    self.elevator.passengers.remove(leaving_passenger)
                                    print("(" + str(self.time) + " alight), " + leaving_passenger.name + ", " + floor.name + ", " + leaving_passenger.destination)
                                    break

                            if all_elevator_alight:
                                for floor_passenger in floor.passengers:
                                    if len(self.elevator.passengers) < self.elevator.capacity:
                                        all_elevator_board = False
                                        self.elevator.passengers.append(floor_passenger)
                                        floor.passengers.remove(floor_passenger)
                                        print("(" + str(self.time) + " board), " + floor_passenger.name + ", " + floor.name + ", " + floor_passenger.destination)
                                        break
                                    elif len(self.elevator.passengers) == self.elevator.capacity:
                                        all_elevator_board = True

                            if all_elevator_alight and all_elevator_board:
                                self.elevator.speed, self.elevator.mode = 10, 'leaving'

                        elif self.elevator.mode == 'turning':
                            self.elevator.speed, self.elevator.mode = 10, 'leaving'
            else:
                self.elevator.mode = 'moving'

            self.time += self.frame_rate
            if self.animation:
                self.animation_update()
            self.elevator.update_position()


floor_0 = Floor('ground', 'end', 600, 300, 0.08, [])
floor_1 = Floor('1st', 'not_end', 600, 200, 0.08, [])
floor_2 = Floor('2st', 'end', 600, 100, 0.08, [])
floors_1 = [floor_0, floor_1, floor_2]

elevator_1 = Elevator(600, 300, -1, 5, 'leaving', 10, [])
# elevator.mode = ['leaving','moving','stationary','turning']

passengers_1 = []

Model_1 = ElevatorNetwork(floors_1, elevator_1, passengers_1, 100, 2)

Model_1.animation_init()


"""and (len(elevator_1.passengers) != 0 or floor.passengers != 0) or :
                for elevator_passenger in elevator_1.passengers:
                    if elevator_passenger.destination == floor.name:
                        elevator_stop = True
                if len(floor.passengers) != 0:
                    elevator_stop = True
                if elevator_1.mode == 'moving' and elevator_stop:
                    elevator_1.speed, elevator_mode = 0, 'stationary'
                    print(floor.name + ' floor reached!')
                    time += 1
                if elevator_1.mode == 'stationary':
                    for elevator_passenger in elevator_1.passengers:
                        if elevator_passenger.destination == floor.name:
                            elevator_1.passengers.remove(elevator_passenger)
                            time += 1
                    if len(elevator_1.passengers) < elevator_1.capacity:
                        for floor_passenger in floor.passengers:
                            elevator_1.passengers.append(floor_passenger)
                            time += 1
                    time += 1
                    if floor.floor_type == 'end':
                        elevator_1.direction *= -1
                    elevator_1.speed = 1
                    elevator_1.mode = 'moving'"""