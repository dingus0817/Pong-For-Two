#File name: SuperSaiyanTheme.py
#Author: Jamie Zhang

import pygame 
pygame.init()
WIDTH = 1000
HEIGHT = 500
surface = pygame.display.set_mode((WIDTH,HEIGHT))

BLACK = (0,0,0)

pygame.mixer.music.load("superSaiyanThemeshort.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(loops = 0)

for seconds in range(10):
    surface.fill(BLACK)
    pygame.display.update()
    pygame.time.delay(1000)
    
pygame.quit()

    
    

    

