
from scipy.stats import beta
import math
import matplotlib.pyplot as plt
import numpy as np
from settings import *

class BayesianAlgorithm:
    """
    Class that represents the Bayesian algorithm
    """ 
    def __init__(self, posterior= 0.99, prior = 1, positive_feedback = True, main_colour=WHITE) -> None:
        """ Create Bayesian Algorithm object
        Args:
            posterior (float, optional): the credible threshold which determines
                if the agents has collected enough samples to make a decision.
                Defaults to 0.99.
            prior (int, optional): the initial value of alpha and beta.
                It represents the prior belief of alpha and beta.
                Defaults to 1.
            positive_feedback (bool, optional): controls if agent broadcast the 
                decision. Defaults to True.
            main_colour (set(int), optional): the colour seen as success in a 
                beta model. Defaults to WHITE.
        """        
        self.decision = -1
        self.prior = prior
        self.alpha = prior
        self.beta = prior
        self.last_C = None
        self.positive_feedback = positive_feedback
        self.posterior = posterior
        self.main_colour = main_colour
        self.pcs = {}
    
    def reset(self, colour):
        """Resets the algorithm's attribuates to its initial values and set
        a new main colour. 

        Args:
            colour (set(int)): RGB values of the colour
        """        
        self.decision = -1
        self.alpha = self.prior
        self.beta = self.prior
        self.last_C = None
        self.main_colour = colour

    def update(self, observation):
        """Update the agent's observations and check if the credible threshold has
        been overcame by the beta model.
        Args:
            observation (set(int)): RGB colours of the observed tile
        """        
        C = 0
        if observation == self.main_colour:
            C = 1
        self.last_C = C
        self.alpha += C
        self.beta += (1 - C)        
        if self.decision == -1:
            p = beta.cdf(0.5, self.alpha, self.beta, loc=0, scale=1)
            if p > self.posterior:
                self.decision = 0
                self.pcs[self.main_colour] = (1 -p)
            elif (1 - p) > self.posterior:
                self.decision = 1
                self.pcs[self.main_colour] = (1 -p)

    def update_ratio(self, observation:int):
        """Update alpha and beta with the observation.
        Observations are 1 if the tile colour is the 'success' colour or
        0 if the tile is any other colour

        Args:
            observation (int): observations are either 0 or 1
        """        
        self.alpha += observation
        self.beta += (1 - observation)

    def __repr__(self) -> str:
        return "Bayesian Algorithm"

class BenchmarkAlgorithm():
    def __init__(self, n_ghosts:int) -> None:
        """_summary_

        Args:
            n_ghosts (int): _description_
        """        
        self.decision = -1
        self.alpha = 1
        self.beta = 1
        self.s = ((4*0.52*0.48*(Z_SCORE**2)) / (EPSILON**2)) / n_ghosts
        self.t_comm = 2 * math.log((n_ghosts ** 2) / 0.1) * (1240)
        self.phase_1 = round(self.s / n_ghosts)
        self.phase_2 = round(self.s + self.t_comm)
        self.observations = {}
        self.colour_map = {GREY: 0, WHITE:1}
    
    def update(self, observation) -> None:
        """

        Args:
            observation (tuple[int]): Tuple representing RGB colours
        """        
        C = self.colour_map[observation]
        if self.phase_1 > 0:
            self.update_ratio(C)
            self.phase_1 -= 1
            return

        if self.phase_2 > self.s:
            self.observations[self] = (self.alpha, self.beta)
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
        
    def update_ratio(self, observation: int) -> None:
        """Updates the Beta model with a new observation
        Args:
            observation (int): Either 1 or 0. Where 1 represents the current 
                main colour and 0 any other colour
        """        
        self.alpha += observation
        self.beta += (1 - observation)
    
    def receive_info(self, id:object, alpha: int, beta: int):
        """Add observations by other agents to dictonary

        Args:
            id (GhostAgent): another agent
            alpha (int): the other agent's alpha values
            beta (int): the other agent's beta values
        """        
        if self.phase_1 <= 0:
            self.observations[id] = (alpha, beta)

    def __repr__(self) -> str:
        return "Benchmark Algorithm"