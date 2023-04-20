import pygame
from config import *


# Function that just map to the tile that need
def GetTileSprite(x, y):
    sprite = pygame.Surface([16, 16])
    sprite.blit(pygame.image.load('img/CastleTiles.png').convert_alpha(), (0, 0), ((x-1) * 16, (y-1) * 16, 16, 16))
    sprite.set_colorkey(WHITE)
    return sprite


# All the Tiles Used To Build
TileData = [
    [48, 32, 16, 16],  # 00 Castle Floor Light
    [96, 16, 16, 16],  # 01 Castle Floor Light 2
    [64, 32, 16, 16],  # 02 Castle Floor Full Shadow
    [80, 32, 16, 16],  # 03 Castle Floor Half Shadow Top
    [96, 32, 16, 16],  # 04 Castle Floor Half Shadow Bottom
    [112, 16, 16, 16],  # 05 Castle Floor Weak Shadow
    [109, 32, 16, 16],  # 06 Castle Floor Weak Shadow Connect to Dirt
    [80, 0, 16, 32],  # 07 Iron Door Closed
    [64, 0, 16, 32],  # 08 Iron Door Opened
    [32, 16, 16, 16],  # 09 Dirt Path Top
    [32, 0, 16, 16],  # 10 Dirt Path Bottom
    [16, 16, 16, 16],  # 11 Castle Wall Bricks 1
    [0, 16, 16, 16],  # 12 Castle Wall Bricks 2
    [16, 0, 16, 16],  # 13 Castle Wall Dark Corner 1
    [96, 0, 16, 16],  # 14 Castle Wall Base of Tower Left
    [112, 0, 16, 16],  # 15 Castle Wall Base of Tower Right
    [0, 40, 16, 16],  # 16 Castle Wall Tower Top Top Left
    [16, 40, 16, 16],  # 17 Castle Wall Tower Top Top
    [32, 40, 16, 16],  # 18 Castle Wall Tower Top Top Right
    [0, 56, 16, 16],  # 19 Castle Wall Tower Top Left 1
    [16, 56, 16, 16],  # 20 Castle Wall Tower Top Middle
    [32, 56, 16, 16],  # 21 Castle Wall Tower Top Right 1
    [0, 72, 16, 16],  # 22 Castle Wall Tower Top Bottom Left
    [16, 72, 16, 16],  # 23 Castle Wall Tower Top Bottom
    [32, 72, 16, 16],  # 24 Castle Wall Tower Top Bottom Right
    [0, 96, 16, 16],  # 25 Castle Wall Tower Bars
    [16, 96, 16, 16],  # 26 Castle Wall Tower Shadow
    [32, 96, 16, 16],  # 27 Castle Wall Tower Hole 1
    [32, 112, 16, 16],  # 28 Castle Wall Tower Hole 2
    [16, 112, 16, 16],  # 29 Castle Wall Tower Hole 3
    [0, 112, 16, 16],  # 30 Castle Wall Bricks 3
    [0, 128, 16, 16],  # 31 Castle Wall Bricks 4
    [16, 128, 16, 16],  # 32 Castle Wall Tower Hole 4
    [32, 128, 16, 16],  # 33 Castle Wall Double Pipe 2
    [0, 144, 16, 16],  # 34 Castle Wall Bricks 5
    [16, 144, 16, 16],  # 35 Castle Wall Double Pipe
    [32, 144, 16, 16],  # 36 Castle Wall Stone Fence 1
    [0, 160, 16, 16],  # 37 Castle Wall Double Pipe Horizontal
    [16, 160, 16, 16],  # 38 Castle Wall Double Pipe 3
    [32, 160, 16, 16],  # 39 Castle Wall Stone Fence 2
    [0, 176, 16, 16],  # 40 Castle Wall Double Pipe Horizontal 2
    [16, 176, 16, 16],  # 41 Castle Wall Double Pipe 4
    [32, 176, 16, 16],  # 42 Castle Wall Stone Fence 3
    [0, 16, 16, 16],  # 43
    [0, 16, 16, 16],  # 44
    [0, 16, 16, 16],  # 45
    [0, 16, 16, 16],  # 46
    [0, 16, 16, 16],  # 47
    [0, 16, 16, 16],  # 48
    [0, 16, 16, 16],  # 49
    [0, 16, 16, 16],  # 50
    [0, 16, 16, 16],  # 51
    [0, 16, 16, 16],  # 52
    [0, 16, 16, 16],  # 53
    [0, 16, 16, 16],  # 54
    [0, 16, 16, 16],  # 55
    [0, 16, 16, 16],  # 56
    [0, 16, 16, 16],  # 57
    [0, 16, 16, 16],  # 58
    [0, 16, 16, 16],  # 59
    [0, 16, 16, 16],  # 60
    [0, 16, 16, 16],  # 61
    [0, 16, 16, 16],  # 62
    [0, 16, 16, 16],  # 63
    [0, 16, 16, 16],  # 64
    [0, 16, 16, 16],  # 65
    [0, 16, 16, 16],  # 66
    [0, 16, 16, 16],  # 67
    [0, 16, 16, 16],  # 68
    [0, 16, 16, 16],  # 69

]
