import math
import random

import pygame
from config import *
from Player_Data import *
from Itens import *
from zones import *
from TileData import *


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(WHITE)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name='', render=False):
        self.game = game

        self.x = x * TILESIZE
        self.y = y * TILESIZE - 16
        self.render = render
        self.x_change = 0
        self.y_change = 0
        self.walkTick = 0
        self.data = DataPlayer(name)
        self.facing = 'down'
        self.interact_timer = 0
        self.animation_loop = 1
        self.itemToUse = None
        self.confirmTeleport = None

        self.width = self.data.sprite[2]
        self.height = self.data.sprite[3]
        self.image = pygame.transform.scale(
            self.game.playableNpcs_spritesheet.get_sprite(self.data.sprite[0] + 60, self.data.sprite[1], self.width,
                                                          self.height), (self.width * 2, self.height * 2))
        self.imagebattle = self.image
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(0, -16).copy()
        self.hitbox.y = self.rect.y + 16
        if self.render:
            self._layer = PLAYER_LAYER
            self.groups = self.game.all_sprites
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self._layer = GUI_LAYER - 1
            self.groups = self.game.battle_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        if self.render:
            if self.interact_timer > 0:
                self.interact_timer -= 1
            if self.x_change == 0 and self.y_change == 0:
                self.movement()
            self.animate()

            if self.x_change != 0:
                self.rect.x += self.x_change / abs(self.x_change) * PLAYER_SPEED
            self.collide_blocks('x')
            if self.y_change != 0:
                self.rect.y += self.y_change / abs(self.y_change) * PLAYER_SPEED
            self.collide_blocks('y')
            self.collide_npcs()

            if self.x_change != 0:
                self.x_change += -self.x_change / abs(self.x_change) * PLAYER_SPEED
            elif self.y_change != 0:
                self.y_change += -self.y_change / abs(self.y_change) * PLAYER_SPEED

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.y_change = GLOBAL_SPEED
            self.facing = 'down'
            # for sprite in self.game.all_sprites:
            #     sprite.rect.y -= PLAYER_SPEED
        elif keys[pygame.K_w]:
            self.y_change = - GLOBAL_SPEED
            self.facing = 'up'
            # for sprite in self.game.all_sprites:
            #     sprite.rect.y += PLAYER_SPEED
        elif keys[pygame.K_a]:
            self.x_change = - GLOBAL_SPEED
            self.facing = 'left'
            # for sprite in self.game.all_sprites:
            #     sprite.rect.x += PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.x_change = GLOBAL_SPEED
            self.facing = 'right'
            # for sprite in self.game.all_sprites:
            #     sprite.rect.x -= PLAYER_SPEED
        if keys[pygame.K_e]:
            if self.interact_timer == 0:
                self.interact_timer = 30
                if self.confirmTeleport:
                    self.rect.x = self.confirmTeleport[0]
                    self.rect.y = self.confirmTeleport[1]
                    print('Zoned to', self.confirmTeleport)
                    pygame.mixer.Sound.play(pygame.mixer.Sound("ost/dooropening.wav"))
                    self.confirmTeleport = None
        self.confirmTeleport = None

    def collide_blocks(self, direction):
        self.hitbox = self.rect.inflate(0, -16).copy()
        self.hitbox.y = self.rect.y + 16
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False, collided)
        hits1 = pygame.sprite.spritecollide(self, self.game.objects, False, collided)
        if hits:
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right - (self.rect.width - self.hitbox.width)
                self.x_change = 0
            if direction == 'y':
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom - (self.rect.height - self.hitbox.height)
                self.y_change = 0
        if hits1:
            if hits1[0].type == 'chest':
                if hits1[0].content and (self.data.checkInv('key') or hits1[0].state == 1):
                    if hits1[0].state == 0:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("ost/chestopening.wav"))
                        self.data.removeFromInv('key')
                    for item in hits1[0].content:
                        self.data.addToInv(item)
                    AlertText(self.game, 'Chest Open', self.rect.x - 8, self.rect.y - 32, YELLOW, 'info')
                    hits1[0].content = []
                    hits1[0].state = 1
            if hits1[0].type == 'warptile':
                self.confirmTeleport = [hits1[0].content[0] + self.game.zeroCoord.rect.x,
                                        hits1[0].content[1] + self.game.zeroCoord.rect.y - 16]
            elif direction == 'x':
                if hits1:
                    if self.x_change > 0:
                        self.rect.x = hits1[0].rect.left - self.rect.width
                    if self.x_change < 0:
                        self.rect.x = hits1[0].rect.right - (self.rect.width - self.hitbox.width)
                    self.x_change = 0
            elif direction == 'y':
                if hits1:
                    if self.y_change > 0:
                        self.rect.y = hits1[0].rect.top - self.rect.height
                    if self.y_change < 0:
                        self.rect.y = hits1[0].rect.bottom - (self.rect.height - self.hitbox.height)
                    self.y_change = 0

    def collide_npcs(self):
        self.hitbox = self.rect.inflate(0, -16).copy()
        self.hitbox.y = self.rect.y + 16
        hits = pygame.sprite.spritecollide(self, self.game.npc_sprites, False, collided)
        if hits:
            if hits[0].data.hasHitBox:
                if hits[0].data.textBox:
                    missionList = []
                    for text in hits[0].data.textBox:
                        print(text, self.data.missions)
                        if text[0].lower() == 'mission' and text[1] not in self.data.missions:
                            missionList.append(text[1])
                    if missionList:
                        AlertText(self.game, 'New Mission', self.rect.x, self.rect.y - 32, BLUE, 'info')
                        pygame.mixer.Sound.play(pygame.mixer.Sound("ost/received_something.wav"))
                    self.data.missions += missionList
                    # print(self.data.missions)
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right - (self.rect.width - self.hitbox.width)
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom - (self.rect.height - self.hitbox.height)
                self.x_change = 0
                self.y_change = 0

    def animate(self):
        coord = self.data.sprite
        down_animations = [self.game.playableNpcs_spritesheet.get_sprite(coord[0], coord[1], self.width, self.height),
                           self.game.playableNpcs_spritesheet.get_sprite(coord[0], coord[1] + 30, self.width,
                                                                         self.height),
                           self.game.playableNpcs_spritesheet.get_sprite(coord[0], coord[1] + 60, self.width,
                                                                         self.height)]
        up_animations = [
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 30, coord[1], self.width, self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 30, coord[1] + 30, self.width,
                                                          self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 30, coord[1] + 60, self.width,
                                                          self.height)]
        left_animations = [
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 60, coord[1], self.width, self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 60, coord[1] + 30, self.width,
                                                          self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 60, coord[1] + 60, self.width,
                                                          self.height)]
        right_animations = [
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 90, coord[1], self.width, self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 90, coord[1] + 30, self.width, self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 90, coord[1] + 60, self.width, self.height)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.playableNpcs_spritesheet.get_sprite(coord[0], coord[1], self.width,
                                                                           self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 30, coord[1], self.width,
                                                                           self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 60, coord[1], self.width,
                                                                           self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 90, coord[1], self.width,
                                                                           self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        self.image = pygame.transform.scale(self.image, (self.width * 2, self.height * 2))

    def useItem(self, itemName, alertPos=None):
        for i in range(len(self.data.inv)):
            if self.data.inv[i].name.lower() == itemName.lower():
                textForAlertBox = []
                colorForAlertBox = []
                for element in self.data.inv[i].tags:
                    if element[0].lower() == 'hp':
                        self.data.hp += element[1]
                        if self.data.hp >= self.data.maxhpmp[0]:
                            self.data.hp = self.data.maxhpmp[0]
                        if alertPos:
                            textForAlertBox.append(element)
                            colorForAlertBox.append(RED)
                    elif element[0].lower() == 'mp':
                        self.data.mp += element[1]
                        if self.data.mp >= self.data.maxhpmp[1]:
                            self.data.mp = self.data.maxhpmp[1]
                        if alertPos:
                            textForAlertBox.append(element)
                            colorForAlertBox.append(PURPLE)
                if alertPos:
                    AlertText(self.game, textForAlertBox, alertPos[2][0][0], alertPos[2][0][1], colorForAlertBox,
                              'info')
                del self.data.inv[i]
                break


class Npc(pygame.sprite.Sprite):
    def __init__(self, game, x, y, map, name='guard'):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.npc_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.name = name
        self.map = map
        self.data = DataNpc(self.name, map=self.map)
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 1
        self.movementTick = 0
        self.internalTick = 0
        if self.data.holdPosition:
            self.x = self.data.holdPosition[0]
            self.y = self.data.holdPosition[1]
            self.facing = self.data.holdPosition[1]
        self.width = self.data.sprite[2]
        self.height = self.data.sprite[3]

        self.image = pygame.transform.scale(
            self.game.playableNpcs_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1], self.width,
                                                          self.height), (self.width * 2, self.height * 2))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.hitbox = self.rect.inflate(0, -16).copy()
        self.hitbox.y += 16

    def update(self):
        if self.internalTick > 0:
            self.internalTick -= 1
        if self.internalTick == 0:
            self.internalTick = 60
        if self.internalTick % 3 == 0:
            self.movement()
            self.animate()
        # pygame.draw.rect(self.image, PURPLE, (0, 16, self.hitbox.width, self.hitbox.height))
        if self.data.holdPosition:
            self.x_change = 0
            self.y_change = 0
        if self.x_change != 0:
            self.rect.x += self.x_change / abs(self.x_change) * 1
        self.collide_blocks('x')
        if self.y_change != 0:
            self.rect.y += self.y_change / abs(self.y_change) * 1
        self.collide_blocks('y')
        if self.x_change != 0:
            self.x_change += -self.x_change / abs(self.x_change) * 1
        elif self.y_change != 0:
            self.y_change += -self.y_change / abs(self.y_change) * 1

    def movement(self):
        if not self.data.holdPosition:
            if self.movementTick > 0:
                self.movementTick -= 1
            if self.movementTick == 0:
                self.facing = random.choice(['left', 'right', 'down', 'up'])
                self.movementTick = random.randint(60, 300)
            if self.facing == 'left':
                self.x_change = - GLOBAL_SPEED
            elif self.facing == 'right':
                self.x_change = GLOBAL_SPEED
            elif self.facing == 'up':
                self.y_change = - GLOBAL_SPEED
            elif self.facing == 'down':
                self.y_change = GLOBAL_SPEED

    def collide_blocks(self, direction):
        self.hitbox = self.rect.inflate(0, -16).copy()
        self.hitbox.y = self.rect.y + 16
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False, collided)
        hits1 = pygame.sprite.spritecollide(self, self.game.objects, False, collided)
        if direction == 'x':
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    self.facing = random.choice(['down', 'left', 'up'])
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right - (self.rect.width - self.hitbox.width)
                    self.facing = random.choice(['down', 'right', 'up'])
                self.x_change = 0
        if direction == 'y':
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    self.facing = random.choice(['left', 'up', 'right'])
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom - (self.rect.height - self.hitbox.height)
                    self.facing = random.choice(['left', 'down', 'right'])
                self.y_change = 0
        if direction == 'x':
            if hits1:
                if self.x_change > 0:
                    self.rect.x = hits1[0].rect.left - self.rect.width
                    self.facing = random.choice(['down', 'left', 'up'])
                if self.x_change < 0:
                    self.rect.x = hits1[0].rect.right - (self.rect.width - self.hitbox.width)
                    self.facing = random.choice(['down', 'right', 'up'])
                self.x_change = 0
        if direction == 'y':
            if hits1:
                if self.y_change > 0:
                    self.rect.y = hits1[0].rect.top - self.rect.height
                    self.facing = random.choice(['left', 'up', 'right'])
                if self.y_change < 0:
                    self.rect.y = hits1[0].rect.bottom - (self.rect.height - self.hitbox.height)
                    self.facing = random.choice(['left', 'down', 'right'])
                self.y_change = 0

    def animate(self):
        coord = self.data.sprite
        down_animations = [self.game.playableNpcs_spritesheet.get_sprite(coord[0], coord[1], self.width, self.height),
                           self.game.playableNpcs_spritesheet.get_sprite(coord[0], coord[1] + 30, self.width,
                                                                         self.height),
                           self.game.playableNpcs_spritesheet.get_sprite(coord[0], coord[1] + 60, self.width,
                                                                         self.height)]
        up_animations = [
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 30, coord[1], self.width, self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 30, coord[1] + 30, self.width,
                                                          self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 30, coord[1] + 60, self.width,
                                                          self.height)]
        left_animations = [
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 60, coord[1], self.width, self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 60, coord[1] + 30, self.width,
                                                          self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 60, coord[1] + 60, self.width,
                                                          self.height)]
        right_animations = [
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 90, coord[1], self.width, self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 90, coord[1] + 30, self.width, self.height),
            self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 90, coord[1] + 60, self.width, self.height)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = pygame.transform.scale(
                    self.game.playableNpcs_spritesheet.get_sprite(coord[0], coord[1], self.width, self.height),
                    (self.width * 2, self.height * 2))
            else:
                self.image = pygame.transform.scale(down_animations[math.floor(self.animation_loop)],
                                                    (self.width * 2, self.height * 2))
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = pygame.transform.scale(
                    self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 30, coord[1], self.width,
                                                                  self.height), (self.width * 2, self.height * 2))
            else:
                self.image = pygame.transform.scale(up_animations[math.floor(self.animation_loop)],
                                                    (self.width * 2, self.height * 2))
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = pygame.transform.scale(
                    self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 60, coord[1], self.width,
                                                                  self.height), (self.width * 2, self.height * 2))
            else:
                self.image = pygame.transform.scale(left_animations[math.floor(self.animation_loop)],
                                                    (self.width * 2, self.height * 2))
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = pygame.transform.scale(
                    self.game.playableNpcs_spritesheet.get_sprite(coord[0] + 90, coord[1], self.width,
                                                                  self.height), (self.width * 2, self.height * 2))
            else:
                self.image = pygame.transform.scale(right_animations[math.floor(self.animation_loop)],
                                                    (self.width * 2, self.height * 2))
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, name=''):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.battle_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.data = DataEnemy(name)
        self.x_change = 0
        self.y_change = 0

        self.image = self.game.creatures_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1],
                                                                self.data.box[0], self.data.box[1])

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        pass


class BackgroundMap(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.name = name
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = 6120
        self.height = 2048
        self.music = None

        self.image = self.game.map_spritesheet.get_sprite(0, 0, 6120, 2048)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.warpCoord = []

        if self.name == 'DomaCastle':
            # DomaCastleTheme
            self.music = "ost/113_Cyan.mp3"
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.set_volume(0.5)
            # pygame.mixer.music.play(-1)

            # WarpCoords
            self.warpCoord.append(['spawn0', [33, 38]])
            self.warpCoord.append(['DomaCastleExterior0', [1052, 1522]])
            self.warpCoord.append(['DomaCastleExterior1', [1060, 1160]])
            self.warpCoord.append(['DomaCastleInterior1', [4390, 1488]])  # Main Room
            self.warpCoord.append(['DomaCastleInterior1Exit', [894, 1053]])
            self.warpCoord.append(['DomaCastleInterior2', [5862, 1610]])  # Bedrooms 1
            self.warpCoord.append(['DomaCastleInterior2Exit', [4232, 1422]])
            self.warpCoord.append(['DomaCastleInterior3', [4200, 338]])  # Bedrooms 2
            self.warpCoord.append(['DomaCastleInterior3Exit', [4552, 1422]])
            self.warpCoord.append(['DomaCastleInterior4', [5352, 274]])  # Kitchen 1.1
            self.warpCoord.append(['DomaCastleInterior4Exit', [4202, 1082]])
            self.warpCoord.append(['DomaCastleInterior5', [5640, 274]])  # Kitchen 1.2
            self.warpCoord.append(['DomaCastleInterior5Exit', [4586, 1082]])
            self.warpCoord.append(['DomaCastleInterior6', [5704, 882]])  # Stairs 1
            self.warpCoord.append(['DomaCastleInterior6Exit', [4614, 1138]])
            self.warpCoord.append(['DomaCastleInterior7', [3742, 1938]])  # Storage 1
            self.warpCoord.append(['DomaCastleInterior7Exit', [5352, 274]])
            self.warpCoord.append(['DomaCastleInterior8', [4968, 1074]])  # Bedrooms 3
            self.warpCoord.append(['DomaCastleInterior8Exit', [5416, 274]])
            self.warpCoord.append(['DomaCastleInterior9', [4968, 1650]])  # Armory 1
            self.warpCoord.append(['DomaCastleInterior9Exit', [5672, 818]])
            self.warpCoord.append(['DomaCastleInteriorThroneRoom', [4872, 466]])
            self.warpCoord.append(['DomaCastleInteriorThroneRoomExit', [4392, 1138]])

            # Teleport Zones
            Block(self.game, 1000, 1232, 160, 16, YELLOW, 'DomaCastleExterior0')
            Block(self.game, 1048, 1440, 40, 64, YELLOW, 'DomaCastleExterior1')
            Block(self.game, 882, 1020, 62, 32, YELLOW, 'DomaCastleInterior1')  # Main Room
            Block(self.game, 4392, 1546, 32, 22, YELLOW, 'DomaCastleInterior1Exit')
            Block(self.game, 4234, 1392, 32, 40, YELLOW, 'DomaCastleInterior2')  # Bedrooms 1
            Block(self.game, 5864, 1664, 32, 32, YELLOW, 'DomaCastleInterior2Exit')
            Block(self.game, 4556, 1392, 32, 40, YELLOW, 'DomaCastleInterior3')  # Bedrooms 2
            Block(self.game, 4200, 384, 32, 40, YELLOW, 'DomaCastleInterior3Exit')
            Block(self.game, 4202, 1064, 32, 16, YELLOW, 'DomaCastleInterior4')  # Kitchen 1.1
            Block(self.game, 5352, 320, 32, 32, YELLOW, 'DomaCastleInterior4Exit')
            Block(self.game, 4586, 1064, 32, 16, YELLOW, 'DomaCastleInterior5')  # Kitchen 1.2
            Block(self.game, 5640, 320, 32, 32, YELLOW, 'DomaCastleInterior5Exit')
            Block(self.game, 4614, 1184, 32, 32, YELLOW, 'DomaCastleInterior6')  # Stairs 1
            Block(self.game, 5704, 928, 32, 32, YELLOW, 'DomaCastleInterior6Exit')
            Block(self.game, 5352, 256, 32, 32, YELLOW, 'DomaCastleInterior7')  # Storage 1
            Block(self.game, 3742, 1984, 32, 32, YELLOW, 'DomaCastleInterior7Exit')
            Block(self.game, 5416, 256, 32, 32, YELLOW, 'DomaCastleInterior8')  # Bedrooms 3
            Block(self.game, 4968, 1120, 32, 32, YELLOW, 'DomaCastleInterior8Exit')
            Block(self.game, 5608, 864, 32, 32, YELLOW, 'DomaCastleInterior9')  # Armory 1
            Block(self.game, 4968, 1696, 32, 32, YELLOW, 'DomaCastleInterior9Exit')
            Block(self.game, 4376, 1088, 64, 64, YELLOW, 'DomaCastleInteriorThroneRoom')
            Block(self.game, 4872, 512, 32, 32, YELLOW, 'DomaCastleInteriorThroneRoomExit')

            # Fixed NPCs:
            Npc(self.game, -1, -1, self.name, 'king')

            # Left Side of Castle Gate
            Block(self.game, 1016, 1440, 32, 64)
            Block(self.game, 1016, 1440, 32, 64)
            Block(self.game, 576, 1378, 288, 216)
            Block(self.game, 778, 1594, 50, 30)
            Block(self.game, 368, 1314, 208, 192)
            Block(self.game, 352, 1218, 64, 320)
            Block(self.game, 832, 1346, 184, 224)
            Block(self.game, 980, 1570, 36, 96)

            # Right Side of Castle Gate
            Block(self.game, 1048, 1440, 48, 32)
            Block(self.game, 1088, 1440, 32, 64)
            Block(self.game, 1120, 1346, 192, 224)
            Block(self.game, 1120, 1570, 32, 96)
            Block(self.game, 1312, 1378, 352, 224)
            Block(self.game, 1276, 1570, 36, 32)
            Block(self.game, 1324, 1602, 32, 16)
            Block(self.game, 1632, 1282, 128, 224)

            # DomaCastleExterior1
            Block(self.game, 882, 1000, 64, 2)
            Block(self.game, 984, 1238, 160, 32)
            Block(self.game, 968, 1190, 32, 48)
            Block(self.game, 1144, 1190, 32, 48)
            Block(self.game, 672, 1120, 356, 70)
            Block(self.game, 1118, 1120, 32, 64)
            Block(self.game, 1150, 966, 32, 160)
            Block(self.game, 1150, 966, 352, 32)
            Block(self.game, 1502, 672, 32, 320)
            Block(self.game, 1534, 576, 32, 96)
            Block(self.game, 1406, 540, 128, 32)
            Block(self.game, 1406, 540, 32, 352)  # Possible that we set floors tag in there
            Block(self.game, 1086, 872, 352, 32)
            Block(self.game, 1054, 872, 32, 180)
            Block(self.game, 734, 1020, 148, 32)
            Block(self.game, 734, 872, 32, 180)
            Block(self.game, 546, 1024, 128, 192)
            Block(self.game, 450, 720, 32, 500)
            Block(self.game, 450, 1220, 96, 32)
            Block(self.game, 258, 720, 222, 32)
            Block(self.game, 258, 572, 318, 32)
            Block(self.game, 258, 572, 32, 160)
            Block(self.game, 354, 572, 128, 96)
            Block(self.game, 544, 572, 62, 388)
            Block(self.game, 546, 896, 128, 64)
            Block(self.game, 672, 896, 64, 32)
            Block(self.game, 944, 1020, 128, 32)
            Npc(self.game, 490, 684, self.name, 'guard')
            Npc(self.game, 1472, 600, self.name, 'guard')

            # DomaCastleWalls
            Block(self.game, 736, 736, 32, 160)
            Block(self.game, 736, 704, 64, 32)
            Block(self.game, 1056, 736, 32, 160)
            Block(self.game, 1024, 704, 64, 32)
            Block(self.game, 800, 736, 224, 64)
            Block(self.game, 768, 864, 320, 32)
            Block(self.game, 960, 800, 64, 16)
            Block(self.game, 800, 800, 64, 16)
            Objects(self.game, 1024, 736, 32, 32, 'chest', mapName=self.name)
            Npc(self.game, 896, 804, self.name, 'guard')
            Npc(self.game, 912, 804, self.name, 'guard')

            # DomaCastleInterior1 MainRoom
            Block(self.game, 4327, 1546, 65, 22)
            Block(self.game, 4424, 1546, 68, 22)
            Block(self.game, 4392, 1568, 32, 11)
            Block(self.game, 4488, 1504, 31, 48)
            Block(self.game, 4520, 1504, 68, 16)
            Block(self.game, 4584, 1375, 6, 129)
            Block(self.game, 4296, 1504, 32, 52)
            Block(self.game, 4228, 1504, 68, 16)
            Block(self.game, 4222, 1375, 6, 129)
            Block(self.game, 4270, 1375, 20, 60)
            Block(self.game, 4297, 1455, 32, 1)
            Block(self.game, 4485, 1455, 32, 1)
            Block(self.game, 4524, 1375, 20, 60)
            Block(self.game, 4336, 1306, 18, 166)
            Block(self.game, 4464, 1306, 18, 166)
            Block(self.game, 4163, 1184, 165, 135)
            Block(self.game, 4488, 1184, 125, 135)
            Block(self.game, 4648, 1184, 32, 32)
            Block(self.game, 4148, 993, 16, 189)
            Block(self.game, 4680, 993, 16, 189)
            Block(self.game, 4148, 993, 36, 16)
            Block(self.game, 4166, 1064, 36, 16)
            Block(self.game, 4234, 1064, 94, 16)
            Block(self.game, 4328, 1064, 48, 88)
            Block(self.game, 4440, 1064, 48, 88)
            Block(self.game, 4488, 1064, 98, 16)
            Block(self.game, 4618, 1064, 66, 16)
            Block(self.game, 4648, 1080, 36, 8)
            Block(self.game, 4234, 1360, 32, 32)
            Block(self.game, 4555, 1360, 32, 32)
            Block(self.game, 4617, 1217, 32, 32)
            Block(self.game, 4580, 1032, 32, 32)
            Block(self.game, 4200, 1032, 32, 32)
            Block(self.game, 4375, 1064, 64, 32)
            Npc(self.game, 4874, 292, self.name, 'guard')
            Npc(self.game, 4874, 260, self.name, 'guard')

            # DoomCastleInterior2 Bedroom1
            Block(self.game, 5864, 1696, 32, 32)
            Block(self.game, 5896, 1664, 64, 32)
            Block(self.game, 5928, 1472, 32, 224)
            Block(self.game, 5480, 1472, 512, 32)
            Block(self.game, 5480, 1472, 32, 224)
            Block(self.game, 5480, 1664, 384, 32)
            Block(self.game, 5537, 1504, 46, 75)
            Block(self.game, 5665, 1504, 46, 75)
            Block(self.game, 5793, 1504, 46, 75)
            Block(self.game, 5537, 1628, 46, 65)
            Block(self.game, 5665, 1628, 46, 65)
            Block(self.game, 5793, 1628, 46, 65)
            Block(self.game, 5738, 1508, 28, 28)
            Objects(self.game, 5865, 1504, 32, 32, 'chest', mapName=self.name)
            Npc(self.game, 5665, 1536, self.name, 'guard')

            # DoomCastleInterior3 Bedroom2
            Block(self.game, 4200, 416, 32, 32)
            Block(self.game, 4232, 384, 260, 32)
            Block(self.game, 4456, 158, 32, 216)
            Block(self.game, 4132, 126, 416, 32)
            Block(self.game, 4100, 126, 32, 280)
            Block(self.game, 4100, 384, 96, 32)
            Block(self.game, 4144, 150, 80, 42)
            Block(self.game, 4168, 224, 32, 32)
            Block(self.game, 4258, 144, 44, 88)
            Block(self.game, 4386, 144, 44, 88)
            Block(self.game, 4386, 276, 44, 88)
            Block(self.game, 4258, 276, 44, 88)
            Objects(self.game, 4136, 352, 32, 32, 'chest', mapName=self.name)
            Objects(self.game, 4136, 320, 32, 32, 'chest', mapName=self.name)
            Objects(self.game, 4136, 288, 32, 32, 'chest', mapName=self.name)
            Npc(self.game, 4168, 320, self.name, 'guard')
            Npc(self.game, 4304, 232, self.name, 'guard')

            # DoomCastleInterior4/5 Kitchen
            Block(self.game, 5672, 320, 224, 32)
            Block(self.game, 5384, 320, 256, 32)
            Block(self.game, 5288, 320, 64, 32)
            Block(self.game, 5288, 256, 32, 96)
            Block(self.game, 5320, 256, 32, 32)
            Block(self.game, 5384, 256, 32, 32)
            Block(self.game, 5448, 256, 192, 32)
            Block(self.game, 5352, 352, 32, 32)
            Block(self.game, 5640, 352, 32, 32)
            Block(self.game, 5352, 240, 32, 16)
            Block(self.game, 5416, 240, 32, 16)
            Block(self.game, 5512, 32, 128, 256)
            Block(self.game, 5640, 128, 256, 32)
            Block(self.game, 5864, 32, 32, 288)
            Block(self.game, 5712, 142, 80, 50)
            Block(self.game, 5640, 160, 32, 32)
            Block(self.game, 5704, 224, 32, 32)
            Block(self.game, 5800, 232, 32, 89)
            Block(self.game, 5800, 232, 64, 46)
            Objects(self.game, 5832, 160, 32, 32, 'chest', mapName=self.name)
            Npc(self.game, 5768, 232, self.name, 'guard')

            # DomaCastleInterior6 Stairs1
            Block(self.game, 5736, 928, 160, 32)
            Block(self.game, 5704, 960, 32, 32)
            Block(self.game, 5640, 864, 64, 96)
            Block(self.game, 5608, 896, 32, 32)
            Block(self.game, 5576, 800, 32, 96)
            Block(self.game, 5576, 800, 320, 32)
            Block(self.game, 5832, 800, 32, 160)
            Npc(self.game, 5770, 860, self.name, 'guard')

            # DomaCastleInterior7 Storage1
            Block(self.game, 3742, 2016, 32, 32)
            Block(self.game, 3774, 1984, 128, 32)
            Block(self.game, 3710, 1984, 32, 32)
            Block(self.game, 3678, 1824, 32, 160)
            Block(self.game, 3678, 1824, 224, 32)
            Block(self.game, 3870, 1824, 32, 160)
            Objects(self.game, 3806, 1856, 32, 32, 'chest', mapName=self.name)
            Objects(self.game, 3838, 1856, 32, 32, 'chest', mapName=self.name)

            # DomaCastleInterior8 Bedroom3
            Block(self.game, 5000, 1120, 192, 32)
            Block(self.game, 4968, 1152, 32, 32)
            Block(self.game, 4904, 1120, 64, 32)
            Block(self.game, 4904, 896, 32, 224)
            Block(self.game, 4944, 952, 80, 40)
            Block(self.game, 5000, 766, 32, 192)
            Block(self.game, 5032, 864, 96, 32)
            Block(self.game, 5128, 864, 32, 96)
            Block(self.game, 5128, 928, 160, 32)
            Block(self.game, 5256, 960, 32, 64)
            Block(self.game, 5160, 1024, 128, 96)
            Block(self.game, 5154, 944, 76, 96)
            Objects(self.game, 5128, 1088, 32, 32, 'chest', mapName=self.name)

            # DomaCastleInterior9 Armory1
            Block(self.game, 5000, 1696, 96, 32)
            Block(self.game, 4968, 1728, 32, 32)
            Block(self.game, 4936, 1696, 32, 32)
            Block(self.game, 4904, 1536, 32, 160)
            Block(self.game, 4904, 1536, 224, 32)
            Block(self.game, 5096, 1536, 32, 192)
            Block(self.game, 4936, 1568, 32, 32)
            Block(self.game, 5032, 1568, 32, 32)
            Block(self.game, 4936, 1632, 32, 32)
            Objects(self.game, 4968, 1568, 32, 32, 'chest', mapName=self.name)
            Objects(self.game, 5064, 1600, 32, 32, 'chest', mapName=self.name)
            Objects(self.game, 5064, 1664, 32, 32, 'chest', mapName=self.name)
            Objects(self.game, 5032, 1664, 32, 32, 'chest', mapName=self.name)
            Objects(self.game, 4936, 1664, 32, 32, 'chest', mapName=self.name)
            Npc(self.game, 5000, 1632, self.name, 'guard')

            # DoomCastleInterior ThroneRoom
            Block(self.game, 4872, 544, 32, 32)
            Block(self.game, 4904, 512, 32, 32)
            Block(self.game, 4840, 512, 32, 32)
            Block(self.game, 4936, 480, 32, 32)
            Block(self.game, 4808, 480, 32, 32)
            Block(self.game, 4776, 368, 32, 116)
            Block(self.game, 4968, 368, 32, 116)
            Block(self.game, 5000, 416, 64, 64)
            Block(self.game, 5064, 192, 32, 224)
            Block(self.game, 5000, 222, 64, 98)
            Block(self.game, 5000, 94, 32, 128)
            Block(self.game, 4840, 128, 32, 32)
            Block(self.game, 4904, 128, 32, 32)
            Block(self.game, 4872, 96, 32, 32)
            Block(self.game, 4776, 128, 64, 116)
            Block(self.game, 4936, 128, 64, 116)
            Block(self.game, 4712, 224, 64, 96)
            Block(self.game, 4712, 224, 32, 144)
            Block(self.game, 5034, 224, 32, 144)
            Block(self.game, 4712, 416, 64, 32)
            Block(self.game, 4690, 354, 22, 62)
            Block(self.game, 4808, 384, 32, 32)
            Block(self.game, 4936, 384, 32, 32)
            Block(self.game, 4850, 268, 10, 10)
            Block(self.game, 4914, 268, 10, 10)

            # Left Side Ocean of Castle Gate
            Block(self.game, 0, 1984, 832, 32)
            Block(self.game, 832, 1952, 96, 32)
            Block(self.game, 928, 1854, 32, 96)
            Block(self.game, 704, 1704, 128, 32)
            Block(self.game, 608, 1768, 320, 96)
            Block(self.game, 672, 1736, 192, 32)
            Block(self.game, 448, 1640, 64, 96)
            Block(self.game, 512, 1704, 32, 32)
            Block(self.game, 544, 1736, 32, 32)
            Block(self.game, 576, 1768, 32, 32)
            Block(self.game, 320, 1608, 128, 32)
            Block(self.game, 288, 1448, 32, 160)
            Block(self.game, 320, 1416, 32, 32)

            # Right Side Ocean of Castle Gate
            Block(self.game, 1184, 1800, 32, 96)
            Block(self.game, 1216, 1768, 32, 32)
            Block(self.game, 1248, 1704, 32, 64)
            Block(self.game, 1280, 1736, 32, 32)
            Block(self.game, 1312, 1768, 64, 32)
            Block(self.game, 1376, 1736, 96, 32)
            Block(self.game, 1472, 1704, 32, 32)
            Block(self.game, 1504, 1672, 32, 32)
            Block(self.game, 1520, 1656, 16, 16)
            Block(self.game, 1536, 1704, 32, 32)
            Block(self.game, 1568, 1736, 64, 32)
            Block(self.game, 1632, 1704, 32, 32)
            Block(self.game, 1664, 1672, 64, 32)
            Block(self.game, 1728, 1576, 32, 96)
            Block(self.game, 1760, 1512, 32, 64)
            Block(self.game, 1216, 1896, 96, 32)
            Block(self.game, 1312, 1928, 128, 32)
            Block(self.game, 1440, 1960, 64, 32)
            Block(self.game, 1472, 1984, 640, 32)

            # Out of Bounds:
            Block(self.game, -32, -32, 2080, 32, RED)
            Block(self.game, -32, -32, 32, 2080, RED)
            Block(self.game, 2048, -32, 32, 2112, RED)
            Block(self.game, -32, 2048, 2080, 32, RED)

    def update(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.set_volume(0.5)
            # pygame.mixer.music.play(-1)


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, color=GREEN, zone=None, hasHitBox=True, sprite=None, tags=None,
                 isGround=False, setLayer=False):
        # Using them as walls and teleport zones for uncanny reasons
        self.game = game
        self._layer = BLOCK_LAYER
        self.hasHitBox = hasHitBox
        self.zone = zone
        self.tags = tags
        if self.zone:
            self.groups = self.game.all_sprites, self.game.teleportZone
        elif self.hasHitBox:
            self.groups = self.game.all_sprites, self.game.blocks
        elif isGround:
            self.groups = self.game.all_sprites
            self._layer = GROUND_LAYER
        else:
            self.groups = self.game.all_sprites
            self._layer = BLOCK_LAYER
        if setLayer:
            self._layer = PLAYER_LAYER + 1
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        if sprite:
            self.image = pygame.transform.scale(sprite, (32, 32))
        else:
            self.image.fill(self.color)
            self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.hitbox = self.rect.inflate(0, 0)

    def update(self):
        self.hitbox = self.rect.inflate(0, 0)


class BattleScene(pygame.sprite.Sprite):
    def __init__(self, game, party, mapName, tier, x=0, y=0):
        self.game = game
        self._layer = GUI_LAYER
        self.groups = self.game.all_sprites, self.game.battle_sprites, self.game.mousecheck, self.game.keyboardcheck
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.map = mapName
        self.tier = tier
        self.party = party
        self.font = pygame.font.Font('text/arial.ttf', 16)

        self.x = x
        self.y = y
        self.width = WIN_WIDTH
        self.height = WIN_HEIGHT

        self.wonBattle = False
        self.round = 0
        self.didSomethingThisRound = []
        self.checkAttack = False
        self.toAttack = Enemy
        self.checkAction = []
        self.checkMove = None
        self.usingInv = None
        self.invHitBox = []
        self.confirmItemUsage = False
        self.listOfHitBox = []
        self.checkSpell = []
        self.chooseSpell = []
        self.waitingForTarget = False
        self.returnBox = []
        self.trackAction = None
        self.waitForPlayer = False
        self.waitingForEnemy = 0
        self.lootBag = []
        self.lootBagPrint = []
        self.lootScreenTimer = 0
        self.updateOst = True

        # Enemies
        self.enemies = []
        tempEnemies = zoneSpawn(self.map, self.tier)
        for enemy in tempEnemies[0]:
            self.enemies.append(Enemy(self.game, enemy))
        # Base Background
        self.image = pygame.Surface((640, 640))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.originalImage = pygame.transform.scale(
            self.game.backgrounds_spritesheet.get_sprite(tempEnemies[1][0], tempEnemies[1][1], 240, 160), (640, 426))
        self.image.blit(self.originalImage, (0, (640 - 537) / 2))

        self.enemyPositions = [
            (64, 200),
            (64, 260),
            (64, 320),
            (64, 380),
            (128, 200),
            (128, 260),
            (128, 320),
            (128, 380),
            (192, 200),
            (192, 260),
            (192, 320),
            (192, 380),
            (256, 200),
            (256, 260),
            (256, 320),
            (256, 380),
        ]
        self.playerPositions = [
            (368, 200),
            (368, 260),
            (368, 320),
            (368, 380),
            (432, 200),
            (432, 260),
            (432, 320),
            (432, 380),
            (494, 200),
            (494, 260),
            (494, 320),
            (494, 380),
            (568, 200),
            (568, 260),
            (568, 320),
            (568, 380),
        ]
        self.partyMap = [
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
        ]
        self.enemyMap = [
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
        ]

        # Battle Theme
        pygame.mixer.music.pause()
        pygame.mixer.music.load("ost/105_Battle_Theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # blit enemies and player sprites
        for player in self.party:
            position = random.randint(0, 15)
            while self.partyMap[position] != 0:
                position = random.randint(0, 15)
            self.partyMap[position] = 1
            image = player.imagebattle
            tempX = self.playerPositions[position][0] - 0
            tempY = self.playerPositions[position][1] - player.rect.height / 2
            self.image.blit(image, (tempX, tempY))
            image = image.get_rect()
            image.x = tempX
            image.y = tempY
            player.data.dot = []
            self.listOfHitBox.append([image, player, position])
        for enemy in self.enemies:
            position = random.randint(0, 15)
            while self.enemyMap[position] != 0:
                position = random.randint(0, 15)
            self.enemyMap[position] = 1
            image = enemy.image
            tempX = self.enemyPositions[position][0] - 0
            tempY = self.enemyPositions[position][1] - enemy.rect.height / 2
            self.image.blit(image, (tempX, tempY))
            image = image.get_rect()
            image.x = tempX
            image.y = tempY
            self.listOfHitBox.append([image, enemy, position])
            for item in enemy.data.drop:
                if random.random() < item[1]:
                    self.lootBag.append(item[0])

        # list of general buttons of this shit
        self.battleBoxes = []  # [type, x, y, rect.x, rect.y]

    def info(self):
        # Keep track of variables
        return [
            self.x,
            self.y,
            self.width,
            self.height,
            self.round,
            self.didSomethingThisRound,
            self.checkAttack,
            self.toAttack,
            self.checkAction,
            self.checkMove,
            self.usingInv,
            self.invHitBox,
            self.confirmItemUsage,
            self.listOfHitBox,
            self.checkSpell,
            self.chooseSpell,
            self.waitingForTarget,
            self.returnBox,
            self.battleBoxes,
        ]

    def update(self):
        # Check how many actions left and update round
        if len(self.didSomethingThisRound) == 0 and self.waitingForEnemy == 0:
            # Reset actions variables for each creature
            for m, creature in enumerate(self.listOfHitBox):
                creature.append(False)  # Has Moved variable, pos 3
                creature.append(False)  # Has Used Skill/Used Item, pos 4
                creature.append(False)  # Has Used Bigger Skill, pos 5
                # Apply effects to player
                doNothingThisRound = False
                if type(creature[1]) is Player:
                    if creature[1].data.dot:
                        for tag in creature[1].data.dot:
                            if tag[0] == 'stun1':
                                doNothingThisRound = True
                                self.waitingForEnemy = 60
                                AlertText(self.game, 'STUN', creature[0].x,
                                          creature[0].y - 64, YELLOW, 'damage')
                        dotDamage = creature[1].data.dotTick()
                        AlertText(self.game, str(dotDamage), creature[0].x,
                                  creature[0].y, PURPLE, 'damage')
                        creature[1].data.hp -= dotDamage
                # If creature have spd higher than one, put it again in the didsomething var
                if not doNothingThisRound:
                    for i in range(creature[1].data.spd):
                        self.didSomethingThisRound.append(creature)
            self.round += 1
            AlertText(self.game, 'round: ' + str(self.round), 300, 54, FF4WHITE, 'description')
        # Enemies actions
        else:
            # Remove player from didsomethingthisround and queue monsters actions:
            self.waitForPlayer = False
            for i in range(len(self.didSomethingThisRound) - 1, -1, -1):
                if type(self.didSomethingThisRound[i][1]) == Player:
                    if self.didSomethingThisRound[i][3] and self.didSomethingThisRound[i][4] and \
                            self.didSomethingThisRound[i][5]:
                        del self.didSomethingThisRound[i]
                        AlertText(self.game, 'Enemy Turn', 300, 54, FF4WHITE, 'description')
                        self.waitingForEnemy = 60
                    else:
                        self.waitForPlayer = True

            if self.waitingForEnemy > 0:
                self.waitingForEnemy -= 1
            if not self.waitForPlayer:
                # Actual enemies actions
                for i in range(len(self.didSomethingThisRound) - 1, -1, -1):
                    if type(self.didSomethingThisRound[i][1]) == Enemy and self.didSomethingThisRound[i][
                        1].data.hp <= 0:
                        del self.didSomethingThisRound[i]
                    elif type(self.didSomethingThisRound[i][1]) == Enemy and self.waitingForEnemy == 0:
                        doNothingThisRound = False
                        if self.didSomethingThisRound[i][1].data.dot:
                            dotDamage = self.didSomethingThisRound[i][1].data.dotTick()
                            AlertText(self.game, str(dotDamage), self.didSomethingThisRound[i][0].x,
                                      self.didSomethingThisRound[i][0].y, PURPLE, 'damage')
                            self.didSomethingThisRound[i][1].data.hp -= dotDamage
                            for tag in self.didSomethingThisRound[i][1].data.dot:
                                if tag[0] == 'stun1':
                                    print(self.didSomethingThisRound[i][1].data.dot)
                                    doNothingThisRound = True
                                    AlertText(self.game, 'STUN', self.didSomethingThisRound[i][0].x,
                                              self.didSomethingThisRound[i][0].y - 64, YELLOW, 'damage')
                            if self.didSomethingThisRound[i][1].data.hp <= 0:
                                for j, creature in enumerate(self.listOfHitBox):
                                    if creature[1] == self.didSomethingThisRound[i][1]:
                                        del self.listOfHitBox[j]
                                        j -= 1
                                del self.didSomethingThisRound[i]
                                continue
                            if doNothingThisRound:
                                continue
                        if self.waitingForEnemy == 0:
                            self.waitingForEnemy = 60

                        enemySkill = []
                        totalOdd = []
                        for skill in self.didSomethingThisRound[i][1].data.skl:
                            for tag in skill.tags:
                                if tag[0] == 'value':
                                    enemySkill.append(skill)
                                    totalOdd.append(tag[1])

                        skill = random.choices(enemySkill, weights=totalOdd, k=1)[0]
                        AlertText(self.game, skill.name, self.didSomethingThisRound[i][0].x,
                                  self.didSomethingThisRound[i][0].y, FF4WHITE, 'description')
                        positions = [
                            [0, 1, 2, 3],  # Range 1
                            [4, 5, 6, 7],  # Range 2
                            [8, 9, 10, 11],  # Range 3
                            [12, 13, 14, 15],  # Range 4
                        ]
                        positionsnxn = [
                            [12, 13, 14, 15],
                            [8, 9, 10, 11],
                            [4, 5, 6, 7],
                            [0, 1, 2, 3],
                        ]
                        if skill.ran == 1:
                            rang = [0, 1, 2, 3]
                        elif skill.ran == 2:
                            rang = [0, 1, 2, 3, 4, 5, 6, 7]
                        elif skill.ran == 3:
                            rang = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                        elif skill.ran == 4:
                            rang = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
                        else:
                            rang = []

                        # Applying the skill to player in are of attack
                        if skill.are[0] == 'single':
                            for k, creature in enumerate(self.listOfHitBox):
                                if creature[2] in rang and type(creature[1]) is not Enemy:

                                    skill.runSound()

                                    damage = skill.dam - creature[1].data.totalArmour
                                    if damage < 0:
                                        damage = 0
                                    creature[1].data.hp = creature[1].data.hp - damage
                                    for tag in skill.tags:
                                        if tag[0] in ListOfDot:
                                            temptag = tag.copy()
                                            temptag.append(skill.dam)
                                            creature[1].data.dot.append(temptag)
                                        if tag[0] == 'push1':
                                            if creature[2] < 12:
                                                for j, creature2 in enumerate(self.listOfHitBox):
                                                    if creature2[1] == creature[1]:
                                                        self.partyMap[creature[2]] = 0
                                                        creature[2] += 4
                                                        self.partyMap[creature[2]] = 1
                                                        self.listOfHitBox[j][2] = creature[2]
                                        if tag[0] == 'pull1':
                                            if creature[2] > 3:
                                                for j, creature2 in enumerate(self.listOfHitBox):
                                                    if creature2[1] == creature[1]:
                                                        self.partyMap[creature[2]] = 0
                                                        creature[2] -= 4
                                                        self.partyMap[creature[2]] = 1
                                                        self.listOfHitBox[j][2] = creature[2]
                                    AlertText(self.game, damage, creature[0].x, creature[0].y, RED,
                                              'damage')
                                    if creature[1].data.hp <= 0:
                                        print('you died')
                        if skill.are[0] == 'area':
                            possibleTargets = []
                            for k, creature in enumerate(self.listOfHitBox):
                                if creature[2] in rang and type(creature[1]) is not Enemy:
                                    possibleTargets.append(creature)
                            if possibleTargets:

                                skill.runSound()

                                target = random.choice(possibleTargets)
                                if skill.are[1] == 3:
                                    indexofI = []
                                    positionAre = []
                                    for l, line in enumerate(positionsnxn):
                                        if target[2] in line:
                                            indexofI = [l, line.index(target[2])]
                                    positionAre.append(target[2])
                                    if indexofI[1] != 0:
                                        positionAre.append(target[2] - 1)
                                        if indexofI[0] != 0:
                                            positionAre.append(target[2] + 3)
                                        if indexofI[0] != 3:
                                            positionAre.append(target[2] - 5)
                                    if indexofI[1] != 3:
                                        positionAre.append(target[2] + 1)
                                        if indexofI[0] != 0:
                                            positionAre.append(target[2] + 5)
                                        if indexofI[0] != 3:
                                            positionAre.append(target[2] - 3)
                                    if indexofI[0] != 0:
                                        positionAre.append(target[2] + 4)
                                        if indexofI[1] != 0:
                                            positionAre.append(target[2] + 3)
                                        if indexofI[1] != 3:
                                            positionAre.append(target[2] + 5)
                                    if indexofI[0] != 3:
                                        positionAre.append(target[2] - 4)
                                        if indexofI[1] != 0:
                                            positionAre.append(target[2] - 5)
                                        if indexofI[1] != 3:
                                            positionAre.append(target[2] - 3)
                                    positionAre = list(dict.fromkeys(positionAre))
                                    positionAre.sort()

                                    for l, creature2 in enumerate(self.listOfHitBox):
                                        if creature2[2] in positionAre and type(creature2[1]) is not Enemy:
                                            damage = skill.dam - creature2[1].data.totalArmour
                                            if damage < 0:
                                                damage = 0
                                            creature2[1].data.hp = creature2[1].data.hp - damage
                                            AlertText(self.game, damage, creature2[0].x, creature2[0].y, RED,
                                                      'damage')
                                            for tag in skill.tags:
                                                if tag[0] in ListOfDot:
                                                    temptag = tag.copy()
                                                    temptag.append(skill.dam)
                                                    creature2[1].data.dot.append(temptag)
                                            if creature2[1].data.hp <= 0:
                                                print('you died')

                                if skill.are[1] == 5:
                                    for l, creature2 in enumerate(self.listOfHitBox):
                                        if creature2[2] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                                            15] and type(creature2[1]) is not Enemy:
                                            damage = skill.dam - creature2[1].data.totalArmour
                                            if damage < 0:
                                                damage = 0
                                            creature2[1].data.hp = creature2[1].data.hp - damage
                                            AlertText(self.game, damage, creature2[0].x, creature2[0].y, RED,
                                                      'damage')
                                            for tag in skill.tags:
                                                if tag[0] in ListOfDot:
                                                    temptag = tag.copy()
                                                    temptag.append(skill.dam)
                                                    creature2[1].data.dot.append(temptag)
                                            if creature2[1].data.hp <= 0:
                                                print('you died')

                        del self.didSomethingThisRound[i]

        # Base Background
        self.image = pygame.Surface((640, 640))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.image.blit(self.originalImage, (0, (640 - 537) / 2))
        # Print Creatures again:
        for i, creature in enumerate(self.listOfHitBox):
            if type(creature[1]) is Player:
                image = creature[1].imagebattle
                tempX = self.playerPositions[creature[2]][0] - 0
                tempY = self.playerPositions[creature[2]][1] - creature[1].rect.height / 2
                self.image.blit(image, (tempX, tempY))
                image = image.get_rect()
                image.x = tempX
                image.y = tempY
                self.listOfHitBox[i] = ([image, creature[1], creature[2]])
            elif type(creature[1] is Enemy):
                image = creature[1].image
                tempX = self.enemyPositions[creature[2]][0] - (creature[1].rect.w / 2 - 16)
                tempY = self.enemyPositions[creature[2]][1] - creature[1].rect.height / 2
                self.image.blit(image, (tempX, tempY))
                image = image.get_rect()
                image.x = tempX
                image.y = tempY
                self.listOfHitBox[i] = ([image, creature[1], creature[2]])
                pass
        # Base Box
        CreateGuiBox(self.image, 0, 435, 640, 105)
        # Base Enemy Box
        CreateGuiBox(self.image, 0, 435, 196, 105)
        tempEnemyCount, tempEnemyCountVar = [], 0
        for enemy in self.listOfHitBox:
            if type(enemy[1]) is Enemy:
                if enemy[1].data.name not in tempEnemyCount:
                    j = 0
                    for enemy2 in self.listOfHitBox:
                        if type(enemy2[1]) is Enemy:
                            if enemy2[1].data.name == enemy[1].data.name:
                                j += 1
                    self.image.blit(self.font.render(str(j) + 'x ' + enemy[1].data.name, True, FF4WHITE),
                                    (10, 445 + 16 * tempEnemyCountVar))
                    tempEnemyCountVar += 1
                    tempEnemyCount.append(enemy[1].data.name)
        # Base Player Status Box
        CreateGuiBox(self.image, 300, 435, 340, 105)
        for i, player in enumerate(self.party):
            self.image.blit(self.font.render(player.data.name, True, FF4WHITE), (315, 445 + 16 * i))
            self.image.blit(
                self.font.render('Hp: ' + str(player.data.hp) + '/' + str(player.data.maxhpmp[0]), True, FF4WHITE),
                (390, 445 + 16 * i))
            self.image.blit(
                self.font.render('Mp: ' + str(player.data.mp) + '/' + str(player.data.maxhpmp[1]), True, FF4WHITE),
                (510, 445 + 16 * i))
        # Reminder of game Mechanic:
        self.image.blit(self.font.render('Use Mouse', True, FF4WHITE), (208, 475))
        # Base Action Box
        if self.checkAction:
            CreateGuiBox(self.image, self.checkAction[0] - 48, self.checkAction[1] - 128, 96, 105)
            self.image.blit(self.font.render('SKILL', True, FF4WHITE),
                            (self.checkAction[0] + 26 - 48, self.checkAction[1] + 11 - 128))
            self.battleBoxes.append([
                'skill', self.checkAction[2], pygame.Rect(self.checkAction[0] + 26 - 48 - 1,
                                                          self.checkAction[1] + 11 - 128 - 1, 43, 16)])
            self.image.blit(self.font.render('ITEM', True, FF4WHITE),
                            (self.checkAction[0] + 29 - 48, self.checkAction[1] + 33 - 128))
            self.battleBoxes.append([
                'item', self.checkAction[2], pygame.Rect(self.checkAction[0] + 29 - 48 - 1,
                                                         self.checkAction[1] + 33 - 128 - 1, 43, 16)])
            self.image.blit(self.font.render('MOVE', True, FF4WHITE),
                            (self.checkAction[0] + 24 - 48, self.checkAction[1] + 55 - 128))
            self.battleBoxes.append([
                'move', self.checkAction[2], pygame.Rect(self.checkAction[0] + 24 - 48 - 1,
                                                         self.checkAction[1] + 55 - 128 - 1, 43, 16)])
            self.image.blit(self.font.render('WAIT', True, FF4WHITE),
                            (self.checkAction[0] + 28 - 48, self.checkAction[1] + 76 - 128))
            self.battleBoxes.append([
                'wait', self.checkAction[2], pygame.Rect(self.checkAction[0] + 28 - 48 - 1,
                                                         self.checkAction[1] + 76 - 128 - 1, 43, 16)])
        # Check and blit winBattle Screen
        self.wonBattle = True
        for creature in self.listOfHitBox:
            if type(creature[1]) is Enemy:
                self.wonBattle = False
        if self.wonBattle:
            if self.updateOst:
                pygame.mixer.music.load("ost/106 Fanfare.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                self.updateOst = False
            self.lootScreenTimer += 1
            for item in self.lootBag:
                self.listOfHitBox[0][1].data.inv.append(Item(item))
                self.lootBagPrint.append(Item(item))
            self.lootBag = []
            CreateGuiBox(self.image, 160, 160, 320, 320)
            tempItemCount, tempItemCountVar = [], 0
            self.image.blit(self.font.render('Loot Bag', True, FF4WHITE), (288, 176))
            incrementToX = 0
            for item in self.lootBagPrint:
                if item.name not in tempItemCount:
                    j = 0
                    if tempItemCountVar % 16 == 0 and tempItemCountVar != 0:
                        incrementToX += 72
                    for item2 in self.lootBagPrint:
                        if item2.name == item.name:
                            j += 1
                    self.image.blit(self.font.render(str(j) + 'x ' + item.name, True, FF4WHITE),
                                    (176 + incrementToX, 200 + 16 * tempItemCountVar))
                    tempItemCountVar += 1
                    tempItemCount.append(item.name)
            pygame.image.save(self.image, 'image.png')
            if self.lootScreenTimer >= 120:
                pygame.mixer.music.stop()
                self.game.gameState = 1
                for sprite in self.game.battle_sprites:
                    sprite.kill()
        # Highlight Squares:
        if self.checkMove:
            for i, position in enumerate(self.partyMap):
                if position == 0:
                    pygame.draw.rect(self.image, BLUE,
                                     (self.playerPositions[i][0], self.playerPositions[i][1] - 16, 32, 1))
                    pygame.draw.rect(self.image, BLUE,
                                     (self.playerPositions[i][0] + 32, self.playerPositions[i][1] - 16, 1, 32))
                    pygame.draw.rect(self.image, BLUE,
                                     (self.playerPositions[i][0], self.playerPositions[i][1] - 16 + 32, 32, 1))
                    pygame.draw.rect(self.image, BLUE,
                                     (self.playerPositions[i][0], self.playerPositions[i][1] - 16, 1, 32))
                else:
                    pygame.draw.rect(self.image, RED,
                                     (self.playerPositions[i][0], self.playerPositions[i][1] - 16, 32, 1))
                    pygame.draw.rect(self.image, RED,
                                     (self.playerPositions[i][0] + 32, self.playerPositions[i][1] - 16, 1, 32))
                    pygame.draw.rect(self.image, RED,
                                     (self.playerPositions[i][0], self.playerPositions[i][1] - 16 + 32, 32, 1))
                    pygame.draw.rect(self.image, RED,
                                     (self.playerPositions[i][0], self.playerPositions[i][1] - 16, 1, 32))
                    self.returnBox = tuple((self.playerPositions[i][0], self.playerPositions[i][1] - 16, 32, 32))
        # Open inventory to use:
        if self.usingInv:
            CreateGuiBox(self.image, 192, 136, 256, 256)
            tempItemCount, tempItemCountVar = [], 0
            self.image.blit(self.font.render('INVENTORY', True, FF4WHITE), (276, 151))
            for item in self.usingInv.data.inv:
                if item.name not in tempItemCount and isConsumable(item.name):
                    j = 0
                    for item2 in self.usingInv.data.inv:
                        if item2.name == item.name:
                            j += 1
                    self.image.blit(self.font.render(str(j) + 'x ' + item.name, True, FF4WHITE),
                                    (207, 167 + 16 * tempItemCountVar))
                    self.invHitBox.append([pygame.Rect(229, 167 + 16 * tempItemCountVar, 64, 16), item.name])
                    tempItemCountVar += 1
                    tempItemCount.append(item.name)
            if self.confirmItemUsage:
                self.usingInv.useItem(self.confirmItemUsage, self.trackAction)
                self.invHitBox = []
                self.battleBoxes = []
                self.returnBox = []
                self.confirmItemUsage = None
                self.usingInv = None
            else:
                self.image.blit(self.font.render('Return', True, FF4WHITE),
                                (296, 359))
                self.returnBox = tuple((296, 359))
        # Open skills available to player
        if self.checkSpell:
            CreateGuiBox(self.image, self.checkSpell[2][0].x - 53, self.checkSpell[2][0].y - 144, 128, 192)
            self.image.blit(self.font.render('SKILLS', True, FF4WHITE),
                            (self.checkSpell[2][0].x - 17, self.checkSpell[2][0].y - 134))
            for i, skill in enumerate(self.checkSpell[2][1].data.skl):
                self.image.blit(self.font.render(skill.name, True, FF4WHITE),
                                (self.checkSpell[2][0].x - 38, self.checkSpell[2][0].y - 108 + 16 * i))
                if (skill, self.checkSpell[2][0].x - 38, self.checkSpell[2][0].y - 105 + 16 * i, 44, 13,
                    self.checkSpell[2][1]) not in self.chooseSpell:
                    self.chooseSpell.append((
                        skill, self.checkSpell[2][0].x - 38, self.checkSpell[2][0].y - 105 + 16 * i,
                        44, 13, self.checkSpell[2][1]))
                self.image.blit(self.font.render('Return', True, FF4WHITE),
                                (self.checkSpell[2][0].x - 12, self.checkSpell[2][0].y - 134 + 154))
                self.returnBox = tuple((self.checkSpell[2][0].x - 12, self.checkSpell[2][0].y - 134 + 154))
        # Highlight enemy boxes for skill hitbox
        if self.waitingForTarget:
            positions = [
                [12, 13, 14, 15],  # Range 1
                [8, 9, 10, 11],  # Range 2
                [4, 5, 6, 7],  # Range 3
                [0, 1, 2, 3],  # Range 4
            ]
            for i, box in enumerate(self.enemyPositions):
                if i >= positions[self.waitingForTarget[1][0].ran - 1][0]:
                    pygame.draw.rect(self.image, BLUE,
                                     (box[0], box[1] - 16, 32, 1))
                    pygame.draw.rect(self.image, BLUE,
                                     (box[0] + 32, box[1] - 16, 1, 32))
                    pygame.draw.rect(self.image, BLUE,
                                     (box[0], box[1] - 16 + 32, 32, 1))
                    pygame.draw.rect(self.image, BLUE,
                                     (box[0], box[1] - 16, 1, 32))
                else:
                    pygame.draw.rect(self.image, RED,
                                     (box[0], box[1] - 16, 32, 1))
                    pygame.draw.rect(self.image, RED,
                                     (box[0] + 32, box[1] - 16, 1, 32))
                    pygame.draw.rect(self.image, RED,
                                     (box[0], box[1] - 16 + 32, 32, 1))
                    pygame.draw.rect(self.image, RED,
                                     (box[0], box[1] - 16, 1, 32))
                temp = self.trackAction[2][2]
                pygame.draw.rect(self.image, RED,
                                 (self.playerPositions[temp][0], self.playerPositions[temp][1] - 16, 32, 1))
                pygame.draw.rect(self.image, RED,
                                 (self.playerPositions[temp][0] + 32, self.playerPositions[temp][1] - 16, 1, 32))
                pygame.draw.rect(self.image, RED,
                                 (self.playerPositions[temp][0], self.playerPositions[temp][1] - 16 + 32, 32, 1))
                pygame.draw.rect(self.image, RED,
                                 (self.playerPositions[temp][0], self.playerPositions[temp][1] - 16, 1, 32))
                self.returnBox = tuple((self.playerPositions[temp][0], self.playerPositions[temp][1] - 16, 32, 32))

        pygame.image.save(self.image, 'image.png')

    def check_click(self, mouse):
        if self.waitForPlayer and not self.wonBattle:
            # Check if clicking creature
            if not self.checkMove and not self.battleBoxes and not self.invHitBox:
                for creature in self.listOfHitBox:
                    if creature[0].collidepoint(mouse):
                        if type(creature[1]) is Player and not self.checkMove and not self.usingInv:
                            print('click')
                            self.trackAction = [creature[0][0] + 16, creature[0][1] + 16, creature]
                            self.checkAction = [creature[0][0] + 16, creature[0][1] + 16, creature]
            # Check if clicked a square to move
            if self.checkMove is not None:
                for i, positionOnMap in enumerate(self.partyMap):
                    image = pygame.Surface((32, 32)).get_rect()
                    image.x = self.playerPositions[i][0]
                    image.y = self.playerPositions[i][1] - 16
                    if image.collidepoint(mouse):
                        if positionOnMap == 0:
                            self.partyMap[i] = 1
                            for j, creature in enumerate(self.listOfHitBox):
                                if creature[1] == self.checkMove:
                                    self.partyMap[self.listOfHitBox[j][2]] = 0
                                    self.listOfHitBox[j][2] = i
                                    for k in range(len(self.didSomethingThisRound) - 1, -1, -1):
                                        if self.didSomethingThisRound[k][1] == self.listOfHitBox[j][1]:
                                            self.didSomethingThisRound[k][3] = True
                                            break
                            self.checkMove = None
            # Check which action bar GOT CLICKED
            for box in self.battleBoxes:
                if box[2].collidepoint(mouse):
                    if box[0] == 'move':
                        if self.didSomethingThisRound[0][3]:
                            AlertText(self.game, 'cant do that', self.checkAction[0] - 16, self.checkAction[1], FF4BLUE,
                                      'info')
                        else:
                            print('move')
                            self.checkMove = self.checkAction[2][1]
                        self.checkAction = []
                        self.battleBoxes = []
                        break
                    elif box[0] == 'wait':
                        print('wait')
                        self.didSomethingThisRound[0][3] = True
                        self.didSomethingThisRound[0][4] = True
                        self.didSomethingThisRound[0][5] = True
                        self.checkAction = []
                        self.battleBoxes = []
                        break
                    elif box[0] == 'item':
                        if self.didSomethingThisRound[0][4]:
                            AlertText(self.game, 'cant do that', self.checkAction[0] - 16, self.checkAction[1], FF4BLUE,
                                      'info')
                        else:
                            print('item')
                            self.usingInv = self.checkAction[2][1]
                        self.checkAction = []
                        break
                    elif box[0] == 'skill':
                        if self.didSomethingThisRound[0][4] and self.didSomethingThisRound[0][5]:
                            print('something')
                            AlertText(self.game, 'cant do that', self.checkAction[0] - 16, self.checkAction[1], FF4BLUE,
                                      'info')
                        else:
                            print('skill')
                            self.checkSpell = self.checkAction
                        self.checkAction = []
                        break
                for creature in self.listOfHitBox:
                    if creature[0].collidepoint(mouse):
                        if type(creature[1]) is Player:
                            self.checkAction = []
                            self.battleBoxes = []
            # Check if clicked some item from inventory
            if self.invHitBox:
                for box in self.invHitBox:
                    if box[0].collidepoint(mouse):
                        self.confirmItemUsage = box[1]
                        for k in range(len(self.didSomethingThisRound) - 1, -1, -1):
                            if self.didSomethingThisRound[k][1] == self.trackAction[2][1]:
                                self.didSomethingThisRound[k][4] = True
                                break
                self.invHitBox = []
            # Check if clicked where to activate the skill
            if self.chooseSpell:
                for textbox in self.chooseSpell:
                    if (pygame.Rect(textbox[1], textbox[2], textbox[3], textbox[4]).collidepoint(
                            mouse) and not self.waitingForTarget) or self.waitingForTarget:
                        if not self.waitingForTarget:
                            self.waitingForTarget = [True, textbox]
                        self.checkSpell = []
                        for i, box in enumerate(self.enemyPositions):
                            if pygame.Rect(box[0], box[1] - 16, 32, 32).collidepoint(mouse):
                                requirements = True
                                for tag in self.waitingForTarget[1][0].tags:
                                    if 'mpcost' == tag[0]:
                                        if textbox[5].data.mp - tag[1] < 0:
                                            AlertText(self.game, 'No Mp', box[0], box[1], YELLOW, 'info')
                                            requirements = False
                                        else:
                                            textbox[5].data.mp -= tag[1]
                                if requirements:
                                    positions = [
                                        [12, 13, 14, 15],  # Range 1
                                        [8, 9, 10, 11],  # Range 2
                                        [4, 5, 6, 7],  # Range 3
                                        [0, 1, 2, 3],  # Range 4
                                    ]
                                    if i in positions[self.waitingForTarget[1][0].ran - 1] or i > \
                                            positions[self.waitingForTarget[1][0].ran - 1][3]:

                                        self.waitingForTarget[1][0].runSound()

                                        # Applying the skill to enemies in are of attack
                                        if self.waitingForTarget[1][0].are[0] == 'single':
                                            for j, creature in enumerate(self.listOfHitBox):
                                                if creature[2] == i and type(creature[1]) is not Player:
                                                    damage = self.waitingForTarget[1][0].dam - creature[1].data.damRed
                                                    if damage < 0:
                                                        damage = 0
                                                    creature[1].data.hp = creature[1].data.hp - damage
                                                    AlertText(self.game, damage, box[0], box[1], RED, 'damage')
                                                    for tag in self.waitingForTarget[1][0].tags:
                                                        if tag[0] in ListOfDot:
                                                            temptag = tag.copy()
                                                            temptag.append(self.waitingForTarget[1][0].dam)
                                                            creature[1].data.dot.append(temptag)
                                                    if creature[1].data.hp <= 0:
                                                        del self.listOfHitBox[j]
                                        if self.waitingForTarget[1][0].are[0] == 'area':
                                            arenxn = self.waitingForTarget[1][0].are[1]
                                            positionAre = []
                                            if arenxn == 3:
                                                indexofI = []
                                                for j, line in enumerate(positions):
                                                    if i in line:
                                                        indexofI = [j, line.index(i)]
                                                positionAre.append(i)
                                                if indexofI[1] != 0:
                                                    positionAre.append(i - 1)
                                                    if indexofI[0] != 0:
                                                        positionAre.append(i + 3)
                                                    if indexofI[0] != 3:
                                                        positionAre.append(i - 5)
                                                if indexofI[1] != 3:
                                                    positionAre.append(i + 1)
                                                    if indexofI[0] != 0:
                                                        positionAre.append(i + 5)
                                                    if indexofI[0] != 3:
                                                        positionAre.append(i - 3)
                                                if indexofI[0] != 0:
                                                    positionAre.append(i + 4)
                                                    if indexofI[1] != 0:
                                                        positionAre.append(i + 3)
                                                    if indexofI[1] != 3:
                                                        positionAre.append(i + 5)
                                                if indexofI[0] != 3:
                                                    positionAre.append(i - 4)
                                                    if indexofI[1] != 0:
                                                        positionAre.append(i - 5)
                                                    if indexofI[1] != 3:
                                                        positionAre.append(i - 3)
                                                positionAre = list(dict.fromkeys(positionAre))
                                                positionAre.sort()

                                                for pos in positionAre:
                                                    for k, creature in enumerate(self.listOfHitBox):
                                                        if creature[2] == pos and type(creature[1]) is not Player:
                                                            damage = self.waitingForTarget[1][0].dam - creature[
                                                                1].data.damRed
                                                            if damage < 0:
                                                                damage = 0
                                                            creature[1].data.hp = creature[1].data.hp - damage
                                                            AlertText(self.game, damage, self.enemyPositions[pos][0],
                                                                      self.enemyPositions[pos][1], RED, 'damage')
                                                            for tag in self.waitingForTarget[1][0].tags:
                                                                if tag[0] in ListOfDot:
                                                                    temptag = tag.copy()
                                                                    temptag.append(self.waitingForTarget[1][0].dam)
                                                                    creature[1].data.dot.append(temptag)
                                                            if creature[1].data.hp <= 0:
                                                                del self.listOfHitBox[k]
                                            if arenxn == 5:
                                                for pos in range(16):
                                                    for k, creature in enumerate(self.listOfHitBox):
                                                        if creature[2] == pos and type(creature[1]) is not Player:
                                                            damage = self.waitingForTarget[1][0].dam - creature[
                                                                1].data.damRed
                                                            if damage < 0:
                                                                damage = 0
                                                            creature[1].data.hp = creature[1].data.hp - damage
                                                            AlertText(self.game, damage, self.enemyPositions[pos][0],
                                                                      self.enemyPositions[pos][1], RED, 'damage')
                                                            for tag in self.waitingForTarget[1][0].tags:
                                                                if tag[0] in ListOfDot:
                                                                    temptag = tag.copy()
                                                                    temptag.append(self.waitingForTarget[1][0].dam)
                                                                    creature[1].data.dot.append(temptag)
                                                            if creature[1].data.hp <= 0:
                                                                del self.listOfHitBox[k]
                                    for j in range(len(self.didSomethingThisRound) - 1, -1, -1):
                                        if self.didSomethingThisRound[j][1] == self.trackAction[2][1]:
                                            isHeavySkill = False
                                            for tag in self.waitingForTarget[1][0].tags:
                                                if tag[0] == 'heavy':
                                                    isHeavySkill = True
                                                    break
                                            if isHeavySkill:
                                                self.didSomethingThisRound[j][5] = True
                                                self.didSomethingThisRound[j][4] = True
                                            else:
                                                if self.didSomethingThisRound[j][4]:
                                                    self.didSomethingThisRound[j][5] = True
                                                else:
                                                    self.didSomethingThisRound[j][4] = True
                                            break

                                self.checkAttack = False
                                self.toAttack = Enemy
                                self.checkAction = []
                                self.checkMove = None
                                self.usingInv = None
                                self.confirmItemUsage = False
                                self.chooseSpell = []
                                self.waitingForTarget = False
                                self.returnBox = []
                                self.battleBoxes = []
                                self.trackAction = None
            # Reset actionBox and derivations
            if self.returnBox:
                if len(self.returnBox) > 2:
                    if pygame.Rect(self.returnBox[0], self.returnBox[1], 32, 32).collidepoint(mouse):
                        print('cleanse1')
                        self.checkAttack = False
                        self.toAttack = Enemy
                        self.checkAction = []
                        self.checkMove = None
                        self.usingInv = None
                        self.confirmItemUsage = False
                        self.checkSpell = []
                        self.chooseSpell = []
                        self.returnBox = []
                        self.battleBoxes = []
                        self.trackAction = None
                        self.waitingForTarget = False
                else:
                    if pygame.Rect(self.returnBox[0], self.returnBox[1], 46, 12).collidepoint(mouse):
                        print('cleanse2')
                        self.checkAttack = False
                        self.toAttack = Enemy
                        self.checkAction = []
                        self.checkMove = None
                        self.usingInv = None
                        self.confirmItemUsage = False
                        self.checkSpell = []
                        self.chooseSpell = []
                        self.returnBox = []
                        self.battleBoxes = []
                        self.trackAction = None
                        self.waitingForTarget = False

    def check_key(self, key):
        if key == pygame.K_SPACE and not self.wonBattle:
            print('spacebar')
            pygame.mixer.music.stop()
            self.game.gameState = 1
            for sprite in self.game.battle_sprites:
                sprite.kill()


class AlertText(pygame.sprite.Sprite):
    def __init__(self, game, text, x, y, color, t):
        self.game = game

        self._layer = GUI_LAYER
        self.groups = self.game.all_sprites, self.game.battle_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.font = pygame.font.Font('text/arial.ttf', 16)
        self.color = color
        self.originalText = text
        self.originalColor = color

        if t == 'description':
            self.text = self.font.render(str(text), True, self.color)
            self.text_rect = self.text.get_rect(center=(96 // 2, 32 // 2))
            y += 32
        elif type(text) != list:
            self.text = self.font.render(str(text), True, self.color)
            self.text_rect = self.text.get_rect(center=(96 // 2, 32 // 2))
        else:
            self.text = self.font.render(str(self.originalText[0][1]), True, self.originalColor[0])
            self.text_rect = self.text.get_rect(center=(96 // 2, 32 // 2))
            pygame.mixer.Sound.play(pygame.mixer.Sound("ost/c5cure1part2.mp3"))

        self.x = x
        self.y = y
        self.type = t

        self.image = pygame.Surface((96, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x - 32
        self.rect.y = self.y + 16
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.image.blit(self.text, self.text_rect)

        self.animation_loop = 0
        self.distance = 0
        self.state = 0
        self.timer = 0
        self.valuePosPrint = 0

        if self.type == 'description':
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            pygame.draw.rect(self.image, FF4BLACK, (0, 0, 96, 32))
            pygame.draw.rect(self.image, FF4WHITE, (0 + 2, 0 + 2, 96 - 4, 32 - 4))
            pygame.draw.rect(self.image, FF4BLUE, (0 + 5, 0 + 5, 96 - 10, 32 - 10))
            self.image.blit(self.text, self.text_rect)

    def update(self):
        if self.type == 'damage' or self.type == 'info':
            self.rect.y += self.animation_loop
            self.distance -= self.animation_loop
            self.animation_loop = 0

            if self.state == 0 and self.distance <= 16:
                self.animation_loop -= 3
            elif self.state == 0 and self.distance > 16:
                self.state = 1
            elif self.state == 2 and self.distance <= 8:
                self.animation_loop -= 3
            elif self.state == 2 and self.distance > 8:
                self.state = 3
            elif self.state == 4 and self.distance <= 4:
                self.animation_loop -= 3
            elif self.state == 4 and self.distance > 4:
                self.state = 5
            elif self.state == 6 and self.distance <= 2:
                self.animation_loop -= 3
            elif self.state == 6 and self.distance > 2:
                self.state = 7
            elif self.state == 8 and self.distance <= 1:
                self.animation_loop -= 3
            elif self.state == 8 and self.distance > 1:
                self.state = 9

            elif self.distance > 0:
                self.animation_loop += 3
            elif self.state >= 10:
                self.timer += 1
            elif self.distance == 0:
                self.state += 1

            if self.timer > 15:
                if type(self.originalText) is list:
                    if self.valuePosPrint <= len(self.originalText) - 1:
                        self.valuePosPrint += 1
                    if self.valuePosPrint > len(self.originalText) - 1:
                        self.kill()
                    elif self.valuePosPrint <= len(self.originalText) - 1:
                        self.text = self.font.render(str(self.originalText[self.valuePosPrint][1]), True,
                                                     self.originalColor[self.valuePosPrint])
                        self.text_rect = self.text.get_rect(center=(96 // 2, 32 // 2))
                        self.image.fill(BLACK)
                        # self.image.set_colorkey(BLACK)
                        self.image.blit(self.text, self.text_rect)
                        pygame.mixer.Sound.play(pygame.mixer.Sound("ost/c5cure1part2.mp3"))
                        self.timer = 0
                        self.state = 0
                        self.distance = 0
                else:
                    self.kill()
        if self.type == 'description':
            self.animation_loop += 1
            if self.animation_loop > 55:
                self.kill()


class Inventory(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game

        self._layer = GUI_LAYER
        self.groups = self.game.all_sprites, self.game.gui_sprites, self.game.keyboardcheck, self.game.mousecheck
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.font = pygame.font.Font('text/arial.ttf', 16)

        self.listOfHitBox = []
        self.itemToUse = []
        self.state = 0

        self.image = pygame.Surface((480, 480))
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = 80
        CreateGuiBox(self.image, 0, 0, 480, 480)

    def update(self):
        pass

    def check_mouse(self):
        pass

    def check_key(self):
        pass


def CreateGuiBox(image, x, y, width, height):
    pygame.draw.rect(image, FF4BLACK, (x, y, width, height))
    pygame.draw.rect(image, FF4WHITE, (x + 2, y + 2, width - 4, height - 4))
    pygame.draw.rect(image, FF4BLUE, (x + 5, y + 5, width - 10, height - 10))


def collided(sprite, other):
    return sprite.hitbox.colliderect(other.hitbox)
