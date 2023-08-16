import pygame
import helpers

pygame.font.init()
FONT = pygame.font.SysFont(None, 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DRAWING = False
LAST_POS = (0, 0)
COLOR = WHITE
RADIUS = 7

WINDOW_WIDTH = 640
WINDOW_HEIGHT = WINDOW_WIDTH

# initializing screen
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
SCREEN.fill(BLACK)
pygame.font.init()


def screenshot(screen):
    cropped = pygame.Surface((WINDOW_WIDTH - 5, WINDOW_HEIGHT - 30))
    cropped.blit(screen, (0, 0), (0, 0, WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5))
    return cropped


def roundLine(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)


prediction = None
run = True

while run:

    events = pygame.event.wait()

    # clear screen after right click
    if events.type == pygame.MOUSEBUTTONDOWN and events.button == 3:
        SCREEN.fill(BLACK)
        prediction = None

    # quit
    if events.type == pygame.QUIT:
        run = False

    # start drawing after left click
    if events.type == pygame.MOUSEBUTTONDOWN and events.button != 3:
        pygame.draw.circle(SCREEN, COLOR, events.pos, RADIUS)
        DRAWING = True

    # stop drawing after releasing left click
    if events.type == pygame.MOUSEBUTTONUP and events.button != 3:
        DRAWING = False
        filename = "out.png"

        img = screenshot(SCREEN)
        pygame.image.save(img, filename)

        prediction = helpers.get_image_prediction(filename)

        textTBD = FONT.render("CLASSIFIED AS:" + str(prediction), True, WHITE)
        SCREEN.blit(textTBD, (350, 0))

    # start drawing line on screen if draw is true
    if events.type == pygame.MOUSEMOTION:
        if DRAWING:
            pygame.draw.circle(SCREEN, COLOR, events.pos, RADIUS)
            roundLine(SCREEN, COLOR, events.pos, LAST_POS, RADIUS)
            LAST_POS = events.pos

    pygame.display.flip()

pygame.quit()
exit()
