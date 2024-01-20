import pygame
from helpers import *
import numpy as np
pygame.init()
# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
ORANGE = ()

BackgroundColor = (89, 86, 76)
squareSize = int(input("Size of the window: "))
chosenLevel = int(input("Select the diffulty (0 easy, 1 medium, 2 hard, 3 no-win): "))

size = (squareSize, squareSize)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("3x3 Tris")

carryOn = True
clock = pygame.time.Clock()

size3 = squareSize/3

board = [[0 for i in range(3)] for i in range(3)]
piecesCount = 0

levels = [2, 5, 7, 9]
howDeep = levels[chosenLevel]
def drawX(pos, size = 100):
    pygame.draw.line(screen, WHITE, pos, [pos[0]+size, pos[1]+size], width=5)
    pygame.draw.line(screen, WHITE,  [pos[0]+size, pos[1]], [pos[0], pos[1]+size], width=5)
def drawO(pos, rad = 80):
    pygame.draw.circle(screen, WHITE, pos, rad, 5)

def drawBoard():
    #offSet = 20
    pygame.draw.rect(screen, WHITE, [0, size3, squareSize, 5],0)
    pygame.draw.rect(screen, WHITE, [0, size3*2, squareSize, 5],0)
    pygame.draw.rect(screen, WHITE, [size3, 0, 5, squareSize],0)
    pygame.draw.rect(screen, WHITE, [size3*2, 0, 5, squareSize],0)

    for i in range(3):
        for j in range(3):
            if board[i][j] == 1:
                drawX([size3*i+size3/2-size3/5, size3*j+size3/2-size3/5], squareSize/8)
            if board[i][j] == 2:
                drawO([size3*i+size3/2, size3*j+size3/2], squareSize/10)


def minimax(state, piecesCountL=0, depth=4, isMax=True):
    result = isFinished(state)

    if result != -1:
        return -1*depth if result == 1 else 1
    if piecesCountL >= 9 or depth == 0:
        return 0

    if isMax:
        maxV = -100000
        for x in range(3):
            for y in range(3):
                if state[x][y] == 0:
                    state[x][y] = 2
                    maxV = max(minimax(state, piecesCountL+1, depth-1, False), maxV)
                    state[x][y] = 0
        return maxV
    else:
        minV = 100000
        for x in range(3):
            for y in range(3):
                if state[x][y] == 0:
                    state[x][y] = 1
                    minV = min(minimax(state, piecesCountL+1, depth-1, True), minV)
                    state[x][y] = 0
        return minV

def choosePiece(board, piecesCount):
    bestMove = [0,0]
    currentValue = -1000000
    bestValue = -1000000
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
                board[x][y] = 2
                piecesCount += 1
                currentValue = minimax(board, piecesCount, howDeep, False)
                piecesCount -= 1
                board[x][y] = 0
                if currentValue > bestValue:
                    bestMove = [x, y]
                    bestValue = currentValue

    board[bestMove[0]][bestMove[1]] = 2


player = 0
canDo = True
gameFinished = False
while carryOn:

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we can exit the while loop

    screen.fill(BackgroundColor)
    x,y = pygame.mouse.get_pos()

    if canDo and pygame.mouse.get_pressed()[0] and board[int(x/size3)][int(y/size3)] == 0 and not gameFinished:
        board[int(x/size3)][int(y/size3)] = 1
        piecesCount += 1
        if piecesCount < 9:
            choosePiece(board, piecesCount);
            piecesCount += 1
        canDo = False
    if not pygame.mouse.get_pressed()[0]:
        canDo = True
    drawBoard();
    resultedGame = isFinished(board)
    if resultedGame != -1 and not gameFinished:
        gameFinished = True
        print(("X" if resultedGame == 1 else "O") + " has won!")
    if ( piecesCount >= 9 and not gameFinished):
        gameFinished = True
        print("Tie!")

    pygame.display.flip()
    clock.tick(60)

#Once we have exited the main program loop we can stop the game engine:
pygame.quit()

