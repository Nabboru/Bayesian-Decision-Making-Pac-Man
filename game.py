import pygame
import sys
import random
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
from ghosts import GhostAgent
from algorithms import *
from settings import *

# Initiate Pygame module
pygame.init()

class Game:
    """
    
    """
    def __init__(self, algorithm_id, ratio, map_name, n_ghosts, n_games, n_colours) -> None:
        # Building the map
        self.ratio = ratio
        self.n_games = n_games
        self.n_ghosts = n_ghosts
        self.n_colours = n_colours
        self.map_name = map_name
        self.build_map(self.map_name)
        self.algorithm_id = algorithm_id

        SCREEN_HEIGHT = len(self.map[0]) * CELL_HEIGHT
        SCREEN_WIDTH = len(self.map) * CELL_WIDTH

        # Pygame settings
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption('Ghosts')
        self.load_icon()
        self.print_configurations()

        self.start_simulation()
    def print_configurations(self):
        print("\nSimulation Configuration ")
        print("=========================")
        print("Algorithm:", self.algorithm_id)
        print("Map name: ", self.map_name)
        print("Number of runs: ", self.n_games)
        print("Number of colours: ", self.n_colours)
        print("Ratio: ", self.ratio)
        print('Number of agents: ', self.n_ghosts)
    
    def get_algorithm(self) -> BayesianAlgorithm | BenchmarkAlgorithm:
        if self.algorithm_id == 1:
            return BayesianAlgorithm()
        elif self.algorithm_id == 2:
            rows = len(self.map)
            columns = len(self.map[0])
            return BenchmarkAlgorithm(rows, columns, self.n_ghosts)
        
    def start_simulation(self) -> None:
        self.frame = 0
        self.decision = False
        self.set_tiles_colours()
        self.read_layout(self.map_name)
        self.all_sprites = pygame.sprite.Group()
        self.add_ghosts()
        self.colour_count = 0
        self.reset_ghosts = False

    def load_icon(self) -> None:
        self.icon = pygame.image.load('.\images\icon.jpg').convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (30, 30))
        pygame.display.set_icon(self.icon)

    def run(self) -> None:
        total_avg = 0
        accuracies = []
        times = []
        self.count = self.n_games
        while self.count:
            self.start_simulation()
            self.running = True
            self.count -=1 
            while self.running:
                self.game_loop()
            
            accuracy = self.stats()
            total_avg += accuracy
            accuracies.append(accuracy)
            times.append(self.frame)
        
        self.plot_results(times, accuracies)
        pygame.quit()
        sys.exit()

    def game_loop(self) -> None:
        self.frame += 1
        self.events()
        self.update()
        self.draw()          
        self.clock.tick(500)

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.count = 0
        if self.decision and self.n_colours == 2:
            self.running = False
        elif self.decision and self.colour_count > self.n_colours - 2:
            self.running = False
        elif self.decision:
            self.colour_count += 1
            self.reset_ghosts = True
            
    def update(self) -> None:
        self.decision = True
        for s in self.all_sprites:
            s.update()
            if self.reset_ghosts:
                s.reset_algorithm(CCOLOURS[self.colour_count])
            if s.algorithm.decision == -1:
                self.decision = False
            collided_enemies = pygame.sprite.spritecollide(s, self.all_sprites, False, pygame.sprite.collide_circle_ratio(2.0))
            if s in collided_enemies:
                collided_enemies.remove(s)
            for j in collided_enemies:
                s.broadcast(j)
        self.reset_ghosts = False

    def draw(self) -> None:
        self.screen.fill(BLACK)
        self.draw_layout()
        self.all_sprites.draw(self.screen)
        pygame.display.update()

    def stats(self) -> float:
        if self.n_colours == 2:
            decision_count = [0, 0]
            for i in self.all_sprites:
                if i.algorithm.decision == 0:
                    decision_count[0] += 1
                else:
                    decision_count[1] += 1
            avg = (decision_count[1]) / self.n_ghosts
            return avg
        else:
            count = {WHITE: 0, GREY: 0, PINK: 0}
            for i in self.all_sprites:
                count[max(i.algorithm.pcs, key=i.algorithm.pcs.get)] += 1
            avg = count[GREY] / self.n_ghosts
            return avg

    def plot_results(self, times, accuracies):
        x = np.array(times)
        y = np.array(accuracies)
        print('\nResults')
        print('==========')
        print("Average time: ", mean(times))
        print("Average accuracy: ", mean(accuracies))
        plt.scatter(x, y)
        plt.xlabel('Frames', fontsize='12')
        plt.ylabel('Accuracy', fontsize='12')
        plt.show()
            
    def build_map(self, layout) -> None:
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
        colour_tiles = [[]] * self.n_colours
        for i in range(self.n_colours-1):
            colour_ratio = n_tiles * self.ratio[i]
            colour_tiles[i] = [CCOLOURS[i]] * round(colour_ratio)
        colour_ratio = n_tiles * (1 - sum(self.ratio))
        colour_tiles[self.n_colours-1] = [CCOLOURS[self.n_colours-1]] * round(colour_ratio)
        self.colour_list = [item for sublist in colour_tiles for item in sublist]
        random.shuffle(self.colour_list)

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
            ghost = GhostAgent(position, colour, self.map, self.n_ghosts, self.get_algorithm())
            self.all_sprites.add(ghost)

    def add_wall(self, x: int, y:int) -> None:
        self.map[x][y] = Tile(wall=True)

    def add_tile(self, x, y) -> None:
        colour = self.colour_list.pop()
        self.map[x][y] = Tile(colour=colour)

class Tile():
    def __init__(self, wall = False, colour=""):
        self.wall = wall
        self.colour = colour
    def is_wall(self) -> bool:
        return self.wall
    def get_colour(self) -> str:
        return self.colour