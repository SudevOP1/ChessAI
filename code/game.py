from simul.chess_game import ChessGame
from simul.settings import PLAYER_OPTIONS


def input_player_option(color: str) -> str:
    player = input(f"enter {color} player: ")
    while player not in PLAYER_OPTIONS.keys():
        player = input(f"enter valid player option for {color}: ")
    return PLAYER_OPTIONS[player]


if __name__ == "__main__":

    print("player options:", PLAYER_OPTIONS.keys())
    white = input_player_option("white")
    black = input_player_option("black")

    game = ChessGame(white=white, black=black)
    game.run()
