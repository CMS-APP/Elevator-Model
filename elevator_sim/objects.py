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

    def update_position(self):
        self.y += self.speed * self.direction
