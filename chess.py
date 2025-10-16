import pygame as py
from settings import *

# py setup
py.init()
screen = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = py.time.Clock()
running = True

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # rendering game here
    screen.fill("black")
    mouse_x, mouse_y = py.mouse.get_pos()
    py.draw.circle(screen, (255, 0, 0), (mouse_x, mouse_y), 20)

    py.display.flip()
    clock.tick(GAME_FPS) # fps

py.quit()

