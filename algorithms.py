
from scipy.stats import beta
import math

class BayesianAlgorithm:
    def __init__(self) -> None:
        self.decision = -1
        self.alpha = 1
        self.beta = 1

    def update(self, C):
        self.update_ratio(C)
        if self.decision == -1:
            p = beta.cdf(0.5, self.alpha+1, self.beta+1, loc=0, scale=1)
            if p > 0.999:
                self.decision = 0
            elif (1 - p) > 0.999:
                self.decision = 1

    def update_ratio(self, observation):
        self.alpha += observation
        self.beta += (1 - observation)

class BenchmarkAlgorithm():
    def __init__(self, rows, columns) -> None:
        self.decision = -1
        self.alpha = 1
        self.beta = 1
        self.s = (rows * columns)
        self.t_comm = 2 * math.log(4 ** 2 / 0.1) * (rows + columns)
        self.phase_1 = self.s
        self.phase_2 = self.s + self.t_comm 
        self.observations = {}
    
    def update(self, C):
        if self.phase_1 > 0:
            self.update_ratio(C)
            self.phase_1 -= 1
            return None

        if self.phase_2 > self.s:
            self.observations[self] = (self.alpha, self.beta)
            self.phase_2 -= 1
            return (self.alpha, self.beta)

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