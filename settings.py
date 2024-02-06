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

# SCORE SIZE
WIDHT_SCORE_FIELD = WIDTH_FIELD * 0.5
HEIGHT_SCORE_FIELD  = WIDHT_SCORE_FIELD

# PREVIEW SIZE 
WIDHT_PREVIEW_FIELD = WIDHT_SCORE_FIELD
HEIGHT_PREVIEW_FIELD  = HEIGHT_SCORE_FIELD * 1.3

# PIECE
BLOCK_DIMENSION = WIDTH_FIELD // 10
PIECES = {
    'I':[[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]],
    'O':[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]],
    'T':[[0,0,0],[1,1,1],[0,1,0]],
    'L':[[0,1,0],[0,1,0],[0,1,1]],
    'J':[[0,1,0],[0,1,0],[1,1,0]],
    'S':[[0,0,0],[0,1,1],[1,1,0]],
    'Z':[[0,0,0],[1,1,0],[0,1,1]]
}

PIECES_COLORS = {
    'I':(232, 19, 19),
    'O':(227, 220, 18),
    'T':(24, 201, 196),
    'L':(214, 137, 28),
    'J':(36, 91, 209),
    'S':(207, 27, 183),
    'Z':(42, 199, 28)
}

PIECES_LIST = ['I', 'O', 'T', 'L', 'J', 'S', 'Z']


# SURFACES COLOR
MAIN_SCREEN_SURFACE_COLOR = (5, 61, 110)
FIELD_SURFACE_COLOR = (13, 13, 13)
LINE_SURFACE_COLOR = (0, 255, 0)
BORDER_LINE_COLOR = (200, 200, 200)
LINE_COLOR = (100, 100, 100)
TEXT_COLOR = ()

# TIMERS
UPDATE_START_SPEED = 500
MOVE_WAIT_TIME = 180
ROTATE_WAIT_TIME = 180

# TEXT SIZE
PREVIEW_FONT_SIZE = round(BLOCK_DIMENSION * 0.6)
SCORE_FONT_SIZE = round(BLOCK_DIMENSION * 0.6)

# SCORING
POINTS = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}