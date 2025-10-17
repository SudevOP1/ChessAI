import pygame as py
import os

from settings import *
from sprites import *
from helpers import *

DEBUG = True


class ChessGame:

    # ====================== main functions ======================

    def __init__(self):

        # window setup
        py.init()
        self.window = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        py.display.set_caption(WINDOW_NAME)
        py.display.set_icon(py.image.load(WINDOW_ICON).convert_alpha())

        # vars
        self.board = INIT_POS
        self.clock = py.time.Clock()
        self.running = True
        self.held_piece: py.sprite.Sprite | None = None

        # load assets
        py.mixer.init()
        self.sounds = self.load_sounds()
        self.font_24 = self.load_font(24)
        self.board_surf = self.load_board_surf()
        self.piece_surfs = self.load_piece_surfs()
        self.pieces = self.load_pieces()

    def run(self):
        while self.running:
            for event in py.event.get():

                # quit
                if event.type == py.QUIT or (
                    event.type == py.KEYDOWN and event.key == py.K_ESCAPE
                ):
                    self.running = False
                    break

                # start dragging piece
                if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    for _piece in self.pieces.sprites():
                        if _piece.rect.collidepoint(event.pos):
                            self.held_piece = _piece
                            self.pieces.remove(self.held_piece)
                            self.pieces.add(self.held_piece)

                # drop held piece
                if event.type == py.MOUSEBUTTONUP and event.button == 1:
                    if self.held_piece is not None:
                        _mouse_x, _mouse_y = event.pos
                        _square_index_ok, (_n_col_i, _n_row_i) = get_square_index(
                            _mouse_x, _mouse_y
                        )
                        _square_center = get_square_center(_n_col_i, _n_row_i)
                        if _square_index_ok:
                            self.held_piece.rect.center = _square_center
                            self.board[self.held_piece.row_i][
                                self.held_piece.col_i
                            ] = " "
                            _capture = False
                            for _piece in self.pieces.sprites():
                                if (
                                    _piece is not self.held_piece
                                    and _piece.rect.collidepoint(_square_center)
                                ):
                                    self.pieces.remove(_piece)
                                    _capture = True
                                    break
                            self.board[_n_row_i][_n_col_i] = self.held_piece.name
                            self.held_piece.row_i = _n_row_i
                            self.held_piece.col_i = _n_col_i
                            self.held_piece = None

                            if _capture:
                                self.play_sound("capture")
                            else:
                                self.play_sound("move")
                        else:
                            self.held_piece.rect.center = get_square_center(
                                self.held_piece.row_i, self.held_piece.col_i
                            )
                            self.held_piece = None

                # move held piece
                if event.type == py.MOUSEMOTION and self.held_piece is not None:
                    _mouse_x, _mouse_y = event.pos
                    self.held_piece.rect.centerx = _mouse_x
                    self.held_piece.rect.centery = _mouse_y

            # rendering game here
            self.window.fill(BG_COLOR)

            self.draw_board()
            self.draw_pieces()
            self.draw_fps()

            py.display.flip()
            self.clock.tick(GAME_FPS)  # fps

        py.quit()

    # ====================== load functions ======================

    def load_piece_surfs(self) -> dict[str, py.Surface]:
        try:
            _piece_surfs = {}
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
                _piece_surfs[_piece_name] = py.transform.smoothscale(
                    _piece_surf, (SQUARE_SIZE, SQUARE_SIZE)
                )
            print_debug(DEBUG, f"loaded piece imgs")
            return _piece_surfs
        except Exception as e:
            print(f"failed to load piece img {_piece_path}: {e}")
            exit()

    def load_pieces(self) -> py.sprite.Group:
        _pieces = py.sprite.Group()
        for _row_i in range(8):
            for _col_i in range(8):
                _piece_name = self.board[_row_i][_col_i]
                if _piece_name != " ":
                    _piece_surf = self.piece_surfs[_piece_name]
                    _pieces.add(
                        ChessPiece(
                            _piece_surf,
                            row_i=_row_i,
                            col_i=_col_i,
                            center=get_square_center(_row_i, _col_i),
                            name=_piece_name,
                        )
                    )
        return _pieces

    def load_board_surf(self) -> py.Surface:
        _board_surf = py.Surface((8 * SQUARE_SIZE, 8 * SQUARE_SIZE), py.SRCALPHA)
        return _board_surf

    def load_sounds(self) -> dict[str, py.mixer.Sound]:
        try:
            _sounds = {}
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
                _sounds[_sound_name] = _sound
            print_debug(DEBUG, f"loaded sounds")
            return _sounds
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

    # ====================== draw functions ======================

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
        _padding_x, _padding_y = get_window_board_padding()
        self.window.blit(
            self.board_surf,
            (_padding_x, _padding_y),
        )

    def draw_pieces(self) -> None:
        self.pieces.draw(self.window)

    def draw_fps(self) -> None:
        _fps = int(self.clock.get_fps())
        _padding = 20
        _text_surf = self.font_24.render(str(_fps), True, (0, 255, 0))
        _text_rect = _text_surf.get_rect()
        _text_rect.topright = (WINDOW_WIDTH - _padding, _padding)
        self.window.blit(_text_surf, _text_rect)

    # ====================== other functions ======================

    def play_sound(self, sound_name: str) -> None:
        self.sounds[sound_name].play()


if __name__ == "__main__":
    game = ChessGame()
    game.run()
