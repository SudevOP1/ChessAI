import chess

from code.bots.common import *


def bot_classic_depth(board: chess.Board, depth: int = 3) -> str:
    """
    chooses the best move by evaluating all legal moves up to a given depth using a minimax search
    returns the best move in uci string
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


def search(board: chess.Board, depth: int) -> int:
    """
    performs a depth-limited negamax search to evaluate all possible moves
    from the current board position and returns the best evaluation score
    from the perspective of the current player
    """

    if depth == 0:
        return get_eval(board)

    # checkmate or draw
    if board.is_game_over():
        if board.is_checkmate():
            return NEG_INF
        return 0

    _best_eval = NEG_INF
    for _move_obj in list(board.legal_moves):
        _temp_board = board.copy()
        _temp_board.push(_move_obj)
        _best_eval = max(_best_eval, -search(_temp_board, depth - 1))

    return _best_eval
