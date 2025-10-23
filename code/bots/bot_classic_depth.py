import chess

POS_INF = 10**7
NEG_INF = -POS_INF


def bot_classic_depth(board: chess.Board, depth: int = 3) -> str:
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

    if depth == 0:
        return get_eval(board)

    # checkmate or draw
    if board.is_game_over():
        if board.is_checkmate():
            return NEG_INF
        return 0

    _best_eval = NEG_INF
    for _move_obj in board.legal_moves:
        _temp_board = board.copy()
        _temp_board.push(_move_obj)
        _best_eval = max(_best_eval, -search(_temp_board, depth - 1))

    return _best_eval


def get_eval(board: chess.Board) -> int:
    _piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 300,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0,
    }

    _value = 0
    for _piece in _piece_values.keys():
        _value += len(board.pieces(_piece, chess.WHITE)) * _piece_values[_piece]
        _value -= len(board.pieces(_piece, chess.BLACK)) * _piece_values[_piece]
    return _value if board.turn == chess.WHITE else -_value
