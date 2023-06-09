
""" Thanks to
https://www.chronocompendium.com/Term/Text_List_of_Sound_Effects.html
https://www.spriters-resource.com/snes/ff6/
https://bghq.com/bgs.php?n=pg
https://www.zophar.net/music/nintendo-snes-spc/final-fantasy-vi
https://www.ff6hacking.com/wiki/doku.php?id=ff3:ff3us:doc:asm:list:sfx#list_of_sound_effects


"""

WIN_WIDTH = 640
WIN_HEIGHT = 640
TILESIZE = 32
FPS = 60
PAUSE, INGAME, INVENTORY, SHOP = -1, 0, 1, 2
FIXEDCAM = True

GUI_LAYER = 7
PLAYER_LAYER = 5
ENEMY_LAYER = 4
BLOCK_LAYER = 3
GROUND_LAYER = 1

GLOBAL_SPEED = 32
PLAYER_SPEED = 8

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
FF4BLUE = (2, 0, 106)
FF4DARKWHITE = (55, 55, 55)
FF4WHITE = (202, 203, 220)
FF4BLACK = (55, 55, 30)


tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......................................B',
    'B.....................E................B',
    'B.........EE...........................B',
    'B.......B...B......B...................B',
    'B.........B............E...............B',
    'B.....B.....B..........................B',
    'B.......B........P...N.................B',
    'B....B......B..........................B',
    'B......B..B.........B..................B',
    'B.....................E................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B...........E..........................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

WorldSize = 40
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

