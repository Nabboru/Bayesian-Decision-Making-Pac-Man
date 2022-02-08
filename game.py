from numpy import broadcast
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
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption('Ghosts')
        self.map = [[Tile() for j in range(ROWS)] for i in range(COLS)]
        self.all_sprites = pygame.sprite.Group()
        self.read_layout()
        self.load_icon()
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

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_layout()
        self.all_sprites.draw(self.screen)
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
                    pygame.draw.rect(self.screen, NAVY, (x*CELL_WIDTH, y*CELL_HEIGHT,
                                                    CELL_WIDTH - 1, CELL_HEIGHT-1), 0, 3)
                elif self.map[x][y].get_colour():
                    pygame.draw.rect(self.screen, self.map[x][y].get_colour(), (x*CELL_WIDTH, y*CELL_HEIGHT,
                                                CELL_WIDTH - 1, CELL_HEIGHT-1), 0, 3)


    def add_ghosts(self):
        ghost1 = GhostAgent([11,12], self, 'pink', self.map, self.all_sprites)
        self.all_sprites.add(ghost1)
        ghost2 = GhostAgent([16,12], self, 'yellow', self.map, self.all_sprites)
        self.all_sprites.add(ghost2)
        ghost3 = GhostAgent([14,13], self, 'red', self.map, self.all_sprites)
        self.all_sprites.add(ghost3)
        ghost4 = GhostAgent([11,14], self, 'blue', self.map, self.all_sprites)
        self.all_sprites.add(ghost4)

    def add_wall(self, x,y):
        self.map[x][y] = Tile(wall=True)

    def add_tile(self, x, y):
        colour = random.choices(population=[WHITE, GREY],weights=[0.7, 0.3])
        self.map[x][y] = Tile(colour=colour[0])

class Tile():
    def __init__(self, wall = False, colour=""):
        self.wall = wall
        self.colour = colour
    def is_wall(self):
        return self.wall
    def get_colour(self):
        return self.colour
class GhostAgent(pygame.sprite.Sprite):
    def __init__(self, pos, g, colour='pink', wall_map = None, friends = None):
        pygame.sprite.Sprite.__init__(self)
        self.ratio = 0
        self.pos = pos
        self.direction = (1,1)
        self.colour = colour

        self.friends = friends

        self.map = wall_map
        self.image = pygame.image.load(f'ghost_{colour}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center= (pos[0]*CELL_WIDTH+10,pos[1]*CELL_HEIGHT+10)

        self.alpha = 1
        self.beta = 1
        self.index = 0
        self.decision = -1
        self.observations = {}
        self.s = (28 * 26) / 4
        self.t_comm = 2 * math.log(4 ** 2 / 0.1) * (28 + 26)
        self.phase_1 = self.s
        self.phase_2 = self.s + self.t_comm
        self.stop = False

    def __str__(self) -> str:
        return "Ghost " + self.colour

    def get_next_move(self):
        moves = self.get_possible_actions()
        next_move = random.choice(moves)
        return next_move

    def update(self):
        self.bayesian_algorithm()
    
    def walk(self):
        self.direction = self.get_next_move()
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        self.rect.x += (self.direction[0] * CELL_WIDTH)
        self.rect.y += (self.direction[1] * CELL_HEIGHT)
    
    def get_possible_actions(self):
        possible = []
        x = self.pos[0] + self.direction[0]
        y = self.pos[1] + self.direction[1]
        if not self.map[x][y].is_wall():
            return [self.direction]
        for vec in Actions.directions:
            x = self.pos[0] + vec[0]
            y = self.pos[1] + vec[1]
            if not self.map[x][y].is_wall():
                possible.append(vec)
        return possible
    
    def bayesian_algorithm(self):
        self.walk()
        C = COLOURS[self.map[self.pos[0]][self.pos[1]].get_colour()]
        self.update_ratio(C)
        self.index += 1
        if self.decision == -1:
            p = beta.cdf(0.5, self.alpha, self.beta, loc=0, scale=1)
            if p > 0.99:
                self.decision = 0
            elif (1 - p) > 0.99:
                self.decision = 1
        """
        print(f'\n{self}')
        print(f'alpha: {self.alpha}')
        print(f'beta: {self.beta}')
        print(f'i: {self.index}')        
        """
        print(f'decision: {self.decision}')
    
        if self.decision != -1:
            self.bayes_broadcast(self.index, self.decision)
        else:
            self.bayes_broadcast(self.index, C)   

    def update_ratio(self, observation):
        self.alpha += observation
        self.beta += (1 - observation)

    def bayes_broadcast(self, index, info):
        for s in self.friends.sprites():
            if s != self:
                if abs(s.pos[0] - self.pos[0]) < 2 and abs(s.pos[1] - self.pos[1]) < 2:
                    s.bayes_receive(self.colour, index, info)

    def bayes_receive(self, id, i, info):
        if id in self.observations:
            if self.observations[id] != (i, info):
                self.update_ratio(info)
            print(f'communication from {id} to {self.colour}')
        else:
            self.observations[id] = (i, info)
            self.update_ratio(info)
            print(f'communication from {id} to {self.colour}')

    def bdm_broadcast(self, alpha, beta):
        for s in  game.all_sprites.sprites():
            if s != self:
                if abs(s.pos[0] - self.pos[0]) < 2 and abs(s.pos[1] - self.pos[1]) < 2:
                    s.bdm_receive(self.colour, alpha, beta)

    def bdm_receive(self, id, alpha, beta):
        self.observations[id] = (alpha, beta)

    def benchmark_algorithm(self):
        if self.stop:
            return
        if self.phase_1 > 0:
            self.walk()
            C = COLOURS[game.map[self.pos[0]][self.pos[1]].get_colour()]
            self.update_ratio(C)
            self.phase_1 -= 1
            return
        if self.phase_2 > self.s:
            self.walk()
            self.observations[self.colour] = (self.alpha, self.beta)
            self.bdm_broadcast(self.alpha, self.beta)
            self.phase_2 -= 1
            return
        alpha_t = 0
        beta_t = 0
        for value in self.observations.values():
            alpha_t += value[0]
            beta_t += value[1]
        if beta_t > alpha_t:
            self.decision = 0
        else:
            self.decision = 1
        print(self.decision)
        self.stop = True
    def event():
        pass

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

game = Game()