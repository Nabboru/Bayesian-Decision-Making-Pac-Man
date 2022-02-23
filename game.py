import pygame
import sys
from settings import *
import random
from scipy.stats import beta
import math
from ghosts import GhostAgent

pygame.init()
Vector2 = pygame.math.Vector2

class Game:
    def __init__(self, algorithm=1, ratio=0.6) -> None:
        self.map = []
        self.ratio = ratio
        COLS = 0
        print(COLS)

        self.build_map()
        self.read_layout()
        print(len(self.map))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption('Ghosts')
        self.algorithm = algorithm
        self.all_sprites = pygame.sprite.Group()
        self.read_layout()
        self.load_icon()
        self.add_ghosts()
    
    def load_icon(self) -> None:
        self.icon = pygame.image.load('icon.jpg').convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (30, 30))
        pygame.display.set_icon(self.icon)

    def run(self) -> None:
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

        sys.exit()
    
    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_layout()
        self.all_sprites.draw(self.screen)
        pygame.display.update()
    
    def build_map(self):
        rows = 0
        cols = 0
        with open('classicMaze.lay', 'r') as file:
            for y, line in enumerate(file):
                rows += 1
                cols = len(line)                    

        self.map = [[Tile() for j in range(rows)] for i in range(cols)]

    def read_layout(self):
        with open("classicMaze.lay", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "%":
                        self.add_wall(x, y)
                    elif char == "*":
                        self.add_tile(x, y)

    
    def draw_layout(self):
        for x in range(COLS):
            for y in range(ROWS):
                if self.map[x][y].is_wall():
                    pygame.draw.rect(self.screen, NAVY, (x*CELL_WIDTH, y*CELL_HEIGHT,
                                                    CELL_WIDTH - 1, CELL_HEIGHT-1), 0, 3)
                elif self.map[x][y].get_colour():
                    pygame.draw.rect(self.screen, self.map[x][y].get_colour(), (x*CELL_WIDTH, y*CELL_HEIGHT,
                                                CELL_WIDTH - 1, CELL_HEIGHT-1), 0, 3)


    def add_ghosts(self):
        ghost1 = GhostAgent([14,15], 'pink', self.map, self.all_sprites, self.algorithm)
        self.all_sprites.add(ghost1)
        ghost2 = GhostAgent([1,1], 'yellow', self.map, self.all_sprites, self.algorithm)
        self.all_sprites.add(ghost2)
        ghost3 = GhostAgent([12,11], 'red', self.map, self.all_sprites, self.algorithm)
        self.all_sprites.add(ghost3)
        ghost4 = GhostAgent([26,26], 'blue', self.map, self.all_sprites, self.algorithm)
        self.all_sprites.add(ghost4)
        ghost5 = GhostAgent([1,1], 'pink', self.map, self.all_sprites, self.algorithm)
        self.all_sprites.add(ghost5)
        ghost6 = GhostAgent([1,1], 'yellow', self.map, self.all_sprites, self.algorithm)
        self.all_sprites.add(ghost6)
        ghost7 = GhostAgent([1,1], 'red', self.map, self.all_sprites, self.algorithm)
        self.all_sprites.add(ghost7)
        ghost8 = GhostAgent([1,8], 'blue', self.map, self.all_sprites, self.algorithm)
        self.all_sprites.add(ghost8)

    def add_wall(self, x,y):
        self.map[x][y] = Tile(wall=True)

    def add_tile(self, x, y):
        colour = random.choices(population=[WHITE, GREY],weights=[self.ratio, 1-self.ratio])
        self.map[x][y] = Tile(colour=colour[0])

class Tile():
    def __init__(self, wall = False, colour=""):
        self.wall = wall
        self.colour = colour
    def is_wall(self) -> bool:
        return self.wall
    def get_colour(self):
        return self.colour