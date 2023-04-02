import random
import pygame
from PIL import ImageFont, ImageDraw
from sprites import *
from config import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGTH))
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial', 32)
        self.running, self.screenState = True, None
        self.font = pygame.font.Font('text/arial.ttf', 32)
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pressed = pygame.mouse.get_pressed()

        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemies.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.inventory_spritesheet = Spritesheet('img/SOLID COLORS.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.go_background = pygame.image.load('img/gameover.png')

    def createTileMap(self, cardinality=4):
        RandomMap = True
        SpawnProofBlock = [[-1, -1], [-1, -1], [-1, -1]]
        MapExits = random.randint(1, 3)
        if RandomMap:
            MapSizeX = WIN_WIDTH / TILESIZE - 1
            MapSizeY = WIN_HEIGTH / TILESIZE - 1
            PlayerSpawn = [0, 0]
            if cardinality == 1:
                PlayerSpawn = [0, 9]
                SpawnProofBlock[0] = [0, 10]
                SpawnProofBlock[1] = [1, 9]
                SpawnProofBlock[2] = [1, 10]
            elif cardinality == 2:
                PlayerSpawn = [9, 0]
                SpawnProofBlock[0] = [10, 0]
                SpawnProofBlock[1] = [9, 1]
                SpawnProofBlock[2] = [10, 1]
            elif cardinality == 3:
                PlayerSpawn = [19, 9]
                SpawnProofBlock[0] = [19, 10]
                SpawnProofBlock[1] = [18, 9]
                SpawnProofBlock[2] = [18, 10]
            else:
                PlayerSpawn = [9, 19]
                SpawnProofBlock[0] = [10, 19]
                SpawnProofBlock[1] = [9, 18]
                SpawnProofBlock[2] = [10, 18]
            self.player = Player(self, PlayerSpawn[0], PlayerSpawn[1])

        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if RandomMap is False:
                    if column == 'B':
                        Block(self, j, i)
                    elif column == 'P':
                        self.player = Player(self, j, i)
                    elif column == 'E':
                        Enemy(self, j, i, 'goblin')
                else:
                    if j == PlayerSpawn[0] and i == PlayerSpawn[1]:
                        # Does not put blocks on Player
                        continue
                    if i == 0 or i == MapSizeY or j == 0 or j == MapSizeX:
                        # 2x1 entrance to the map
                        if j == SpawnProofBlock[0][0] and i == SpawnProofBlock[0][1]:
                            continue
                        # Define Borders
                        Block(self, j, i)
                    else:
                        if random.randint(0, 100) < 10:
                            # 2x2 entrance to the map
                            SpawnProofVerification = False
                            for l in range(1, 3):
                                if j == SpawnProofBlock[l][0] and i == SpawnProofBlock[l][1]:
                                    SpawnProofVerification = True
                                    print('block', j, i)
                                    break
                            if SpawnProofVerification:
                                continue
                            # Random Blocks
                            Block(self, j, i)
                        elif random.randint(0, 100) < 3:
                            # Random Enemies
                            Enemy(self, j, i, 'goblin')

    def new(self):
        self.playing = True
        self.tick = 0

        self.inventory_background = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.playerSprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTileMap(cardinality=random.randint(1, 4))

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    print(self.player.data.inv)
                if self.screenState == INGAME:
                    if event.key == pygame.K_q:
                        if self.player.facing == 'up':
                            Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE, self.player.data.skl,
                                   'player')
                        if self.player.facing == 'down':
                            Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE, self.player.data.skl,
                                   'player')
                        if self.player.facing == 'left':
                            Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y, self.player.data.skl,
                                   'player')
                        if self.player.facing == 'right':
                            Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y, self.player.data.skl,
                                   'player')
                    elif event.key == pygame.K_e:
                        Inventory(self, 1)
                        self.screenState = INVENTORY
                elif self.screenState == INVENTORY:
                    if event.key == pygame.K_e:
                        temp = len(self.inventory_background.sprites())
                        for sprite in self.inventory_background:
                            sprite.kill()
                        if temp >= 4:
                            # The basic amount of sprites in inventory, close inventory
                            self.screenState = INGAME
                        else:
                            # Close anothers tabs
                            Inventory(self, 1)
                    elif event.key == pygame.K_i:
                        pass
                    elif event.key == pygame.K_1:
                        pass
                    elif event.key == pygame.K_2:
                        pass

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pressed = pygame.mouse.get_pressed()
        if self.screenState == INGAME:
            self.all_sprites.update()
        elif self.screenState == INVENTORY:
            self.inventory_background.update()

    def draw(self):
        # Draw sprites
        self.clock.tick(FPS)
        if self.screenState == INGAME:
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
        elif self.screenState == INVENTORY:
            # self.draw_text("Inventory", self.font, WHITE, WIN_WIDTH / 2, WIN_HEIGTH / 2)
            # print('draw')
            self.inventory_background.draw(self.screen)
            for i in range(len(self.player.data.inv)):
                # self.draw_text(self.player.data.inv[i], self.font, WHITE, 0, i * TILESIZE)
                pass
        pygame.display.update()

    def draw_text(self, text, font, text_col, x, y):
        # Draw text
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def main(self):
        # game loop
        self.screenState = INGAME
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.tick += 1

    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGTH / 2))

        restart_button = Button(10, WIN_HEIGTH - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = self.font.render('Great Day', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


# print(pygame.font.get_fonts())
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
