WIN_WIDTH = 640
WIN_HEIGTH = 640
TILESIZE = 32
FPS = 60
PAUSE, INGAME, INVENTORY, SHOP = -1, 0, 1, 2
FIXEDCAM = True

PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3
ENEMY_SPEED = 2

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

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
"""
    L = 16
    WorldMap = [[0]*L]*L
    for i in range(len(WorldMap)):
        for j in range(len(WorldMap[0])):
            WorldMap[i][j] = random.randint(5, 15)
    print(WorldMap)
"""