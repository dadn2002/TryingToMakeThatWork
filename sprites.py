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
        sprite.set_colorkey(WHITE)
        return sprite


class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.playerSprites
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
        self.isAttacking = False

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
        if self.data.hp <= 0:
            self.kill()
        if self.internalTick % 5 != 0:
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

    def useItem(self, itemName):
        for i in range(len(self.data.inv)):
            print('checking', i, self.data.inv[i].info(), itemName)
            if self.data.inv[i].name.lower() == itemName.lower():
                for element in self.data.inv[i].tags:
                    if element[0].lower() == 'hp':
                        self.data.hp += element[1]
                        if self.data.hp >= self.data.maxhpmp[0]:
                            self.data.hp = self.data.maxhpmp[0]
                    elif element[0].lower() == 'mp':
                        self.data.mp += element[1]
                        if self.data.mp >= self.data.maxhpmp[1]:
                            self.data.mp = self.data.maxhpmp[1]
                del self.data.inv[i]
                break

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if not FIXEDCAM:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += self.data.spd
            self.x_change -= self.data.spd
            self.facing = 'left'
        if keys[pygame.K_d]:
            if not FIXEDCAM:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= self.data.spd
            self.x_change += self.data.spd
            self.facing = 'right'
        if keys[pygame.K_s]:
            if not FIXEDCAM:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= self.data.spd
            self.y_change += self.data.spd
            self.facing = 'down'
        if keys[pygame.K_w]:
            if not FIXEDCAM:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += self.data.spd
            self.y_change -= self.data.spd
            self.facing = 'up'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        hits1 = pygame.sprite.spritecollide(self, self.game.attacks, False)
        if hits or hits1:
            # i-frames set to 60
            self.iframe += 1

            if self.iframe > 60:
                # Obtain data from each enemy object colliding with player
                hitsList = []
                if hits:
                    # check if its contact damage
                    for entity in self.game.enemies:
                        if pygame.sprite.collide_rect(self, entity):
                            hitsList.append(entity)
                    # Get the contact damage from one of them
                    i = random.randint(0, len(hitsList) - 1)
                    # print(hitsList[i].data.skl)
                    ReducedDamage = int(hitsList[i].data.skl[0].dam) - self.data.totalArmour
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
                elif hits1:
                    # Check if its skill damage
                    for entity in self.game.attacks:
                        if pygame.sprite.collide_rect(self, entity) and entity.ally == self.game.playerSprites:
                            hitsList.append(entity)
                    if len(hitsList) == 0:
                        # Sometimes the enemy dies at the same frame he hit us so, just to be safe
                        pass
                    else:
                        if len(hitsList) == 1:
                            i = 0
                        else:
                            i = random.randint(0, len(hitsList) - 1)
                        # print(hitsList[i].wpn[random.randint(1, len(hitsList[i].wpn)-1)].dam)
                        ReducedDamage = int(
                            hitsList[i].wpn[random.randint(1, len(hitsList[i].wpn) - 1)].dam) - self.data.totalArmour
                        # print(hitsList[i].wpn[random.randint(1, len(hitsList[i].wpn) - 1)].dam)
                        if ReducedDamage < 0:
                            ReducedDamage = 0
                        Text(self.game, self.rect.x, self.rect.y - 32, ReducedDamage, RED, 1, 'damage', self)
                        self.data.hp -= ReducedDamage
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
                            sprite.rect.x += self.data.spd
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    if not FIXEDCAM:
                        for sprite in self.game.all_sprites:
                            sprite.rect.x -= self.data.spd
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.width
                    if not FIXEDCAM:
                        for sprite in self.game.all_sprites:
                            sprite.rect.y += self.data.spd
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    if not FIXEDCAM:
                        for sprite in self.game.all_sprites:
                            sprite.rect.y -= self.data.spd

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
    def __init__(self, game, x, y, name):
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
        self.isAttacking = False

        self.data = DataEnemy(name)
        self.image = self.game.enemy_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1], self.width,
                                                            self.height)
        pygame.image.save(self.image, "image.jpg")

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.aggro = False
        self.aggroTick = 60
        self.aggroSummon = False
        self.collided = 0
        self.iframe = 0
        self.last_shark_seen = None
        self.DistanceFromPlayerX = self.rect.x - self.game.player.rect.x
        self.DistanceFromPlayerY = self.rect.y - self.game.player.rect.y
        self.DistanceFromPlayer = math.sqrt(
            pow(self.DistanceFromPlayerX, 2) + pow(self.DistanceFromPlayerY, 2))

        self.internalTick = 0
        self.down_animations = [
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1], self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0] + 32, self.data.sprite[1], self.width,
                                                   self.height),
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0] + 65, self.data.sprite[1], self.width,
                                                   self.height)]
        self.up_animations = [
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1] + 32, self.width,
                                                   self.height),
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0] + 32, self.data.sprite[1] + 32, self.width,
                                                   self.height),
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0] + 65, self.data.sprite[1] + 32, self.width,
                                                   self.height)]
        self.left_animations = [
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1] + 96, self.width,
                                                   self.height),
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0] + 32, self.data.sprite[1] + 96, self.width,
                                                   self.height),
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0] + 65, self.data.sprite[1] + 96, self.width,
                                                   self.height)]
        self.right_animations = [
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1] + 64, self.width,
                                                   self.height),
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0] + 32, self.data.sprite[1] + 64, self.width,
                                                   self.height),
            self.game.enemy_spritesheet.get_sprite(self.data.sprite[0] + 65, self.data.sprite[1] + 64, self.width,
                                                   self.height)]

    def data(self):
        return self.data

    def update(self):
        print(self.internalTick)
        if self.data.hp <= 0:
            if self.data.name == 'watcher':
                for sprite in self.game.enemies:
                    sprite.aggroSummon = False
            self.kill()
        if self.internalTick % 4 == 0 or (self.aggro and self.internalTick % 2 == 0):
            # 0.4 inactive / 0.6 active
            self.movement()
            self.animate()
            pass

        self.rect.x += self.x_change
        # print('x, y', self.x_change, self.y_change)
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        # print(self.x_change, self.y_change)

        self.x_change = 0
        self.y_change = 0
        if self.iframe > 0:
            self.iframe -= 1
        self.internalTick += 1
        if self.internalTick > 60:
            self.internalTick = 0

    def movement(self):
        dx = self.rect.x - self.game.player.rect.x
        dy = self.rect.y - self.game.player.rect.y
        self.DistanceFromPlayer = math.sqrt(
            pow(dx, 2) + pow(dy, 2))
        if self.data.ai.lower() == 'zombie1':
            # Direct View
            if (abs(dx) < 128 or self.aggro or self.aggroSummon) and abs(dy) < 48 and self.facing != 'right' and dx > 1:
                self.aggro = True
                self.facing = 'left'
                self.x_change -= self.data.spd
            elif (abs(dx) < 128 or self.aggro or self.aggroSummon) and abs(
                    dy) < 48 and self.facing != 'left' and dx < 1:
                self.aggro = True
                self.facing = 'right'
                self.x_change += self.data.spd
            elif (abs(dy) < 128 or self.aggro or self.aggroSummon) and abs(
                    dx) < 48 and self.facing != 'down' and dy > 1:
                self.aggro = True
                self.facing = 'up'
                self.y_change -= self.data.spd
            elif (abs(dy) < 128 or self.aggro or self.aggroSummon) and abs(dx) < 48 and self.facing != 'up' and dy < 0:
                self.aggro = True
                self.facing = 'down'
                self.y_change += self.data.spd
            # Player near or aggro trigged
            elif self.DistanceFromPlayer < 64 or self.aggro or self.aggroSummon:
                self.aggro = True
                if self.DistanceFromPlayer > 128:
                    self.aggro = False
                ToMove = PathingDirection(self.rect.x, self.rect.y, self.game.player.rect.x, self.game.player.rect.y)
                if ToMove == [0, 0]:
                    self.facing = random.choice(['left', 'right', 'up', 'down'])
                elif ToMove[0] == 0:
                    self.y_change += ToMove[1] / abs(ToMove[1]) * self.data.spd
                    if ToMove[1] / abs(ToMove[1]) > 0:
                        self.facing = 'down'
                    else:
                        self.facing = 'up'
                elif ToMove[1] == 0:
                    self.x_change += ToMove[0] / abs(ToMove[0]) * self.data.spd
                    if ToMove[0] / abs(ToMove[0]) > 0:
                        self.facing = 'right'
                    else:
                        self.facing = 'left'
                else:
                    # theta = math.atan(ToMove[1]/ToMove[0])
                    self.x_change += ToMove[0] / abs(ToMove[0]) * self.data.spd
                    self.y_change += ToMove[1] / abs(ToMove[1]) * self.data.spd
                    if ToMove[1] / abs(ToMove[1]) > 0:
                        self.facing = 'down'
                    else:
                        self.facing = 'up'
                # Attack animation limiter
                if self.DistanceFromPlayer <= 32:
                    self.isAttacking += 1
                    if self.isAttacking > 60:
                        Attack(self.game, self.rect.x, self.rect.y - TILESIZE, self.data.skl, 'enemy', self.facing)
                        self.isAttacking = 0
                else:
                    self.isAttacking = 60
            # Wandering
            else:
                self.DistanceFromPlayer = math.sqrt(
                    pow(self.x - self.game.player.x, 2) + pow(self.y - self.game.player.y, 2))
                if self.facing == 'left':
                    self.x_change -= self.data.spd
                    self.movement_loop -= 1
                    if self.movement_loop <= -self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                elif self.facing == 'up':
                    self.y_change -= self.data.spd
                    self.movement_loop -= 1
                    if self.movement_loop <= -self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                elif self.facing == 'right':
                    self.x_change += self.data.spd
                    self.movement_loop += 1
                    if self.movement_loop >= self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                elif self.facing == 'down':
                    self.y_change += self.data.spd
                    self.movement_loop += 1
                    if self.movement_loop >= self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
        if self.data.ai.lower() == 'watcher1':
            if self.DistanceFromPlayer < 256:
                if self.aggroTick >= 60:
                    self.aggroTick = 0
                    Text(self.game, self.rect.x, self.rect.y - 32, '!', RED, 1, 'alert', self)
                self.aggroTick += 1
                self.aggro = True
                for entity in self.game.enemies:
                    entity.aggroSummon = True
                ToMove = PathingDirection(self.rect.x, self.rect.y, self.game.player.rect.x, self.game.player.rect.y)
                if self.DistanceFromPlayer < 128:
                    if ToMove == [0, 0]:
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                    elif ToMove[0] == 0:
                        self.y_change -= ToMove[1] / abs(ToMove[1]) * self.data.spd
                        if ToMove[1] / abs(ToMove[1]) > 0:
                            self.facing = 'down'
                        else:
                            self.facing = 'up'
                    elif ToMove[1] == 0:
                        self.x_change -= ToMove[0] / abs(ToMove[0]) * self.data.spd
                        if ToMove[0] / abs(ToMove[0]) > 0:
                            self.facing = 'right'
                        else:
                            self.facing = 'left'
                    else:
                        # theta = math.atan(ToMove[1]/ToMove[0])
                        self.x_change -= ToMove[0] / abs(ToMove[0]) * self.data.spd
                        self.y_change -= ToMove[1] / abs(ToMove[1]) * self.data.spd
                        if ToMove[1] / abs(ToMove[1]) > 0:
                            self.facing = 'down'
                        else:
                            self.facing = 'up'
                elif self.DistanceFromPlayer > 128:
                    if ToMove == [0, 0]:
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                    elif ToMove[0] == 0:
                        self.y_change += ToMove[1] / abs(ToMove[1]) * self.data.spd
                        if ToMove[1] / abs(ToMove[1]) > 0:
                            self.facing = 'down'
                        else:
                            self.facing = 'up'
                    elif ToMove[1] == 0:
                        self.x_change += ToMove[0] / abs(ToMove[0]) * self.data.spd
                        if ToMove[0] / abs(ToMove[0]) > 0:
                            self.facing = 'right'
                        else:
                            self.facing = 'left'
                    else:
                        # theta = math.atan(ToMove[1]/ToMove[0])
                        self.x_change += ToMove[0] / abs(ToMove[0]) * self.data.spd
                        self.y_change += ToMove[1] / abs(ToMove[1]) * self.data.spd
                        if ToMove[1] / abs(ToMove[1]) > 0:
                            self.facing = 'down'
                        else:
                            self.facing = 'up'
            else:
                self.aggro = False
                self.aggroTick = 60
                self.DistanceFromPlayer = math.sqrt(
                    pow(self.x - self.game.player.x, 2) + pow(self.y - self.game.player.y, 2))
                if self.facing == 'left':
                    self.x_change -= self.data.spd
                    self.movement_loop -= 1
                    if self.movement_loop <= -self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                if self.facing == 'up':
                    self.y_change -= self.data.spd
                    self.movement_loop -= 1
                    if self.movement_loop <= -self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                if self.facing == 'right':
                    self.x_change += self.data.spd
                    self.movement_loop += 1
                    if self.movement_loop >= self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
                if self.facing == 'down':
                    self.y_change += self.data.spd
                    self.movement_loop += 1
                    if self.movement_loop >= self.max_travel:
                        self.max_travel = random.randint(5, 20) * TILESIZE
                        self.movement_loop = 0
                        self.facing = random.choice(['left', 'right', 'up', 'down'])
        else:
            if self.facing == 'left':
                self.x_change -= self.data.spd
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.max_travel = random.randint(10, 30)
                    self.movement_loop = 0
                    self.facing = 'up'
            if self.facing == 'up':
                self.y_change -= self.data.spd
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.max_travel = random.randint(10, 30)
                    self.movement_loop = 0
                    self.facing = 'right'
            if self.facing == 'right':
                self.x_change += self.data.spd
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.max_travel = random.randint(10, 30)
                    self.movement_loop = 0
                    self.facing = 'down'
            if self.facing == 'down':
                self.y_change += self.data.spd
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
        # print(self.data.sprite[0], self.data.sprite[1])
        doStop = True
        if self.data.ai == 'watcher1':
            if not self.aggro:
                animation_increment = 0.1
            else:
                animation_increment = 0.2
                doStop = False
        else:
            animation_increment = 0.1

        if self.facing == "down":
            if self.y_change == 0 and doStop:
                self.image = self.game.enemy_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1],
                                                                    self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += animation_increment
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        elif self.facing == "up":
            if self.y_change == 0 and doStop:
                self.image = self.game.enemy_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1] + 32,
                                                                    self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += animation_increment
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        elif self.facing == "left":
            if self.x_change == 0 and doStop:
                self.image = self.game.enemy_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1] + 96,
                                                                    self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += animation_increment
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        elif self.facing == "right":
            if self.x_change == 0 and doStop:
                self.image = self.game.enemy_spritesheet.get_sprite(self.data.sprite[0], self.data.sprite[1] + 64,
                                                                    self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += animation_increment
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
        if Type != 'gui':
            if Type == 'alert':
                self._layer -= 1
            self.groups = self.game.all_sprites
        else:
            self.groups = self.game.inventory_background
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

        if self.type == 'damage' or self.type == 'damageE' or self.type == 'alert':
            self.image = pygame.Surface((self.width * self.size, self.height))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            if self.type == 'damageE' or self.type == 'alert':
                self.rect.x = self.Target.x * TILESIZE - (2 + TILESIZE * self.size / 2)
                self.rect.y = self.Target.y * TILESIZE - TILESIZE
            else:
                self.rect.x = self.x - (2 + TILESIZE * self.size / 2)
                self.rect.y = self.y - TILESIZE
            # print('damage1', self.text)
            self.text2 = self.font.render(str(self.text), True, self.color)
            self.text_rect = self.text2.get_rect(center=(self.width * self.size / 2, self.height / 2))
            self.image.blit(self.text2, self.text_rect)
            # print('damage2', self.text)
        elif self.type == 'hp':
            self.image = pygame.Surface((self.width * self.size, self.height))
            # self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

            self.text = self.font.render(self.text, True, GREEN)
            self.text_rect = self.text.get_rect(center=(self.width * 3 / 2, self.height / 2))
            self.image.blit(self.text, self.text_rect)
        elif self.type == 'gui':
            # self.groups = self.game.inventory_background
            self._layer = GUI_LAYER
            # print(self.size)
            L, W, X, Y, J = 0, 0, 0, 0, 0
            Cx = self.x / 32
            Cy = self.y / 32

            self.textList = self.game.player.data.info()
            self.textList = [
                self.textList[0],
                self.textList[1],
                self.textList[2],
                self.textList[3],
                self.textList[4].info(),
                self.textList[5][0].info(),
                self.textList[5][1].info(),
                self.textList[5][2].info(),
                self.textList[5][3].info(),
                self.textList[5][4].info(),
                self.textList[6],
                self.textList[7],
                self.textList[8],
                self.textList[9],
                self.textList[10]
            ]

            if self.size == 0:
                # Player Info General Base Inventory
                L, W, X, Y, J = 363, 160, 0, 0, 3
            if self.size == 1:
                # Base Menu Screen
                L, W, X, Y, J = 520, 560, 5, 8, 3
            elif self.size == 2:
                # Info Bar 1
                L, W, X, Y, J = 150, 360, 0, 0, 3
            elif self.size == 3:
                # Money Bar
                L, W, X, Y, J = 150, 64, 0, 0, 3
            elif self.size == 4:
                # Inventory Screen
                L, W, X, Y, J = 363, 360, 0, 0, 3
            elif self.size == 5:
                # Some Info
                L, W, X, Y, J = 150, 126, 0, 0, 3
            elif self.size == 6:
                # Item usage confirmation
                L, W, X, Y, J = 150, 42, 0, 0, 3
                pass

            self.image = pygame.Surface((L, W))
            self.image.fill(FF4WHITE, (X, Y, L - 2 * X, W - 2 * Y))
            self.image.fill(FF4BLUE, (X + J, Y + J, L - 2 * (X + J), W - 2 * (Y + J)))
            if self.size == 0:
                pos = [
                    # Y = 10, 46, 82 for more characters
                    [10, 46],  # Character
                    [50, 33],  # Name
                    [120, 33],  # Class
                    [50, 51],  # Level
                    [50, 67],  # HP
                    [50, 83],  # MP
                ]
                # print(self.textList)
                PlayerImage = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
                self.image.blit(PlayerImage, pos[0])
                self.image.blit(self.font.render(str(self.textList[0]), True, FF4WHITE), pos[1])  # name
                self.image.blit(self.font.render('Warrior', True, FF4WHITE), pos[2])  # Class
                self.image.blit(self.font.render(('Level: ' + str(self.textList[13])), True, FF4WHITE), pos[3])  # Level
                self.image.blit(
                    self.font.render(('HP: ' + str(self.textList[1]) + '/' + str(self.textList[14][0])), True,
                                     FF4WHITE), pos[4])  # HP
                self.image.blit(
                    self.font.render(('MP: ' + str(self.textList[2]) + '/' + str(self.textList[14][1])), True,
                                     FF4WHITE), pos[5])  # MP
            elif self.size == 4:
                pos = [
                    [50, 10]
                ]
                Repeat = []
                i = 0
                for element in self.game.player.data.inv:
                    # print(element)
                    if element.name not in Repeat:
                        j = 0
                        for element2 in self.game.player.data.inv:
                            if element2.name == element.name:
                                j += 1
                        text = str(j) + 'x ' + str(element.name)
                        self.image.blit(self.font.render(str(i + 1) + ':', True, FF4WHITE), (10, 10 + 16 * i))  # name
                        # self.image.blit(self.font.render(text, True, FF4WHITE),
                        # (pos[0][0], pos[0][1] + 16 * i))
                        text_width, text_height = self.font.size(text)
                        # print('before', [pos[0][0] + Cx, pos[0][1] + 16 * i + Cy])
                        Button(pos[0][0] + Cx, pos[0][1] + 16 * i + Cy, text_width, text_height, FF4WHITE, FF4BLUE,
                               text, 16,
                               'gui', self.game, str(element.name))
                        i += 1
                        Repeat.append(element.name)
            elif self.size == 6:
                self.image.blit(self.font.render('Confirm', True, FF4WHITE), [48, 5])
                text_width, text_height = self.font.size('YES')
                # self.image.blit(self.font.render('YES', True, FF4WHITE), [20, 21])
                Button(20 + Cx, 21 + Cy, text_width, text_height, FF4WHITE, FF4BLUE,
                       'YES', 16,
                       'gui', self.game, self.game.player.itemToUse)
                text_width, text_height = self.font.size('NO')
                # self.image.blit(self.font.render('NO', True, FF4WHITE), [98, 21])
                Button(98 + Cx, 21 + Cy, text_width, text_height, FF4WHITE, FF4BLUE,
                       'NO', 16,
                       'gui', self.game)

            self.rect = self.image.get_rect()
            self.rect.x = Cx
            self.rect.y = Cy
            # print(self.image, self.rect)
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
        if self.type == 'damage' or self.animation_loop >= 1 or self.type == 'damageE' or self.type == 'alert':
            if self.type == 'damageE' or self.type == 'alert':
                self.rect.x = self.Target.rect.x - (2 + self.compensation)
                self.rect.y = self.Target.rect.y - (32 * (self.animation_loop / 36))
            else:
                self.rect.x = self.game.player.rect.x - (2 + self.compensation)
                self.rect.y = self.game.player.rect.y - (32 * (self.animation_loop / 36))
            self.image.blit(self.text2, self.text_rect)
            if self.animation_loop == 36:
                self.kill()
            self.animation_loop += 1
        if self.type == 'gui':
            if self.size == 6:
                self.game.screen.blit(self.image, self.rect)
        else:
            # Standard above head text
            self.text = text
            self.text2 = self.font.render(self.text, True, BLUE)
            self.text_rect = self.text2.get_rect(center=(self.width * self.size / 2, self.height / 2))
            self.image.blit(self.text2, self.text_rect)
            # print('Damage Done2', self.rect.x, self.rect.y, self.game.player.rect.x, self.game.player.rect.y, self.internalTick)


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, wpn, Allys='', facing=''):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        if Allys == 'enemy':
            self.ally = self.game.playerSprites
            self.innerFacing = facing
            y += TILESIZE
            if self.innerFacing == 'up':
                y -= TILESIZE
            elif self.innerFacing == 'down':
                y += TILESIZE
            elif self.innerFacing == 'left':
                x -= TILESIZE
            elif self.innerFacing == 'right':
                x += TILESIZE
        else:
            self.ally = self.game.enemies
            self.innerFacing = self.game.player.facing

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
        self.animate()
        if self.ally != self.game.playerSprites:
            self.game.player.attacking = True
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
            ReducedDamage = self.wpn.dam - ChoosenOne.data.damRed
            if ReducedDamage < 0:
                ReducedDamage = 0
            elif ChoosenOne.last_shark_seen != self and ChoosenOne.iframe == 0 and ReducedDamage > 0:
                ChoosenOne.last_shark_seen = self
                ChoosenOne.iframe = 60
                # print('attack', self.wpn.dam)
                Text(self.game, ChoosenOne.rect.x, ChoosenOne.rect.y - 32, ReducedDamage, BLUE, 1, 'damageE',
                     ChoosenOne)
                ChoosenOne.data.hp -= ReducedDamage
                # print(self.data)
                # Text(self.game, self.rect.x, self.rect.y, self.data[0], GREEN, 1, '')

    def animate(self):
        if self.ally == self.game.enemies:
            direction = self.game.player.facing
        else:
            direction = self.innerFacing
        # print(direction)

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


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, fg, bg, content, fontsize, Type='', Game=None, itemToUse=None):
        # print(x, y, width, height)
        if Type == 'gui':
            self._layer = PLAYER_LAYER - 1
            self.groups = Game.inventory_background
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.game = Game
        self.font = pygame.font.Font('text/arial.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.itemToUse = itemToUse

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
        pygame.image.save(self.image, "image.jpg")

    def update(self):
        self.game.screen.blit(self.image, self.rect)
        if self.is_pressed(self.game.mouse_pos, self.game.mouse_pressed):
            if self.content not in ['YES', 'NO']:
                self.game.player.itemToUse = self.itemToUse
                Inventory(self.game, 3)
            elif self.content == 'YES':
                self.game.player.useItem(self.game.player.itemToUse)
                self.game.player.itemToUse = None
                Inventory(self.game, 1)
            elif self.content == 'NO':
                self.game.player.itemToUse = None
                Inventory(self.game, 1)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


def Inventory(self, state):
    for sprite in self.inventory_background:
        sprite.kill()
    if state == 1:
        # Inventory Screen Base
        Text(self, 60, 40, '', FF4BLUE, 1, 'gui', None)
        Text(self, 65, 48, '', FF4BLUE, 0, 'gui', None)
        Text(self, 425, 528, '', FF4BLUE, 3, 'gui', None)
        Text(self, 65, 171, '', FF4BLUE, 4, 'gui', None)
        # Text(self, 65, 48, '', FF4BLUE, 4, 'gui', None)
    # X +- 5, Y +- 8 to fit State 1, does not generate black rect
    elif state == 2:
        # Inventory Options Bar
        Text(self, 425, 48, '', FF4BLUE, 2, 'gui', None)
        Text(self, 425, 405, '', FF4BLUE, 5, 'gui', None)
    elif state == 3:
        # Inventory Item Confirmation
        Text(self, self.mouse_pos[0], self.mouse_pos[1], '', FF4BLUE, 6, 'gui', None)
