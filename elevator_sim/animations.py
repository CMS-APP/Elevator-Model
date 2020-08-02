import pygame

DisplayWidth = 1280
DisplayHeight = 720
white = (255, 255, 255)
black = (0, 0, 0)


def animation_init(model):
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Elevator Simulation")
    model.elevator.image = pygame.image.load('lift.png')
    model.elevator.image = pygame.transform.scale(model.elevator.image, (100, 100))
    model.game_display = pygame.display.set_mode((DisplayWidth, DisplayHeight))
    model.game_clock = pygame.time.Clock()
    model.animation = True
    model.simulation()


def message_display(model, text, font_size, text_x, text_y, colour):  # Function to simplify displaying messages
    font = pygame.font.Font("freesansbold.ttf", font_size)  # uses font module to create a font
    display_text = font.render(str(text), True, colour)  # Creates the font with the text and the colour
    model.game_display.blit(display_text, [text_x, text_y])  # Places to the x and y locations


def animation_update(model):
    model.game_display.fill(white)
    # Draw each floor
    for floor in model.floors:
        pygame.draw.rect(model.game_display, black, (floor.x - 100, floor.y + 90, 100, 10))
        message_display(model, floor.name, 20, floor.x - 75, floor.y + 70, black)
        for passenger in range(len(floor.passengers)):
            # Draw each passenger
            pygame.draw.rect(model.game_display, black, (floor.x - (passenger * 15) - 15, floor.y + 110, 10, 10))
    # Draw elevator and number of passengers inside
    model.game_display.blit(model.elevator.image, (model.elevator.x, model.elevator.y))
    message_display(model, str(len(model.elevator.passengers)) + " / " + str(model.elevator.capacity), 20,
                    model.elevator.x + 25, model.elevator.y - 20, black)
    pygame.display.update()
    model.game_clock.tick(model.frame_rate)
