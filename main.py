import random

import pygame

from sprites import *
from config import *
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

        self.character_spritesheet = Spritesheet('img/characters.png')
        self.creatures_spritesheet = Spritesheet('img/creatures1.png')
        self.backgrounds_spritesheet = Spritesheet('img/battle_backgrounds.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')

    def createMap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'P':
                    self.player = Player(self, j, i, 'Belmont', render=True)
                    self.party.append(self.player)
        for sprite in self.all_sprites:
            sprite.rect.x += 320 - self.player.rect.x - 16
            sprite.rect.y += 320 - self.player.rect.y - 16

    def new(self):
        self.gameState = 1

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
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
            if self.gameState == 1:
                # Main game running
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.gameState = 2
                        Inventory(self, 1)
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
            pygame.mixer.music.stop()
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
