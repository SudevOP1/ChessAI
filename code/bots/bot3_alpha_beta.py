import chess

from code.bots.common import *


def bot_alpha_beta(board: chess.Board, depth: int = 3) -> str:
    """
    chooses the best move for the current player using a depth-limited minimax search with alpha-beta pruning
    returns the selected move in uci string
    """
    _best_move: chess.Move | None = None
    _best_move_eval = NEG_INF

    for _move in board.legal_moves:
        _temp_board = board.copy()
        _temp_board.push(_move)
        _eval = -search(_temp_board, depth)
        if _best_move is None or _best_move_eval < _eval:
            _best_move = _move
            _best_move_eval = _eval

    return _best_move.uci()


def search(
    board: chess.Board,
    depth: int,
    alpha: int = NEG_INF,
    beta: int = POS_INF,
) -> int:
    """
    recursively evaluates the board using negamax with alpha-beta pruning
    returns the best evaluation score from the perspective of the current player
    """

    if depth == 0:
        return calc_eval(board)

    # checkmate or draw
    if board.is_game_over():
        if board.is_checkmate():
            return NEG_INF
        return 0

    for _move_obj in list(board.legal_moves):
        _temp_board = board.copy()
        _temp_board.push(_move_obj)
        _eval = -search(_temp_board, depth - 1, -beta, -alpha)
        if _eval >= beta:
            return beta
        alpha = max(alpha, _eval)

    return alpha
