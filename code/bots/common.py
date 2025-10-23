import chess


piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}


def get_piece_value(piece: chess.Piece) -> int:
    if piece not in piece_values.keys():
        raise Exception(f"encountered invalid piece: {piece}")
    return piece_values[piece]


def get_eval(board: chess.Board) -> int:
    _value = 0
    for _piece in piece_values.keys():
        _value += len(board.pieces(_piece, chess.WHITE)) * get_piece_value(_piece)
        _value -= len(board.pieces(_piece, chess.BLACK)) * get_piece_value(_piece)
    return _value if board.turn == chess.WHITE else -_value
