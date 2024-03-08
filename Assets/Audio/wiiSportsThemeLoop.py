#File name: wiiSportsThemeLoop.py
#Author: Jamie Zhang

import pygame 
pygame.init()
WIDTH = 1000
HEIGHT = 500
surface = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.mixer.music.load("wiiSportsThemeLoop.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(loops = -1)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    
pygame.quit()
