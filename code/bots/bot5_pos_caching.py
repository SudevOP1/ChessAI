import chess

from code.bots.common import *

"""
key     = fen
value   = (depth, score, best_move, flag)
flag    ∈ {'EXACT', 'LOWER', 'UPPER'}
"""
transposition_table: dict[str, tuple[int, int, str, str]] = {}


def bot_pos_caching(board: chess.Board, depth: int = 5) -> str:
    _best_move, _ = search_root(board, depth)
    return _best_move.uci()


def search_root(board: chess.Board, depth: int = 3) -> tuple[chess.Move, int]:
    """returns both move_obj and evaluation"""
    _best_move: chess.Move | None = None
    _best_eval = NEG_INF
    _alpha = NEG_INF
    _beta = POS_INF

    for _move in get_ordered_moves(board):
        _temp_board = board.copy()
        _temp_board.push(_move)
        _eval = -search(_temp_board, depth - 1, -_beta, -_alpha)

        if _best_move is None or _best_eval < _eval:
            _best_move = _move
            _best_eval = _eval
        _alpha = max(_alpha, _eval)

    return _best_move, _best_eval


def search(
    board: chess.Board,
    depth: int,
    alpha: int = NEG_INF,
    beta: int = POS_INF,
) -> int:
    _og_alpha = alpha
    _fen = board.fen()

    if _fen in transposition_table:
        (
            _cached_depth,
            _cached_score,
            _cached_move,
            _cached_flag,
        ) = transposition_table[_fen]
        if _cached_depth >= depth:

            if _cached_flag == "EXACT":
                return _cached_score
            elif _cached_flag == "LOWER":
                alpha = max(alpha, _cached_score)
            elif _cached_flag == "UPPER":
                beta = min(beta, _cached_score)

            if alpha >= beta:
                return _cached_score

    if depth == 0:
        return get_eval(board)

    if board.is_game_over():
        if board.is_checkmate():
            return NEG_INF
        return 0

    _best_score = NEG_INF
    _best_move = None

    for _move_obj in get_ordered_moves(board):
        _temp_board = board.copy()
        _temp_board.push(_move_obj)
        _eval = -search(_temp_board, depth - 1, -beta, -alpha)

        if _eval > _best_score:
            _best_score = _eval
            _best_move = _move_obj.uci()

        if _eval >= beta:
            transposition_table[_fen] = (depth, _best_score, _best_move, "LOWER")
            return _best_score

        alpha = max(alpha, _eval)

    _flag = "UPPER" if _best_score <= _og_alpha else "EXACT"
    transposition_table[_fen] = (depth, _best_score, _best_move, _flag)
    return _best_score


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
