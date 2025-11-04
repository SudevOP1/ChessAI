import chess

from code.bots.common import *


def bot_active_square(board: chess.Board, depth: int = 4) -> str:
    global transposition_table
    _best_move, _ = search_root(board, get_eval, depth)

    if board.is_irreversible(_best_move):
        transposition_table.clear()

    return _best_move.uci()


def get_eval(board: chess.Board) -> int:
    _value = 0
    _value += calc_eval(board)
    _value += calc_active_square_eval(board)
    return _value
