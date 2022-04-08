import pygame
from settings import *
import random
from scipy.stats import beta
import math
from algorithms import BayesianAlgorithm, BenchmarkAlgorithm

class GhostAgent(pygame.sprite.Sprite):
    def __init__(self, pos, colour='pink', wall_map = None, algorithm = None):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.direction = (0,0)
        self.colour = colour
        self.algorithm = algorithm
        self.map = wall_map
        self.update_colour()


    def __str__(self) -> str:
        return "Ghost " + self.colour

    def get_next_move(self):
        moves = self.get_possible_actions()
        next_move = random.choice(moves)
        return next_move

    def update(self, reset=False):
        if reset:
            self.reset_algorithm()
        self.walk()
        x, y = self.pos
        C = self.map.get_tile_colour(x,y)
        self.algorithm.update(C)
        if self.algorithm.decision != -1 and (self.colour != 'black' or self.colour != 'white'):
            self.update_colour()
    
    def reset_algorithm(self, colour):
        self.algorithm.reset(colour)
        self.update_colour()

    def walk(self):
        self.direction = self.get_next_move()
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        self.rect.x += (self.direction[0] * CELL_WIDTH)
        self.rect.y += (self.direction[1] * CELL_HEIGHT)
    
    def get_possible_actions(self) -> list:
        """_summary_

        Args:
            self (_type_): _description_
            int (_type_): _description_

        Returns:
            _type_: _description_
        """        
        possible = []
        for vec in Actions.directions:
            x = self.pos[0] + vec[0]
            y = self.pos[1] + vec[1]
            if not self.map.is_wall(x,y):
                possible.append(vec)
        return possible
    
    def broadcast(self, ghost: object) -> None:
        """_summary_

        Args:
            ghost (GhostAgent): _description_
        """        
        if isinstance(self.algorithm, BayesianAlgorithm):
            if self.algorithm.decision != -1 and self.algorithm.positive_feedback:
                ghost.bayes_receive(self.algorithm.decision)
            else:
                ghost.bayes_receive(self.algorithm.last_C)
        else:
            ghost.bdm_receive(self, self.algorithm.alpha, self.algorithm.beta)


    def bayes_receive(self, info):
        if info:
            self.algorithm.update_ratio(info)
    
    def bdm_receive(self, id: object, alpha: int, beta: int) -> None:
        """_summary_

        Args:
            id (GhostAgent): _description_
            alpha (int): _description_
            beta (int): _description_
        """        
        self.algorithm.receive_info(id, alpha, beta)

    def update_colour(self) -> None:
        """_summary_
        """        
        if self.algorithm.decision == -1:
            self.image = pygame.image.load(f'.\images\ghost_{self.colour}.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect.center= (self.pos[0]*CELL_WIDTH+10,self.pos[1]*CELL_HEIGHT+10)
        elif self.algorithm.decision == 0:
            self.image = pygame.image.load(f'.\images\ghost_black.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect.center= (self.pos[0]*CELL_WIDTH+10,self.pos[1]*CELL_HEIGHT+10)
        elif self.algorithm.decision == 1:
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