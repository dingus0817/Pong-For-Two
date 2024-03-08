#File name: PongMainGame.py
#Description: This is the program for the main game
#Author: Vienna Liu, Jamie Zhang

import pygame
import time
import random
pygame.init()
# ------------------ get screen info so it fits any computer screen size
screenInfo = pygame.display.Info()
WIDTH = screenInfo.current_w 
HEIGHT = screenInfo.current_h
screen = pygame.display.set_mode((WIDTH,HEIGHT))
# ------------------------------

# loaded images/audio
tennis = pygame.image.load("../Images/mainMenuBackground.png")
tennis = pygame.transform.scale(tennis,(WIDTH,HEIGHT))
selectBox = pygame.image.load("../Images/selectBox.png")
woodPlank = pygame.image.load("../Images/plank.png")
woodPlank = pygame.transform.scale(woodPlank,(WIDTH//4,HEIGHT//4))
sunny = pygame.image.load("../Images/background_sunny.png")
sunny = pygame.transform.scale(sunny,(WIDTH,HEIGHT))
beach = pygame.image.load("../Images/background_beach.png")
beach = pygame.transform.scale(beach,(WIDTH,HEIGHT))
volcano = pygame.image.load("../Images/background_volcano.png")
volcano = pygame.transform.scale(volcano,(WIDTH,HEIGHT))
sky = pygame.image.load("../Images/background_sky.png")
sky = pygame.transform.scale(sky,(WIDTH,HEIGHT))
foot = pygame.image.load("../Images/background_foot.png")
foot = pygame.transform.scale(foot,(WIDTH,HEIGHT))
pygame.mixer.music.load("../Audio/wiiSportsThemeLoop.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(loops = -1)
tennisSound = pygame.mixer.Sound("../Audio/TennisSound.wav")
tennisSound.set_volume(2)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)
GREEN = (100,210,50)

# --------------- ## VIENNA LIU ## ----------------#

# Classes
class Option: # class for text options
    hovered = False #Is mouse over this button?
    
    def __init__(self, text, pos): #Initialize properties
        self.text = text
        self.pos = pos
        self.set_rect() 
        self.draw() #Draw button
            
    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect) #Overlay button onto screen
        
    def set_rend(self):
        self.rend = clickFONT.render(self.text, True, self.get_color()) #Render text
        
    def get_color(self): #Determine the colour depending if mouse is hovering or not
        if self.hovered:
            return (RED)
        else:
            return (BLUE)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect() #Get the rect object properties from button
        self.rect.topleft = self.pos #Set position of rect object to own position

def init(w, h):
    global WHITE
    global GREEN
    global BLACK
    global INIT_SPEED
    global MARGIN
    global SPEED_RANGE
    global MAX_SPEED_MULT
    global GRAVITY
    global MAX_GRAVITY
    global FEEDBACK_STEPS
    global HIT_ENERGY
    global MAX_ENERGY
    global BALL_R
    global PADDLE_LENGTH
    global PADDLE_Y
    global PADDLE_SPEED
    global CENTRE_POS
    global ballX
    global ballY
    global paddle1X
    global paddle2X
    global feedback
    global shift
    global score1
    global score2
    global WIDTH
    global HEIGHT

    WIDTH = w
    HEIGHT = h
    
# ------------------------- CONSTANTS
# Speed
INIT_SPEED = [WIDTH/250, -HEIGHT/88] #Initial movement speed. FIRST value should be the average of SPEED_RANGE. SECOND value should be equal to negative HIT_ENERGY.
MAX_SPEED_MULT = [2,3,5] #Maximum speed is x times faster than regular speed
DIFF_MULT = MAX_SPEED_MULT[1]
MARGIN = WIDTH / 250 #Margin for collisions
SPEED_RANGE = ((WIDTH//384), (WIDTH//240)) #Speed is randomly determined between the speed range
# Gravity
GRAVITY = (HEIGHT/540)  #Gravity
MAX_GRAVITY = (HEIGHT/300)  #Maximum gravity.
FEEDBACK_STEPS = 12 #Number of hits it takes to reach max speed
HIT_ENERGY = HEIGHT/88   #Initial speed of ball when it bounces back up
MAX_ENERGY = HEIGHT/43   #Maximum vertical energy
# Ball and paddle properties
BALL_R = WIDTH/76.8 
PADDLE_LENGTH = WIDTH/8 
PADDLE_Y = HEIGHT * 0.73 
PADDLE_SPEED = WIDTH/100 
CENTRE_POS = WIDTH / 2 #Centre position, paddles can't cross this boundary

# --------------------- VARIABLES
ballX = WIDTH / 2 #Stores the coordinates of the ball
ballY = HEIGHT * 0.6
paddle1X = (WIDTH * 0.4) - PADDLE_LENGTH #Stores the coordinates of the paddles
paddle2X = WIDTH * 0.6
feedback = 0 #Feedback loop, causing the ball to incrementally get faster and faster
shift = INIT_SPEED * 5 
score1 = 0
score2 = 0

# ---------------- FUNCTIONS
#Detect when the ball collides with a paddle. Returns T/F
def paddleHit():
    if(ballY > (PADDLE_Y - (BALL_R + MARGIN)) and ballY < (PADDLE_Y + (BALL_R + MARGIN))): #Check if ball is low enough to hit the paddles
        if(ballX > paddle1X - (BALL_R + MARGIN) and ballX < (paddle1X + PADDLE_LENGTH + BALL_R + MARGIN)): #Is the X of the ball correct?
            return True
        elif(ballX > paddle2X - (BALL_R + MARGIN) and ballX < (paddle2X + PADDLE_LENGTH + BALL_R + MARGIN)): #Is the X of the ball correct?
            return True
        else:
            return False
    else:
        return False
    
#Calculates the vertical, horizontal speed of the ball, as well as its gravity
def calcEnergy():
    speed = HIT_ENERGY #Set to base energy
    speed += (MAX_ENERGY - HIT_ENERGY) * (feedback / FEEDBACK_STEPS) #Add feedback
    speed *= random.randint(8, 12) / 10 #Add slight variation in energy
    return -speed
def calcSpeed():
    speed = SPEED_RANGE[0] + (
        (SPEED_RANGE[0] * DIFF_MULT) - SPEED_RANGE[0]) * (feedback / FEEDBACK_STEPS), SPEED_RANGE[1] + ((SPEED_RANGE[1] * DIFF_MULT) - SPEED_RANGE[1]) * (feedback / FEEDBACK_STEPS) #Calculate speed range
    speed = random.randint(int(speed[0]), int(speed[1])) #Choose random speed within range
    speed *= (shift[0] / abs(shift[0])) #Make sure we keep going in the same direction
    return speed
def calcGrav():
    gravity = GRAVITY #Set to base gravity
    gravity += (MAX_GRAVITY - GRAVITY) * (feedback / FEEDBACK_STEPS) #Feedback
    gravity /= 10 #Scale down
    return gravity

#Visualizes everything
def drawScreen(screen):
    pygame.draw.circle(screen, GREEN, (ballX, ballY), BALL_R) #Draw ball
    pygame.draw.line(screen, RED, (paddle1X, PADDLE_Y + 10), (paddle1X + PADDLE_LENGTH, PADDLE_Y + 10), 30) #Left paddle
    pygame.draw.line(screen, BLUE, (paddle2X, PADDLE_Y + 10), (paddle2X + PADDLE_LENGTH, PADDLE_Y + 10), 30) #Right paddle
    
#Handles the general ball movement
def ballUpdate():
    global shift
    global ballX
    global ballY
    global feedback
    global score1
    global score2
    
    shift = [shift[0], shift[1] + calcGrav()] #Simulate gravity
    ballX += shift[0] #Move the ball
    ballY += shift[1]
    
    if(paddleHit()): #If hit the paddle, bounce back up
        ballY = PADDLE_Y - (BALL_R + MARGIN) #Make sure we don't hit multiple times, teleports ball to slightly above the paddle
        shift = [calcSpeed(), calcEnergy()] #Bounce
        if(feedback < FEEDBACK_STEPS): feedback += 1 #Increment feedback loop
        tennisSound.play()
    
    if(ballX > (WIDTH - (BALL_R + MARGIN)) or ballX < (MARGIN + BALL_R)): #If hit a side, reverse horizontal direction
        shift[0] *= -1
    if(ballY > (HEIGHT - (BALL_R + (HEIGHT//5)))): #Hit ground, player loses
        if(ballX < CENTRE_POS):
            playerLose(-1)
            score2 = score2 + 1
        if(ballX > CENTRE_POS):
            playerLose(1)
            score1 = score1 + 1
    if(ballY < (MARGIN + BALL_R)): #If hit the ceiling, immediately lose energy
        shift[1] = 1
        
#Handles the paddle controls
def paddleControl():
    global paddle1X
    global paddle2X
    global keys #idk why I have to define it as a global. normally variables that are only used inside the function don't need to, but this one does. weird.
    
    pygame.event.clear()
    keys = pygame.key.get_pressed()

    if(keys[pygame.K_a]): # left paddle: go right or left
        paddle1X -= PADDLE_SPEED
    elif(keys[pygame.K_d]):
        paddle1X += PADDLE_SPEED
    if(keys[pygame.K_RIGHT]): #right paddle: go right or left
        paddle2X += PADDLE_SPEED
    elif(keys[pygame.K_LEFT]):
        paddle2X -= PADDLE_SPEED

    #Keep paddles within bounds
    if(paddle1X > CENTRE_POS - PADDLE_LENGTH): #Left paddle hits centre
        paddle1X -= PADDLE_SPEED
    elif(paddle1X < 0): #Left paddle hits left side
        paddle1X += PADDLE_SPEED
    if(paddle2X < CENTRE_POS): #Right paddle hits centre
        paddle2X += PADDLE_SPEED
    elif(paddle2X > WIDTH - PADDLE_LENGTH): #Right paddle hits right side
        paddle2X -= PADDLE_SPEED

#Ball hits the ground, end round
def playerLose(player): #player = 1 means right player lost, player = -1 means left lost
    global ballX
    global ballY
    global shift
    global feedback
    global paddle1X
    global paddle2X

    #Reset ball
    ballX = CENTRE_POS
    ballY = HEIGHT * 0.6
    shift = [0, 0]
    feedback = 0
    paddle1X = (WIDTH * 0.4) - PADDLE_LENGTH
    paddle2X = WIDTH * 0.6

    shift = [INIT_SPEED[0] * -player, INIT_SPEED[1]] #Shoot ball out, going in the direction of the player that just won

# ----------------------------------------------- #

# ------------------ ## JAMIE ZHANG ## -------------------- #
                  
# fonts used
clickFONT = pygame.font.SysFont("Courier New",int(WIDTH//19.2))
titleFont = pygame.font.SysFont("Times", int(WIDTH//10))
regularFont = pygame.font.SysFont("Times",int(WIDTH//18))

# lists of clickable text
startOptions = [
    (Option("PLAY", (WIDTH//2.28,HEIGHT//1.8))),(
        Option("SETTINGS", (WIDTH//2.66,HEIGHT//1.35))),(
            Option("QUIT",(WIDTH//1.15,HEIGHT//1.1)))] 
settingsOptions = [
    Option("EASY",(WIDTH//10,HEIGHT//5)),(
        Option("MEDIUM",(WIDTH//10,HEIGHT//3.33))),(
            Option("HARD",(WIDTH//10,HEIGHT//2.5))),(
                Option("DEFAULT",(WIDTH//80,HEIGHT//1.5))),(
                    Option("BEACH",(WIDTH//3.8,HEIGHT//1.5))),(
                        Option("VOLCANO",(WIDTH//2.2,HEIGHT//1.5))),(
                            Option("SKY",(WIDTH//1.4,HEIGHT//1.5))),(
                                Option("FOOT",(WIDTH//1.2,HEIGHT//1.5))),(
                                    Option("<-- MAIN MENU",(WIDTH//50,HEIGHT//1.1)))]
speedSelectPos = [(WIDTH//10,HEIGHT//5),(WIDTH//10,HEIGHT//3.33),(WIDTH//10,HEIGHT//2.5)]
backgroundSelectPos = [
    (WIDTH//80,HEIGHT//1.5),(
        WIDTH//3.8,HEIGHT//1.5),(
            WIDTH//2.2,HEIGHT//1.5),(
                WIDTH//1.4,HEIGHT//1.5),(
                    WIDTH//1.2,HEIGHT//1.5)]
doneButton = [Option("DONE",(WIDTH//1.6,HEIGHT//1.5))]
postGameOptions = [Option("PLAY AGAIN",(WIDTH//10,HEIGHT//1.7)),Option("MAIN MENU",(WIDTH//1.6,HEIGHT//1.7))]

# determining the select box position and dimensions
defaultSpeed = speedSelectPos[1]
defaultSpeedWidth = settingsOptions[1].rend.get_rect()[2]
defaultSpeedHeight = settingsOptions[1].rend.get_rect()[3]
defaultBackground = backgroundSelectPos[0]
defaultBackgroundW = settingsOptions[3].rend.get_rect()[2]
defaultBackgroundH = settingsOptions[3].rend.get_rect()[3]

# determining the background
chosenBackground = sunny

# remembering player names
player1Text = ""
player2Text = ""
name1 = regularFont.render(player1Text,1,(RED))
name2 = regularFont.render(player2Text,1,(BLUE))

# the winning score
winningScore = 7

#FPS
clock = pygame.time.Clock()
FPS = 80
frame = 0

running = True
inStart = True
inSettings = False
inPlay = False
inPlayer1 = False
inPlayer2 = False
inGame = False
postGame = False

while running:
    while inStart: # draw main menu
        pygame.event.pump() #Ensure all events are current
        screen.blit(tennis,(0,0))
        textTitle = titleFont.render("PONG FOR TWO",1,WHITE)
        screen.blit(textTitle,(WIDTH//7,HEIGHT//10.8))

        # iterate through all menu buttons
        for option in startOptions: 
            if option.rect.collidepoint(pygame.mouse.get_pos()): #Check if mouse is within bounds of the button
                option.hovered = True #If so, set that to true
            else:
                option.hovered = False #Otherwise, false
            option.draw() #Redraw the button: red or blue
        pygame.display.update()

        # deciding where to go next depending on the button that's pressed
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startOptions[0].rect.collidepoint(pygame.mouse.get_pos()):
                    inStart = False
                    inPlay = True
                    inPlayer1 = True
                elif startOptions[1].rect.collidepoint(pygame.mouse.get_pos()):
                    inStart = False
                    inSettings = True
                elif startOptions[2].rect.collidepoint(pygame.mouse.get_pos()):
                    inStart = False
                    running = False

    while inSettings: # draw settings options 
        pygame.event.pump()
        screen.blit(tennis,(0,0))
        textSpeed = regularFont.render("BALL SPEED",1,WHITE)
        screen.blit(textSpeed,(WIDTH//12.8,HEIGHT//16))
        speedSelect = pygame.transform.scale(selectBox,(defaultSpeedWidth,defaultSpeedHeight))
        screen.blit(speedSelect,defaultSpeed)
        textMusic = regularFont.render("MUSIC",1,WHITE)
        screen.blit(textMusic, (WIDTH//1.8,HEIGHT//16))
        musicSelect = pygame.transform.scale(selectBox,(WIDTH//6,HEIGHT//6))
        screen.blit(musicSelect, (WIDTH//1.8,HEIGHT//5))
        screen.blit(musicSelect, (WIDTH//1.3,HEIGHT//5))
        musicOnText = clickFONT.render("ON",1,BLACK)
        screen.blit(musicOnText, (WIDTH//1.65,HEIGHT//4.4))
        musicOffText = clickFONT.render("OFF",1,BLACK)
        screen.blit(musicOffText, (WIDTH//1.25,HEIGHT//4.4))
        screen.blit(woodPlank, (WIDTH//1.38,HEIGHT//5.7))
        textBackgrounds = regularFont.render("BACKGROUNDS",1,WHITE)
        screen.blit(textBackgrounds, (WIDTH//1.8,HEIGHT//2))
        backgroundSelect = pygame.transform.scale(selectBox,(defaultBackgroundW,defaultBackgroundH))
        screen.blit(backgroundSelect,defaultBackground)

        # iterate through all menu buttons
        for option in settingsOptions: 
            if option.rect.collidepoint(pygame.mouse.get_pos()): 
                option.hovered = True 
            else:
                option.hovered = False
            option.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inSettings = False
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
            # -------- difficulty options 
                if settingsOptions[0].rect.collidepoint(pygame.mouse.get_pos()):
                    defaultSpeedWidth = settingsOptions[0].rend.get_rect()[2]
                    defaultSpeedHeight = settingsOptions[0].rend.get_rect()[3]
                    defaultSpeed = speedSelectPos[0]
                    DIFF_MULT = MAX_SPEED_MULT[0]
                    PADDLE_LENGTH = WIDTH/6
                elif settingsOptions[1].rect.collidepoint(pygame.mouse.get_pos()):
                    defaultSpeedWidth = settingsOptions[1].rend.get_rect()[2]
                    defaultSpeedHeight = settingsOptions[1].rend.get_rect()[3]
                    defaultSpeed = speedSelectPos[1]
                    DIFF_MULT = MAX_SPEED_MULT[1]
                elif settingsOptions[2].rect.collidepoint(pygame.mouse.get_pos()):
                    defaultSpeedWidth = settingsOptions[2].rend.get_rect()[2]
                    defaultSpeedHeight = settingsOptions[2].rend.get_rect()[3]
                    defaultSpeed = speedSelectPos[2]
                    DIFF_MULT = MAX_SPEED_MULT[2]
                    PADDLE_LENGTH = WIDTH/13
            # ----------------------
            # --------- background options 
                elif settingsOptions[3].rect.collidepoint(pygame.mouse.get_pos()):
                    defaultBackground = backgroundSelectPos[0]
                    defaultBackgroundW = settingsOptions[3].rend.get_rect()[2]
                    defaultBackgroundH = settingsOptions[3].rend.get_rect()[3]
                    chosenBackground = sunny
                elif settingsOptions[4].rect.collidepoint(pygame.mouse.get_pos()):
                    defaultBackground = backgroundSelectPos[1]
                    defaultBackgroundW = settingsOptions[4].rend.get_rect()[2]
                    defaultBackgroundH = settingsOptions[4].rend.get_rect()[3]
                    chosenBackground = beach
                elif settingsOptions[5].rect.collidepoint(pygame.mouse.get_pos()):
                    defaultBackground = backgroundSelectPos[2]
                    defaultBackgroundW = settingsOptions[5].rend.get_rect()[2]
                    defaultBackgroundH = settingsOptions[5].rend.get_rect()[3]
                    chosenBackground = volcano
                elif settingsOptions[6].rect.collidepoint(pygame.mouse.get_pos()):
                    defaultBackground = backgroundSelectPos[3]
                    defaultBackgroundW = settingsOptions[6].rend.get_rect()[2]
                    defaultBackgroundH = settingsOptions[6].rend.get_rect()[3]
                    chosenBackground = sky
                elif settingsOptions[7].rect.collidepoint(pygame.mouse.get_pos()):
                    defaultBackground = backgroundSelectPos[4]
                    defaultBackgroundW = settingsOptions[7].rend.get_rect()[2]
                    defaultBackgroundH = settingsOptions[7].rend.get_rect()[3]
                    chosenBackground = foot
            # ----------------------
                # go back to main menu
                elif settingsOptions[8].rect.collidepoint(pygame.mouse.get_pos()):
                    inSettings = False
                    inStart = True
                    
    score1 = 0
    score2 = 0
    while inPlay: # when players press play
        name1 = regularFont.render(player1Text,1,(RED))
        rect = name1.get_rect()
        rect.topleft = (WIDTH//10,HEIGHT//4)
        cursor = pygame.Rect(rect.topright,(3,rect.height))
        while inPlayer1: # asks for player 1 to input their name
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player1Text = player1Text[:-1]
                    else:
                        player1Text = player1Text + event.unicode
                    name1 = regularFont.render(player1Text,1,(RED))
                    rect.size = name1.get_size()
                    cursor.topleft = rect.topright
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if doneButton[0].rect.collidepoint(pygame.mouse.get_pos()):
                        inPlayer1 = False
                        inPlayer2 = True
                    
            screen.fill(BLACK)
            nameintro1 = regularFont.render("Player 1, enter your name:",1,WHITE)
            screen.blit(nameintro1,(WIDTH//10,HEIGHT//10))
            screen.blit(name1,(WIDTH//10,HEIGHT//4))

            if time.time() % 1 > 0.5:
                pygame.draw.rect(screen,(RED),cursor)
                
            for option in doneButton:
                if option.rect.collidepoint(pygame.mouse.get_pos()): 
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()
            pygame.display.update()

        name2 = regularFont.render(player2Text,1,(BLUE))
        rect = name2.get_rect()
        rect.topleft = (WIDTH//10,HEIGHT//4)
        cursor = pygame.Rect(rect.topright,(3,rect.height))
        while inPlayer2: # asks for player 2 to input their name
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player2Text = player2Text[:-1]
                    else:
                        player2Text = player2Text + event.unicode
                    name2 = regularFont.render(player2Text,1,(BLUE))
                    rect.size = name2.get_size()
                    cursor.topleft = rect.topright
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if doneButton[0].rect.collidepoint(pygame.mouse.get_pos()):
                        inPlayer2 = False
                        inGame = True
                    
            screen.fill(BLACK)
            nameintro2 = regularFont.render("Player 2, enter your name:",1,WHITE)
            screen.blit(nameintro2,(WIDTH//10,HEIGHT//10))
            screen.blit(name2,(WIDTH//10,HEIGHT//4))
            
            if time.time() % 1 > 0.5:
                pygame.draw.rect(screen,(BLUE),cursor)
                
            for option in doneButton:
                if option.rect.collidepoint(pygame.mouse.get_pos()): 
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()
            pygame.display.update()
        
        players = [Option(player1Text,(WIDTH//4,HEIGHT//1.2)),Option(player2Text,(WIDTH//1.5,HEIGHT//1.2))]
        while inGame: 
            pygame.event.pump()
            screen.blit(chosenBackground,(0,0))

            # --------- Vienna ------# 
            drawScreen(screen) #Visualize
            
            ballUpdate() #Update the ball's position and physics

            paddleControl()
            # -------------------------- #

            # store player names, visualize names and scores
            textName1 = regularFont.render(player1Text,1,RED)
            textName2 = regularFont.render(player2Text,1,BLUE)
            textScore1 = regularFont.render(str(score1),1,RED)
            textScore2 = regularFont.render(str(score2),1,BLUE)

            screen.blit(textName1,(WIDTH//4,HEIGHT//1.2))
            screen.blit(textName2,(WIDTH//1.8,HEIGHT//1.2))
            screen.blit(textScore1,(WIDTH//50,HEIGHT//1.2))
            screen.blit(textScore2,(WIDTH//1.07,HEIGHT//1.2))

            pygame.display.update()
            clock.tick(FPS)

            for event in pygame.event.get():
                # ---------- cheat: Emily ------------------------------#
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        import PongCheatMode as cheatGame
                        winner = cheatGame.playCheatGame(player1Text,player2Text)
                        pygame.mixer.music.load("../Audio/wiiSportsThemeLoop.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(loops = -1)
                        if winner == player1Text:
                            score1 = score1 + 1
                        if winner == player2Text:
                            score2 = score2 + 1
                # -----------------------------------------#
               
            if score1 == winningScore or score2 == winningScore:
                inGame = False
                inPlay = False
                postGame = True

    winner = ""
    while postGame: # game over screen
        pygame.event.pump()
        screen.blit(chosenBackground,(0,0))
        gameOverText = titleFont.render("GAME OVER",1,PURPLE)
        screen.blit(gameOverText,(WIDTH//4.8,HEIGHT//20))

        # display the winner and final score
        if score1 == winningScore:
            winner = player1Text
            winnerText = regularFont.render(player1Text + " is the winner!",1,RED)
            screen.blit(winnerText,(WIDTH//4.8,HEIGHT//4))
        if score2 == winningScore:
            winner = player2Text
            winnerText = regularFont.render(player2Text + " is the winner!",1,BLUE)
            screen.blit(winnerText,(WIDTH//4.8,HEIGHT//4))

        for option in postGameOptions:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()

        finalScore = str(score1) + " - " + str(score2)
        finalScoreText = regularFont.render(finalScore,1,PURPLE)
        screen.blit(finalScoreText,(WIDTH//2.3,HEIGHT//2.5))
        pygame.display.update()

        # options for where to go next
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if postGameOptions[0].rect.collidepoint(pygame.mouse.get_pos()):
                    postGame = False
                    inPlay = True
                    inPlayer1 = False
                    inPlayer2 = False
                    inGame = True
                    score1 = 0
                    score2 = 0
                if postGameOptions[1].rect.collidepoint(pygame.mouse.get_pos()):
                    postGame = False
                    inStart = True


pygame.quit() 
