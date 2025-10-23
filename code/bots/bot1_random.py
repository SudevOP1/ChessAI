import chess, random


def bot_random(board: chess.Board) -> str:
    _available_uci_moves = [_move.uci() for _move in board.legal_moves]
    _random_move = random.choice(_available_uci_moves)
    return _random_move
