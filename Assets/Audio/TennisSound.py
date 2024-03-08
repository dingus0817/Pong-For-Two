#File name: TennisSound.py
#Author: Jamie Zhang

import pygame
pygame.init()
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH,HEIGHT))

WHITE = (255,255,255)

tennisSound = pygame.mixer.Sound("TennisSound.wav")
tennisSound.set_volume(2)

running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            tennisSound.play()
    pygame.display.update()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
pygame.quit()
            
        
