import pygame
import random    
from pygame. constants import QUIT, K_s, K_w, K_a, K_d
from os import listdir

#general\\\\\\\\\\\\\\\\\\\\\\\\\\\
pygame.init()

FPS = pygame.time.Clock()

screen = width, heigth = 1720, 1000

font = pygame.font.SysFont('Verdana', 20)
#general///////////////////////////

#colour_list\\\\\\\\\
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 0, 255
BLUE = 0, 255, 0
#colour_list/////////

main_surface = pygame.display.set_mode(screen)