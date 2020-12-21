import pygame
import random


WIDTH = 360
HEIGHT = 480
FPS = 30
#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

running = True

while running:

    clock.tick(FPS)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
   
    screen.fill(BLACK)
    #keep loop running at right speed
    pygame.display.flip()

pygame.quit()
    
    
    
    
    
    
    
    
    