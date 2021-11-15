import pygame
import sys
from settings import *
import random

pygame.init()
vec = pygame.math.Vector2

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption('Ghosts')
        self.load_background()
        self.load_icon()
    
    def load_background(self):
        self.background = pygame.image.load('layout.jpg')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.graph()
    
    def load_icon(self):
        self.icon = pygame.image.load('icon.jpg')
        self.icon = pygame.transform.scale(self.icon, (30, 30))
        pygame.display.set_icon(self.icon)
    
    def load_walls(self):
        pass

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
        pass

    def draw(self):
        pygame.display.update()
        self.screen.blit(self.background, (0,0))

    
    def graph(self):
        self.cell_width = SCREEN_WIDTH//COLS
        self.cell_height = SCREEN_HEIGHT//ROWS
        with open("classicMaze.lay", 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "%":
                        pass
                        pygame.draw.rect(self.background, DARK_BLUE, (x*self.cell_width, y*self.cell_height,
                                                                 self.cell_width, self.cell_height))
                        #self.add_wall(vec(x,y))
                    elif char == "*":
                        colour = random.choice([GREY, BLACK])
                        #self.add_tile(vec(x,y))
                        pygame.draw.rect(self.background, colour, (x*self.cell_width, y*self.cell_height,
                                                                  self.cell_width, self.cell_height))
                
        """
        for x in range(SCREEN_WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, SCREEN_HEIGHT))
        for x in range(SCREEN_HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             (SCREEN_WIDTH, x*self.cell_height))
        """