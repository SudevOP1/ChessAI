import chess

from code.bots.common import *


def bot_move_ordering(board: chess.Board, depth: int = 3) -> str:
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

    if depth == 0:
        return get_eval(board)

    # checkmate or draw
    if board.is_game_over():
        if board.is_checkmate():
            return NEG_INF
        return 0

    for _move_obj in get_ordered_moves(board):
        _temp_board = board.copy()
        _temp_board.push(_move_obj)
        _eval = -search(_temp_board, depth - 1, -beta, -alpha)
        if _eval >= beta:
            return beta
        alpha = max(alpha, _eval)

    return alpha


def get_ordered_moves(board: chess.Board) -> list[chess.Move]:
    """returns all legal moves sorted by their score (highest first)"""
    _legal_moves = list(board.legal_moves)
    return sorted(_legal_moves, key=lambda m: get_move_score(board, m), reverse=True)


def get_move_score(board: chess.Board, move: chess.Move) -> int:
    """calculates a heuristic score for a move based on captures, promotions, and pawn threats to guide move ordering"""
    _move_score = 0
    _moved_piece = board.piece_at(move.from_square)
    _captured_piece = board.piece_at(move.to_square)

    if _captured_piece is not None:
        _move_score += 10 * get_piece_value(_captured_piece) - get_piece_value(
            _moved_piece
        )

    if len(move.uci()) == 5:
        _move_score += get_piece_value(move.uci()[4])

    if is_square_attacked_by_pawn(board, move.to_square):
        _move_score -= get_piece_value(_moved_piece)

    return _move_score


def is_square_attacked_by_pawn(board: chess.Board, square: chess.Square) -> bool:
    """returns True if the given square is attacked by any opposing pawn"""
    opponent_color = chess.BLACK if board.turn == chess.WHITE else chess.WHITE
    for attacker in board.attackers(opponent_color, square):
        if board.piece_type_at(attacker) == chess.PAWN:
            return True
    return False


if __name__ == "__main__":
    print(get_ordered_moves(chess.Board()))
