import pygame
from settings import *
import random
from scipy.stats import beta
import math
from algorithms import BayesianAlgorithm, BenchmarkAlgorithm

class GhostAgent(pygame.sprite.Sprite):
    def __init__(self, pos, colour='pink', wall_map = None, friends = None, algorithm_id=1):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.direction = (0,0)
        self.colour = colour
        self.friends = friends
        self.algorithm = None

        self.map = wall_map
        self.image = pygame.image.load(f'.\images\ghost_{colour}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center= (pos[0]*CELL_WIDTH+10,pos[1]*CELL_HEIGHT+10)
        self.observations = {}
        self.index = 0

        if algorithm_id == 1:
            self.algorithm = BayesianAlgorithm()
        else:
            rows = (len(self.map))
            columns = len(self.map[0])
            self.algorithm = BenchmarkAlgorithm(rows, columns)

        self.stop = False
        self.algorithm_id = algorithm_id

    def __str__(self) -> str:
        return "Ghost " + self.colour

    def get_next_move(self):
        moves = self.get_possible_actions()
        next_move = random.choice(moves)
        return next_move

    def update(self):
        if self.algorithm_id == 1:
            self.bayesian_algorithm()
        else:
            self.benchmark_algorithm()

    def walk(self):
        self.direction = self.get_next_move()
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        self.rect.x += (self.direction[0] * CELL_WIDTH)
        self.rect.y += (self.direction[1] * CELL_HEIGHT)
    
    def get_possible_actions(self):
        possible = []
        for vec in Actions.directions:
            x = self.pos[0] + vec[0]
            y = self.pos[1] + vec[1]
            if not self.map[x][y].is_wall():
                possible.append(vec)
        return possible
    
    def bayesian_algorithm(self):
        self.walk()
        C = -1
        if self.algorithm.decision == -1:
            C = COLOURS[self.map[self.pos[0]][self.pos[1]].get_colour()]
            self.algorithm.update(C)

        #print(f'{self.colour} decision: {self.algorithm.decision}')
    
        if self.algorithm.decision != -1:
            self.bayes_broadcast(self.index, self.algorithm.decision)
            self.update_colour()
        else:
            self.bayes_broadcast(self.index, C)

    def bayes_broadcast(self, index, info):
        for s in self.friends.sprites():
            if s != self and isinstance(s, GhostAgent):
                if abs(s.pos[0] - self.pos[0]) < 3 and abs(s.pos[1] - self.pos[1]) < 3:
                    s.bayes_receive(self.colour, index, info)

    def bayes_receive(self, id, i, info):
        if id in self.observations:
            if self.observations[id] != (i, info):
                self.algorithm.update_ratio(info)
        else:
            self.observations[id] = (i, info)
            self.algorithm.update_ratio(info)

    def benchmark_algorithm(self):
        if self.stop:
            return
        self.walk()
        C = COLOURS[self.map[self.pos[0]][self.pos[1]].get_colour()]
        f = self.algorithm.update(C)

        if f:
            alpha = f[0]
            beta = f[1]
            self.bdm_broadcast(alpha, beta)
        
        if self.algorithm.decision != -1:
            print(f'{self.colour} decision: {self.algorithm.decision}')
            self.update_colour()
            self.stop = True
    
    def bdm_broadcast(self, alpha, beta):
        for s in self.friends.sprites():
            if s != self:
                if abs(s.pos[0] - self.pos[0]) < 2 and abs(s.pos[1] - self.pos[1]) < 2:
                    s.bdm_receive(self, alpha, beta)

    def bdm_receive(self, id, alpha, beta):
        self.algorithm.observations[id] = (alpha, beta)


    def update_colour(self):
        if self.algorithm.decision == 0:
            self.image = pygame.image.load(f'.\images\ghost_black.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect.center= (self.pos[0]*CELL_WIDTH+10,self.pos[1]*CELL_HEIGHT+10)
        if self.algorithm.decision == 1:
            self.image = pygame.image.load(f'.\images\ghost_white.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect.center= (self.pos[0]*CELL_WIDTH+10,self.pos[1]*CELL_HEIGHT+10)

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