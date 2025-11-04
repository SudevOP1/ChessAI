import chess

from code.bots.common import *


def bot_pos_caching(board: chess.Board, depth: int = 4) -> str:
    global transposition_table
    _best_move, _ = search_root(board, calc_eval, depth)

    if board.is_irreversible(_best_move):
        transposition_table.clear()

    return _best_move.uci()
