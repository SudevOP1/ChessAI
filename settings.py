WINDOW_NAME = "chess"
WINDOW_ICON = "assets/pieces/wn.png"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
GAME_FPS = 60


SQUARE_SIZE = 80
BOARD_CORNER_RADIUS = 20


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
THEMES = {
    "ocean": ["#7397AC", "#D4DFE5"],
    "neo": ["#739552", "#ebecd0"],
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
SOUND_PATHS = {
    "capture":  "assets/sounds/capture.mp3",
    "castle":   "assets/sounds/castle.mp3",
    "check":    "assets/sounds/check.mp3",
    "move":     "assets/sounds/move.mp3",
    "promotion":"assets/sounds/promotion.mp3",
}
