import pygame
from settings import *
import random
from scipy.stats import beta
import math
from algorithms import BayesianAlgorithm, BenchmarkAlgorithm

class GhostAgent(pygame.sprite.Sprite):
    def __init__(self, pos, colour='pink', wall_map = None, n_ghosts = 0, algorithm_id = 1,graphs =False):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.direction = (0,0)
        self.colour = colour
        self.algorithm = None
        self.graphs = graphs
        self.map = wall_map
        self.image = pygame.image.load(f'.\images\ghost_{colour}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center= (pos[0]*CELL_WIDTH+10,pos[1]*CELL_HEIGHT+10)

        if self.graphs:
            self.algorithm.graphs = True
        if algorithm_id == 1:
            self.algorithm = BayesianAlgorithm()
        else:
            rows = (len(self.map))
            columns = len(self.map[0])
            self.algorithm = BenchmarkAlgorithm(rows, columns, n_ghosts)

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
        C = COLOURS[self.map[self.pos[0]][self.pos[1]].get_colour()]
        self.algorithm.update(C)
        if self.algorithm.decision != -1:
            self.update_colour()

    def broadcast(self, ghost):
        if self.algorithm_id == 1:
            if self.algorithm.decision != -1 and self.algorithm.positive_feedback:
                ghost.bayes_receive(self.algorithm.decision)
            else:
                ghost.bayes_receive(self.algorithm.last_C)

        if self.algorithm_id == 2:
            ghost.bdm_receive(self, self.algorithm.alpha, self.algorithm.beta)


    def bayes_receive(self, info):
        self.algorithm.update_ratio(info)

    def benchmark_algorithm(self):
        if self.stop:
            return
        self.walk()
        C = COLOURS[self.map[self.pos[0]][self.pos[1]].get_colour()]
        self.algorithm.update(C)
        
        if self.algorithm.decision != -1:
            print(f'{self.colour} decision: {self.algorithm.decision}')
            self.update_colour()
            self.stop = True
    
    def bdm_receive(self, id, alpha, beta):
        self.algorithm.receive_info(id, alpha, beta)

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