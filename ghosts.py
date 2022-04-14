import pygame
from settings import *
import random
from algorithms import BayesianAlgorithm
import os

class GhostAgent(pygame.sprite.Sprite):
    """Class representing the agents. It is responsible for its own image and
    movement. It is a subclass of pygame's Sprite.

    """    
    def __init__(self, pos, colour='pink', wall_map = None, algorithm = None):
        """Create GhostAgent object

        Args:
            pos (list[int]): initial position of agent
            colour (str, optional): agent's colour. Defaults to 'pink'.
            wall_map (object, optional): map indicating all tiles. Defaults to None.
            algorithm (object, optional): algorithm. Defaults to None.
        """        
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
        """Return a random move

        Returns:
            set(int): direction
        """        
        moves = self.get_possible_actions()
        next_move = random.choice(moves)
        return next_move

    def update(self, reset=False):
        """Updates the agents. The agent moves, observes the tiles and update its
        algorithm accordingly.

        Args:
            reset (bool, optional): _description_. Defaults to False.
        """        
        if reset:
            self.reset_algorithm()
        self.walk()
        x, y = self.pos
        C = self.map.get_tile_colour(x,y)
        self.algorithm.update(C)
        if self.algorithm.decision != -1 and (self.colour != 'black' or self.colour != 'white'):
            self.update_colour()
    
    def reset_algorithm(self, colour):
        """Reset its own algorithm with a new main colour.

        Args:
            colour (set(str)): rgb value of a colour
        """        
        self.algorithm.reset(colour)
        self.update_colour()

    def walk(self):
        """Walk in the map
        """        
        self.direction = self.get_next_move()
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        self.rect.x += (self.direction[0] * CELL_WIDTH)
        self.rect.y += (self.direction[1] * CELL_HEIGHT)
    
    def get_possible_actions(self) -> list:
        """Returns all possible actions a agent can make.

        Returns:
            list: all possible directions agent can go.
        """        
        possible = []
        for vec in Actions.directions:
            x = self.pos[0] + vec[0]
            y = self.pos[1] + vec[1]
            if not self.map.is_wall(x,y):
                possible.append(vec)
        return possible
    
    def broadcast(self, ghost: object) -> None:
        """Broadcast observation/decision to another agent.

        Args:
            ghost (GhostAgent): other agent
        """        
        if isinstance(self.algorithm, BayesianAlgorithm):
            if self.algorithm.decision != -1 and self.algorithm.positive_feedback:
                ghost.bayes_receive(self.algorithm.decision)
            else:
                ghost.bayes_receive(self.algorithm.last_C)
        else:
            ghost.bdm_receive(self, self.algorithm.alpha, self.algorithm.beta)


    def bayes_receive(self, info):
        """Pass comunicated infomartion to Bayesian algorithm.

        Args:
            info (int): observation or decision
        """        
        if info:
            self.algorithm.update_ratio(info)
    
    def bdm_receive(self, id: object, alpha: int, beta: int) -> None:
        """Pass comunicated infomartion to Benchmark algorithm.

        Args:
            id (GhostAgent): agent that sent the information
            alpha (int): white observations
            beta (int): black observations
        """        
        self.algorithm.receive_info(id, alpha, beta)

    def update_colour(self) -> None:
        """Update agent's own image according to its decision.
        """        
        if self.algorithm.decision == -1:
            image = os.path.join('images', f'ghost_{self.colour}.png')
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect.center= (self.pos[0]*CELL_WIDTH+10,self.pos[1]*CELL_HEIGHT+10)
        elif self.algorithm.decision == 0:
            image = os.path.join('images', 'ghost_black.png')
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect.center= (self.pos[0]*CELL_WIDTH+10,self.pos[1]*CELL_HEIGHT+10)
        elif self.algorithm.decision == 1:
            image = os.path.join('images', 'ghost_white.png')
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_WIDTH, CELL_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect.center= (self.pos[0]*CELL_WIDTH+10,self.pos[1]*CELL_HEIGHT+10)

class Actions:
    """
    A collection of static attributes representing move actions.
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