import chess


POS_INF = 10**7
NEG_INF = -POS_INF

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}


def get_piece_value(piece: chess.Piece | int | str) -> int:

    if isinstance(piece, str):
        return piece_values[chess.Piece.from_symbol(piece).piece_type]

    if isinstance(piece, chess.Piece):
        return piece_values[piece.piece_type]

    if isinstance(piece, int) and piece in piece_values:
        return piece_values[piece]

    raise Exception(f"encountered invalid piece: {type(piece)} {piece}")


def calc_eval(board: chess.Board) -> int:
    _value = 0
    for _piece in piece_values.keys():
        _value += len(board.pieces(_piece, chess.WHITE)) * get_piece_value(_piece)
        _value -= len(board.pieces(_piece, chess.BLACK)) * get_piece_value(_piece)
    return _value if board.turn == chess.WHITE else -_value


def calc_active_square_eval(board: chess.Board) -> int:
    _value = 0

    _white_active_squares = 0
    _black_active_squares = 0
    for _move in board.legal_moves:
        _piece = board.piece_at(_move.from_square)
        if not _piece:
            continue
        _active_squares_bonus = get_piece_value(_piece) / 100
        if _piece.color == chess.WHITE:
            _white_active_squares += _active_squares_bonus
        else:
            _black_active_squares += _active_squares_bonus

    _value += _white_active_squares
    _value += _black_active_squares

    return _value
