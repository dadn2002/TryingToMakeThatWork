import random

import pygame

from sprites import *
from config import *
from Maps import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('text/arial.ttf', 32)
        self.running = True
        self.gameState = 0
        self.party = []

        self.character_spritesheet = Spritesheet('img/character.png')
        self.playableNpcs_spritesheet = Spritesheet('img/playable_npcs.png')
        self.creatures_spritesheet = Spritesheet('img/creatures1.png')
        self.castleTiles_spritesheet = Spritesheet('img/CastleTiles.png')
        self.backgrounds_spritesheet = Spritesheet('img/battle_backgrounds.png')
        self.map_spritesheet = Spritesheet('img/DomaCastleExterior.png')

    def createMap(self):
        self.zeroCoord = Block(self, 0, 0, 32, 32, hasHitBox=False)
        # self.map = BackgroundMap(self, 0, 0, 'DomaCastle')
        self.player = Player(self, 8, 7, 'Belmont', render=True)  # 33, 52
        self.party.append(self.player)
        GenerateMap(self, 'domacastle')
        if FIXEDCAM:
            valueToIncrease = [self.player.rect.x, self.player.rect.y]
            for sprite in self.all_sprites:
                sprite.rect.x += 320 - valueToIncrease[0] - 16
                sprite.rect.y += 320 - valueToIncrease[1] - 16

    def new(self):
        self.gameState = 1

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.objects = pygame.sprite.LayeredUpdates()
        self.npc_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.animations = pygame.sprite.LayeredUpdates()
        self.gui_sprites = pygame.sprite.LayeredUpdates()
        self.battle_sprites = pygame.sprite.LayeredUpdates()
        self.mousecheck = pygame.sprite.LayeredUpdates()
        self.keyboardcheck = pygame.sprite.LayeredUpdates()

        self.createMap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.gameState = -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    print(self.blocks, self.all_sprites)
            if self.gameState == 1:
                # Main game running
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        self.gameState = 2
                        Inventory(self)
                    if event.key == pygame.K_r:
                        self.gameState = 3
                        BattleScene(self, self.party, 'plains', 0)
            if self.gameState == 2:
                # Inventory open
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.gameState = 1
                        for sprite in self.gui_sprites:
                            sprite.kill()
                    for s in self.keyboardcheck:
                        s.check_click(event.key)
                elif event.type == pygame.MOUSEBUTTONUP:
                    for s in self.mousecheck:
                        s.check_click(event.pos)
            if self.gameState == 3:
                # Battle instance
                if event.type == pygame.KEYDOWN:
                    for s in self.keyboardcheck:
                        s.check_key(event.key)
                elif event.type == pygame.MOUSEBUTTONUP:
                    for s in self.mousecheck:
                        s.check_click(event.pos)

    def update(self):
        if self.gameState == 1:
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_pressed = pygame.mouse.get_pressed()
            self.all_sprites.update()
        elif self.gameState == 2:
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_pressed = pygame.mouse.get_pressed()
            self.gui_sprites.update()
        elif self.gameState == 3:
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_pressed = pygame.mouse.get_pressed()
            self.battle_sprites.update()

    def draw(self):
        if self.gameState == 1:
            if FIXEDCAM:
                # My man in stupid as shit, save the increment before messing with everything else
                valueToIncrease = [self.player.rect.x, self.player.rect.y]
                for sprite in self.all_sprites:
                    # New centering camera method, solved issues with random width/height blocks
                    sprite.rect.x += 304 - valueToIncrease[0]
                    sprite.rect.y += 304 - valueToIncrease[1]
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
        elif self.gameState == 2:
            self.gui_sprites.draw(self.screen)
        elif self.gameState == 3:
            self.battle_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.gameState != -1:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def intro_screen(self):
        pass

    def game_over(self):
        pass


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
