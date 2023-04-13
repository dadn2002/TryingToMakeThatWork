import math
import random

import pygame
from config import *
from Player_Data import *
from Itens import *
from zones import *


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
        self.y = y * TILESIZE
        self.render = render
        self.x_change = 0
        self.y_change = 0
        self.data = DataPlayer(name)
        self.facing = 'down'
        self.animation_loop = 1
        self.itemToUse = None
        self.width = 20
        self.height = 38

        self.image = self.game.character_spritesheet.get_sprite(6, 2, self.width, self.height)
        self.imagebattle = self.image
        self.rect = self.image.get_rect()
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
            self.movement()
            self.animate()

            self.rect.x += self.x_change
            self.collide_blocks('x')
            self.rect.y += self.y_change
            self.collide_blocks('y')
            self.x_change = 0
            self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.y_change += 1
            self.facing = 'down'
            for sprite in self.game.all_sprites:
                sprite.rect.y -= 1
        elif keys[pygame.K_w]:
            self.y_change -= 1
            self.facing = 'up'
            for sprite in self.game.all_sprites:
                sprite.rect.y += 1
        elif keys[pygame.K_a]:
            self.x_change -= 1
            self.facing = 'left'
            for sprite in self.game.all_sprites:
                sprite.rect.x += 1
        elif keys[pygame.K_d]:
            self.x_change += 1
            self.facing = 'right'
            for sprite in self.game.all_sprites:
                sprite.rect.x -= 1

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += 1
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= 1
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += 1
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= 1

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]
        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]
        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]
        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

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
    def __init__(self, game, x, y, name=''):

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
        self.data = DataPlayer('')
        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(38, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.y_change += 1
            self.facing = 'down'
            for sprite in self.game.all_sprites:
                sprite.rect.y -= 1
        elif keys[pygame.K_w]:
            self.y_change -= 1
            self.facing = 'up'
            for sprite in self.game.all_sprites:
                sprite.rect.y += 1
        elif keys[pygame.K_a]:
            self.x_change -= 1
            self.facing = 'left'
            for sprite in self.game.all_sprites:
                sprite.rect.x += 1
        elif keys[pygame.K_d]:
            self.x_change += 1
            self.facing = 'right'
            for sprite in self.game.all_sprites:
                sprite.rect.x -= 1

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += 1
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= 1
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += 1
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= 1

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]
        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]
        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]
        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
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


class Block(pygame.sprite.Sprite):

    def __init__(self, game, x, y, tag=''):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.tags = tag
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tag=''):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.tags = tag
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class HardCodedButton(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, fg, bg, content=None, fontsize=16, tags=[], itemToUse=None,
                 Target=None):
        if 'gui' in tags or itemToUse:
            self._layer = PLAYER_LAYER + 1
            self.groups = game.gui_sprites
            pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.font = pygame.font.Font('text/arial.ttf', fontsize)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.content = content
        if itemToUse and not content:
            self.content = itemToUse
        self.tags = tags
        self.itemToUse = itemToUse

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

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


class GuiHelp(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text, color, state, Type='', Target=''):
        self.game = game
        self._layer = GUI_LAYER
        self.groups = self.game.all_sprites, self.game.gui_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.state = state
        self.text = text
        self.color = color
        self.type = Type
        self.target = Target
        self.font = pygame.font.Font('text/arial.ttf', 16)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.Cx = x
        self.Cy = y
        self.internalTick = 0
        self.animation_loop = 0
        self.textList = self.game.party[0].data

        if state == 1:
            self._layer = PLAYER_LAYER + 1

        L, W, X, Y, J = 0, 0, 0, 0, 0
        if self.state == 0:
            # Player Info General Base Inventory
            L, W, X, Y, J = 363, 160, 0, 0, 3
        elif self.state == 1:
            # Base Menu Screen
            L, W, X, Y, J = 520, 560, 5, 8, 3
        elif self.state == 2:
            # Info Bar 1
            L, W, X, Y, J = 150, 360, 0, 0, 3
        elif self.state == 3:
            # Money Bar
            L, W, X, Y, J = 150, 64, 0, 0, 3
        elif self.state == 4:
            # Inventory Screen
            L, W, X, Y, J = 363, 360, 0, 0, 3
        elif self.state == 5:
            # Some Info
            L, W, X, Y, J = 150, 126, 0, 0, 3
        elif self.state == 6:
            # Item usage confirmation
            L, W, X, Y, J = 150, 42, 0, 0, 3

        self.image = pygame.Surface((L, W))
        if self.state == 1:
            pygame.draw.rect(self.image, FF4BLACK, (3, 6, 514, 548))
        self.image.fill(FF4WHITE, (X, Y, L - 2 * X, W - 2 * Y))
        self.image.fill(FF4BLUE, (X + J, Y + J, L - 2 * (X + J), W - 2 * (Y + J)))
        self.image.set_colorkey(BLACK)

        if self.state == 0:
            pos = [
                # Y = 10, 46, 82 for more characters
                [10, 46],  # Character
                [50, 33],  # Name
                [120, 33],  # Class
                [50, 51],  # Level
                [50, 67],  # HP
                [50, 83],  # MP
            ]
            PlayerImage = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            self.image.blit(PlayerImage, pos[0])
            self.image.blit(self.font.render(str(self.textList.name), True, FF4WHITE), pos[1])  # name
            self.image.blit(self.font.render('Warrior', True, FF4WHITE), pos[2])  # Class
            self.image.blit(self.font.render(('Level: ' + str(self.textList.lvl)), True, FF4WHITE), pos[3])  # Level
            self.image.blit(
                self.font.render(('HP: ' + str(self.textList.hp) + '/' + str(self.textList.maxhpmp[0])), True,
                                 FF4WHITE), pos[4])  # HP
            self.image.blit(
                self.font.render(('MP: ' + str(self.textList.mp) + '/' + str(self.textList.maxhpmp[1])), True,
                                 FF4WHITE), pos[5])  # MP
        elif self.state == 4:
            pos = [
                [50, 10]
            ]
            Repeat = []
            i = 0
            for element in self.game.player.data.inv:
                if element.name not in Repeat:
                    j = 0
                    for element2 in self.game.player.data.inv:
                        if element2.name == element.name:
                            j += 1
                    text = str(j) + 'x ' + str(element.name)
                    self.image.blit(self.font.render(str(i + 1) + ':', True, FF4WHITE), (10, 10 + 16 * i))  # name
                    text_width, text_height = self.font.size(text)
                    HardCodedButton(self.game, pos[0][0] + self.Cx, pos[0][1] + 16 * i + self.Cy, text_width,
                                    text_height,
                                    FF4WHITE, FF4BLUE, text, tags=['gui'], itemToUse=element.name)
                    i += 1
                    Repeat.append(element.name)
        elif self.state == 6:
            if isConsumable(self.game.player.itemToUse):
                self.image.blit(self.font.render('Use item?', True, FF4WHITE), [40, 5])
            else:
                self.image.blit(self.font.render('Trash item?', True, FF4WHITE), [35, 5])
            text_width, text_height = self.font.size('YES')
            # self.image.blit(self.font.render('YES', True, FF4WHITE), [20, 21])
            HardCodedButton(self.game, 20 + self.Cx, 21 + self.Cy, text_width, text_height, FF4WHITE, FF4BLUE,
                            'YES', 16, ['gui'])
            text_width, text_height = self.font.size('NO')
            # self.image.blit(self.font.render('NO', True, FF4WHITE), [98, 21])
            HardCodedButton(self.game, 98 + self.Cx, 21 + self.Cy, text_width, text_height, FF4WHITE, FF4BLUE,
                            'NO', 16, ['gui'])

        self.rect = self.image.get_rect()
        self.rect.x = self.Cx
        self.rect.y = self.Cy

    def update(self, text=''):
        pass


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
        self.originalImage = pygame.transform.scale(self.game.backgrounds_spritesheet.get_sprite(tempEnemies[1][0], tempEnemies[1][1], 240, 160), (640, 426))
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
        pygame.mixer.music.load("ost/105_Battle_Theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play(-1)

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
                                          creature[0].y-64, YELLOW, 'damage')
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
                    if type(self.didSomethingThisRound[i][1]) == Enemy and self.didSomethingThisRound[i][1].data.hp <= 0:
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
                                              self.didSomethingThisRound[i][0].y-64, YELLOW, 'damage')
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


def Inventory(self, state):
    for sprite in self.gui_sprites:
        sprite.kill()
    if state == 1:
        # Inventory Screen Base
        GuiHelp(self, 60, 40, '', FF4BLUE, 1, 'gui', None)
        GuiHelp(self, 65, 48, '', FF4BLUE, 0, 'gui', None)
        GuiHelp(self, 425, 528, '', FF4BLUE, 3, 'gui', None)
        GuiHelp(self, 65, 171, '', FF4BLUE, 4, 'gui', None)
        # Text(self, 65, 48, '', FF4BLUE, 4, 'gui', None)
    # X +- 5, Y +- 8 to fit State 1, does not generate black rect
    elif state == 2:
        # Inventory Options Bar
        GuiHelp(self, 425, 48, '', FF4BLUE, 2, 'gui', None)
        GuiHelp(self, 425, 405, '', FF4BLUE, 5, 'gui', None)
    elif state == 3:
        # Inventory Item Confirmation
        GuiHelp(self, self.mouse_pos[0], self.mouse_pos[1], '', FF4BLUE, 6, 'gui', None)


def CreateGuiBox(image, x, y, width, height):
    pygame.draw.rect(image, FF4BLACK, (x, y, width, height))
    pygame.draw.rect(image, FF4WHITE, (x + 2, y + 2, width - 4, height - 4))
    pygame.draw.rect(image, FF4BLUE, (x + 5, y + 5, width - 10, height - 10))
