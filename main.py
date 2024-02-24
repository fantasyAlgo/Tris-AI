import pygame
from Agents.helpers import isFinished
import AIs as AIs
import numpy as np
import time

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
ORANGE = ()
BackgroundColor = (89, 86, 76)

class TrisNxN:
    def __init__(self, squareSize, sizeBoard, pieceToCheck, visual, enemyAI = AIs.SimpleAi, playerAI = "input", *args):
        self.visual = visual
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
        self.size = (squareSize, squareSize)
        if self.visual:
            pygame.init()
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

        self.timeSleep = 0.0
        
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
            if self.visual:
                print(("X" if resultedGame == 1 else "O") + " has won!")
            #print("Press enter to start another game and esc to exit")
        if ( self.piecesCount >= self.sizeBoard*self.sizeBoard and not self.gameFinished ):
            self.gameFinished = True
            if self.visual:
                print("Tie!")
            #print("Press enter to start another game and esc to exit")

    def choosePiece(self, pl = 2):
        move = (self.enemyAI if pl == 2 else self.playerAI).choosePiece(self.board, self.piecesCount)
        if self.board[move[0]][move[1]] == 0:
            self.board[move[0]][move[1]] = pl
        else: return False
        return True
    
    def moveProcess(self):
        if (self.gameFinished or self.piecesCount >= self.sizeBoard*self.sizeBoard):
            self.piecesCount += 1
            return
        size3Loc = self.size3
        if self.visual: x,y = pygame.mouse.get_pos()
        if self.playerAI == "input":
            if (not self.turn) and self.canDo and pygame.mouse.get_pressed()[0] and self.board[int(x/size3Loc)][int(y/size3Loc)] == 0 and not self.gameFinished:
                self.board[int(x/self.size3)][int(y/self.size3)] = 1
                self.piecesCount += 1
                self.canDo = False
                self.turn = True
        elif (not self.turn):
            if self.choosePiece(1):
                self.piecesCount += 1
            self.turn = True
            time.sleep(self.timeSleep)
            
        if (isFinished(self.board, self.sizeBoard, self.pieceToCheck) != -1 and self.piecesCount < self.sizeBoard*self.sizeBoard): return
        if self.enemyAI == "input":
            if self.turn and self.canDo and pygame.mouse.get_pressed()[0] and self.board[int(x/size3Loc)][int(y/size3Loc)] == 0 and not self.gameFinished:
                self.board[int(x/self.size3)][int(y/self.size3)] = 2
                self.piecesCount += 1
                self.canDo = False
                self.turn = False
        elif (self.turn):
            if self.piecesCount < self.sizeBoard*self.sizeBoard:
                self.choosePiece()
            self.piecesCount += 1
            self.turn = False
            time.sleep(self.timeSleep)

        if self.visual and not pygame.mouse.get_pressed()[0]: self.canDo = True
    
    def inputHandler(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self.carryOn = False # Flag that we are done so we can exit the while loop

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.gameFinished = False
                self.board = [[0 for i in range(self.sizeBoard)] for i in range(self.sizeBoard)]
                self.piecesCount = 0
                self.turn = False

    def update(self):
        if self.visual:
            self.inputHandler()
            self.screen.fill(BackgroundColor)
        self.moveProcess()
        if self.visual: self.drawBoard()
        self.finishProcess()
        if self.visual:
            pygame.display.flip()
            self.clock.tick(60)

def fight(tris, n_times):
    firstWin = 0
    secondWin = 0
    tie = 0
    for _ in range(n_times):
        states = []
        while tris.carryOn and isFinished(tris.board) == -1 and tris.piecesCount <= 9:
            tris.update()
            states.append(tris.board)
        isFin =isFinished(tris.board)
        if isFin == 1:
            firstWin += 1
        elif isFin == 2: secondWin += 1
        else: tie += 1
        tris.gameFinished = False
        tris.board = [[0 for i in range(tris.sizeBoard)] for i in range(tris.sizeBoard)]
        tris.piecesCount = 0
        tris.turn = False
    return secondWin, firstWin, tie

if __name__ == "__main__":
    useMinimax = False
    if useMinimax:
        squareSize = int(input("Size of the window: "))
        sizeBoard = int(input("Size of the board (3x3, 4x4 and so on): "))
        chosenLevel = int(input("Select the diffulty (0 easy, 1 medium, 2 hard, 3 no-win): "))
        pieceToCheck = sizeBoard
    else:
        squareSize = 800
        sizeBoard = 3
        chosenLevel = 2
        pieceToCheck = sizeBoard
    
    levels = [2, 5, 7, 10]
    tris = TrisNxN(squareSize, sizeBoard, pieceToCheck, False, AIs.DontCheckAI, AIs.MCTSAI, levels[chosenLevel], 3)
    ######## To use the genetic AI
    #weights = np.load('weights.npy')
    #tris.playerAI = AIs.NeuralAI(sizeBoard, pieceToCheck, [])
    #tris.playerAI.weights = weights
    #### To set up the sleep time for the AI
    #tris.timeSleep = 0.6
    print(fight(tris, 20))
    pygame.quit()
