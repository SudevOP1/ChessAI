from simul.chess_game import ChessGame
from simul.settings import PLAYER_OPTIONS
from simul.helpers import print_colors


def input_player_option(color: str) -> str:
    player = input(
        print_colors["yellow"] + f"enter {color} player: " + print_colors["clear"]
    )
    while player not in PLAYER_OPTIONS.keys():
        player = input(
            print_colors["red"]
            + f"enter valid player option for {color}: "
            + print_colors["clear"]
        )
    return PLAYER_OPTIONS[player]


if __name__ == "__main__":

    print()
    print(
        f"{print_colors['yellow']}player options: {', '.join(PLAYER_OPTIONS.keys())}{print_colors['clear']}"
    )
    white = input_player_option("white")
    black = input_player_option("black")
    print()

    game = ChessGame(white=white, black=black)
    game.run()
