import chess

from code.bots.common import *
from code.simul.settings import *


def bot_sqaure_heuristics(board: chess.Board, depth: int = 5) -> str:
    global transposition_table
    _best_move, _ = search_root(board, get_eval, depth)

    if board.is_irreversible(_best_move):
        transposition_table.clear()

    return _best_move.uci()


def get_eval(board: chess.Board) -> int:
    _value = 0
    _value += calc_eval(board)
    _value += calc_heu_eval(board)
    return _value
