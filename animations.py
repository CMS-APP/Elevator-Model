import pygame

DisplayWidth = 1280
DisplayHeight = 720
white = (255, 255, 255)
black = (0, 0, 0)


def animation_init(self):
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Elevator Simulation")
    self.elevator.image = pygame.image.load('lift.png')
    self.elevator.image = pygame.transform.scale(self.elevator.image, (100, 100))
    self.game_display = pygame.display.set_mode((DisplayWidth, DisplayHeight))
    self.game_clock = pygame.time.Clock()
    self.animation = True
    self.simulation()


def message_display(self, text, font_size, text_x, text_y, colour):  # Function to simplify displaying messages
    font = pygame.font.Font("freesansbold.ttf", font_size)  # uses font module to create a font
    display_text = font.render(str(text), True, colour)  # Creates the font with the text and the colour
    self.game_display.blit(display_text, [text_x, text_y])  # Places to the x and y locations


def animation_update(self):
    self.game_display.fill(white)
    for floor in self.floors:
        pygame.draw.rect(self.game_display, black, (floor.x - 100, floor.y + 90, 100, 10))
        message_display(self, floor.name, 20, floor.x - 75, floor.y + 70, black)
        for passenger in range(len(floor.passengers)):
            pygame.draw.rect(self.game_display, black, (floor.x - (passenger * 15) - 15, floor.y + 110, 10, 10))
    self.game_display.blit(self.elevator.image, (self.elevator.x, self.elevator.y))
    message_display(self, str(len(self.elevator.passengers)) + " / " + str(self.elevator.capacity), 20,
                         self.elevator.x + 25, self.elevator.y - 20, black)
    pygame.display.update()
    self.game_clock.tick(self.frame_rate)
