import time
import pygame
from pathlib import Path
from config import *
from AuxiliarFunctions import *
from Player_Data import *
from Itens import *

import math
import random
import openpyxl


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 1
        self.internalTick = 0
        self.iframe = 40

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-6, -6)
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]
        self.up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]
        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]
        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]

        self.data = DataPlayer('none')

    def dataPrint(self):
        Text(self.game, self.rect.x, self.rect.y - 32, self.data[0], BLUE, 1, 'damage')
        pass

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0
        self.internalTick += 1
        if self.internalTick > 600:
            self.internalTick = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if not FIXEDCAM:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            if not FIXEDCAM:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_s]:
            if not FIXEDCAM:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        if keys[pygame.K_w]:
            if not FIXEDCAM:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            # i-frames set to 60
            self.iframe += 1

            if self.iframe > 60:
                # Obtain data from each enemy object colliding with player
                hitsList = []
                for entity in self.game.enemies:
                    if pygame.sprite.collide_rect(self, entity):
                        hitsList.append(entity)
                # Get the contact damage from one of them
                i = random.randint(0, len(hitsList) - 1)
                ReducedDamage = hitsList[i].data[3] - self.data.totalArmour
                if ReducedDamage < 0:
                    ReducedDamage = 0
                Text(self.game, self.rect.x, self.rect.y - 32, ReducedDamage, RED, 1, 'damage', self)
                self.data.hp -= ReducedDamage
                # print(self.data)
                # Text(self.game, self.rect.x, self.rect.y, self.data[0], GREEN, 1, '')
                self.iframe = 0
                if self.data.hp <= 0:
                    self.kill()
                    self.game.playing = False
        else:
            self.iframe = 40

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    if not FIXEDCAM:
                        for sprite in self.game.all_sprites:
                            sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    if not FIXEDCAM:
                        for sprite in self.game.all_sprites:
                            sprite.rect.x -= PLAYER_SPEED
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.width
                    if not FIXEDCAM:
                        for sprite in self.game.all_sprites:
                            sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    if not FIXEDCAM:
                        for sprite in self.game.all_sprites:
                            sprite.rect.y -= PLAYER_SPEED

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(10, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.aggro = False
        self.collided = 0
        self.iframe = 0
        self.last_shark_seen = None
        self.DistanceFromPlayerX = self.rect.x - self.game.player.rect.x
        self.DistanceFromPlayerY = self.rect.y - self.game.player.rect.y
        self.DistanceFromPlayer = math.sqrt(
            pow(self.DistanceFromPlayerX, 2) + pow(self.DistanceFromPlayerY, 2))

        self.internalTick = random.randint(0, 100)
        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]
        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]
        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]
        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                                 self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]

        Data = Path("data/Mob Data.xlsx")
        Dataobj = openpyxl.load_workbook(Data, data_only=True)
        ObjData = Dataobj.active
        PlayerDataExcel = []
        for i in range(5):
            PlayerDataExcel.append(ObjData['B' + str(i + 3)].value)
        # print(PlayerDataExcel)
        Dataobj.save(Data)
        self.data = PlayerDataExcel

    def data(self):
        return self.data

    def update(self):
        if self.internalTick > 60 or (self.aggro and self.internalTick > 40):
            self.movement()
            self.animate()

        self.rect.x += self.x_change
        # print('x, y', self.x_change, self.y_change)
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0
        self.internalTick = random.randint(0, 100)
        if self.iframe > 0:
            self.iframe -= 1

    def movement(self):
        dx = self.rect.x - self.game.player.rect.x
        dy = self.rect.y - self.game.player.rect.y
        self.DistanceFromPlayer = math.sqrt(
            pow(dx, 2) + pow(dy, 2))
        if self.data[4].lower() == 'zombie1':
            if self.DistanceFromPlayer < 64 or self.aggro:
                self.aggro = True
                if self.DistanceFromPlayer > 128:
                    self.aggro = False
                ToMove = PathingDirection(self.rect.x, self.rect.y, self.game.player.rect.x, self.game.player.rect.y)
                if ToMove == [0, 0]:
                    self.facing = random.choice(['left', 'right', 'up', 'down'])
                elif ToMove[0] == 0:
                    self.y_change += self.data[2] * ToMove[1] / abs(ToMove[1])
                    if ToMove[1] / abs(ToMove[1]) > 0:
                        self.facing = 'down'
                    else:
                        self.facing = 'up'
                elif ToMove[1] == 0:
                    self.x_change += self.data[2] * ToMove[0] / abs(ToMove[0])
                    if ToMove[0] / abs(ToMove[0]) > 0:
                        self.facing = 'right'
                    else:
                        self.facing = 'left'
                else:
                    # theta = math.atan(ToMove[1]/ToMove[0])
                    self.x_change += self.data[2] * ToMove[0] / abs(ToMove[0])
                    self.y_change += self.data[2] * ToMove[1] / abs(ToMove[1])
                    if ToMove[1] / abs(ToMove[1]) > 0:
                        self.facing = 'down'
                    else:
                        self.facing = 'up'

            elif abs(dx) < 128 and abs(dy) < 32 and self.facing == 'left' and dx > 1:
                self.aggro = True
                self.x_change -= self.data[2]
            elif abs(dx) < 128 and abs(dy) < 32 and self.facing == 'right' and dx < 1:
                self.aggro = True
                self.x_change += self.data[2]
            elif abs(dy) < 128 and abs(dx) < 32 and self.facing == 'up' and dy > 1:
                self.aggro = True
                self.y_change -= self.data[2]
            elif abs(dy) < 128 and abs(dx) < 32 and self.facing == 'down' and dy < 0:
                self.aggro = True
                self.y_change += self.data[2]
            else:
                self.DistanceFromPlayer = math.sqrt(
                    pow(self.x - self.game.player.x, 2) + pow(self.y - self.game.player.y, 2))
                if self.facing == 'left':
                    self.x_change -= self.data[2]
                    self.movement_loop -= 1
                    if self.movement_loop <= -self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                if self.facing == 'up':
                    self.y_change -= self.data[2]
                    self.movement_loop -= 1
                    if self.movement_loop <= -self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                if self.facing == 'right':
                    self.x_change += self.data[2]
                    self.movement_loop += 1
                    if self.movement_loop >= self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                if self.facing == 'down':
                    self.y_change += self.data[2]
                    self.movement_loop += 1
                    if self.movement_loop >= self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
        else:
            if self.facing == 'left':
                self.x_change -= ENEMY_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.max_travel = random.randint(10, 30)
                    self.movement_loop = 0
                    self.facing = 'up'
            if self.facing == 'up':
                self.y_change -= ENEMY_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.max_travel = random.randint(10, 30)
                    self.movement_loop = 0
                    self.facing = 'right'
            if self.facing == 'right':
                self.x_change += ENEMY_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.max_travel = random.randint(10, 30)
                    self.movement_loop = 0
                    self.facing = 'down'
            if self.facing == 'down':
                self.y_change += ENEMY_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.max_travel = random.randint(10, 30)
                    self.movement_loop = 0
                    self.facing = 'left'
            # Walking in circles

    def collide_enemy(self, direction):
        pass

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    if not self.aggro:
                        self.facing = random.choice(['left', 'up', 'down'])
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    if not self.aggro:
                        self.facing = random.choice(['right', 'up', 'down'])
                    self.rect.x = hits[0].rect.right
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    if not self.aggro:
                        self.facing = random.choice(['left', 'right', 'up'])
                    self.rect.y = hits[0].rect.top - self.rect.width
                if self.y_change < 0:
                    if not self.aggro:
                        self.facing = random.choice(['left', 'right', 'down'])
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Block(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Text(pygame.sprite.Sprite):
    # def __init__(self, text, game, size, color, width, height):
    def __init__(self, game, x, y, text, color, size, Type, Target):
        # print('define', x, y)
        # text = '9999/9999'
        # text = 'aaaaaaa'
        self.game = game
        self._layer = PLAYER_LAYER - 1
        self.groups = self.game.all_sprites
        self.type = Type
        self.Target = Target
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.text = text
        self.text2 = ''
        self.color = color
        self.font = pygame.font.Font('text/arial.ttf', 16)
        self.size = size
        while len(str(self.text)) / 3 > self.size:
            self.size += 1
        self.compensation = (self.size - 1) / 2 * TILESIZE
        self.internalTick = 0
        self.animation_loop = 0

        if self.type == 'damage' or self.type == 'damageE':
            self.image = pygame.Surface((self.width * self.size, self.height))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            if self.type == 'damageE':
                self.rect.x = self.Target.x * TILESIZE - (2 + TILESIZE * self.size / 2)
                self.rect.y = self.Target.y * TILESIZE - TILESIZE
            else:
                self.rect.x = self.x - (2 + TILESIZE * self.size / 2)
                self.rect.y = self.y - TILESIZE
            self.text = self.font.render(str(self.text), True, self.color)
            self.text_rect = self.text.get_rect(center=(self.width * self.size / 2, self.height / 2))
            self.image.blit(self.text, self.text_rect)
        elif self.type == 'hp':
            self.image = pygame.Surface((self.width * self.size, self.height))
            # self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

            self.text = self.font.render(self.text, True, GREEN)
            self.text_rect = self.text.get_rect(center=(self.width * 3 / 2, self.height / 2))
            self.image.blit(self.text, self.text_rect)
        else:
            self.image = pygame.Surface((self.width * self.size, self.height))
            # self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = self.x - (2 + TILESIZE * self.size / 2)
            self.rect.y = self.y - TILESIZE

            self.text = self.font.render(self.text, True, BLUE)
            self.text_rect = self.text.get_rect(center=(self.width * self.size / 2, self.height / 2))
            self.image.blit(self.text, self.text_rect)

    def update(self, text=''):
        self.internalTick += 1
        if self.type == 'damage' or self.animation_loop >= 1 or self.type == 'damageE':
            if self.type == 'damageE':
                self.rect.x = self.Target.rect.x - (2 + self.compensation)
                self.rect.y = self.Target.rect.y - (32 * (self.animation_loop / 36))
            else:
                self.rect.x = self.game.player.rect.x - (2 + self.compensation)
                self.rect.y = self.game.player.rect.y - (32 * (self.animation_loop / 36))
            self.image.blit(self.text, self.text_rect)
            # print('Damage Done1', self.rect.x, self.rect.y, self.game.player.rect.x, self.game.player.rect.y, self.internalTick)
            if self.animation_loop == 36:
                self.kill()
            self.animation_loop += 1
        else:
            # Standard above head text
            self.text = text
            self.text2 = self.font.render(self.text, True, BLUE)
            self.text_rect = self.text2.get_rect(center=(self.width * self.size / 2, self.height / 2))
            self.image.blit(self.text2, self.text_rect)
            # print('Damage Done2', self.rect.x, self.rect.y, self.game.player.rect.x, self.game.player.rect.y, self.internalTick)


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, wpn):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.wpn = wpn
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.game.player.attacking = True
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            # Obtain data from each enemy object colliding with player
            hitsList = []
            for entity in self.game.enemies:
                if pygame.sprite.collide_rect(self, entity):
                    hitsList.append(entity)
            # Get the contact damage from one of them
            i = random.randint(0, len(hitsList) - 1)
            ChoosenOne = hitsList[i]
            if ChoosenOne.last_shark_seen != self and ChoosenOne.iframe == 0:
                ChoosenOne.last_shark_seen = self
                ChoosenOne.iframe = 60
                # print('attack', self.wpn.dam)
                Text(self.game, ChoosenOne.rect.x, ChoosenOne.rect.y - 32, self.wpn.dam, BLUE, 1, 'damageE', ChoosenOne)
                ChoosenOne.data[0] -= self.wpn.dam
                # print(self.data)
                # Text(self.game, self.rect.x, self.rect.y, self.data[0], GREEN, 1, '')
                if ChoosenOne.data[0] <= 0:
                    ChoosenOne.kill()

    def animate(self):
        direction = self.game.player.facing

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]
        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]
        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]
        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('text/arial.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
