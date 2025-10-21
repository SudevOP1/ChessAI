import chess, os

from simul.settings import *
from simul.sprites import *


# ====================== chess related ======================


def get_uci_move(
    chess_piece: ChessPiece,
    to_row_i: int,
    to_col_i: int,
    promotion: str | None = None,
) -> str:
    _from_row_i = chess_piece.row_i
    _from_col_i = chess_piece.col_i
    _from_sq = get_square_notation(_from_row_i, _from_col_i)
    _to_sq = get_square_notation(to_row_i, to_col_i)
    promotion = promotion.lower() if promotion else ""
    return _from_sq + _to_sq + promotion


def get_san_history(board: chess.Board) -> list[str]:
    temp_board = chess.Board()
    _san_moves = []
    for _move in board.move_stack:
        _san = temp_board.san(_move)
        _san_moves.append(_san)
        temp_board.push(_move)
    return _san_moves


# ====================== others ======================

print_colors = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "dark": "\033[90m",
    "clear": "\033[00m",
}


def print_debug(DEBUG: bool, *args, color: str = "dark", **kwargs) -> None:
    if DEBUG:
        color_code = print_colors.get(color, "")
        clear_code = print_colors["clear"]
        print(f"{color_code}[DEBUG]", *args, clear_code, **kwargs)


def get_window_board_padding() -> tuple[int, int]:
    """tells how much empty space is around the board to keep it centered"""
    return (
        (WINDOW_WIDTH - (8 * SQUARE_SIZE) - MOVES_WIDTH) // 3,
        (WINDOW_HEIGHT - 8 * SQUARE_SIZE) // 2,
    )


def get_square_center(row_i: int, col_i: int) -> tuple[int, int]:
    """gives the pixel location of the middle of a square on the board"""
    _padding_x, _padding_y = get_window_board_padding()
    return (
        _padding_x + (col_i * SQUARE_SIZE) + (SQUARE_SIZE / 2),
        _padding_y + (row_i * SQUARE_SIZE) + (SQUARE_SIZE / 2),
    )


def get_square_index(x: int, y: int) -> tuple[bool, tuple[int, int]]:
    """tells which square the a pixel is over, if its on the board"""
    _padding_x, _padding_y = get_window_board_padding()
    if (
        x < _padding_x
        or x > WINDOW_WIDTH - _padding_x
        or y < _padding_y
        or y > WINDOW_HEIGHT - _padding_y
    ):
        return False, (x, y)
    _row_i = (y - _padding_y) // SQUARE_SIZE
    _col_i = (x - _padding_x) // SQUARE_SIZE
    return True, (_row_i, _col_i)


def get_square_notation(row_i: int, col_i: int) -> str:
    """returns uci notation (e.g., 'e4') for a given board index"""
    return chr(col_i + 97) + str(8 - row_i)


def get_index_notation(square: str) -> tuple[int, int]:
    """returns board indices (row_i, col_i) for a given uci notation"""
    _col_i = ord(square[0]) - 97
    _row_i = 8 - int(square[1])
    return (_row_i, _col_i)


def save_game(board: chess.Board) -> str:
    os.makedirs(SAVED_GAMES_DIRECTORY, exist_ok=True)

    temp_board = chess.Board()
    san_moves = []
    for move in board.move_stack:
        san_moves.append(temp_board.san(move))
        temp_board.push(move)

    file_index = 1
    while True:
        filename = f"game_{file_index}.txt"
        filepath = os.path.join(SAVED_GAMES_DIRECTORY, filename)
        if not os.path.exists(filepath):
            break
        file_index += 1

    with open(filepath, "w", encoding="utf-8") as f:
        for move in san_moves:
            f.write(move + "\n")

    return filepath
