WINDOW_NAME = "chess"
WINDOW_ICON = "assets/pieces/wn.png"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
GAME_FPS = 60


SQUARE_SIZE = 80
BOARD_CORNER_RADIUS = 20
PROMOTION_QUERY_CLOSE_BTN_HEIGHT = SQUARE_SIZE * 0.5


INIT_POS = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]


BG_COLOR = "#00082A"
PROMOTION_QUERY_BG_COLOR = "#ffffff"
PROMOTION_QUERY_CLOSE_BTN_BG_COLOR = "#c8c8c8"
PROMOTION_QUERY_CLOSE_BTN_COLOR = "#000000"
THEMES = {
    "ocean" : ["#7397AC", "#D4DFE5"],
    "neo"   : ["#739552", "#ebecd0"],
}
THEME = "ocean"

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
