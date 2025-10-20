WINDOW_NAME = "chess"
WINDOW_ICON = "assets/pieces/wn.png"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
GAME_FPS = 60


SQUARE_SIZE = 80
BOARD_CORNER_RADIUS = 20
PROMOTION_QUERY_CLOSE_BTN_HEIGHT = SQUARE_SIZE * 0.5
AVAILABLE_MOVES_INDICATOR_RADIUS = SQUARE_SIZE * 0.1
AVAILABLE_MOVES_CAPTURE_INDICATOR_RADIUS = SQUARE_SIZE * 0.3

INIT_POS = "rnbqkbnr/pppppppp/8/8/8/2Q5/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
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
SOUNDS = { # TODO: set appropriate volume
    "capture"   : { "volume": 1, "path": "assets/sounds/capture.mp3"    },
    "castle"    : { "volume": 1, "path": "assets/sounds/castle.mp3"     },
    "check"     : { "volume": 1, "path": "assets/sounds/check.mp3"      },
    "move"      : { "volume": 1, "path": "assets/sounds/move.mp3"       },
    "promotion" : { "volume": 1, "path": "assets/sounds/promotion.mp3"  },
}
