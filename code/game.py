from typing import Callable

from code.simul.chess_game import ChessGame
from code.simul.settings import PLAYER_OPTIONS
from code.simul.helpers import print_colors


def set_printing_color(color: str) -> None:
    print(print_colors[color], end="")


def input_player_option(color: str) -> Callable | None:

    set_printing_color("yellow")
    print(f"enter {color} player: ", end="")
    set_printing_color("clear")
    _choice = input()
    while True:
        if not (_choice.isdigit() and (0 <= int(_choice) < len(PLAYER_OPTIONS))):
            set_printing_color("red")
            print(f"enter valid {color} player: ", end="")
            set_printing_color("clear")
            _choice = input()
            continue

        _key = list(PLAYER_OPTIONS.keys())[int(_choice)]
        return PLAYER_OPTIONS[_key]


def print_player_options():
    set_printing_color("yellow")
    print("player options:")
    for _idx, _player_option in enumerate(PLAYER_OPTIONS.keys()):
        set_printing_color("clear")
        print(_idx, end="")
        set_printing_color("yellow")
        print(" for ", end="")
        set_printing_color("clear")
        print(_player_option)
    set_printing_color("clear")


if __name__ == "__main__":

    print()
    print_player_options()
    print()
    white = input_player_option("white")
    print()
    black = input_player_option("black")
    print()

    game = ChessGame(white=white, black=black)
    game.run()
