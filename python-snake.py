import pygame
import random
import numpy as np
import time
pygame.init()

pygame.display.set_caption("Patrick's Python Snake")
clock = pygame.time.Clock()

SCREEN_WIDTH    = 750
SCREEN_HEIGHT   = 750
numPixelsWidth  = 30
numPixelsHeight = 30

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

blue = (0,0,255)
green = (0,255,0)
orange = (255,165,0)
purple = (255,0,255)
turquoise = (0,255,255)
red = (255,0,0)
yellow = (255,255,0)



backgroundColor = (0, 0, 0)
backgroundColor1 = (0, 51, 0)
backgroundColor2 = (0, 78, 0)
snakeColor = (0, 0, 255)
foodColor  = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
activeColor = (200,200,200)


pixelSizeWidth  = SCREEN_WIDTH / numPixelsWidth
pixelSizeHeight = SCREEN_HEIGHT / numPixelsHeight
Board = np.zeros((numPixelsHeight, numPixelsWidth))
BackgroundBoard = np.zeros((numPixelsHeight, numPixelsWidth))


posX = round(numPixelsWidth / 2)
posY = round(numPixelsHeight / 2)
gotFood = True
dead = False
prevPosX = posX
prevPosY = posY
snakeSize = 1
snakeArrayX = []
snakeArrayY = []
increaseSize = False
wallCollision = True
snakeCollision = True
backgroundColorToggle = 1

upFlag = False
rightFlag = False
downFlag = False
leftFlag = False

delay = .2

score = 0

clock = pygame.time.Clock()
FPS = 18

def displayMessage(text,x,y,size,color=white):
    largeText = pygame.font.SysFont("comicsansms", size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (x,y)
    screen.blit(TextSurf, TextRect)
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def initializeBoard():
    x = 0
    y = 0

    # Create an alternative checkerboard pattern on the board
    while x < numPixelsWidth:
        while y < numPixelsHeight:
            if (x % 2 == 1) and (y % 2 == 1):
                BackgroundBoard[y][x] = 1
            if (x % 2 == 0) and (y % 2 == 0):
                BackgroundBoard[y][x] = 1
            y += 1
        y = 0
        x += 1

    #print(Board)
def displayBoard():

    global snakeArrayX, snakeArrayY

    rectX = 0
    width = pixelSizeWidth
    rectY = 0
    height = pixelSizeHeight
    x = 0
    y = 0

    while y < numPixelsHeight:
        while x < numPixelsWidth:
            if BackgroundBoard[y][x] == 0:
                pygame.draw.rect(screen, backgroundColor1, pygame.Rect(rectX, rectY, width, height))
            elif BackgroundBoard[y][x] == 1:
                pygame.draw.rect(screen, backgroundColor2, pygame.Rect(rectX, rectY, width, height))
            if Board[y][x] == 2:
                pygame.draw.rect(screen, foodColor, pygame.Rect(rectX, rectY, width, height))
            elif Board[y][x] == 3:
                pygame.draw.rect(screen, snakeColor, pygame.Rect(rectX, rectY, width, height))

            rectX += pixelSizeWidth
            x += 1
        rectX = 0
        x = 0
        rectY += pixelSizeHeight
        y += 1

    #Display the score in the top right
    displayMessage("Score: " + str(score), SCREEN_WIDTH - 100, 30,30)

    pygame.display.flip()
def placeFood():

    global gotFood, foodX, foodY

    if gotFood == True:
        foodX = random.randint(0,numPixelsWidth-1)
        foodY = random.randint(0,numPixelsHeight-1)

        Board[foodY][foodX] = 2

        gotFood = False
def moveSnake(direction):
    global dead, posX, posY, foodY, foodX, gotFood, snakeSize, snakeArrayX, snakeArrayY, increaseSize, score

    prevPosX = posX
    prevPosY = posY

    size = len(snakeArrayY)

    if size > 0:
        Board[snakeArrayY.pop()][snakeArrayX.pop()] = 0

    if increaseSize == True:
        snakeArrayY.append(posY)
        snakeArrayX.append(posX)
        increaseSize = False

    if direction == 0:
        posY -= 1
    elif direction == 1:
        posX += 1
    elif direction == 2:
        posY += 1
    elif direction == 3:
        posX -= 1

    #Conditions for being dead

    if wallCollision:
        if posY < 0 or numPixelsHeight - 1 < posY:
            posY = prevPosY
            dead = True
        if posX < 0 or numPixelsWidth - 1 < posX:
            posX = prevPosX
            dead = True

    if not wallCollision:
        if posY < 0:
            posY = numPixelsHeight - 1
        if posY > numPixelsHeight - 1:
            posY = 0
        if posX < 0:
            posX = numPixelsWidth - 1
        if posX > numPixelsWidth - 1:
            posX = 0

    if snakeCollision:
        checkDeadLoop = 0
        while checkDeadLoop < len(snakeArrayY) - 1:
            if posY == snakeArrayY[checkDeadLoop] and posX == snakeArrayX[checkDeadLoop]:
                dead = True
            checkDeadLoop += 1

    snakeArrayY.append(posY)
    snakeArrayX.append(posX)

    #Conditions for getting food
    if posY == foodY and posX == foodX:
        gotFood = True
        increaseSize = True
        score += 10

    snakeArrayY.append(snakeArrayY.pop(0))
    snakeArrayX.append(snakeArrayX.pop(0))

    loop = 0
    while loop < len(snakeArrayY):
        Board[snakeArrayY[loop]][snakeArrayX[loop]] = 3
        loop += 1
def button(text,size,x,y,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    font = pygame.font.SysFont("comicsansms", size)

    text_width, text_height = font.size(text)

    if x+text_width/2 > mouse[0] > x-text_width/2 and y+text_height/2 > mouse[1] > y-text_height/2:
        img = font.render(text, True, ac)


        if click[0] == 1 and action != None:
            displayBoard()
            action()
            return
    else:
        img = font.render(text, True, ic)

    screen.blit(img, (x-text_width/2, y-text_height/2))
def increaseSnakeSpeed():
    global FPS, delay
    FPS += 1
    time.sleep(delay)
def decreaseSnakeSpeed():
    global FPS, delay
    FPS -= 1
    if FPS < 1:
        FPS = 1
    time.sleep(delay)
def toggleWallCollision():
    global wallCollision, delay
    if wallCollision == True:
        wallCollision = False
    else:
        wallCollision = True
    time.sleep(delay)
def toggleSnakeCollision():
    global snakeCollision, delay
    if snakeCollision == True:
        snakeCollision = False
    else:
        snakeCollision = True
    time.sleep(delay)
def toggleSnakeColor():
    global snakeColor, delay

    if snakeColor == (255, 0, 0):
        snakeColor = (0,0,255)
        time.sleep(delay)
        return
    elif snakeColor == (0, 0, 255):
        snakeColor = (0,255,0)
        time.sleep(delay)
        return
    elif snakeColor == (0, 255, 0):
        snakeColor = (0,255,255)
        time.sleep(delay)
        return
    elif snakeColor == (0, 255, 255):
        snakeColor = (255,165,0)
        time.sleep(delay)
        return
    elif snakeColor == (255, 165, 0):
        snakeColor = (255,255,0)
        time.sleep(delay)
        return
    elif snakeColor == (255, 255, 0):
        snakeColor = (255,0,0)
        time.sleep(delay)
        return
def toggleBackgroundColor():
    global backgroundColor1, backgroundColor2, backgroundColorToggle, delay

    #Blue
    if backgroundColorToggle == 1:
        backgroundColor1 = (3,132,252)
        backgroundColor2 = (14,92,181)
        backgroundColorToggle = 2
        displayBoard()
        time.sleep(delay)
        return
    #Red
    elif backgroundColorToggle == 2:
        backgroundColor1 = (219,18,18)
        backgroundColor2 = (161,6,6)
        backgroundColorToggle = 3
        displayBoard()
        time.sleep(delay)
        return
    #Purple
    elif backgroundColorToggle == 3:
        backgroundColor1 = (202,15,212)
        backgroundColor2 = (184,4,181)
        backgroundColorToggle = 4
        displayBoard()
        time.sleep(delay)
        return
    #Orange
    elif backgroundColorToggle == 4:
        backgroundColor1 = (222,163,2)
        backgroundColor2 = (191,142,6)
        backgroundColorToggle = 5
        displayBoard()
        time.sleep(delay)
        return
    #Black
    elif backgroundColorToggle == 5:
        backgroundColor1 = (64,64,64)
        backgroundColor2 = (38,38,38)
        backgroundColorToggle = 6
        displayBoard()
        time.sleep(delay)
        return
    #Yellow
    elif backgroundColorToggle == 6:
        backgroundColor1 = (220,220,0)
        backgroundColor2 = (200,200,0)
        backgroundColorToggle = 7
        displayBoard()
        time.sleep(delay)
        return
    #Funky
    elif backgroundColorToggle == 7:
        backgroundColor1 = (187,20,187)
        backgroundColor2 = (7,214,237)
        backgroundColorToggle = 8
        displayBoard()
        time.sleep(delay)
        return
    # Green
    elif backgroundColorToggle == 8:
        backgroundColor1 = (0, 78, 0)
        backgroundColor2 = (0, 51, 0)
        backgroundColorToggle = 1
        displayBoard()
        time.sleep(delay)
        return
def toggleFoodColor():
    global foodColor, delay

    #Red
    if foodColor == red:
        foodColor = green
        time.sleep(delay)
        return

    #Green
    elif foodColor == green:
        foodColor = blue
        time.sleep(delay)
        return
    #Blue
    elif foodColor == blue:
        foodColor = yellow
        time.sleep(delay)
        return
    #Yellow
    elif foodColor == yellow:
        foodColor = turquoise
        time.sleep(delay)
        return

    #Turquoise
    elif foodColor == turquoise:
        foodColor = purple
        time.sleep(delay)
        return

    #Purple
    elif foodColor == purple:
        foodColor = red
        time.sleep(delay)
        return
def increaseNumPixelsWidth():
    global numPixelsWidth, delay

    numPixelsWidth += 1

    restartComplete()

    time.sleep(delay)
def decreaseNumPixelsWidth():
    global numPixelsWidth, delay

    numPixelsWidth -= 1
    if numPixelsWidth < 10:
        numPixelsWidth = 10

    restartComplete()

    time.sleep(delay)
def increaseNumPixelsHeight():
    global numPixelsHeight, delay

    numPixelsHeight += 1

    restartComplete()

    time.sleep(delay)
def decreaseNumPixelsHeight():
    global numPixelsHeight, delay

    numPixelsHeight -= 1
    if numPixelsHeight < 10:
        numPixelsHeight = 10

    restartComplete()

    time.sleep(delay)
def restart():
    global posX,posY,gotFood,dead,prevPosX,prevPosY,snakeSize,snakeArrayX,snakeArrayY,increaseSize,upFlag,rightFlag,downFlag,leftFlag,score,Board,BackgroundBoard
    posX = round(numPixelsWidth / 2)
    posY = round(numPixelsHeight / 2)
    gotFood = True
    dead = False
    prevPosX = posX
    prevPosY = posY
    snakeSize = 1
    snakeArrayX = []
    snakeArrayY = []
    increaseSize = False

    upFlag = False
    rightFlag = False
    downFlag = False
    leftFlag = False

    score = 0

    Board = np.zeros((numPixelsHeight, numPixelsWidth))
    time.sleep(delay)
    time.sleep(delay)
def restartComplete():
    global posX,posY,gotFood,dead,prevPosX,prevPosY,snakeSize,snakeArrayX,snakeArrayY,increaseSize,upFlag,rightFlag,downFlag,leftFlag,score,Board,BackgroundBoard,pixelSizeWidth,pixelSizeHeight
    posX = round(numPixelsWidth / 2)
    posY = round(numPixelsHeight / 2)
    gotFood = True
    dead = False
    prevPosX = posX
    prevPosY = posY
    snakeSize = 1
    snakeArrayX = []
    snakeArrayY = []
    increaseSize = False

    upFlag = False
    rightFlag = False
    downFlag = False
    leftFlag = False

    score = 0

    pixelSizeWidth = SCREEN_WIDTH / numPixelsWidth
    pixelSizeHeight = SCREEN_HEIGHT / numPixelsHeight
    Board = np.zeros((numPixelsHeight, numPixelsWidth))
    BackgroundBoard = np.zeros((numPixelsHeight, numPixelsWidth))
    initializeBoard()
    time.sleep(delay)
    time.sleep(delay)

def settings():
    global white, dullWhite, FPS, wallCollision, snakeCollision, snakeColor, backgroundColorToggle, foodColor, numPixelsWidth, numPixelsHeight

    displayBoard()
    while True:
        displayMessage("Snake Speed: ", SCREEN_WIDTH/3, SCREEN_HEIGHT/9,30)
        displayMessage("Wall Collision: ", SCREEN_WIDTH/3, 2*SCREEN_HEIGHT / 9, 30)
        displayMessage("Snake Collision: ", SCREEN_WIDTH/3, 3*SCREEN_HEIGHT / 9, 30)
        displayMessage("Snake Color: ", SCREEN_WIDTH/3, 4*SCREEN_HEIGHT / 9, 30)
        displayMessage("Background Color: ", SCREEN_WIDTH/3, 5*SCREEN_HEIGHT / 9, 30)
        displayMessage("Food Color: ", SCREEN_WIDTH/3, 6*SCREEN_HEIGHT / 9, 30)
        displayMessage("# Pixels X: ", SCREEN_WIDTH/3, 7*SCREEN_HEIGHT / 9, 30)
        displayMessage("# Pixels Y: ", SCREEN_WIDTH/3, 8*SCREEN_HEIGHT / 9, 30)

        #Back button
        button("Back", 32, 50, 30, white, activeColor, startMenu)

        #Snake Speed
        displayMessage(str(FPS),2*SCREEN_WIDTH/3,SCREEN_HEIGHT/9,32)
        button("^", 32, 2 * SCREEN_WIDTH / 3+40, SCREEN_HEIGHT / 9 - 10, white, activeColor, increaseSnakeSpeed)
        button("v", 32, 2 * SCREEN_WIDTH / 3 + 40, SCREEN_HEIGHT / 9 + 10, white, activeColor, decreaseSnakeSpeed)
        #Wall Collision
        if wallCollision:
            button("On",32,2*SCREEN_WIDTH/3,2*SCREEN_HEIGHT/9,white,activeColor,toggleWallCollision)
        else:
            button("Off",32,2*SCREEN_WIDTH/3,2*SCREEN_HEIGHT/9,white,activeColor,toggleWallCollision)

        #Snake Collision
        if snakeCollision:
            button("On",32,2*SCREEN_WIDTH/3,3*SCREEN_HEIGHT/9,white,activeColor,toggleSnakeCollision)
        else:
            button("Off",32,2*SCREEN_WIDTH/3,3*SCREEN_HEIGHT/9,white,activeColor,toggleSnakeCollision)

        #Snake Color
        if snakeColor == (255,0,0):
            button("Red",32,2*SCREEN_WIDTH/3,4*SCREEN_HEIGHT/9,red,activeColor,toggleSnakeColor)
        elif snakeColor == (0,0,255):
            button("Blue", 32, 2*SCREEN_WIDTH/3, 4*SCREEN_HEIGHT/9, blue, activeColor,toggleSnakeColor)
        elif snakeColor == (0,255,0):
            button("Green", 32, 2 * SCREEN_WIDTH / 3, 4 * SCREEN_HEIGHT / 9, green, activeColor,toggleSnakeColor)
        elif snakeColor == (0,255,255):
            button("Turquoise", 32, 2 * SCREEN_WIDTH / 3, 4 * SCREEN_HEIGHT / 9, turquoise, activeColor,toggleSnakeColor)
        elif snakeColor == (255,165,0):
            button("Orange", 32, 2 * SCREEN_WIDTH / 3, 4 * SCREEN_HEIGHT / 9, orange, activeColor,toggleSnakeColor)
        elif snakeColor == (255,255,0):
            button("Yellow", 32, 2 * SCREEN_WIDTH / 3, 4 * SCREEN_HEIGHT / 9, yellow, activeColor,toggleSnakeColor)

        #Background Color
        if backgroundColorToggle == 1:
            button("Green", 32, 2 * SCREEN_WIDTH / 3, 5 * SCREEN_HEIGHT / 9, white, activeColor,toggleBackgroundColor)
        elif backgroundColorToggle == 2:
            button("Blue", 32, 2 * SCREEN_WIDTH / 3, 5 * SCREEN_HEIGHT / 9, white, activeColor,toggleBackgroundColor)
        elif backgroundColorToggle == 3:
            button("Red", 32, 2 * SCREEN_WIDTH / 3, 5 * SCREEN_HEIGHT / 9, white, activeColor,toggleBackgroundColor)
        elif backgroundColorToggle == 4:
            button("Purple", 32, 2 * SCREEN_WIDTH / 3, 5 * SCREEN_HEIGHT / 9, white, activeColor,toggleBackgroundColor)
        elif backgroundColorToggle == 5:
            button("Orange", 32, 2 * SCREEN_WIDTH / 3, 5 * SCREEN_HEIGHT / 9, white, activeColor,toggleBackgroundColor)
        elif backgroundColorToggle == 6:
            button("Black", 32, 2 * SCREEN_WIDTH / 3, 5 * SCREEN_HEIGHT / 9, white, activeColor,toggleBackgroundColor)
        elif backgroundColorToggle == 7:
            button("Yellow", 32, 2 * SCREEN_WIDTH / 3, 5 * SCREEN_HEIGHT / 9, white, activeColor,toggleBackgroundColor)
        elif backgroundColorToggle == 8:
            button("Funky", 32, 2 * SCREEN_WIDTH / 3, 5 * SCREEN_HEIGHT / 9, white, activeColor,toggleBackgroundColor)

        #Food Color
        if foodColor == red:
            button("Red",32,2*SCREEN_WIDTH/3,6*SCREEN_HEIGHT/9,red,activeColor,toggleFoodColor)
        elif foodColor == green:
            button("Green", 32, 2*SCREEN_WIDTH/3, 6*SCREEN_HEIGHT/9, green, activeColor,toggleFoodColor)
        elif foodColor == blue:
            button("Blue", 32, 2 * SCREEN_WIDTH / 3, 6 * SCREEN_HEIGHT / 9, blue, activeColor,toggleFoodColor)
        elif foodColor == yellow:
            button("Yellow", 32, 2 * SCREEN_WIDTH / 3, 6 * SCREEN_HEIGHT / 9, yellow, activeColor,toggleFoodColor)
        elif foodColor == turquoise:
            button("Turquoise", 32, 2 * SCREEN_WIDTH / 3, 6 * SCREEN_HEIGHT / 9, turquoise, activeColor,toggleFoodColor)
        elif foodColor == purple:
            button("Purple", 32, 2 * SCREEN_WIDTH / 3, 6 * SCREEN_HEIGHT / 9, purple, activeColor,toggleFoodColor)

        # num pixels X
        displayMessage(str(numPixelsWidth), 2 * SCREEN_WIDTH / 3, 7*SCREEN_HEIGHT / 9, 32)
        button("^", 32, 2 * SCREEN_WIDTH / 3+40, 7*SCREEN_HEIGHT / 9 - 10, white, activeColor, increaseNumPixelsWidth)
        button("v", 32, 2 * SCREEN_WIDTH / 3 + 40, 7*SCREEN_HEIGHT / 9 + 10, white, activeColor, decreaseNumPixelsWidth)

        # num pixels Y
        displayMessage(str(numPixelsHeight), 2 * SCREEN_WIDTH / 3, 8 * SCREEN_HEIGHT / 9, 32)
        button("^", 32, 2 * SCREEN_WIDTH / 3+40, 8*SCREEN_HEIGHT / 9 - 10, white, activeColor, increaseNumPixelsHeight)
        button("v", 32, 2 * SCREEN_WIDTH / 3 + 40, 8*SCREEN_HEIGHT / 9 + 10, white, activeColor, decreaseNumPixelsHeight)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def gameLoop():
    global upFlag,rightFlag,downFlag,leftFlag
    run = True
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_UP:
                    upFlag = True
                    rightFlag = False
                    downFlag = False
                    leftFlag = False
                if event.key == pygame.K_RIGHT:
                    upFlag = False
                    rightFlag = True
                    downFlag = False
                    leftFlag = False
                if event.key == pygame.K_DOWN:
                    upFlag = False
                    rightFlag = False
                    downFlag = True
                    leftFlag = False
                if event.key == pygame.K_LEFT:
                    upFlag = False
                    rightFlag = False
                    downFlag = False
                    leftFlag = True
        if upFlag:
            moveSnake(0)
        if rightFlag:
            moveSnake(1)
        if downFlag:
            moveSnake(2)
        if leftFlag:
            moveSnake(3)

        while dead:
            run = False
            displayMessage("Game over! :(", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100, 72)
            button("Restart?", 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100, white, activeColor, restart)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
        placeFood()
        displayBoard()

def startMenu():
    displayBoard()
    while True:
        displayMessage("MENU", SCREEN_WIDTH/2, SCREEN_HEIGHT/4,42)
        button("PLAY", 36, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, white, activeColor,gameLoop)
        button("SETTINGS", 36, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2+100, white, activeColor,settings)
        pygame.display.flip()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()



initializeBoard()
startMenu()



