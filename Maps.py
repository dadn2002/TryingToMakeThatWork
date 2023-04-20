import math
import random

import pygame
from TileData import *
from config import *
from sprites import Block
from zones import *


def GenerateMap(game, name):
    spacing = 2048
    GenerateStructures(game, 'debugroom', 0, 0, mapName=name, doorsTag=[256, 256])
    if name.lower() == 'domacastle':
        # Plot each structure spacing units away form each other
        # GenerateStructures(game, 'castlethroneroom1', 64, 0, mapName=name, doorsTag=[256, 256])
        # GenerateStructures(game, 'castlebedroom1'   , 1 * spacing, 1 * spacing, mapName=name, doorsTag=[64, 128])  # 88 Block Sprites and 282 All_sprites
        # GenerateStructures(game, 'castlebedroom2'   , 2 * spacing, 2 * spacing, mapName=name, doorsTag=[448, 128])  # 72 Block Sprites and 197 All_sprites
        # GenerateStructures(game, 'castlebedroom3'   , 3 * spacing, 3 * spacing, mapName=name, doorsTag=[96, 480])  # [[12320, 12480], [14368, 14528], [16416, 16576], [8224, 8384], [416, 480]])
        # GenerateStructures(game, 'castlemainroom1'  , 0 * spacing, 0 * spacing, mapName=name, doorsTag=[[2112, 2368], [256, 256], [4160, 4352], [256, 256], [6208, 6528], [10496, 10880]])
        # GenerateStructures(game, 'castlestorage1'   , 4 * spacing, 4 * spacing, mapName=name, doorsTag=[10336, 10772])
        # GenerateStructures(game, 'castlestairs1'    , 5 * spacing, 5 * spacing, mapName=name, doorsTag=[[8224, 8384], [12320, 12480], [14368, 14528], [16416, 16576], [416, 480]])
        # GenerateStructures(game, 'castlestorage1'   , 6 * spacing, 6 * spacing, mapName=name, doorsTag=[10656, 10772])
        # GenerateStructures(game, 'castlestorage1'   , 7 * spacing, 7 * spacing, mapName=name, doorsTag=[10336, 10384])
        # GenerateStructures(game, 'castlestorage1'   , 8 * spacing, 8 * spacing, mapName=name, doorsTag=[10656, 10384])
        pass


def GenerateStructures(game, name, x, y, width=0, height=0, mapName='', facing='', doorsTag=None, tag=None, setLayer=None):
    # Mapping table for 32px Coords (up to 20x20)
    # 0 32 64 96 128 160 192 224 256 288 320 352 384 416 448 480 512 544 576 608 640 672 704 736 768 800 832 864 896 928 960 992 1024
    # 0 01 02 03 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028 029 030 031 0032
    if name.lower() ==   'debugroom':
        GenerateStructures(game, 'room_personalized_debugroom', x, y)
    elif name.lower() == 'castlebedroom1':
        GenerateStructures(game, 'room', x + 0, y + 0, 10, 8)
        GenerateStructures(game, 'bed', x + 0, y + 96)
        GenerateStructures(game, 'bed', x + 96, y + 96)
        GenerateStructures(game, 'green_carpet', x + 0, y + 96, 10, 3)
        GenerateStructures(game, 'fireplace', x + 232, y + 96)
        GenerateStructures(game, 'wood_desk', x + 160, y + 96, 2)
        GenerateStructures(game, 'wood_bedcase', x + 56, y + 96)
        GenerateStructures(game, 'flowerpot', x + 188, y + 64)
        GenerateStructures(game, 'wood_chair_facing_left', x + 38, y + 240)
        GenerateStructures(game, 'wood_whitetable', x + 0, y + 256)
        GenerateStructures(game, 'candle', x + 16, y + 16)
        GenerateStructures(game, 'candle', x + 108, y + 16)
        GenerateStructures(game, 'doorwarptile', x + 64, y + 352, facing='up', doorsTag=doorsTag)
        Objects(game, x + 9 * 32, y + 8 * 32, 32, 32, 'chest', mapName=mapName)
        Objects(game, x + 9 * 32, y + 9 * 32, 32, 32, 'chest', mapName=mapName)
        Objects(game, x + 9 * 32, y + 10 * 32, 32, 32, 'chest', mapName=mapName)
    elif name.lower() == 'castlebedroom2':
        GenerateStructures(game, 'room', x + 0, y + 0, 8, 6)
        GenerateStructures(game, 'bed', x + 192, y + 96)
        GenerateStructures(game, 'green_carpet', x + 96, y + 96, 5, 3)
        GenerateStructures(game, 'fireplace', x + 16, y + 96)
        GenerateStructures(game, 'wood_chair_facing_up', x + 44, y + 128)
        GenerateStructures(game, 'wood_bedcase', x + 128, y + 96)
        GenerateStructures(game, 'brick_window', x + 128, y + 0)
        GenerateStructures(game, 'flowerpot', x + 0, y + 256)
        GenerateStructures(game, 'wood_chair_facing_right', x + 192, y + 240)
        GenerateStructures(game, 'wood_whitetable', x + 224, y + 256)
        GenerateStructures(game, 'candle', x + 208, y + 16)
        GenerateStructures(game, 'doorwarptile', x + 64, y + 288, facing='up', doorsTag=doorsTag)
        Objects(game, x + 0 * 32, y + 7 * 32, 32, 32, 'chest', mapName=mapName)
        Objects(game, x + 0 * 32, y + 8 * 32, 32, 32, 'chest', mapName=mapName)
    elif name.lower() == 'castlebedroom3':
        GenerateStructures(game, 'room', x + 0, y + 0, 12, 10)
        GenerateStructures(game, 'bed', x + 320, y + 96)
        GenerateStructures(game, 'bed', x + 192, y + 96)
        GenerateStructures(game, 'bed', x + 320, y + 256)
        GenerateStructures(game, 'bed', x + 192, y + 256)
        GenerateStructures(game, 'green_carpet', x + 160, y + 96, 7, 8)
        GenerateStructures(game, 'wood_bedcase', x + 264, y + 96)
        GenerateStructures(game, 'wood_desk', x + 0, y + 96, 5)
        GenerateStructures(game, 'wood_chair_facing_up', x + 0, y + 128)
        GenerateStructures(game, 'wood_chair_facing_up', x + 42, y + 128)
        GenerateStructures(game, 'wood_chair_facing_up', x + 86, y + 128)
        GenerateStructures(game, 'wood_chair_facing_up', x + 128, y + 128)
        GenerateStructures(game, 'flowerpot', x + 0, y + 256)
        GenerateStructures(game, 'flowerpot', x + 320, y + 384)
        GenerateStructures(game, 'flowerpot', x + 352, y + 384)
        GenerateStructures(game, 'candle', x + 72, y + 16)
        GenerateStructures(game, 'candle', x + 208, y + 16)
        GenerateStructures(game, 'candle', x + 336, y + 16)
        GenerateStructures(game, 'doorwarptile', x + 64, y + 416, facing='up', doorsTag=doorsTag)
        Objects(game, x + 0, y + 288, 32, 32, 'chest', mapName=mapName)
        Objects(game, x + 0, y + 320, 32, 32, 'chest', mapName=mapName)
        Objects(game, x + 0, y + 352, 32, 32, 'chest', mapName=mapName)
        Objects(game, x + 0, y + 384, 32, 32, 'chest', mapName=mapName)
    elif name.lower() == 'castlemainroom1':
        GenerateStructures(game, 'room_personalized_castlemainroom', x, y)

        GenerateStructures(game, 'brick_door', x + 64, y + 64, doorsTag=doorsTag[0])
        GenerateStructures(game, 'brick_pillar', x + 32, y + 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'brick_pillar', x + 96, y + 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'interiorbrickwallcorner_facing_left', x + 128, y + 32, height=3)
        GenerateStructures(game, 'snake_candle', x + 96, y + 64)
        GenerateStructures(game, 'bronze_armourstand', x + 128, y + 128)

        GenerateStructures(game, 'interiorbrickwallcorner_facing_left', x + 192, y + 96, height=3)
        GenerateStructures(game, 'interiorbrickwallcorner_facing_right', x + 320, y + 96, height=3)
        GenerateStructures(game, 'snake_candle', x + 200, y + 128)
        GenerateStructures(game, 'brick_doubledoor', x + 224, y + 128, doorsTag=doorsTag[1])
        GenerateStructures(game, 'snake_candle', x + 312, y + 128)

        GenerateStructures(game, 'brick_door', x + 448, y + 64, doorsTag=doorsTag[2])
        GenerateStructures(game, 'brick_pillar', x + 416, y + 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'brick_pillar', x + 480, y + 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'interiorbrickwallcorner_facing_right', x + 384, y + 32, height=3)
        GenerateStructures(game, 'snake_candle', x + 416, y + 64)
        GenerateStructures(game, 'bronze_armourstand', x + 384, y + 128)

        GenerateStructures(game, 'red_carpet', x + 224, y + 192, 3, 2)
        GenerateStructures(game, 'red_carpet', x + 224, y + 288, 3, 3)
        GenerateStructures(game, 'red_carpet', x + 224, y + 512, 3, 2)
        GenerateStructures(game, 'red_carpet', x + 256, y + 576, 1, 1)
        GenerateStructures(game, 'doorwarptile', x + 256, y + 576, facing='up', doorsTag=doorsTag[3])

        GenerateStructures(game, 'brick_red_carpet_stairs', x + 224, y + 256, 3, 1)
        GenerateStructures(game, 'brick_stairs', x + 192, y + 384, 1, 4)
        GenerateStructures(game, 'brick_stairs_special_corner_left', x + 192, y + 256, 1, 1)
        GenerateStructures(game, 'brick_stairs_special_corner_reverse_left', x + 192, y + 288, 1, 1)
        GenerateStructures(game, 'brick_stairs_special_corner_right', x + 320, y + 256, 1, 1)
        GenerateStructures(game, 'brick_stairs_special_corner_reverse_right', x + 320, y + 288, 1, 1)
        GenerateStructures(game, 'interiorbrickwallcorner_facing_right', x + 160, y + 352, height=4)
        GenerateStructures(game, 'brick_handrail_facing_left', x + 192, y + 352, height=4)
        GenerateStructures(game, 'brick_red_carpet_stairs', x + 224, y + 384, 3, 4)
        GenerateStructures(game, 'interiorbrickwallcorner_facing_left', x + 352, y + 352, height=4)
        GenerateStructures(game, 'brick_stairs', x + 320, y + 384, 1, 4)
        GenerateStructures(game, 'brick_handrail_facing_right', x + 320, y + 352, height=4)

        GenerateStructures(game, 'brick_door', x + 96, y + 416, doorsTag=doorsTag[4])
        GenerateStructures(game, 'brick_pillar', x + 128, y + 320 + 16, 1, 4, tag='isWall')
        GenerateStructures(game, 'snake_candle', x + 128, y + 416)
        GenerateStructures(game, 'bronze_armourstand', x + 160, y + 480)

        GenerateStructures(game, 'brick_door', x + 416, y + 416, doorsTag=doorsTag[5])
        GenerateStructures(game, 'brick_pillar', x + 384, y + 320 + 16, 1, 4, tag='isWall')
        GenerateStructures(game, 'snake_candle', x + 384, y + 416)
        GenerateStructures(game, 'bronze_armourstand', x + 352, y + 480)

        GenerateStructures(game, 'brick_pillar_head', x + 32, y + 192)
        GenerateStructures(game, 'brick_pillar_head', x + 160, y + 192)
        GenerateStructures(game, 'brick_pillar_head', x + 352, y + 192)
        GenerateStructures(game, 'brick_pillar_head', x + 480, y + 192)
        GenerateStructures(game, 'brick_pillar_head', x + 160, y + 512)
        GenerateStructures(game, 'brick_pillar_head', x + 352, y + 512)
    elif name.lower() == 'castlestorage1':
        GenerateStructures(game, 'room', x + 0, y + 0, 5, 4)

        GenerateStructures(game, 'brick_window', x + 0, y + 0, 5, 4)
        GenerateStructures(game, 'brick_window', x + 32, y + 0, 5, 4)
        GenerateStructures(game, 'brick_pillar', x + 64, y + 0 - 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'brick_pillar_head', x + 64, y + 192)
        GenerateStructures(game, 'brick_window', x + 96, y + 0, 5, 4)
        GenerateStructures(game, 'brick_window', x + 128, y + 0, 5, 4)

        GenerateStructures(game, 'bronze_armourstand', x + random.choice([0, 32]), y + 96)
        GenerateStructures(game, 'flowerpot', x + 0, y + random.choice([128, 160, 192]))
        Objects(game, x + random.choice([96, 128]), y + 96, 32, 32, 'chest', mapName=mapName, chestTier=1)
        Objects(game, x + 128, y + 128, 32, 32, 'chest', mapName=mapName, chestTier=1)
        Objects(game, x + 128, y + 160, 32, 32, 'chest', mapName=mapName, chestTier=1)
        Objects(game, x + random.choice([96, 128]), y + 192, 32, 32, 'chest', mapName=mapName, chestTier=1)

        GenerateStructures(game, 'doorwarptile', x + 32, y + 224, facing='up', doorsTag=doorsTag)
    elif name.lower() == 'castlestairs1':
        GenerateStructures(game, 'room_personalized_underground_corridor', x, y)

        GenerateStructures(game, 'brick_pillar', x + 64, y + 448 - 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'brick_pillar', x + 128, y + 448 - 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'brick_pillar', x + 384, y + 448 - 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'brick_pillar', x + 448, y + 448 - 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'brick_pillar', x + 64, y + 64 - 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'brick_pillar', x + 128, y + 64 - 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'brick_pillar', x + 384, y + 64 - 16, 1, 3, tag='isWall')
        GenerateStructures(game, 'brick_pillar', x + 448, y + 64 - 16, 1, 3, tag='isWall')

        GenerateStructures(game, 'interiorbrickwallcorner_facing_right', x + 192, y + 64, height=3)
        GenerateStructures(game, 'interiorbrickwallcorner_facing_left', x + 320, y + 64, height=3)
        GenerateStructures(game, 'interiorbrickwallcorner_facing_right', x + 192, y + 448, height=3)
        GenerateStructures(game, 'interiorbrickwallcorner_facing_left', x + 320, y + 448, height=3)

        GenerateStructures(game, 'snake_candle', x + 128, y + 480)
        GenerateStructures(game, 'snake_candle', x + 384, y + 480)
        GenerateStructures(game, 'snake_candle', x + 128, y + 96)
        GenerateStructures(game, 'snake_candle', x + 384, y + 96)

        GenerateStructures(game, 'brick_pillar_head', x + 64, y + 224)
        GenerateStructures(game, 'brick_pillar_head', x + 128, y + 224)
        GenerateStructures(game, 'brick_pillar_head', x + 384, y + 224)
        GenerateStructures(game, 'brick_pillar_head', x + 448, y + 224)
        GenerateStructures(game, 'brick_pillar_head', x + 64, y + 608)
        GenerateStructures(game, 'brick_pillar_head', x + 128, y + 608)
        GenerateStructures(game, 'brick_pillar_head', x + 384, y + 608)
        GenerateStructures(game, 'brick_pillar_head', x + 448, y + 608)

        GenerateStructures(game, 'bronze_armourstand', x + 32, y + 160)
        GenerateStructures(game, 'bronze_armourstand', x + 160, y + 160)
        GenerateStructures(game, 'bronze_armourstand', x + 352, y + 160)
        GenerateStructures(game, 'bronze_armourstand', x + 480, y + 160)
        GenerateStructures(game, 'bronze_armourstand', x + 32, y + 544)
        GenerateStructures(game, 'bronze_armourstand', x + 160, y + 544)
        GenerateStructures(game, 'bronze_armourstand', x + 352, y + 544)
        GenerateStructures(game, 'bronze_armourstand', x + 480, y + 544)

        # GenerateStructures(game, 'flowerpot', x + 0, y + 160)

        GenerateStructures(game, 'brick_door', x + 96, y + 480, facing='up', doorsTag=doorsTag[0])
        GenerateStructures(game, 'brick_door', x + 416, y + 480, facing='up', doorsTag=doorsTag[1])
        GenerateStructures(game, 'brick_door', x + 96, y + 96, facing='up', doorsTag=doorsTag[2])
        GenerateStructures(game, 'brick_door', x + 416, y + 96, facing='up', doorsTag=doorsTag[3])
        GenerateStructures(game, 'doorwarptile', x + 256, y + 672, facing='up', doorsTag=doorsTag[4])
    elif name.lower() == 'castlethroneroom1':
        GenerateStructures(game, 'room_personalized_castlethroneroom', x, y)

        GenerateStructures(game, 'red_curtain_facing_left', x + 160, y + 32)
        GenerateStructures(game, 'blue_throne_chair', x + 192, y + 112)
        GenerateStructures(game, 'red_curtain_facing_right', x + 224, y + 32)

        GenerateStructures(game, 'red_carpet', x + 160, y + 128, 3, 1)
        GenerateStructures(game, 'brick_red_carpet_stairs', x + 160, y + 160, 3, 1)
        GenerateStructures(game, 'red_carpet', x + 128, y + 192, 5, 6)
        GenerateStructures(game, 'brick_stairs', x + 32, y + 384, 3, 1)
        GenerateStructures(game, 'brick_red_carpet_stairs', x + 128, y + 384, 5, 1)
        GenerateStructures(game, 'brick_stairs', x + 288, y + 384, 3, 1)
        GenerateStructures(game, 'red_carpet', x + 128, y + 416, 5, 6)
        GenerateStructures(game, 'red_carpet', x + 160, y + 608, 1, 1)
        GenerateStructures(game, 'red_carpet', x + 192, y + 608, 1, 1)
        GenerateStructures(game, 'red_carpet', x + 224, y + 608, 1, 1)
        GenerateStructures(game, 'red_carpet', x + 192, y + 640, 1, 1)

        GenerateStructures(game, 'brick_pillar', x + 128, y + 96 - 16, 1, 3, tag=['isWall', 'doesNotOverwrite'])
        GenerateStructures(game, 'brick_pillar', x + 256, y + 96 - 16, 1, 3, tag=['isWall', 'doesNotOverwrite'])
        GenerateStructures(game, 'brick_pillar', x + 128, y + 448, 1, 3, setLayer=PLAYER_LAYER + 1)
        # GenerateStructures(game, 'brick_pillar', x + 64, y + 448 - 16, 1, 3, tag='isWall')
        # GenerateStructures(game, 'brick_pillar', x + 64, y + 448 - 16, 1, 3, tag='isWall')
        # GenerateStructures(game, 'brick_pillar', x + 64, y + 448 - 16, 1, 3, tag='isWall')
        # GenerateStructures(game, 'brick_pillar', x + 64, y + 448 - 16, 1, 3, tag='isWall')
        # GenerateStructures(game, 'brick_pillar', x + 64, y + 448 - 16, 1, 3, tag='isWall')

    elif name.lower() == 'room':
        height += 3
        for i in range(width):
            for j in range(height):
                Block(game, x + i * 32, y + j * 32, 32, 32, sprite=GetTileSprite(4, 3), hasHitBox=False, isGround=True)
                if i == 0:
                    Block(game, x + i * 32 - 32, y + j * 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(17, 10), 180))
                if i == width - 1:
                    Block(game, x + i * 32 + 32, y + j * 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(17, 10), 0))
                if j == height - 1:
                    Block(game, x + i * 32, y + j * 32 + 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(17, 10), 270))
                if j == 0:
                    Block(game, x + i * 32, y + j * 32 - 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(17, 10), 90))
                    GenerateStructures(game, 'interiorvoidwall', x + i * 32, y + j * 32, 1, 3)
        Block(game, x - 32, y - 32, 32, 32, sprite=pygame.transform.rotate(GetTileSprite(21, 3), 0))
        Block(game, x - 32, y + height * 32, 32, 32, sprite=pygame.transform.rotate(GetTileSprite(21, 3), 90))
        Block(game, x + width * 32, y + height * 32, 32, 32, sprite=pygame.transform.rotate(GetTileSprite(21, 3), 180))
        Block(game, x + width * 32, y - 32, 32, 32, sprite=pygame.transform.rotate(GetTileSprite(21, 3), 270))
        height -= 3
    elif 'room_personalized' in name.lower():
        # generate a room up to nxn, 1 for where i can stand and 0 for void
        # PLEASE SURROUND WITH 0
        mapTilenxn = ['']
        floorsRow = []
        if 'castlemainroom' in name.lower():
            mapTilenxn = [
                '00000000000000000',  # 0
                '01111100000111110',  # 1
                '01111100000111110',  # 2
                '01111111111111110',  # 3
                '01111111111111110',  # 4
                '01111111111111110',  # 5
                '01111111111111110',  # 6
                '00000011111000000',  # 7
                '00000011111000000',  # 8
                '00000011111000000',  # 9
                '00000011111000000',  # 10
                '00011111111111000',  # 11
                '00011111111111000',  # 12
                '00011111111111000',  # 13
                '00011111111111000',  # 14
                '00011111111111000',  # 15
                '00011111111111000',  # 16
                '00000011111000000',  # 17
                '00000000100000000',  # 18
                '00000000000000000',  # 19
            ]
            floorsRow = [6, 9]
        elif 'underground_corridor' in name.lower():
            mapTilenxn = [
                '00000000000000000',  # 0
                '00000001110000000',  # 1
                '01111111111111110',  # 2
                '01111111111111110',  # 3
                '01111111111111110',  # 4
                '01111111111111110',  # 5
                '01111111111111110',  # 6
                '01111111111111110',  # 7
                '00000001110000000',  # 8
                '00000001110000000',  # 9
                '00000001110000000',  # 10
                '00000001110000000',  # 11
                '00000001110000000',  # 12
                '00000001110000000',  # 13
                '01111111111111110',  # 14
                '01111111111111110',  # 15
                '01111111111111110',  # 16
                '01111111111111110',  # 17
                '01111111111111110',  # 18
                '01111111111111110',  # 19
                '00000001110000000',  # 20
                '00000000000000000',  # 21
            ]
            floorsRow = []
        elif 'castlethroneroom' in name.lower():
            mapTilenxn = [
                '0000000000000',  # 0
                '0000011100000',  # 1
                '0000011100000',  # 2
                '0001111111000',  # 3
                '0001111111000',  # 4
                '0001111111000',  # 5
                '0001111111000',  # 6
                '0001111111000',  # 7
                '0111111111110',  # 8
                '0111111111110',  # 9
                '0111111111110',  # 10
                '0111111111110',  # 11
                '0111111111110',  # 12
                '0111111111110',  # 13
                '0111111111110',  # 14
                '0111111111110',  # 15
                '0111111111110',  # 16
                '0111111111110',  # 17
                '0001111111000',  # 18
                '0000011100000',  # 19
                '0000001000000',  # 20
                '0000000000000',  # 21

            ]
            floorsRow = [3, 7]
        elif 'debugroom' in name.lower():
            mapTilenxn = [
                '00000000000000000000000000000000000000000',  # 0
                '00111111111111111111111111111111111111100',  # 1
                '00111111111111111111111111111111111111100',  # 2
                '00111111111111111111111111111111111111100',  # 3
                '00111111111111111111111111111111111111100',  # 4
                '00111111111111111111111111111111111111100',  # 4
                '00111111111111111111111111111111111111100',  # 4
                '00000000000000000001110000000000000000000',  # 5
                '00000000000000000001110000000000000000000',  # 6
                '00000000000000000001110000000000000000000',  # 6
                '00111000111111111111111111111111100011100',  # 7
                '00111000111111111111111111111111100011100',  # 8
                '00111000111111111111111111111111100011100',  #
                '00111000111111111111111111111111100011100',  #
                '00111000111111111111111111111111100011100',  #
                '00111000111111111111111111111111100011100',  #
                '00111000111100000000000000000111100011100',  #
                '00111000111100000000000000000111100011100',  #
                '00111000111100000000000000000111100011100',  #
                '00111000111111111111111111111111100011100',  #
                '00111000111111111111111111111111100011100',  #
                '00111000111111111111111111111111100011100',  # 9
                '00111000111111111111111111111111100011100',  # 10
                '00111000111111111111111111111111100011100',  # 11
                '00111000111111111111111111111111100011100',  # 12
                '00111000000000000001110000000000000011100',  # 13
                '00111000000000000001110000000000000011100',  # 14
                '00111000000000000001110000000000000011100',  # 15
                '00000000000000000111111100000000000000000',  # 16
                '00000000000000000111111100000000000000000',  #
                '00000000000000000111111100000000000000000',  #
                '00111111111111111111111111111111111111100',  #
                '00111111111111111111111111111111111111100',  #
                '00111111111111111111111111111111111111100',  #
                '00111111111111111111111111111111111111100',  #
                '00111111111111111111111111111111111111100',  #
                '00111111111111111111111111111111111111100',  # 17
                '00111111111111111111111111111111111111100',  # 18
                '00111111111111111111111111111111111111100',  # 19
                '00111111111111111111111111111111111111100',  # 20
                '00111111111111111111111111111111111111100',  # 21
                '00111111111111111111111111111111111111100',  # 22
                '00111111111111111111111111111111111111100',  # 23
                '00111111111111111111111111111111111111100',  # 24
                '00111111111111111111111111111111111111100',  # 25
                '00111111111111111111111111111111111111100',  # 25
                '00111111111111111111111111111111111111100',  # 25
                '00111111111111111111111111111111111111100',  # 25
                '00111111111111111111111111111111111111100',  # 25
                '00111111111111111111111111111111111111100',  # 25
                '00111111111111111111111111111111111111100',  # 25
                '00111111111111111111111111111111111111100',  # 25
                '00111111111111111111111111111111111111100',  # 26
                '00111111111111111111111111111111111111100',  #
                '00000000000000000000000000000000000000000',  #
            ]
        dropFloor = 0
        # These messed IFs just plot the voidborders following the pattern above, saddly they consume a lot of time so
        # Use the name='room' for rect ones
        for i, row in enumerate(mapTilenxn):
            if i in floorsRow:
                dropFloor += 1
            for j, letter in enumerate(row):
                if letter == '1':
                    Block(game, x + j * 32, y + i * 32, 32, 32, sprite=GetTileSprite(4, 3), hasHitBox=False,
                          isGround=True)
                    if mapTilenxn[i - 1][j] == '0':
                        if j < len(row) - 1 and mapTilenxn[i - 1][j + 1] == '1':
                            Block(game, x + j * 32, y + i * 32 - 32, 32, 32,
                                  sprite=pygame.transform.rotate(GetTileSprite(18, 19), 180))

                        elif j > 0 and mapTilenxn[i - 1][j - 1] == '1':
                            Block(game, x + j * 32, y + i * 32 - 32, 32, 32,
                                  sprite=pygame.transform.rotate(GetTileSprite(18, 19), 90))
                        else:
                            Block(game, x + j * 32, y + i * 32 - 32, 32, 32,
                                  sprite=pygame.transform.rotate(GetTileSprite(17, 10), 90))
                        GenerateStructures(game, 'interiorvoidwall', x + j * 32, y + i * 32, 1,
                                           3 + math.floor(dropFloor / 2))
                    if i == len(mapTilenxn) - 1:
                        Block(game, x + j * 32, y + i * 32 + 32, 32, 32,
                              sprite=pygame.transform.rotate(GetTileSprite(17, 10), 270))
                    elif mapTilenxn[i + 1][j] == '0':
                        if j < len(row) - 1 and mapTilenxn[i + 1][j + 1] == '1':
                            Block(game, x + j * 32, y + i * 32 + 32, 32, 32,
                                  sprite=pygame.transform.rotate(GetTileSprite(18, 19), 270))
                        elif j > 0 and mapTilenxn[i + 1][j - 1] == '1':
                            Block(game, x + j * 32, y + i * 32 + 32, 32, 32,
                                  sprite=pygame.transform.rotate(GetTileSprite(18, 19), 0))
                        else:
                            Block(game, x + j * 32, y + i * 32 + 32, 32, 32,
                                  sprite=pygame.transform.rotate(GetTileSprite(17, 10), 270))
                    if (j == len(row) - 1 or mapTilenxn[i][j + 1] == '0') and mapTilenxn[i + 1][j + 1] == '0' and \
                            mapTilenxn[i - 1][j + 1] == '0':
                        Block(game, x + j * 32 + 32, y + i * 32, 32, 32,
                              sprite=pygame.transform.rotate(GetTileSprite(17, 10), 0))
                    elif (j == 0 or mapTilenxn[i][j - 1] == '0') and mapTilenxn[i + 1][j - 1] == '0' and \
                            mapTilenxn[i - 1][j - 1] == '0':
                        Block(game, x + j * 32 - 32, y + i * 32, 32, 32,
                              sprite=pygame.transform.rotate(GetTileSprite(17, 10), 180))
                    if mapTilenxn[i - 1][j - 1] == '0' and mapTilenxn[i - 1][j] == '0' and mapTilenxn[i][j - 1] == '0':
                        Block(game, x + j * 32 - 32, y + i * 32 - 32, 32, 32,
                              sprite=pygame.transform.rotate(GetTileSprite(21, 3), 0))
                    elif mapTilenxn[i - 1][j + 1] == '0' and mapTilenxn[i - 1][j] == '0' and mapTilenxn[i][
                        j + 1] == '0':
                        Block(game, x + j * 32 + 32, y + i * 32 - 32, 32, 32,
                              sprite=pygame.transform.rotate(GetTileSprite(21, 3), 270))
                    elif mapTilenxn[i + 1][j - 1] == '0' and mapTilenxn[i + 1][j] == '0' and mapTilenxn[i][
                        j - 1] == '0':
                        Block(game, x + j * 32 - 32, y + i * 32 + 32, 32, 32,
                              sprite=pygame.transform.rotate(GetTileSprite(21, 3), 90))
                    elif mapTilenxn[i + 1][j + 1] == '0' and mapTilenxn[i + 1][j] == '0' and mapTilenxn[i][
                        j + 1] == '0':
                        Block(game, x + j * 32 + 32, y + i * 32 + 32, 32, 32,
                              sprite=pygame.transform.rotate(GetTileSprite(21, 3), 180))

    elif name.lower() == 'interiorvoidwall':
        for i in range(width):
            for j in range(height):
                if j == 0:
                    Block(game, x + i * 32, y + j * 32, 32, 32, sprite=GetTileSprite(19, 6))
                elif j == height - 1:
                    Block(game, x + i * 32, y + j * 32, 32, 32, sprite=GetTileSprite(19, 8))
                else:
                    Block(game, x + i * 32, y + j * 32, 32, 32, sprite=GetTileSprite(19, 7))
    elif name.lower() == 'doorwarptile':
        rotVal = [
            [90, 180, 270, 0, 90],  # down
            [0, 270, 180, 90, 270],  # up
            [0, 90, 180, 270, 0],  # left
            [270, 180, 90, 0, 180],  # right
        ]
        posOfBlocks = [
            [32, 0, -32, 0, 32, -32, -32, -32, 0, -32],  # down
            [32, 0, -32, 0, 32, 32, -32, 32, 0, 32],  # up
            [0, 32, 0, -32, 32, 32, 32, -32, 32, 0],  # left
            [0, 32, 0, -32, -32, 32, -32, -32, -32, 0],  # right
        ]
        incrementSize = [
            [0, 0, 0, 0],  # down
            [-1, -1, 2, 2],  # up
            [0, 0, 0, 0],  # left
            [0, 0, 0, 0],  # right
        ]
        if facing == 'down':
            rotValIndex = 0
        elif facing == 'up':
            rotValIndex = 1
        elif facing == 'left':
            rotValIndex = 2
        elif facing == 'right':
            rotValIndex = 3
        else:
            rotValIndex = -1
        print('warptileExit', x, y, 32, 32)
        killAtPosition(game, x, y)
        Block(game, x, y, 32, 32, sprite=GetTileSprite(4, 3), hasHitBox=False, isGround=True)
        Objects(game, x + incrementSize[rotValIndex][0], y + incrementSize[rotValIndex][1],
                32 + incrementSize[rotValIndex][2], 32 + incrementSize[rotValIndex][3], type='warptile',
                content=[doorsTag[0], doorsTag[1]])
        Block(game, x + posOfBlocks[rotValIndex][0], y + posOfBlocks[rotValIndex][1], 32, 32,
              sprite=pygame.transform.rotate(GetTileSprite(18, 19), rotVal[rotValIndex][0]))
        Block(game, x + posOfBlocks[rotValIndex][2], y + posOfBlocks[rotValIndex][3], 32, 32,
              sprite=pygame.transform.rotate(GetTileSprite(18, 19), rotVal[rotValIndex][1]))
        Block(game, x + posOfBlocks[rotValIndex][4], y + posOfBlocks[rotValIndex][5], 32, 32,
              sprite=pygame.transform.rotate(GetTileSprite(21, 3), rotVal[rotValIndex][2]))
        Block(game, x + posOfBlocks[rotValIndex][6], y + posOfBlocks[rotValIndex][7], 32, 32,
              sprite=pygame.transform.rotate(GetTileSprite(21, 3), rotVal[rotValIndex][3]))
        Block(game, x + posOfBlocks[rotValIndex][8], y + posOfBlocks[rotValIndex][9], 32, 32,
              sprite=pygame.transform.rotate(GetTileSprite(18, 20), rotVal[rotValIndex][4]))
    elif name.lower() == 'brick_door':
        print('warptileEntrance', x - 1, y + 32 - 16, 34, 39)
        killAtPosition(game, x, y + 0)
        killAtPosition(game, x, y + 32)
        Block(game, x, y - 32, 32, 32, sprite=GetTileSprite(22, 11), hasHitBox=False)
        Block(game, x, y + 0, 32, 32, sprite=GetTileSprite(25, 1), hasHitBox=False)
        Block(game, x, y + 32, 32, 32, sprite=GetTileSprite(25, 2), hasHitBox=False)
        Objects(game, x - 1, y + 32 - 16, 34, 49, type='warptile', content=[doorsTag[0], doorsTag[1]])
    elif name.lower() == 'brick_doubledoor':
        for i in range(3):
            for j in range(2):
                killAtPosition(game, x + i * 32, y + j * 32)
        Block(game, x + 0, y - 32, 32, 32, sprite=GetTileSprite(22, 11), hasHitBox=False)
        Block(game, x + 32, y - 32, 32, 32, sprite=GetTileSprite(22, 11), hasHitBox=False)
        Block(game, x + 64, y - 32, 32, 32, sprite=GetTileSprite(22, 11), hasHitBox=False)
        Block(game, x + 0, y + 32, 32, 32, sprite=GetTileSprite(4, 3), hasHitBox=False)
        Block(game, x + 32, y + 32, 32, 32, sprite=GetTileSprite(4, 3), hasHitBox=False)
        Block(game, x + 64, y + 32, 32, 32, sprite=GetTileSprite(4, 3), hasHitBox=False)
        Block(game, x + 0, y + 0, 32, 32, sprite=GetTileSprite(29, 1), hasHitBox=False)
        Block(game, x + 0, y + 32, 32, 32, sprite=GetTileSprite(29, 2), hasHitBox=False)
        Block(game, x + 32, y + 0, 32, 32, sprite=GetTileSprite(30, 1), hasHitBox=False)
        Block(game, x + 32, y + 32, 32, 32, sprite=GetTileSprite(30, 2), hasHitBox=False)
        Block(game, x + 64, y + 0, 32, 32, sprite=GetTileSprite(31, 1), hasHitBox=False)
        Block(game, x + 64, y + 32, 32, 32, sprite=GetTileSprite(31, 2), hasHitBox=False)
        Objects(game, x + 16 - 1, y + 32 - 16, 66, 49, type='warptile', content=[doorsTag[0], doorsTag[1]])
    elif name.lower() == 'interiorbrickwallcorner_facing_left':
        for j in range(height):
            killAtPosition(game, x, y + j * 32)
            if j == 0:
                Block(game, x, y + j * 32, 32, 32, sprite=pygame.transform.flip(GetTileSprite(20, 22), True, False))
            elif j == height - 1:
                Block(game, x, y + j * 32, 32, 32, sprite=pygame.transform.flip(GetTileSprite(20, 24), True, False))
            else:
                Block(game, x, y + j * 32, 32, 32, sprite=pygame.transform.flip(GetTileSprite(20, 23), True, False))
    elif name.lower() == 'interiorbrickwallcorner_facing_right':
        for j in range(height):
            if j == 0:
                Block(game, x, y + j * 32, 32, 32, sprite=GetTileSprite(20, 22))
            elif j == height - 1:
                Block(game, x, y + j * 32, 32, 32, sprite=GetTileSprite(20, 24))
            else:
                Block(game, x, y + j * 32, 32, 32, sprite=GetTileSprite(20, 23))
    elif name.lower() == 'brick_pillar':
        for i in range(width):
            for j in range(height):
                if j == 0:
                    if tag and 'isWall' in tag:
                        if 'doesNotOverwrite' not in tag:
                            killAtPosition(game, x + i * 32, y + j * 32 - 32 + 16)
                            Block(game, x + i * 32, y + j * 32 - 32 + 16, 32, 32, sprite=GetTileSprite(21, 5),
                                  hasHitBox=False, setLayer=setLayer)
                    else:
                        Block(game, x + i * 32, y + j * 32 - 32 + 16, 32, 32, sprite=GetTileSprite(22, 21),
                              hasHitBox=False, setLayer=setLayer)
                    Block(game, x + i * 32, y + j * 32 + 16, 32, 32, sprite=GetTileSprite(21, 22), hasHitBox=False, setLayer=setLayer)
                elif j == height - 1:
                    Block(game, x + i * 32, y + j * 32 + 16, 32, 32, sprite=GetTileSprite(21, 24), hasHitBox=False, setLayer=setLayer)
                    Block(game, x + i * 32, y + j * 32 + 32 + 16, 32, 32, sprite=GetTileSprite(21, 25), hasHitBox=False, setLayer=setLayer)
                else:
                    Block(game, x + i * 32, y + j * 32 + 16, 32, 32, sprite=GetTileSprite(21, 23), hasHitBox=False, setLayer=setLayer)
                if not tag or 'isWall' not in tag:
                    # Block(game, x + 0, y + 0, 32 * width, 32 * (height + 1), color=WHITE)
                    pass
    elif name.lower() == 'brick_pillar_head':
        Block(game, x, y, 32, 32, sprite=GetTileSprite(22, 21),
              hasHitBox=False)

    elif name.lower() == 'brick_window':
        Block(game, x, y + 0, 32, 32, sprite=GetTileSprite(22, 9), hasHitBox=False)
        Block(game, x, y + 32, 32, 32, sprite=GetTileSprite(22, 10), hasHitBox=False)
    elif name.lower() == 'red_curtain_facing_left':
        Block(game, x + 0 - 0, y + 0 - 0, 32, 32, sprite=GetTileSprite(32, 17), hasHitBox=False)
        Block(game, x + 0 - 0, y + 32 - 0, 32, 32, sprite=GetTileSprite(32, 18), hasHitBox=False)
        Block(game, x + 0 - 0, y + 64 - 0, 32, 32, sprite=GetTileSprite(23, 14), hasHitBox=False)
        Block(game, x + 0 - 0, y + 96 - 0, 32, 32, sprite=GetTileSprite(21, 14), hasHitBox=False)
    elif name.lower() == 'red_curtain_facing_right':
        Block(game, x + 0 - 0, y + 0 - 0, 32, 32, sprite=pygame.transform.flip(GetTileSprite(32, 17), True, False),
              hasHitBox=False)
        Block(game, x + 0 - 0, y + 32 - 0, 32, 32, sprite=pygame.transform.flip(GetTileSprite(32, 18), True, False),
              hasHitBox=False)
        Block(game, x + 0 - 0, y + 64 - 0, 32, 32, sprite=pygame.transform.flip(GetTileSprite(23, 14), True, False),
              hasHitBox=False)
        Block(game, x + 0 - 0, y + 96 - 0, 32, 32, sprite=pygame.transform.flip(GetTileSprite(21, 14), True, False),
              hasHitBox=False)
    elif name.lower() == 'bed':
        y -= 32
        for i in range(4):
            Block(game, x + 0 - 24, y + (i + 1) * 32 - 48, 32, 32, sprite=GetTileSprite(31, 12 + i), hasHitBox=False)
            Block(game, x + 32 - 24, y + (i + 1) * 32 - 48, 32, 32, sprite=GetTileSprite(32, 12 + i), hasHitBox=False)
            Block(game, x + 64 - 24, y + (i + 1) * 32 - 48, 32, 32, sprite=GetTileSprite(33, 12 + i), hasHitBox=False)
        Block(game, x + 0, y + 0, 48, 96, color=WHITE)
    elif name.lower() == 'green_carpet':
        for i in range(width):
            for j in range(height):
                if i == 0 and j == 0:
                    Block(game, x + i * 32, y + j * 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(26, 11), 0), hasHitBox=False, isGround=True)
                elif i == 0 and j == height - 1:
                    Block(game, x + i * 32, y + j * 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(26, 11), 90), hasHitBox=False, isGround=True)
                elif i == width - 1 and j == 0:
                    Block(game, x + i * 32, y + j * 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(26, 11), 270), hasHitBox=False, isGround=True)
                elif i == width - 1 and j == height - 1:
                    Block(game, x + i * 32, y + j * 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(26, 11), 180), hasHitBox=False, isGround=True)
                elif i == 0:
                    Block(game, x + i * 32, y + j * 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(26, 12), 0), hasHitBox=False, isGround=True)
                elif i == width - 1:
                    Block(game, x + i * 32, y + j * 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(26, 12), 180), hasHitBox=False, isGround=True)
                elif j == 0:
                    Block(game, x + i * 32, y + j * 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(26, 12), 270), hasHitBox=False, isGround=True)
                elif j == height - 1:
                    Block(game, x + i * 32, y + j * 32, 32, 32,
                          sprite=pygame.transform.rotate(GetTileSprite(26, 12), 90), hasHitBox=False, isGround=True)
                else:
                    Block(game, x + i * 32, y + j * 32, 32, 32, sprite=GetTileSprite(27, 12), hasHitBox=False,
                          isGround=True)
        # Block(game, x, y, 32, 32, sprite=GetTileSprite(26, 11), hasHitBox=False, isGround=True)
        # Block(game, x + 32, y, 32, 32, sprite=GetTileSprite(27, 11), hasHitBox=False, isGround=True)
        # Block(game, x, y + 32, 32, 32, sprite=GetTileSprite(26, 12), hasHitBox=False, isGround=True)
        # Block(game, x + 32, y + 32, 32, 32, sprite=GetTileSprite(27, 12), hasHitBox=False, isGround=True)
    elif name.lower() == 'red_carpet':
        for i in range(width):
            for j in range(height):
                if width == 1:
                    Block(game, x + i * 32, y + j * 32, 32, 32, sprite=GetTileSprite(29, 17), hasHitBox=False,
                          isGround=True)
                elif i == 0:
                    Block(game, x + i * 32, y + j * 32, 32, 32,
                          sprite=GetTileSprite(28, 17), hasHitBox=False, isGround=True)
                elif i == width - 1:
                    Block(game, x + i * 32, y + j * 32, 32, 32,
                          sprite=GetTileSprite(30, 17), hasHitBox=False, isGround=True)
                else:
                    Block(game, x + i * 32, y + j * 32, 32, 32, sprite=GetTileSprite(29, 17), hasHitBox=False,
                          isGround=True)
    elif name.lower() == 'fireplace':
        y -= 32
        Block(game, x + 0 - 8, y - 32, 32, 32, sprite=GetTileSprite(28, 13), hasHitBox=False)
        Block(game, x + 32 - 8, y - 32, 32, 32, sprite=GetTileSprite(28, 20), hasHitBox=False)
        Block(game, x + 64 - 8, y - 32, 32, 32, sprite=GetTileSprite(30, 13), hasHitBox=False)
        for i in range(2):
            Block(game, x + 0 - 8, y + (i + 1) * 32 - 32, 32, 32, sprite=GetTileSprite(28, 14 + i), hasHitBox=False)
            Block(game, x + 32 - 8, y + (i + 1) * 32 - 32, 32, 32, sprite=GetTileSprite(29, 14 + i), hasHitBox=False)
            Block(game, x + 64 - 8, y + (i + 1) * 32 - 32, 32, 32, sprite=GetTileSprite(30, 14 + i), hasHitBox=False)
        Block(game, x + 0, y + 0, 80, 64, color=WHITE)
    elif name.lower() == 'wood_desk':
        for i in range(width):
            for j in range(2):
                if i == 0:
                    Block(game, x + i * 32 - 2, y + j * 32 - 16, 32, 32, sprite=GetTileSprite(18, 14 + j),
                          hasHitBox=False)
                elif i == width - 1:
                    Block(game, x + i * 32 - 2, y + j * 32 - 16, 32, 32, sprite=GetTileSprite(20, 14 + j),
                          hasHitBox=False)
                else:
                    Block(game, x + i * 32 - 2, y + j * 32 - 16, 32, 32, sprite=GetTileSprite(19, 14 + j),
                          hasHitBox=False)
        Block(game, x + 0, y + 0, 32 * width, 32, color=WHITE)
    elif name.lower() == 'wood_bedcase':
        Block(game, x + 0 - 0, y + 0 - 16, 32, 32, sprite=GetTileSprite(25, 13), hasHitBox=False)
        Block(game, x + 0 - 0, y + 32 - 16, 32, 32, sprite=GetTileSprite(22, 15), hasHitBox=False)
        Block(game, x + 0 - 0, y + 0 - 16, 32, 32, sprite=GetTileSprite(29, 23), hasHitBox=False)
        Block(game, x + 0 - 0, y - 32 - 16, 32, 32, sprite=GetTileSprite(29, 22), hasHitBox=False)
        Block(game, x + 0, y + 0, 32, 32, color=WHITE)
    elif name.lower() == 'flowerpot':
        Block(game, x + 0 - 0, y + 0, 32, 32, sprite=GetTileSprite(29, 13))
        pass
    elif name.lower() == 'wood_chair_facing_up':
        Block(game, x + 0 - 4, y + 0 - 16, 32, 32, sprite=GetTileSprite(29, 11), hasHitBox=False)
        Block(game, x + 0 - 4, y + 32 - 16, 32, 32, sprite=GetTileSprite(29, 12), hasHitBox=False)
        # Block(game, x + 0, y + 0, 26, 32, color=WHITE)
    elif name.lower() == 'wood_chair_facing_down':
        Block(game, x + 0 - 4, y + 0 - 16, 32, 32, sprite=GetTileSprite(28, 11), hasHitBox=False)
        Block(game, x + 0 - 4, y + 32 - 16, 32, 32, sprite=GetTileSprite(28, 12), hasHitBox=False)
        # Block(game, x + 0, y + 0, 26, 32, color=WHITE)
    elif name.lower() == 'wood_chair_facing_left':
        Block(game, x + 0 - 4, y - 32 - 16, 32, 32, sprite=GetTileSprite(31, 22), hasHitBox=False)
        Block(game, x + 0 - 4, y + 0 - 16, 32, 32, sprite=GetTileSprite(31, 23), hasHitBox=False)
        Block(game, x + 0 - 4, y + 32 - 16, 32, 32, sprite=GetTileSprite(27, 13), hasHitBox=False)
        # Block(game, x + 0, y + 0, 26, 32, color=WHITE)
    elif name.lower() == 'wood_chair_facing_right':
        Block(game, x + 0 - 4, y - 32 - 16, 32, 32, sprite=GetTileSprite(30, 22), hasHitBox=False)
        Block(game, x + 0 - 4, y + 0 - 16, 32, 32, sprite=GetTileSprite(30, 23), hasHitBox=False)
        Block(game, x + 0 - 4, y + 32 - 16, 32, 32, sprite=GetTileSprite(26, 13), hasHitBox=False)
        # Block(game, x + 0, y + 0, 26, 32, color=WHITE)
    elif name.lower() == 'wood_whitetable':
        Block(game, x + 0 - 0, y + 32 - 32, 32, 32, sprite=GetTileSprite(29, 16), hasHitBox=False)
        Block(game, x + 0 - 0, y + 0 - 32, 32, 32, sprite=GetTileSprite(31, 17), hasHitBox=False)
        Block(game, x + 0, y + 0, 32, 32, color=WHITE)
    elif name.lower() == 'candle':
        Block(game, x + 0 - 0, y + 0 - 0, 32, 32, sprite=GetTileSprite(25, 18), hasHitBox=False)
        pass
    elif name.lower() == 'snake_candle':
        Block(game, x + 0 - 0, y + 0 - 0, 32, 32, sprite=GetTileSprite(22, 23), hasHitBox=False)
        pass
    elif name.lower() == 'brick_stairs':
        for i in range(width):
            for j in range(height):
                Block(game, x + i * 32 - 0, y + j * 32 - 0, 32, 32, sprite=GetTileSprite(32, 28), hasHitBox=False)
    elif 'brick_stairs_special' in name.lower():
        if 'corner_left' in name.lower():
            for j in range(height):
                Block(game, x, y + j * 32, 32, 32, sprite=GetTileSprite(29, 29), hasHitBox=False)
        elif 'corner_right' in name.lower():
            for j in range(height):
                Block(game, x, y + j * 32, 32, 32, sprite=GetTileSprite(28, 29), hasHitBox=False)
        elif 'corner_reverse_left' in name.lower():
            for j in range(height):
                Block(game, x, y + j * 32, 32, 32, sprite=GetTileSprite(29, 30), hasHitBox=False)
        elif 'corner_reverse_right' in name.lower():
            for j in range(height):
                Block(game, x, y + j * 32, 32, 32, sprite=GetTileSprite(28, 30), hasHitBox=False)
        elif 'facing_left' in name.lower():
            for j in range(height):
                Block(game, x, y + j * 32, 32, 32, sprite=GetTileSprite(30, 29), hasHitBox=False)
        elif 'facing_right' in name.lower():
            for j in range(height):
                Block(game, x, y + j * 32, 32, 32, sprite=GetTileSprite(31, 29), hasHitBox=False)
    elif name.lower() == 'brick_red_carpet_stairs':
        for i in range(width):
            for j in range(height):
                if i == 0:
                    Block(game, x + i * 32 - 0, y + j * 32 - 0, 32, 32, sprite=GetTileSprite(32, 29), hasHitBox=False)
                elif i == width - 1:
                    Block(game, x + i * 32 - 0, y + j * 32 - 0, 32, 32, sprite=GetTileSprite(33, 29), hasHitBox=False)
                else:
                    Block(game, x + i * 32 - 0, y + j * 32 - 0, 32, 32, sprite=GetTileSprite(33, 28), hasHitBox=False)
    elif name.lower() == 'brick_handrail_facing_left':
        for i in range(height):
            if i == 0:
                Block(game, x + 0 - 0, y + i * 32 - 32, 32, 32, sprite=GetTileSprite(26, 3), hasHitBox=False)
                Block(game, x + 0 - 0, y + i * 32, 32, 32, sprite=GetTileSprite(29, 4), hasHitBox=False)
            elif i == height - 1:
                Block(game, x + 0 - 0, y + i * 32, 32, 32, sprite=GetTileSprite(27, 4), hasHitBox=False)
                Block(game, x + 0 - 0, y + i * 32 + 32, 32, 32, sprite=GetTileSprite(26, 4), hasHitBox=False)
            else:
                Block(game, x + 0 - 0, y + i * 32, 32, 32, sprite=GetTileSprite(28, 4), hasHitBox=False)
        Block(game, x + 0 - 0, y + 0 - 0, 32, (height + 1) * 32, color=WHITE)
    elif name.lower() == 'brick_handrail_facing_right':
        for i in range(height):
            if i == 0:
                Block(game, x + 0 - 0, y + i * 32 - 32, 32, 32, sprite=GetTileSprite(26, 3), hasHitBox=False)
                Block(game, x + 0 - 0, y + i * 32, 32, 32, sprite=GetTileSprite(29, 3), hasHitBox=False)
            elif i == height - 1:
                Block(game, x + 0 - 0, y + i * 32, 32, 32, sprite=GetTileSprite(27, 3), hasHitBox=False)
                Block(game, x + 0 - 0, y + i * 32 + 32, 32, 32, sprite=GetTileSprite(26, 4), hasHitBox=False)
            else:
                Block(game, x + 0 - 0, y + i * 32, 32, 32, sprite=GetTileSprite(28, 3), hasHitBox=False)
        Block(game, x + 0 - 0, y + 0 - 0, 32, (height + 1) * 32, color=WHITE)
    elif name.lower() == 'bronze_armourstand':
        Block(game, x + 0 - 0, y + 0 - 32, 32, 32, sprite=GetTileSprite(30, 19), hasHitBox=False)
        Block(game, x + 0 - 0, y + 32 - 32, 32, 32, sprite=GetTileSprite(33, 16), hasHitBox=False)
        Block(game, x + 0 - 0, y + 0 - 0, 32, 32, color=WHITE)
    elif name.lower() == 'blue_throne_chair':
        Block(game, x + 0 - 0, y + 0 - 48, 32, 32, sprite=GetTileSprite(23, 19), hasHitBox=False)
        Block(game, x + 0 - 0, y + 32 - 48, 32, 32, sprite=GetTileSprite(23, 20), hasHitBox=False)
        Block(game, x + 0 - 0, y + 64 - 48, 32, 32, sprite=GetTileSprite(25, 20), hasHitBox=False)
        Block(game, x + 0 - 0, y + 0 - 0, 32, 32, color=WHITE)


class Objects(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, type='', color=RED, state=0, content=None, mapName=None, chestTier=0):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.objects
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.type = type
        self.color = color
        self.content = content
        self.state = state
        self.mapName = mapName

        if self.type == 'chest':
            self.image = pygame.transform.scale(self.game.castleTiles_spritesheet.get_sprite(320, 16, 16, 16), (32, 32))
            self.content = zoneChestLoot(self.mapName, chestTier)
        if self.type == 'warptile':
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.color)
            # self.content is the warp [x, y]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.hitbox = self.rect.inflate(0, 0)

    def update(self):
        self.hitbox = self.rect.inflate(0, 0)
        if self.type == 'chest':
            if self.state == 0:
                self.image = pygame.transform.scale(self.game.castleTiles_spritesheet.get_sprite(320, 16, 16, 16),
                                                    (32, 32))
            else:
                self.image = pygame.transform.scale(self.game.castleTiles_spritesheet.get_sprite(304, 16, 16, 16),
                                                    (32, 32))


def killAtPosition(game, x, y):
    for block in game.blocks:
        if not hasattr(block, 'isGround') and block.rect.x == x and block.rect.y == y:
            block.kill()
