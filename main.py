import pygame
from helpers import isFinished
from obligatedMoves import isObligatedMove
import AIs
import numpy as np

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
ORANGE = ()
BackgroundColor = (89, 86, 76)

class TrisNxN:
    def __init__(self, squareSize, sizeBoard, pieceToCheck, enemyAI = AIs.SimpleAi, playerAI = "input", *args):
        self.squareSize = squareSize
        self.sizeBoard = sizeBoard
        self.pieceToCheck = pieceToCheck
        if enemyAI == "input":
            self.enemyAI = enemyAI
        else: self.enemyAI = enemyAI(sizeBoard, pieceToCheck, args[:int(len(args)/2)])
        if playerAI == "input":
            self.playerAI = playerAI
        else: self.playerAI = playerAI(sizeBoard, pieceToCheck, args[int(len(args)/2):])
        self.turn = False
        pygame.init()
        self.size = (squareSize, squareSize)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(f"{sizeBoard}x{sizeBoard} Tris")
        self.carryOn = True
        self.clock = pygame.time.Clock()
        self.size3 = squareSize/sizeBoard

        self.board = [[0 for i in range(sizeBoard)] for i in range(sizeBoard)]
        self.piecesCount = 0

        self.player = 0
        self.canDo = True
        self.gameFinished = False
        self.obl = 0
        
    def drawX(self, pos, size = 100):
        pygame.draw.line(self.screen, WHITE, pos, [pos[0]+size, pos[1]+size], width=5)
        pygame.draw.line(self.screen, WHITE,  [pos[0]+size, pos[1]], [pos[0], pos[1]+size], width=5)

    def drawO(self, pos, rad = 80):
        pygame.draw.circle(self.screen, WHITE, pos, rad, 5)

    def drawBoard(self):
        for i in range(1, self.sizeBoard):
            pygame.draw.rect(self.screen, WHITE, [0, self.size3*i, self.squareSize, 5],0)
        for i in range(1, self.sizeBoard):
            pygame.draw.rect(self.screen, WHITE, [self.size3*i, 0, 5, self.squareSize],0)

        for i in range(self.sizeBoard):
            for j in range(self.sizeBoard):
                if self.board[i][j] == 1:
                    self.drawX([self.size3*i+self.size3/2-self.size3/5, self.size3*j+self.size3/2-self.size3/5], self.squareSize/(5+self.sizeBoard))
                if self.board[i][j] == 2:
                    self.drawO([self.size3*i+self.size3/2, self.size3*j+self.size3/2], self.squareSize/(7+self.sizeBoard))


    def finishProcess(self):
        resultedGame = isFinished(self.board, self.sizeBoard, self.pieceToCheck)
        if resultedGame != -1 and not self.gameFinished:
            self.gameFinished = True
            print(("X" if resultedGame == 1 else "O") + " has won!")
            print("Press enter to start another game and esc to exit")
        if ( self.piecesCount >= self.sizeBoard*self.sizeBoard and not self.gameFinished ):
            self.gameFinished = True
            print("Tie!")
            print("Press enter to start another game and esc to exit")

    def choosePiece(self, pl = 2):
        move = (self.enemyAI if pl == 2 else self.playerAI).choosePiece(self.board, self.piecesCount)
        self.board[move[0]][move[1]] = pl

    def moveProcess(self):
        size3Loc = self.size3
        x,y = pygame.mouse.get_pos()
        if self.playerAI == "input":
            if (not self.turn) and self.canDo and pygame.mouse.get_pressed()[0] and self.board[int(x/size3Loc)][int(y/size3Loc)] == 0 and not self.gameFinished:
                self.board[int(x/self.size3)][int(y/self.size3)] = 1
                self.piecesCount += 1
                self.canDo = False
                self.turn = True
        elif (not self.turn):
            self.choosePiece(1)
            self.piecesCount += 1
            self.turn = True

        if (isFinished(self.board, self.sizeBoard, self.pieceToCheck) != -1 and self.piecesCount < self.sizeBoard*self.sizeBoard): return
        if self.enemyAI == "input":
            if self.turn and self.canDo and pygame.mouse.get_pressed()[0] and self.board[int(x/size3Loc)][int(y/size3Loc)] == 0 and not self.gameFinished:
                self.board[int(x/self.size3)][int(y/self.size3)] = 2
                self.piecesCount += 1
                self.canDo = False
                self.turn = False
        elif (self.turn):
            self.choosePiece()
            self.piecesCount += 1
            self.turn = False

        if not pygame.mouse.get_pressed()[0]: self.canDo = True

    def update(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self.carryOn = False # Flag that we are done so we can exit the while loop

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.gameFinished = False
                self.board = [[0 for i in range(self.sizeBoard)] for i in range(self.sizeBoard)]
                self.piecesCount = 0
                self.turn = False

        self.screen.fill(BackgroundColor)
        self.moveProcess()
        self.drawBoard()
        self.finishProcess()
        pygame.display.flip()
        self.clock.tick(60)


squareSize = int(input("Size of the window: "))
sizeBoard = int(input("Size of the board (3x3, 4x4 and so on): "))
chosenLevel = int(input("Select the diffulty (0 easy, 1 medium, 2 hard, 3 no-win): "))
pieceToCheck = sizeBoard

levels = [2, 5, 7, 10]
tris = TrisNxN(squareSize, sizeBoard, pieceToCheck, AIs.SimpleAi, "input", levels[chosenLevel], 0)

while tris.carryOn:
    tris.update()
pygame.quit()
