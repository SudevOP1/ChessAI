from settings import *


def print_debug(DEBUG, *args, **kwargs) -> None:
    if DEBUG:
        print("[DEBUG]", *args, **kwargs)


def get_window_board_padding() -> tuple[int, int]:
    """tells how much empty space is around the board to keep it centered"""
    return (
        (WINDOW_WIDTH - 8 * SQUARE_SIZE) // 2,
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
    """tells which square the mouse (or a pixel) is over, if it’s on the board"""
    _padding_x, _padding_y = get_window_board_padding()
    if (
        x < _padding_x
        or x > WINDOW_WIDTH - _padding_x
        or y < _padding_y
        or y > WINDOW_HEIGHT - _padding_y
    ):
        return False, (x, y)
    col_i = (x - _padding_x) // SQUARE_SIZE
    row_i = (y - _padding_y) // SQUARE_SIZE
    return True, (row_i, col_i)
