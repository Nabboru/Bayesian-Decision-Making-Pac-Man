from turtle import color
import pygame
import sys
from settings import *
import random
from scipy.stats import beta
import math
from ghosts import GhostAgent

#Vector2 = pygame.math.Vector2
pygame.init()

class Game:
    def __init__(self, algorithm=1, ratio=0.6, map_name='line', n_ghosts = 50, n_games = 5) -> None:
        # Building the map
        self.ratio = ratio
        self.n_games = n_games
        self.n_ghosts = n_ghosts
        self.map_name = map_name
        self.build_map(self.map_name)

        self.algorithm = algorithm
        SCREEN_HEIGHT = len(self.map[0]) * 24
        SCREEN_WIDTH = len(self.map) * 20 

        # Pygame settings
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption('Ghosts')
        self.load_icon()
        self.start_simulation()

    
    def start_simulation(self):
        self.decision = False
        self.set_tiles_colours()
        self.read_layout(self.map_name)
        self.all_sprites = pygame.sprite.Group()
        #self.add_ghosts()

    def load_icon(self) -> None:
        self.icon = pygame.image.load('.\images\icon.jpg').convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (30, 30))
        pygame.display.set_icon(self.icon)

    def run(self) -> None:
        avg = 0
        self.count = self.n_games
        while self.count:
            self.start_simulation()
            self.running = True
            self.count -=1 
            while self.running:
                self.game_loop()
            
            avg += self.stats()
        print("Final avg:", avg / self.n_games)
        pygame.quit()

        sys.exit()
    def game_loop(self):
        self.events()
        self.update()
        self.draw()          
        self.clock.tick(400)

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.count = 0
        if self.decision:
            return
            self.running = False
    
    def update(self):
        self.decision = True
        for s in self.all_sprites:
            s.update()
            if s.algorithm.decision == -1:
                self.decision = False
        """
        for i in self.all_sprites:
            collided_enemies = pygame.sprite.spritecollide(i, self.all_sprites, False, pygame.sprite.collide_circle_ratio(2.0))
            if i in collided_enemies:
                collided_enemies.remove(i)
            for j in collided_enemies:
                i.broadcast(j)
        """

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_layout()
        self.all_sprites.draw(self.screen)
        pygame.display.update()

    def stats(self):
        decision_count = [0, 0]
        for i in self.all_sprites:
            if i.algorithm.decision == 0:
                decision_count[0] += 1
            else:
                decision_count[1] += 1
        print("Simulation Results")
        print("-" * 10)
        print("Number of black: ", decision_count[0])
        print("Number of white: ", decision_count[1])
        avg = (decision_count[1]) / self.n_ghosts
        print("Average: ", avg)
        print("\n")
        return avg
    
    def build_map(self, layout):
        rows = 0
        cols = 0
        self.tile_list = []
        with open(f'./layouts/{layout}.lay', 'r') as file:
            for y, line in enumerate(file):
                rows += 1
                cols = len(line)
                for x,char in enumerate(line):
                    if char == "*":
                        self.tile_list.append([x, y])

        self.map = [[Tile() for j in range(rows)] for i in range(cols)]
    
    def set_tiles_colours(self):
        n_tiles = len(self.tile_list)
        white_ratio = n_tiles * self.ratio
        black_ratio = n_tiles * (1 -self.ratio)
        white_block = [WHITE] * round(white_ratio)
        black_block = [GREY] * round(black_ratio)
        self.colour_list = white_block + black_block
        random.shuffle(self.colour_list)
        print(len(self.colour_list ))

    def read_layout(self, layout):
        with open(f"./layouts/{layout}.lay", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "%":
                        self.add_wall(x, y)
                    elif char == "*":
                        self.add_tile(x, y)

    def draw_layout(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if self.map[x][y].is_wall():
                    pygame.draw.rect(self.screen, NAVY, 
                        (x*CELL_WIDTH, 
                        y*CELL_HEIGHT, 
                        CELL_WIDTH - 1, 
                        CELL_HEIGHT-1), 0, 3)
                elif self.map[x][y].get_colour():
                    pygame.draw.rect(self.screen, 
                        self.map[x][y].get_colour(), 
                        (x*CELL_WIDTH, y*CELL_HEIGHT,
                        CELL_WIDTH - 1, CELL_HEIGHT-1), 0, 3)


    def add_ghosts(self):
        colours = ['pink', 'yellow', 'red', 'blue']
        for i in range(self.n_ghosts):
            colour = random.choice(colours)
            position = random.choice(self.tile_list)
            ghost = GhostAgent(position, colour, self.map, self.all_sprites, self.algorithm)
            self.all_sprites.add(ghost)

    def add_wall(self, x,y):
        self.map[x][y] = Tile(wall=True)

    def add_tile(self, x, y):
        colour = self.colour_list.pop()
        self.map[x][y] = Tile(colour=colour)

class Tile():
    def __init__(self, wall = False, colour=""):
        self.wall = wall
        self.colour = colour
    def is_wall(self) -> bool:
        return self.wall
    def get_colour(self):
        return self.colour