
from scipy.stats import beta
import math
import matplotlib.pyplot as plt
import numpy as np

class BayesianAlgorithm:
    def __init__(self, posterior= 0.99, prior = 1, positive_feedback = True) -> None:
        self.decision = -1
        self.alpha = prior
        self.beta = prior
        self.count = 0
        self.graphs = False
        self.last_C = None
        self.positive_feedback = positive_feedback
        self.posterior = posterior

    def update(self, C):
        self.last_C = C
        self.update_ratio(C)
        if self.decision == -1:
            p = beta.cdf(0.5, self.alpha, self.beta, loc=0, scale=1)
            if p > self.posterior:
                self.decision = 0
            elif (1 - p) > self.posterior:
                self.decision = 1

    def update_ratio(self, observation):
        self.alpha += observation
        self.beta += (1 - observation)

class BenchmarkAlgorithm():
    def __init__(self, rows, columns, n_ghosts) -> None:
        self.decision = -1
        self.alpha = 1
        self.beta = 1
        self.s = 4*0.52*(1-0.52)*0.729 / 0.04
        self.t_comm = 2 * math.log(n_ghosts ** 2 / 0.1) * (1240)
        self.phase_1 = self.s / n_ghosts
        self.phase_2 = self.s + self.t_comm 
        self.observations = {}
    
    def update(self, C):
        if self.phase_1 > 0:
            self.update_ratio(C)
            self.phase_1 -= 1
            return

        if self.phase_2 > self.s:
            self.observations[self] = (self.alpha, self.beta)
            self.phase_2 -= 1

        alpha_t = 0
        beta_t = 0
        for value in self.observations.values():
            alpha_t += value[0]
            beta_t += value[1]
        if beta_t > alpha_t:
            self.decision = 0
        else:
            self.decision = 1
        
    def update_ratio(self, observation):
        self.alpha += observation
        self.beta += (1 - observation)
    
    def receive_info(self, id, alpha, beta):
        if self.phase_1 <= 0:
            self.observations[id] = (alpha, beta)
"""
def plot(a,b,count):

    x = np.linspace(beta.ppf(0.01, a, b),beta.ppf(0.99, a, b), 100)

    fig = plt.figure(figsize=(7,7))
    plt.xlim(0, 1)
    plt.plot(x, beta.pdf(x, a, b), 'r-')
    plt.title('Beta Distribution', fontsize='12')
    plt.xlabel('Values of Random Variable X (0, 1)', fontsize='12')
    plt.ylabel('Probability', fontsize='12')
    fig.savefig(f'fig{count}.png')
"""