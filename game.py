import pygame
import sys
from settings import *
import random

pygame.init()
Vector2 = pygame.math.Vector2

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption('Ghosts')
        self.map = [[Tile() for j in range(ROWS)] for i in range(COLS)]
        self.ghosts = []
        self.read_layout()
        self.load_icon()
        self.all_sprites = pygame.sprite.Group()
        self.add_ghosts()

    
    def load_icon(self):
        self.icon = pygame.image.load('icon.jpg').convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (30, 30))
        pygame.display.set_icon(self.icon)

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
        self.all_sprites.update()
        for ghost in self.ghosts:
            ghost.update()
            pass

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_layout()
        self.all_sprites.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw()
        pygame.display.update()

    
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
                    pygame.draw.rect(self.screen, DARK_BLUE, (x*CELL_WIDTH, y*CELL_HEIGHT,
                                                    CELL_WIDTH - 3, CELL_HEIGHT-3), 0, 3)
                elif self.map[x][y].get_colour():
                    pygame.draw.rect(self.screen, self.map[x][y].get_colour(), (x*CELL_WIDTH, y*CELL_HEIGHT,
                                                CELL_WIDTH - 1, CELL_HEIGHT-1), 0, 2)


    def add_ghosts(self):
        ghost1 = GhostAgent([11,12], self, 'pink')
        self.all_sprites.add(ghost1)
        ghost2 = GhostAgent([16,12], self, 'yellow')
        self.all_sprites.add(ghost2)
        ghost3 = GhostAgent([14,13], self, 'red')
        self.all_sprites.add(ghost3)
        ghost4 = GhostAgent([11,14], self, 'blue')
        self.all_sprites.add(ghost4)

    def add_wall(self, x,y):
        self.map[x][y] = Tile(wall=True)

    def add_tile(self, x, y):
        colour = random.choice([WHITE, GREY])
        self.map[x][y] = Tile(colour=colour)


class Tile():
    def __init__(self, wall = False, colour=""):
        self.wall = wall
        self.colour = colour
    def is_wall(self):
        return self.wall
    def get_colour(self):
        return self.colour

class GhostAgent(pygame.sprite.Sprite):
    def __init__(self, pos, game, colour='pink'):
        pygame.sprite.Sprite.__init__(self)
        self.ratio = 0
        self.pos = pos
        self.game = game
        self.direction = (1,1)
        self.image = pygame.image.load(f'ghost_{colour}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center= (pos[0]*CELL_WIDTH,pos[1]*CELL_HEIGHT)

    def get_next_move(self):
        moves = self.get_possible_actions()
        next_move = random.choice(moves)
        return next_move

    def update(self):
        self.direction = self.get_next_move()
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        self.rect.x += (self.direction[0] * CELL_WIDTH)
        self.rect.y += (self.direction[1] * CELL_HEIGHT)
    
    def get_possible_actions(self):
        possible = []
        x = self.pos[0] + self.direction[0]
        y = self.pos[1] + self.direction[1]
        if not self.game.map[x][y].is_wall():
            return [self.direction]
        for vec in Actions.directions:
            x = self.pos[0] + vec[0]
            y = self.pos[1] + vec[1]
            if not self.game.map[x][y].is_wall():
                possible.append(vec)
        return possible
class Actions:
    """
    A collection of static methods for manipulating move actions.
    """
    # Directions
    directions = [
        # North
        (0, 1),
        # South
        (0, -1),
        #East
        (1, 0),
        # West
        (-1, 0)
    ]
    TOLERANCE = .001