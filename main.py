# trying github!
import pygame
from helpers import isFinished
from obligatedMoves import isObligatedMove
import AIs
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
sizeBoard = int(input("Size of the board (3x3, 4x4 and so on): "))
chosenLevel = int(input("Select the diffulty (0 easy, 1 medium, 2 hard, 3 no-win): "))

size = (squareSize, squareSize)
screen = pygame.display.set_mode(size)
pygame.display.set_caption(f"{sizeBoard}x{sizeBoard} Tris")

carryOn = True
clock = pygame.time.Clock()

size3 = squareSize/sizeBoard

board = [[0 for i in range(sizeBoard)] for i in range(sizeBoard)]
piecesCount = 0

levels = [2, 5, 7, 10]
howDeep = levels[chosenLevel]
Ai = AIs.SimpleAi(sizeBoard, howDeep, sizeBoard)
def drawX(pos, size = 100):
    pygame.draw.line(screen, WHITE, pos, [pos[0]+size, pos[1]+size], width=5)
    pygame.draw.line(screen, WHITE,  [pos[0]+size, pos[1]], [pos[0], pos[1]+size], width=5)
def drawO(pos, rad = 80):
    pygame.draw.circle(screen, WHITE, pos, rad, 5)

def drawBoard():
    #offSet = 20
    for i in range(1, sizeBoard):
        pygame.draw.rect(screen, WHITE, [0, size3*i, squareSize, 5],0)
    for i in range(1, sizeBoard):
        pygame.draw.rect(screen, WHITE, [size3*i, 0, 5, squareSize],0)

    for i in range(sizeBoard):
        for j in range(sizeBoard):
            if board[i][j] == 1:
                drawX([size3*i+size3/2-size3/5, size3*j+size3/2-size3/5], squareSize/(5+sizeBoard))
            if board[i][j] == 2:
                drawO([size3*i+size3/2, size3*j+size3/2], squareSize/(7+sizeBoard))


def choosePiece(board, piecesCount):
    move = Ai.choosePiece(board, piecesCount)
    board[move[0]][move[1]] = 2

player = 0
canDo = True
gameFinished = False
obl = 0
while carryOn:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we can exit the while loop
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            gameFinished = False
            board = [[0 for i in range(sizeBoard)] for i in range(sizeBoard)]
            piecesCount = 0

    screen.fill(BackgroundColor)
    x,y = pygame.mouse.get_pos()
    events = pygame.event.get()
    if canDo and pygame.mouse.get_pressed()[0] and board[int(x/size3)][int(y/size3)] == 0 and not gameFinished:
        board[int(x/size3)][int(y/size3)] = 1
        piecesCount += 1
        if piecesCount < sizeBoard*sizeBoard and isFinished(board, sizeBoard, sizeBoard) == -1:
            choosePiece(board, piecesCount)
            piecesCount += 1
        canDo = False

    if not pygame.mouse.get_pressed()[0]:
        canDo = True
        
    drawBoard()
    resultedGame = isFinished(board, sizeBoard, sizeBoard)
    if resultedGame != -1 and not gameFinished:
        gameFinished = True
        print(("X" if resultedGame == 1 else "O") + " has won!")
        print("Press enter to start another game and esc to exit")
    if ( piecesCount >= sizeBoard*sizeBoard and not gameFinished):
        gameFinished = True
        print("Tie!")
        print("Press enter to start another game and esc to exit")

    pygame.display.flip()
    clock.tick(60)

#Once we have exited the main program loop we can stop the game engine:
pygame.quit()