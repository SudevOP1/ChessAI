import pygame as py
import chess

from simul.settings import *
from simul.sprites import *
from simul.helpers import *

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
        self.board = chess.Board() if INIT_POS == "" else chess.Board(INIT_POS)
        self.clock = py.time.Clock()
        self.running = True
        self.held_piece: ChessPiece | None = None
        self.promotion_query: dict | None = None
        self.available_moves: list[str] = [
            _move.uci() for _move in self.board.legal_moves
        ]

        # load assets
        py.mixer.init()
        self.sounds = self.load_sounds()
        self.font_24 = self.load_font(24)
        self.board_surf = self.load_board_surf()
        self.piece_surfs = self.load_piece_surfs()
        self.pieces = self.load_pieces()
        self.moves_bg_surf = self.load_moves_bg_surf()

    def run(self):
        while self.running:
            for event in py.event.get():

                # quit
                if event.type == py.QUIT or (
                    event.type == py.KEYDOWN and event.key == py.K_ESCAPE
                ):
                    self.running = False
                    break

                # mouse pressed
                if event.type == py.MOUSEBUTTONDOWN:

                    # start dragging piece
                    if event.button == 1 and self.promotion_query is None:
                        for _piece in self.pieces.sprites():
                            if _piece.rect.collidepoint(event.pos):
                                self.held_piece = _piece
                                # put held piece at the end of self.pieces to render on top of other pieces
                                self.pieces.remove(_piece)
                                self.pieces.add(_piece)
                                break

                    # promotion query clicked
                    if event.button == 1 and self.promotion_query is not None:
                        _promotion_pieces = ["Q", "R", "B", "N", "q", "r", "b", "n"]
                        for _piece_name, _btn_rect in self.promotion_query[
                            "btns_rects"
                        ].items():
                            if (
                                _btn_rect.collidepoint(event.pos)
                                and _piece_name in _promotion_pieces
                            ):
                                promotion_ok = self.handle_promotion(_piece_name)
                                if promotion_ok:
                                    break

                    # promotion query closed
                    if event.button == 1 and self.promotion_query is not None:
                        _close_btn_rect = self.promotion_query["btns_rects"]["close"]
                        if _close_btn_rect and _close_btn_rect.collidepoint(event.pos):
                            self.reset_held_piece()
                            self.promotion_query = None

                # mouse released
                if event.type == py.MOUSEBUTTONUP:

                    # drop held piece
                    if (
                        event.button == 1
                        and self.held_piece is not None
                        and self.promotion_query is None
                    ):
                        _mouse_x, _mouse_y = event.pos
                        self.drop_held_piece(_mouse_x, _mouse_y)

                # mouse moved
                if event.type == py.MOUSEMOTION:

                    # move held piece
                    if self.held_piece is not None:
                        _mouse_x, _mouse_y = event.pos
                        self.held_piece.rect.centerx = _mouse_x
                        self.held_piece.rect.centery = _mouse_y

            # rendering game here
            self.window.fill(BG_COLOR)

            self.draw_board()
            self.draw_available_moves()
            self.draw_pieces()
            self.draw_moves()
            self.draw_promotion_query()
            self.draw_fps()

            py.display.flip()
            self.clock.tick(GAME_FPS)  # fps

        py.quit()

    # ====================== load functions ======================

    def load_piece_surfs(self) -> dict[str, py.Surface]:
        try:
            _piece_surfs = {}
            for _piece_name in PIECE_NAMES:
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
        _board_matrix = [
            [
                str(self.board.piece_at(chess.square(file, 7 - rank)) or " ")
                for file in range(8)
            ]
            for rank in range(8)
        ]
        for _row_i in range(8):
            for _col_i in range(8):
                _piece_name = _board_matrix[_row_i][_col_i]
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
                _sound_path = SOUNDS[_sound_name]["path"]
                _sound = py.mixer.Sound(_sound_path)
                _sound.set_volume(SOUNDS[_sound_name]["volume"])
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

    def load_moves_bg_surf(self) -> py.Surface:
        _surf = py.Surface((MOVES_WIDTH, 8 * SQUARE_SIZE), py.SRCALPHA)
        return _surf

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
        for sprite in self.pieces.sprites():
            sprite: ChessPiece  # typecasting
            if self.promotion_query is None or sprite is not self.held_piece:
                sprite.draw(self.window)

    def draw_fps(self) -> None:
        _fps = int(self.clock.get_fps())
        _text_surf = self.font_24.render(str(_fps), True, (0, 255, 0))
        _text_rect = _text_surf.get_rect()
        _text_rect.topright = (WINDOW_WIDTH - FPS_PADDING, FPS_PADDING)
        self.window.blit(_text_surf, _text_rect)

    def draw_promotion_query(self) -> None:
        if self.promotion_query is not None:
            _color_white = self.promotion_query["color_white"]
            _reverse = 1 if _color_white else -1
            _to_col_i = self.promotion_query["to_col_i"]
            _to_row_i = self.promotion_query["to_row_i"]

            _promotion_pieces = ["Q", "R", "B", "N"]
            if not _color_white:
                _promotion_pieces = [_piece.lower() for _piece in _promotion_pieces]

            for _idx, _piece in enumerate(_promotion_pieces):
                _piece_surf = self.piece_surfs[_piece]
                if "btns_rects" not in self.promotion_query.keys():
                    self.promotion_query["btns_rects"] = {}
                if _piece not in self.promotion_query["btns_rects"].keys():
                    self.promotion_query["btns_rects"][_piece] = _piece_surf.get_rect(
                        center=get_square_center(_to_row_i + _reverse * _idx, _to_col_i)
                    )
                _piece_rect = self.promotion_query["btns_rects"][_piece]
                py.draw.rect(self.window, PROMOTION_QUERY_BG_COLOR, _piece_rect)
                self.window.blit(_piece_surf, _piece_rect)

            # close btn
            if "close" not in self.promotion_query["btns_rects"].keys():
                self.promotion_query["btns_rects"]["close"] = self.get_close_btn_rect(
                    _to_row_i, _to_col_i, _reverse
                )
            _close_btn_rect = self.promotion_query["btns_rects"]["close"]
            _close_btn_text_surf = self.font_24.render(
                "X", True, PROMOTION_QUERY_CLOSE_BTN_COLOR
            )
            py.draw.rect(
                self.window,
                PROMOTION_QUERY_CLOSE_BTN_BG_COLOR,
                _close_btn_rect,
            )
            self.window.blit(
                _close_btn_text_surf,
                _close_btn_text_surf.get_rect(center=_close_btn_rect.center),
            )

    def draw_available_moves(self) -> None:
        if self.held_piece is None:
            return
        for _move in self.available_moves:
            _from_square_notation = _move[0:2]
            if _from_square_notation == get_square_notation(
                self.held_piece.row_i, self.held_piece.col_i
            ):
                _to_square_notation = _move[2:4]
                _to_row_i, _to_col_i = get_index_notation(_to_square_notation)
                _square_center = get_square_center(_to_row_i, _to_col_i)
                _color = (
                    AVAILABLE_MOVES_INDICATOR_COLOR
                    if self.get_piece_at_square_center(_square_center) is None
                    else AVAILABLE_MOVES_CAPTURE_INDICATOR_COLOR
                )
                _radius = (
                    AVAILABLE_MOVES_INDICATOR_RADIUS
                    if self.get_piece_at_square_center(_square_center) is None
                    else AVAILABLE_MOVES_CAPTURE_INDICATOR_RADIUS
                )
                py.draw.circle(
                    self.window,
                    _color,
                    _square_center,
                    _radius,
                )

    def draw_moves(self) -> None:
        _padding_x, _padding_y = get_window_board_padding()
        _topleft = (
            (8 * SQUARE_SIZE) + 2 * _padding_x,
            _padding_y,
        )
        _rect = py.Rect(0, 0, MOVES_WIDTH, 8 * SQUARE_SIZE)
        py.draw.rect(
            self.moves_bg_surf,
            MOVES_BG_COLOR,
            _rect,
            border_radius=BOARD_CORNER_RADIUS,
        )
        self.window.blit(self.moves_bg_surf, _topleft)

        for _idx, _move in enumerate(get_san_history(self.board)):
            _text_surf = self.font_24.render(_move, True, MOVES_COLOR)
            _text_rect = _text_surf.get_rect()
            _text_rect.topleft = (
                _topleft[0] + (MOVE_PADDING_X if (_idx % 2 == 0) else MOVES_WIDTH // 2),
                _topleft[1] + MOVE_PADDING_Y + (_idx // 2) * self.font_24.get_height(),
            )
            self.window.blit(_text_surf, _text_rect)

    # ====================== chess handling functions ======================

    def drop_held_piece(self, _mouse_x: int, _mouse_y: int) -> None:
        _square_index_ok, (_to_row_i, _to_col_i) = get_square_index(_mouse_x, _mouse_y)
        _to_square_center = get_square_center(_to_row_i, _to_col_i)
        _from_row_i = self.held_piece.row_i
        _from_col_i = self.held_piece.col_i
        if not (
            _square_index_ok
            and not (_from_col_i == _to_col_i and _from_row_i == _to_row_i)
        ):
            self.reset_held_piece()
            return

        # handling promotion
        if (self.held_piece.name == "P" and _to_row_i == 0 and self.board.turn) or (
            self.held_piece.name == "p" and _to_row_i == 7 and not self.board.turn
        ):
            for _move in self.available_moves:
                if len(_move) == 5:
                    self.promotion_query = {
                        "color_white": True if self.held_piece.name == "P" else False,
                        "to_col_i": _to_col_i,
                        "to_row_i": _to_row_i,
                        "piece": self.held_piece,
                    }
                    return

        _uci_move = get_uci_move(self.held_piece, _to_row_i, _to_col_i)
        if _uci_move not in self.available_moves:
            self.reset_held_piece()
            return
        _move_obj = chess.Move.from_uci(_uci_move)

        if self.board.is_castling(_move_obj):
            self.handle_castling(_uci_move)
            return

        if self.board.is_en_passant(_move_obj):
            self.handle_en_passant(_uci_move)
            return

        self.make_confirmed_move(_uci_move)

        _captured_piece = self.get_piece_at_square_center(_to_square_center)
        if _captured_piece is not None:
            self.pieces.remove(_captured_piece)

        self.held_piece.rect.center = _to_square_center
        self.held_piece.row_i = _to_row_i
        self.held_piece.col_i = _to_col_i
        self.held_piece = None

        # playing sound here
        if _captured_piece is not None:
            self.play_sound("capture")
        else:
            self.play_sound("move")

    def handle_promotion(self, piece_name: str) -> bool:
        _to_row_i = self.promotion_query["to_row_i"]
        _to_col_i = self.promotion_query["to_col_i"]
        _pawn_piece = self.promotion_query["piece"]
        _to_square_center = get_square_center(_to_row_i, _to_col_i)

        _uci_move = get_uci_move(
            _pawn_piece,
            _to_row_i,
            _to_col_i,
            piece_name,
        )
        if _uci_move not in self.available_moves:
            return False
        self.make_confirmed_move(_uci_move)

        _captured_piece = self.get_piece_at_square_center(_to_square_center)
        if _captured_piece is not None:
            self.pieces.remove(_captured_piece)
        self.pieces.remove(self.held_piece)
        self.held_piece = None
        self.promotion_query = None

        self.play_sound("promotion")
        self.pieces.add(
            ChessPiece(
                self.piece_surfs[piece_name],
                _to_col_i,
                _to_row_i,
                piece_name,
                center=_to_square_center,
            )
        )
        return True

    def handle_castling(self, _uci_move: str) -> None:
        _castling_handler = {
            "e1g1": {
                "king_from": "e1",
                "king_to": "g1",
                "rook_from": "h1",
                "rook_to": "f1",
            },
            "e1c1": {
                "king_from": "e1",
                "king_to": "c1",
                "rook_from": "a1",
                "rook_to": "d1",
            },
            "e8g8": {
                "king_from": "e8",
                "king_to": "g8",
                "rook_from": "h8",
                "rook_to": "f8",
            },
            "e8c8": {
                "king_from": "e8",
                "king_to": "c8",
                "rook_from": "a8",
                "rook_to": "d8",
            },
        }

        _king_to_square = _castling_handler[_uci_move]["king_to"]
        _rook_to_square = _castling_handler[_uci_move]["rook_to"]

        _king_from_row_i, _king_from_col_i = get_index_notation(
            _castling_handler[_uci_move]["king_from"]
        )
        _rook_from_row_i, _rook_from_col_i = get_index_notation(
            _castling_handler[_uci_move]["rook_from"]
        )
        _king_to_row_i, _king_to_col_i = get_index_notation(_king_to_square)
        _rook_to_row_i, _rook_to_col_i = get_index_notation(_rook_to_square)

        _king_piece = next(
            (
                _piece
                for _piece in self.pieces
                if _piece.row_i == _king_from_row_i and _piece.col_i == _king_from_col_i
            ),
            None,
        )
        _rook_piece = next(
            (
                _piece
                for _piece in self.pieces
                if _piece.row_i == _rook_from_row_i and _piece.col_i == _rook_from_col_i
            ),
            None,
        )

        _king_piece.row_i, _king_piece.col_i = get_index_notation(_king_to_square)
        _rook_piece.row_i, _rook_piece.col_i = get_index_notation(_rook_to_square)
        _king_piece.rect.center = get_square_center(_king_to_row_i, _king_to_col_i)
        _rook_piece.rect.center = get_square_center(_rook_to_row_i, _rook_to_col_i)
        self.held_piece = None

        self.make_confirmed_move(_uci_move)
        self.play_sound("castle")

    def handle_en_passant(self, _uci_move: str) -> None:
        _to_row_i, _to_col_i = get_index_notation(_uci_move[2:4])
        direction = 1 if self.held_piece.name == "P" else -1

        _captured_center = get_square_center(_to_row_i + direction, _to_col_i)
        _captured_piece = self.get_piece_at_square_center(_captured_center)
        self.pieces.remove(_captured_piece)

        self.held_piece.rect.center = get_square_center(_to_row_i, _to_col_i)
        self.held_piece.row_i = _to_row_i
        self.held_piece.col_i = _to_col_i

        self.make_confirmed_move(_uci_move)
        self.play_sound("capture")
        self.held_piece = None

    def make_confirmed_move(self, uci_move: str) -> None:
        print_debug(DEBUG, f"move made: {uci_move}")
        self.board.push_uci(uci_move)
        self.available_moves = [_move.uci() for _move in self.board.legal_moves]
        if self.board.is_game_over():
            pass

    # ====================== other functions ======================

    def play_sound(self, sound_name: str) -> None:
        self.sounds[sound_name].play()

    def get_piece_at_square_center(
        self, to_square_center: tuple[int, int]
    ) -> ChessPiece | None:
        for _piece in self.pieces.sprites():
            if (_piece is not self.held_piece) and _piece.rect.collidepoint(
                to_square_center
            ):
                return _piece
        return None

    def get_close_btn_rect(self, to_row_i: int, to_col_i: int, reverse: int) -> py.Rect:
        _close_btn_rect = py.Rect(0, 0, SQUARE_SIZE, PROMOTION_QUERY_CLOSE_BTN_HEIGHT)
        _close_btn_rect.center = get_square_center(to_row_i + reverse * 4, to_col_i)
        _close_btn_rect.centery -= reverse * _close_btn_rect.height // 2
        return _close_btn_rect

    def reset_held_piece(self):
        if self.held_piece is not None:
            self.held_piece.rect.center = get_square_center(
                self.held_piece.row_i, self.held_piece.col_i
            )
            self.held_piece = None
