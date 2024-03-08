# File Name: PongCheatMode
# Description: Pong CHEAT MODE current version
# Author: Emily Au (edited by Jamie Zhang)

import random
import pygame


def playCheatGame(player1, player2):
    score1 = 0
    score2 = 0
    winScore = 1
    winner = None
    pygame.init()

    # screen info
    screenInfo = pygame.display.Info()
    WIDTH = screenInfo.current_w
    HEIGHT = screenInfo.current_h
    gameWindow = pygame.display.set_mode((WIDTH,HEIGHT))

    WHITE = (255,255,255)
    YELLOW = (255,235,0)
    OUTLINE = 0

    # ball dimensions
    ballR = WIDTH//60
    ballRSmall = WIDTH//80
    ballX = round(WIDTH/2)
    ballY = round(HEIGHT/2)

    # shift of ball
    shiftX = 10
    shiftY = 10
    shiftMin = 9
    shiftMax = 11

    direction = 1

    # paddle dimensions
    paddleW = int(WIDTH//8)
    paddleH = int(HEIGHT//8)
    MARGIN = 10


    # paddle locations
    paddleX1 = int(WIDTH * 0.1)
    paddleY1 = int((HEIGHT//2) + (paddleH//2))
    paddleX2 = int((WIDTH * 0.9) - paddleW)
    paddleY2 = int((HEIGHT//2) + (paddleH//2))

    # speed of paddle
    speedPaddleX = 8
    speedPaddleY = 8

    # barrier of paddle movement
    barrierLeft = int(WIDTH * 0.4)
    barrierRight = int(WIDTH * 0.6)

    # visuals
    iconP1 = pygame.image.load("../Images/cheat_paddle_P1.png")
    iconP1 = pygame.transform.scale(iconP1,(WIDTH//8, HEIGHT//8))
    iconP2 = pygame.image.load("../Images/cheat_paddle_P2.png")
    iconP2 = pygame.transform.scale(iconP2,(WIDTH//8, HEIGHT//8))
    background = pygame.image.load("../Images/background_space.png")
    background = pygame.transform.scale(background,(WIDTH,HEIGHT))

    # audio
    pygame.mixer.music.load("../Audio/supersaiyanthemeshort.mp3")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops = 0)
    tennisSound = pygame.mixer.Sound("../Audio/TennisSound.wav")
    tennisSound.set_volume(2)


    # time
    BEGIN = pygame.time.get_ticks()
    elapsed = 0
    clock = pygame.time.Clock()
    FPS = 60

    inPlay = True

    # while ball in play and time elapsed less than 10 seconds
    while inPlay and elapsed<10000:

    # seconds elapsed
        elapsed = pygame.time.get_ticks() - BEGIN

    # draws visuals
        gameWindow.blit(background,(0,0))
        gameWindow.blit(iconP1,(paddleX1,paddleY1))
        gameWindow.blit(iconP2,(paddleX2,paddleY2))
        pygame.draw.circle(gameWindow, YELLOW, (ballX, ballY), ballR, OUTLINE)
        pygame.draw.circle(gameWindow, WHITE, (ballX, ballY), ballRSmall, OUTLINE)
        
        pygame.display.update()
        clock.tick(FPS)

        pygame.event.clear()

    # moves ball
        ballX += shiftX
        ballY += shiftY

    # ball collision: P1 paddle

        # top of paddle
        if ballY + ballR in range (paddleY1 - MARGIN, paddleY1 + MARGIN) and ballX in range(paddleX1, paddleX1 + paddleW):
            ballY -= 30
            shiftY = (random.randint(shiftMin,shiftMax)) * -1
            tennisSound.play()

        # bottom of paddle
        if ballY - ballR in range (paddleY1 + paddleH - MARGIN, paddleY1 + paddleH + MARGIN) and ballX in range(paddleX1, paddleX1 + paddleW):
            ballY += 30
            shiftY = (random.randint(shiftMin,shiftMax)) * 1
            tennisSound.play()

        # front of paddle
        if ballX - ballR < paddleX1 + paddleW + MARGIN and ballX - ballR > paddleX1 and ballY in range(paddleY1, paddleY1 + paddleH):
            ballX += 30
            shiftX = (random.randint(shiftMin,shiftMax)) * 1
            tennisSound.play()

    # ball collision: P2 paddle

        # top of paddle
        if ballY + ballR in range (paddleY2 - MARGIN, paddleY2 + MARGIN) and ballX in range(paddleX2, paddleX2 + paddleW):
            ballY -= 30
            shiftY = (random.randint(shiftMin,shiftMax)) * -1
            tennisSound.play()

        # bottom of paddle
        if ballY - ballR in range (paddleY2 + paddleH - MARGIN, paddleY2 + paddleH + MARGIN) and ballX in range(paddleX2, paddleX2 + paddleW):
            ballY += 30
            shiftY = (random.randint(shiftMin,shiftMax)) * 1
            tennisSound.play()

        # front of paddle
        if ballX + ballR < paddleX2 + paddleW and ballX + ballR > paddleX2 - MARGIN and ballY in range(paddleY2, paddleY2 + paddleH):
            
            ballX -= 30
            shiftX = (random.randint(shiftMin,shiftMax)) * -1
            tennisSound.play()

    # ball collision: right side (GAME OVER)
        if ballX + ballR > WIDTH:
            ballX -= 30
            direction =- direction
            shiftX = (random.randint(shiftMin,shiftMax)) * direction
            score1 += 1
            inPlay = False # terminates loop, CAN CHANGE

    # ball collision: left side (GAME OVER)
        if ballX - ballR < 0:
            ballX += 30
            direction =- direction
            shiftX = (random.randint(shiftMin,shiftMax)) * direction
            score2 += 1
            inPlay = False # terminates loop, CAN CHANGE

    # ball collision: top of screen
        if ballY - ballR < 0:
            ballY += 30
            direction =- direction
            shiftY = (random.randint(shiftMin,shiftMax)) * direction

    # ball collision: bottom of screen
        if ballY + ballR > HEIGHT:
            ballY -= 30
            direction =- direction
            shiftY = (random.randint(shiftMin,shiftMax)) * direction

    # generates a True/False list for the status of all keys
        keys = pygame.key.get_pressed()

    # paddle movement: P1

        # w key - move up
        if keys[pygame.K_w] and paddleY1 > 0:
            paddleY1 = paddleY1 - speedPaddleY
        # s key - move down
        if keys[pygame.K_s] and paddleY1 + paddleH < HEIGHT:
            paddleY1 = paddleY1 + speedPaddleY
        # a key - move left
        if keys[pygame.K_a] and paddleX1 > 0:
            paddleX1 = paddleX1 - speedPaddleX
        # d key - move right
        if keys[pygame.K_d] and paddleX1 + paddleW < WIDTH:
            paddleX1 = paddleX1 + speedPaddleX

        # paddle barrier
        if paddleX1 + paddleW > barrierLeft:
            paddleX1 = barrierLeft - paddleW

    # paddle movement: P2

        # up key - move up
        if keys[pygame.K_UP] and paddleY2 > 0:
            paddleY2 = paddleY2 - speedPaddleY
        # down key - move down
        if keys[pygame.K_DOWN] and paddleY2 + paddleH < HEIGHT:
            paddleY2 = paddleY2 + speedPaddleY
        # left key - move left
        if keys[pygame.K_LEFT] and paddleX2 > 0:
            paddleX2 = paddleX2 - speedPaddleX
        # right key - move right
        if keys[pygame.K_RIGHT] and paddleX2 + paddleW < WIDTH:
            paddleX2 = paddleX2 + speedPaddleX

        # paddle barrier
        if paddleX2 < barrierRight:
            paddleX2 = barrierRight

    # determines and returns the winner and sends it back to main game file 
    if score1 > score2:
        winner = player1
    elif score1 < score2:
        winner = player2
    return winner    

# TESTING
#print("winner is:", playCheatGame("player1","player2"))

