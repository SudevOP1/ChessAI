import chess, random


def bot_random(board: chess.Board) -> str:
    """returns a random legal move from the current board in UCI format"""
    _available_uci_moves = [_move.uci() for _move in board.legal_moves]
    _random_move = random.choice(_available_uci_moves)
    return _random_move
