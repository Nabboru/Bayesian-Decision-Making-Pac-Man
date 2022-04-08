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
    def __init__(self, algorithm_id:int, ratio: list[float], map_name:str, n_ghosts:int, n_games, n_colours) -> None:
        """Create game object

        Args:
            algorithm_id (int): The algorithm id.
                1 - Bayesian algorithm
                2 - Benchmark algorithm
            ratio (list[float]): List representing the ratios of colours. 
                This list should have the lenght n-1 where n is the number of colours
            map_name (str): Name of text file that represents the map
            n_ghosts (int): Number of agents
            n_games (int): Number of simulations
            n_colours (int): Number of colours tiles will be coloured with
        """        
        self.ratio = ratio
        self.n_games = n_games
        self.n_ghosts = n_ghosts
        self.n_colours = n_colours
        self.map_name = map_name
        self.map = Map(map_name, ratio)
        self.algorithm_id = algorithm_id

        # Building the map
        cols, rows = self.map.size()
        SCREEN_WIDTH = cols * CELL_WIDTH
        SCREEN_HEIGHT = rows * CELL_HEIGHT

        # Pygame settings
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption('Ghosts')
        self.load_icon()

        # Start simulation
        self.print_configurations()
        #self.start_simulation()
        
    def print_configurations(self) -> None:
        """ Prints information about the simulation
        """        
        print("\nSimulation Configuration ")
        print("=========================")
        print("Algorithm:", self.get_algorithm())
        print("Map name: ", self.map_name)
        print("Number of runs: ", self.n_games)
        print("Number of colours: ", self.n_colours)
        print("Ratio: ", self.ratio)
        print('Number of agents: ', self.n_ghosts)
    
    def get_algorithm(self) -> BayesianAlgorithm | BenchmarkAlgorithm:
        """Get algorithm according to its id

        Returns:
            BayesianAlgorithm | BenchmarkAlgorithm: return algorithm object
        """        
        if self.algorithm_id == 1:
            return BayesianAlgorithm()
        elif self.algorithm_id == 2:
            return BenchmarkAlgorithm(self.n_ghosts)
        
    def start_simulation(self) -> None:
        """Start simulation. It set the map colours and create agents.
        """        
        self.frame = 0
        self.decision = False
        self.map.reset_colours()
        self.all_sprites = pygame.sprite.Group()
        self.add_ghosts()
        self.colour_count = 0
        self.reset_ghosts = False

    def load_icon(self) -> None:
        """Load icon image
        """        
        self.icon = pygame.image.load('.\images\icon.jpg').convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (30, 30))
        pygame.display.set_icon(self.icon)

    def run(self) -> None:
        """Runs the application.
        """        
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
            
            accuracy = self.get_average_accuracy()
            total_avg += accuracy
            accuracies.append(accuracy)
            times.append(self.frame)
            print('Simulation',len(times), 'has ended')
        
        self.plot_results(times, accuracies)
        pygame.quit()
        sys.exit()

    def game_loop(self) -> None:
        """ 
        Runs the game loop.
        """
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
        """
        Update all agents. If all agents have made a decision, the game is reset 
        and the next simulation starts. In an environment where there are more 
        than 2 colours, if all agents have made a decision the algorihtm is reset.
        Check if they are close to other agents so they can communicate.
        """        
        self.decision = True
        for s in self.all_sprites:
            s.update()
            if self.reset_ghosts:
                s.reset_algorithm(COLOURS[self.colour_count])
            if s.algorithm.decision == -1:
                self.decision = False
            collided_enemies = pygame.sprite.spritecollide(s, self.all_sprites, False, pygame.sprite.collide_circle_ratio(2.0))
            if s in collided_enemies:
                collided_enemies.remove(s)
            for j in collided_enemies:
                s.broadcast(j)
        self.reset_ghosts = False

    def draw(self) -> None:
        """
        Draws the map and the agents into the screen
        """        
        self.screen.fill(BLACK)
        self.draw_layout()
        self.all_sprites.draw(self.screen)
        pygame.display.update()

    def get_average_accuracy(self) -> float:
        """
        Get all decisions of agents and calculate the average correctness of
        those decisions.

        Returns:
            float: average accuracy
        """        
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
            count = {WHITE: 0, GREY: 0, CORAL: 0}
            for i in self.all_sprites:
                count[max(i.algorithm.pcs, key=i.algorithm.pcs.get)] += 1
            avg = count[WHITE] / self.n_ghosts
            return avg

    def plot_results(self, times, accuracies) -> None:
        """Plot the results of all simulations

        Args:
            times (list[int]): total time of each run
            accuracies (list[float]): average accuracy of each run
        """        
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

    def draw_layout(self) -> None:
        """
        Draw the map into the screen
        """        
        rows, columns = self.map.size()
        for x in range(rows):
            for y in range(columns):
                if self.map.is_wall(x,y):
                    pygame.draw.rect(self.screen, NAVY, 
                        (x*CELL_WIDTH, y*CELL_HEIGHT, 
                        CELL_WIDTH - 1, CELL_HEIGHT-1), 0, 3)
                elif self.map.is_tile(x,y):
                        pygame.draw.rect(self.screen, 
                            self.map.get_tile_colour(x,y),
                            (x*CELL_WIDTH, y*CELL_HEIGHT,
                            CELL_WIDTH - 1, CELL_HEIGHT-1), 0, 3)

    def add_ghosts(self):
        """
        Create ghosts objects and add them to a SpriteGroup
        """        
        for i in range(self.n_ghosts):
            colour = random.choice(AGENTS_COLOURS)
            position = random.choice(self.map.tile_list)
            ghost = GhostAgent(position, colour, self.map, self.get_algorithm())
            self.all_sprites.add(ghost)

class Map():

    def __init__(self, map_name, ratio) -> None:
        self.grid = []
        self.build_map(map_name)
        self.set_tiles_colours(ratio)
        self.create_tiles_walls(map_name)
        self.ratio = ratio
        self.map_name = map_name
    
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
        self.grid = [[Tile() for j in range(rows)] for i in range(cols)]

    def create_tiles_walls(self, layout):
        with open(f'./layouts/{layout}.lay', 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "%":
                        self.add_wall(x, y)
                    elif char == "*":
                        self.add_tile(x, y)

    def reset_colours(self):
        self.set_tiles_colours(self.ratio)
        self.create_tiles_walls(self.map_name)

    def set_tiles_colours(self, ratio):
        n_tiles = len(self.tile_list)
        n_colours = len(ratio) + 1
        colour_tiles = [[]] * n_colours
        for i in range(n_colours-1):
            colour_ratio = n_tiles * ratio[i]
            colour_tiles[i] = [COLOURS[i]] * round(colour_ratio)
        colour_ratio = n_tiles * (1 - sum(ratio))
        colour_tiles[n_colours-1] = [COLOURS[n_colours-1]] * round(colour_ratio)
        self.colour_list = [item for sublist in colour_tiles for item in sublist]
        random.shuffle(self.colour_list)
    
    def add_wall(self, x: int, y:int) -> None:
        self.grid[x][y] = Tile(wall=True)

    def add_tile(self, x, y) -> None:
        colour = self.colour_list.pop()
        self.grid[x][y] = Tile(colour=colour)
    
    def size(self):
        return len(self.grid), len(self.grid[0])
    
    def is_wall(self,x,y):
        return self.grid[x][y].is_wall()
    
    def is_tile(self, x, y) -> bool:
        if self.grid[x][y].get_colour():
            return True
        return False

    def get_tile_colour(self,x,y):
        return self.grid[x][y].get_colour()

class Tile():
    def __init__(self, wall = False, colour=None):
        self.wall = wall
        self.colour = colour
    def is_wall(self) -> bool:
        return self.wall
    def get_colour(self) -> str:
        return self.colour