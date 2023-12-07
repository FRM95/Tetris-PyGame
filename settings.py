from pyautogui import size
import math

# SCREEN SIZE
WIDTH_SCREEN, HEIGHT_SCREEN = size()
WIDTH_SCREEN = math.floor(WIDTH_SCREEN * 0.4)
HEIGHT_SCREEN = math.floor(HEIGHT_SCREEN * 0.8)

# FIELD SIZE
WIDTH_FIELD = WIDTH_SCREEN * 0.45
WIDTH_FIELD = WIDTH_FIELD // 10 * 10
HEIGHT_FIELD = WIDTH_FIELD * 2
COLUMNS = 10
ROWS = 20

# PIECE
BLOCK_DIMENSION = WIDTH_FIELD // 10
# PIECES = {
#     'I':[[1,1,1,1]],
#     'O':[[1,1],[1,1]],
#     'T':[[1,1,1],[0,1,0]],
#     'L':[[1,0],[1,0],[1,1]],
#     'J':[[0,1],[0,1],[1,1]],
#     'S':[[0,1,1],[1,1,0]],
#     'Z':[[1,1,0],[0,1,1]]
# }
PIECES = {
    'I':[[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]],
    'O':[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]],
    'T':[[0,0,0],[1,1,1],[0,1,0]],
    'L':[[0,1,0],[0,1,0],[0,1,1]],
    'J':[[0,1,0],[0,1,0],[1,1,0]],
    'S':[[0,0,0],[0,1,1],[1,1,0]],
    'Z':[[0,0,0],[1,1,0],[0,1,1]]
}

# DEFAULT_TIME_LAPSE = 0.01667
DEFAULT_TIME_LAPSE = 0.05

# SURFACES COLOR
MAIN_SCREEN_SURFACE_COLOR = (0,0,0)
FIELD_SURFACE_COLOR = (25,123,0)
LINE_SURFACE_COLOR = (0,255,0)
LINE_SURFACE_ALPHA = 120
LINE_COLOR = (50,50,50)

# PIECES COLOR
PIECES_COLORS = [
    (219, 67, 95),
    (112, 216, 157),
    (2, 168, 229),
    (181, 10, 204),
    (237, 218, 18),
    (63, 198, 151),
    (155, 13, 120),
    (171, 129, 226),
    (229, 145, 61)
]