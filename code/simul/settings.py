from typing import Callable
import chess

from code.bots.bot1_random              import bot_random
from code.bots.bot2_classic_depth       import bot_classic_depth
from code.bots.bot3_alpha_beta          import bot_alpha_beta
from code.bots.bot4_move_ordering       import bot_move_ordering
from code.bots.bot5_pos_caching         import bot_pos_caching
from code.bots.bot6_sqaure_heuristics   import bot_sqaure_heuristics
from code.bots.bot7_active_square       import bot_active_square
from code.bots.bot8_super_powerful      import bot_super_powerful

WINDOW_NAME = "chess"
WINDOW_ICON = "assets/pieces/wn.png"
SAVED_GAMES_DIRECTORY = "simulated_games"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
GAME_FPS = 60

PLAYER_OPTIONS: dict[str, Callable | None] = {
    "player"                : None,
    "bot_random"            : bot_random,
    "bot_classic_depth"     : bot_classic_depth,
    "bot_alpha_beta"        : bot_alpha_beta,
    "bot_move_ordering"     : bot_move_ordering,
    "bot_pos_caching"       : bot_pos_caching,
    "bot_sqaure_heuristics" : bot_sqaure_heuristics,
    "bot_active_square"     : bot_active_square,
    "bot_super_powerful"    : bot_super_powerful
}

SQUARE_SIZE         = 80
BOARD_CORNER_RADIUS = 20
MOVES_WIDTH         = 4 * SQUARE_SIZE
FPS_PADDING         = 20
MOVE_PADDING_X      = 20
MOVE_PADDING_Y      = 15
MOVES_SCROLL_SPEED  = 30

PROMOTION_QUERY_CLOSE_BTN_HEIGHT = SQUARE_SIZE * 0.5
AVAILABLE_MOVES_INDICATOR_RADIUS = SQUARE_SIZE * 0.1
AVAILABLE_MOVES_CAPTURE_INDICATOR_RADIUS = SQUARE_SIZE * 0.3

INIT_POS = ""
PIECE_NAMES = [
    "K", "k",
    "Q", "q",
    "R", "r",
    "N", "n",
    "B", "b",
    "P", "p",
]


BG_COLOR = "#00082A"
THEMES = {
    "ocean" : ["#7397AC", "#D4DFE5"],
    "neo"   : ["#739552", "#ebecd0"],
}
THEME = "ocean"
PROMOTION_QUERY_BG_COLOR                = "#ffffff"
PROMOTION_QUERY_CLOSE_BTN_BG_COLOR      = "#c8c8c8"
PROMOTION_QUERY_CLOSE_BTN_COLOR         = "#000000"
AVAILABLE_MOVES_INDICATOR_COLOR         = "#ffffff"
AVAILABLE_MOVES_CAPTURE_INDICATOR_COLOR = "#ff0000"
MOVES_BG_COLOR                          = "#000D48"
MOVES_COLOR                             = "#D4DFE5"

FONT_PATH = "assets/GoogleSansCode.ttf"  # (monospace)
PIECE_IMG_PATHS = {
    "k": "assets/pieces/bk.png",
    "q": "assets/pieces/bq.png",
    "r": "assets/pieces/br.png",
    "n": "assets/pieces/bn.png",
    "b": "assets/pieces/bb.png",
    "p": "assets/pieces/bp.png",
    "K": "assets/pieces/wk.png",
    "Q": "assets/pieces/wq.png",
    "R": "assets/pieces/wr.png",
    "N": "assets/pieces/wn.png",
    "B": "assets/pieces/wb.png",
    "P": "assets/pieces/wp.png",
}
SOUNDS = {
    "capture"   : { "volume": 1, "path": "assets/sounds/capture.mp3"    },
    "castle"    : { "volume": 1, "path": "assets/sounds/castle.mp3"     },
    "check"     : { "volume": 1, "path": "assets/sounds/check.mp3"      },
    "move"      : { "volume": 1, "path": "assets/sounds/move.mp3"       },
    "promotion" : { "volume": 1, "path": "assets/sounds/promotion.mp3"  },
    "gameover"  : { "volume": 1, "path": "assets/sounds/gameover.mp3"   },
}
