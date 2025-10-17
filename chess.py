import pygame as py
import os

from settings import *
from sprites import *
from helpers import *

DEBUG = True


class ChessGame:

    def __init__(self):

        # assets
        self.piece_surfs = {}
        self.sounds = {}
        self.font_24 = None
        self.board_surf = None

        # window setup
        py.init()
        self.window = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        py.display.set_caption(WINDOW_NAME)
        py.display.set_icon(py.image.load(WINDOW_ICON).convert_alpha())

        # vars
        self.board = INIT_POS
        self.padding_x = (WINDOW_WIDTH - 8 * SQUARE_SIZE) // 2
        self.padding_y = (WINDOW_HEIGHT - 8 * SQUARE_SIZE) // 2
        self.clock = py.time.Clock()
        self.running = True

        # load assets
        py.mixer.init()
        self.load_piece_surfs()
        self.load_sounds()
        self.font_24 = self.load_font(24)
        self.board_surf = self.load_board_surf()

    def load_piece_surfs(self) -> None:
        try:
            for _piece_name in [
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
                _piece_path = PIECE_IMG_PATHS[_piece_name]
                _piece_surf = py.image.load(_piece_path).convert_alpha()
                self.piece_surfs[_piece_name] = py.transform.smoothscale(
                    _piece_surf, (SQUARE_SIZE, SQUARE_SIZE)
                )
            print_debug(DEBUG, f"loaded piece imgs")
        except Exception as e:
            print(f"failed to load piece img {_piece_path}: {e}")
            exit()

    def load_sounds(self) -> None:
        try:
            for _sound_name in [
                "capture",
                "castle",
                "check",
                "move",
                "promotion",
            ]:
                _sound_path = SOUND_PATHS[_sound_name]
                _sound = py.mixer.Sound(_sound_path)
                # sound.set_volume(1) # TODO: set appropriate volume
                self.sounds[_sound_name] = _sound
            print_debug(DEBUG, f"loaded sounds")
        except Exception as e:
            print(f"failed to load sound file {_sound_path}: {e}")
            exit()

    def load_font(self, font_size: int) -> py.font.Font:
        try:
            _font = py.font.Font(FONT_PATH, font_size)
            print_debug(DEBUG, f"loaded font")
            return _font
        except Exception as e:
            print(f"failed to load font {FONT_PATH}: {e}")
            exit()

    def load_board_surf(self) -> py.Surface:
        _board_surf = py.Surface((8 * SQUARE_SIZE, 8 * SQUARE_SIZE), py.SRCALPHA)
        return _board_surf

    def draw_mouse_pointer(self) -> None:
        _pointer_size = 7
        mouse_x, mouse_y = py.mouse.get_pos()
        py.draw.circle(self.window, (255, 0, 0), (mouse_x, mouse_y), _pointer_size)

        # left mouse button
        if py.mouse.get_pressed()[0]:
            py.draw.circle(self.window, (0, 255, 0), (mouse_x, mouse_y), _pointer_size)

        # right mouse button
        if py.mouse.get_pressed()[2]:
            py.draw.circle(self.window, (0, 0, 255), (mouse_x, mouse_y), _pointer_size)

    def draw_board(self) -> None:
        for _row in range(8):
            for _col in range(8):
                _color = (
                    THEMES[THEME][1] if (_row + _col) % 2 == 0 else THEMES[THEME][0]
                )

                _rect = (
                    _col * SQUARE_SIZE,
                    _row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                )

                py.draw.rect(
                    self.board_surf,
                    _color,
                    _rect,
                    border_top_left_radius=(
                        BOARD_CORNER_RADIUS if _row == 0 and _col == 0 else 0
                    ),
                    border_top_right_radius=(
                        BOARD_CORNER_RADIUS if _row == 0 and _col == 7 else 0
                    ),
                    border_bottom_left_radius=(
                        BOARD_CORNER_RADIUS if _row == 7 and _col == 0 else 0
                    ),
                    border_bottom_right_radius=(
                        BOARD_CORNER_RADIUS if _row == 7 and _col == 7 else 0
                    ),
                )
        self.window.blit(self.board_surf, (self.padding_x, self.padding_y))

    def draw_pieces(self) -> None:
        for _row_ind in range(8):
            for _col_ind in range(8):
                _piece_name = self.board[_row_ind][_col_ind]
                if _piece_name != " ":
                    _piece_surf = self.piece_surfs[_piece_name]
                    _piece_rect = _piece_surf.get_rect(
                        center=(
                            self.padding_x
                            + (_col_ind * SQUARE_SIZE)
                            + (SQUARE_SIZE / 2),
                            self.padding_y
                            + (_row_ind * SQUARE_SIZE)
                            + (SQUARE_SIZE / 2),
                        )
                    )
                    self.window.blit(_piece_surf, _piece_rect)

    def draw_fps(self) -> None:
        _fps = int(self.clock.get_fps())
        _padding = 20
        _text_surf = self.font_24.render(str(_fps), True, (0, 255, 0))
        _text_rect = _text_surf.get_rect()
        _text_rect.topright = (WINDOW_WIDTH - _padding, _padding)
        self.window.blit(_text_surf, _text_rect)

    def run(self):
        while self.running:
            for event in py.event.get():
                if event.type == py.QUIT or (
                    event.type == py.KEYDOWN and event.key == py.K_ESCAPE
                ):
                    self.running = False

            # rendering game here
            self.window.fill(BG_COLOR)

            self.draw_board()
            self.draw_pieces()
            self.draw_mouse_pointer()
            self.draw_fps()

            py.display.flip()
            self.clock.tick(GAME_FPS)  # fps

        py.quit()


if __name__ == "__main__":
    game = ChessGame()
    game.run()
