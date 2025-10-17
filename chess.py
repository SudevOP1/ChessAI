import pygame as py
import os

from settings import *

DEBUG = True


def main():

    board = INIT_POS
    padding_x = (WINDOW_WIDTH - 8 * SQUARE_SIZE) // 2
    padding_y = (WINDOW_HEIGHT - 8 * SQUARE_SIZE) // 2

    piece_surfs = {}
    sounds = {}
    font_24 = None
    board_surf = None

    def print_debug(*args, **kwargs) -> None:
        if DEBUG:
            print("[DEBUG]", *args, **kwargs)

    def load_piece_surfs() -> None:
        try:
            for piece_name in [
                "k",
                "q",
                "r",
                "n",
                "b",
                "p",
                "K",
                "Q",
                "R",
                "N",
                "B",
                "P",
            ]:
                piece_path = PIECE_IMG_PATHS[piece_name]
                piece_surf = py.image.load(piece_path).convert_alpha()
                piece_surfs[piece_name] = py.transform.smoothscale(
                    piece_surf, (SQUARE_SIZE, SQUARE_SIZE)
                )
            print_debug(f"loaded piece imgs")
        except Exception as e:
            print(f"failed to load piece img {piece_path}: {e}")
            exit()

    def load_sounds() -> None:
        try:
            for sound_name in [
                "capture",
                "castle",
                "check",
                "move",
                "promotion",
            ]:
                sound_path = SOUND_PATHS[sound_name]
                sound = py.mixer.Sound(sound_path)
                # sound.set_volume(1)
                sounds[sound_name] = sound
            print_debug(f"loaded sounds")
        except Exception as e:
            print(f"failed to load sound file {sound_path}: {e}")
            exit()

    def load_font(font_size: int) -> py.font.Font:
        try:
            font = py.font.Font(FONT_PATH, font_size)
            print_debug(f"loaded font")
            return font
        except Exception as e:
            print(f"failed to load font {FONT_PATH}: {e}")
            exit()

    def load_board_surf() -> py.Surface:
        board_surf = py.Surface((8 * SQUARE_SIZE, 8 * SQUARE_SIZE), py.SRCALPHA)
        return board_surf

    # window setup
    py.init()
    window = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    py.display.set_caption(WINDOW_NAME)
    py.display.set_icon(py.image.load(WINDOW_ICON).convert_alpha())

    # load assets
    py.mixer.init()
    load_piece_surfs()
    load_sounds()
    font_24 = load_font(24)
    board_surf = load_board_surf()

    clock = py.time.Clock()
    running = True

    def draw_mouse_pointer() -> None:
        py.draw.circle(window, (255, 0, 0), (mouse_x, mouse_y), 10)

        # left mouse button
        if py.mouse.get_pressed()[0]:
            py.draw.circle(window, (0, 255, 0), (mouse_x, mouse_y), 10)

        # right mouse button
        if py.mouse.get_pressed()[2]:
            py.draw.circle(window, (0, 0, 255), (mouse_x, mouse_y), 10)

    def draw_board() -> None:
        global load_board_surf
        for row in range(8):
            for col in range(8):
                color = THEMES[THEME][1] if (row + col) % 2 == 0 else THEMES[THEME][0]

                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

                py.draw.rect(
                    board_surf,
                    color,
                    rect,
                    border_top_left_radius=(
                        BOARD_CORNER_RADIUS if row == 0 and col == 0 else 0
                    ),
                    border_top_right_radius=(
                        BOARD_CORNER_RADIUS if row == 0 and col == 7 else 0
                    ),
                    border_bottom_left_radius=(
                        BOARD_CORNER_RADIUS if row == 7 and col == 0 else 0
                    ),
                    border_bottom_right_radius=(
                        BOARD_CORNER_RADIUS if row == 7 and col == 7 else 0
                    ),
                )
        window.blit(board_surf, (padding_x, padding_y))

    def draw_pieces() -> None:
        for row_ind in range(8):
            for col_ind in range(8):
                piece_name = board[row_ind][col_ind]
                if piece_name != " ":
                    piece_surf = piece_surfs[piece_name]
                    piece_rect = piece_surf.get_rect(
                        center=(
                            padding_x + (col_ind * SQUARE_SIZE) + (SQUARE_SIZE / 2),
                            padding_y + (row_ind * SQUARE_SIZE) + (SQUARE_SIZE / 2),
                        )
                    )
                    window.blit(piece_surf, piece_rect)

    def draw_fps() -> None:
        fps = int(clock.get_fps())
        text_surf = font_24.render(str(fps), True, (0, 255, 0))
        text_rect = text_surf.get_rect()
        text_rect.topright = (WINDOW_WIDTH - 20, 20)
        window.blit(text_surf, text_rect)

    while running:
        for event in py.event.get():
            if event.type == py.QUIT or (
                event.type == py.KEYDOWN and event.key == py.K_ESCAPE
            ):
                running = False
        mouse_x, mouse_y = py.mouse.get_pos()

        # rendering game here
        window.fill(BG_COLOR)

        draw_board()
        draw_pieces()
        draw_mouse_pointer()
        draw_fps()

        py.display.flip()
        clock.tick(GAME_FPS)  # fps

    py.quit()


if __name__ == "__main__":
    main()
