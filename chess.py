import pygame as py
from settings import *


def main():

    # pygame setup
    py.init()
    screen = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = py.time.Clock()
    running = True

    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

        # rendering game here
        screen.fill(BG_COLOR)

        # drawing board
        padding_x = (WINDOW_WIDTH - 8 * SQUARE_SIZE) / 2
        padding_y = (WINDOW_HEIGHT - 8 * SQUARE_SIZE) / 2
        for i in range(8):
            for j in range(8):
                # dark square
                if (i + j) % 2 == 0:
                    py.draw.rect(
                        screen,
                        DARK_COLOR,
                        (
                            padding_x + i * SQUARE_SIZE,
                            padding_y + j * SQUARE_SIZE,
                            SQUARE_SIZE,
                            SQUARE_SIZE,
                        ),
                    )
                # light square
                else:
                    py.draw.rect(
                        screen,
                        LIGHT_COLOR,
                        (
                            padding_x + i * SQUARE_SIZE,
                            padding_y + j * SQUARE_SIZE,
                            SQUARE_SIZE,
                            SQUARE_SIZE,
                        ),
                    )

        # red circle at mouse pos
        mouse_x, mouse_y = py.mouse.get_pos()
        py.draw.circle(screen, (255, 0, 0), (mouse_x, mouse_y), 20)

        py.display.flip()
        clock.tick(GAME_FPS)  # fps

    py.quit()


if __name__ == "__main__":
    main()
