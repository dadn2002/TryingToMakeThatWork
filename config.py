WIN_WIDTH = 640
WIN_HEIGTH = 640
TILESIZE = 32
FPS = 60
PAUSE, INGAME, INVENTORY, SHOP = -1, 0, 1, 2
FIXEDCAM = False

GUI_LAYER = 5
PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

GLOBAL_SPEED = 10
# 10ig = 2rs, 20ig =

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FF4BLUE = (2, 0, 106)
FF4DARKWHITE = (55, 55, 55)
FF4WHITE = (202, 203, 220)

tilemap = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B........E.........B',
    'B..............B...B',
    'B....BB........B...B',
    'B..............B...B',
    'B..................B',
    'B............B.....B',
    'B....P.............B',
    'B.........B........B',
    'B..................B',
    'B...B..............B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'BBBBBBBBBBBBBBBBBBBB',
]
WorldMapExits = 1

WorldMap = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 1, 1, 2, 1, 1, 1],
    [1, 1, 2, 1, 2, 1, 2, 2],
    [1, 1, 2, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1],
    [1, 1, 1, 2, 1, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 2],
    [1, 1, 1, 1, 1, 1, 1, 1],
]
