import chess, time, csv

from code.bots.bot1_random import bot_random
from code.bots.bot2_classic_depth import bot_classic_depth
from code.bots.bot3_alpha_beta import bot_alpha_beta
from code.bots.bot4_move_ordering import bot_move_ordering
from code.bots.bot5_pos_caching import bot_pos_caching


if __name__ == "__main__":

    # fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # default pos
    _fen = "r3k2r/p1ppqpb1/Bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPB1PPP/R3K2R b KQkq - 0 1"

    print(f"testing for fen: {_fen}\n")

    with open("code/analysis/bot_testing.csv", "w", newline="") as _file:
        _csv_writer = csv.writer(_file)
        _csv_writer.writerow(["bot", "move", "depth", "time", "fen"])

        for _name, (_func, _max_depth) in {
            "bot_alpha_beta": (bot_alpha_beta, 4),
            "bot_move_ordering": (bot_move_ordering, 5),
            "bot_pos_caching": (bot_pos_caching, 7),
        }.items():

            print(f"{_name}:")
            _board = chess.Board(_fen) if _fen is not None else chess.Board()
            for _depth in range(1, _max_depth + 1):

                s = time.time()
                _move = _func(_board, _depth)
                f = time.time()

                print(f"depth={_depth} time={(f-s):.6f} move={_move}")
                _csv_writer.writerow([_name, _move, _depth, f - s, _fen])

            print()
