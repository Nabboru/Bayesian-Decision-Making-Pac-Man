import pygame
import sys
from settings import *
import random

pygame.init()
vec = pygame.math.Vector2

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption('Ghosts')
        self.load_background()
        self.load_icon()
        self.walls = ()
        self.tiles = []
        self.ghosts = ()
    
    def load_background(self):
        #self.background = pygame.image.load('layout.jpg')
        #self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.graph()
    
    def load_icon(self):
        self.icon = pygame.image.load('icon.jpg')
        self.icon = pygame.transform.scale(self.icon, (30, 30))
        pygame.display.set_icon(self.icon)
    
    def load_walls(self):
        pass

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

        sys.exit()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        pass

    def draw(self):
        pygame.display.update()
    
    def graph(self):
        self.cell_width = SCREEN_WIDTH//COLS
        self.cell_height = SCREEN_HEIGHT//ROWS
        with open("classicMaze.lay", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "%":
                        pygame.draw.rect(self.screen, DARK_BLUE, (x*self.cell_width, y*self.cell_height,
                                                                 self.cell_width, self.cell_height))
                        self.walls.append(vec(x, y))
                    elif char == "*":
                        colour = random.choice([WHITE, GREY])
                        pygame.draw.rect(self.screen, colour, (x*self.cell_width, y*self.cell_height,
                                                                  self.cell_width, self.cell_height))
                        self.tiles[vec(x, y)] = colour
                    elif char == "G":
                        self.add_ghosts()

    def add_ghosts(self):
        pass

class GhostAgent():
    def __init__(self, index):
        self.index = index
    def get_position(self):
        pass
    def get_legal_action(self):
        pass
    def get_direction(self):
        pass

class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {NORTH: WEST,
            SOUTH: EAST,
            EAST:  NORTH,
            WEST:  SOUTH,
            STOP:  STOP}

    RIGHT = dict([(y,x) for x, y in LEFT.items()])

    REVERSE = {NORTH: SOUTH,
               SOUTH: NORTH,
               EAST: WEST,
               WEST: EAST,
               STOP: STOP}
class Actions:
    """
    A collection of static methods for manipulating move actions.
    """
    # Directions
    directions = {Directions.NORTH: (0, 1),
                   Directions.SOUTH: (0, -1),
                   Directions.EAST:  (1, 0),
                   Directions.WEST:  (-1, 0),
                   Directions.STOP:  (0, 0)}

    directionsAsList = directions.items()

    TOLERANCE = .001

    def get_possible_actions(ghost, walls):
        possible = []
        x, y = ghost.get_position()
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int)  > Actions.TOLERANCE):
            return [ghost.get_direction()]

        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y]: possible.append(dir)

        return possible
    getPossibleActions = staticmethod(get_possible_actions)
