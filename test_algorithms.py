from algorithms import BayesianAlgorithm, BenchmarkAlgorithm
from ghosts import GhostAgent, Actions
from settings import *
import random
import pygame
from settings import *
import pytest

class TestBayesianAlgorithm():
    @pytest.fixture()
    def algorithm(self):
        return BayesianAlgorithm()

    def test_update(self, algorithm):
        algorithm.update(WHITE)
        assert algorithm.alpha > (algorithm.prior)
        assert algorithm.last_C == 1

    def test_update_other(self,algorithm):
        algorithm.update(BLACK)
        assert algorithm.beta > (algorithm.prior)
        assert algorithm.last_C == 0

    def test_update_decision(self, algorithm):
        for i in range(10):
            algorithm.update(WHITE)
        assert algorithm.decision == 1

    def test_update_decision_black(self, algorithm):
        for i in range(10):
            algorithm.update(BLACK)
        assert algorithm.decision == 0
    
    def test_reset(self, algorithm):
        for i in range(10):
            algorithm.update(BLACK)
        assert algorithm.decision == 0
        algorithm.reset(BLACK)
        assert algorithm.decision == -1
        assert algorithm.alpha == algorithm.prior
        assert algorithm.beta == algorithm.prior
        assert algorithm.main_colour == BLACK
    
    def test_reset_decision(self,algorithm):
        algorithm.reset(BLACK)
        for i in range(10):
            algorithm.update(WHITE)
        assert algorithm.decision == 0
    
    def test_reset_decision_black(self, algorithm):
        algorithm.reset(BLACK)

        for i in range(10):
            algorithm.update(BLACK)
        assert algorithm.decision == 1


class TestBenchmarkAlgorithm():
    @pytest.fixture()
    def algorithm(self):
        return BenchmarkAlgorithm(n_ghosts=25)
    @pytest.fixture()
    def agent(self, algorithm):
        return GhostAgent([0,0], algorithm=algorithm)

    def test_update_ratio_black(self,algorithm):
        algorithm.update_ratio(0)
        assert algorithm.beta > 1

    def test_update_ratio_white(self, algorithm):
        algorithm.update_ratio(1)
        assert algorithm.alpha > 1

    def test_update_white(self, algorithm):
        prior_phase1 = algorithm.phase_1
        algorithm.update(WHITE)
        assert algorithm.alpha > 1

    def test_phase1(self,algorithm):
        prior_phase1 = algorithm.phase_1
        for i in range(prior_phase1):
            algorithm.update(WHITE)
        assert algorithm.alpha == prior_phase1 + 1
        assert algorithm.phase_1 == 0
        prior_observation = algorithm.alpha
        algorithm.update(WHITE)
        assert algorithm.alpha == prior_observation
    
    def test_phase2(self, algorithm):
        prior_phase1 = algorithm.phase_1
        for i in range(prior_phase1):
            algorithm.update(WHITE)
        prior_phase2 = algorithm.phase_2
        algorithm.update(WHITE)
        assert algorithm.phase_2 == prior_phase2 - 1

    def test_update_black(self, algorithm):
        algorithm.update(GREY)
        assert algorithm.beta > 1
    
    def test_receive_info(self, algorithm):
        prior_phase1 = algorithm.phase_1
        algorithm2 = BenchmarkAlgorithm(n_ghosts=25)

        for i in range(prior_phase1):
            algorithm2.update(WHITE)

        for i in range(prior_phase1):
            algorithm.update(GREY)
        
        
        