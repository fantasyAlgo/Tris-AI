from Agents.helpers import isFinished
from Agents.obligatedMoves import isObligatedMove
from Agents.MCTS import *
import numpy as np
import random

class SimpleAi:
    def __init__(self, sizeBoard, pieceToCheck, args):
        self.sizeBoard = sizeBoard
        self.depth = args[0]
        self.pieceToCheck = pieceToCheck

    def minimax(self, state, piecesCountL=0, howDeep=-10, alpha=0, beta=0, isMax=False):
        if howDeep == -10: howDeep = self.depth

        result = isFinished(state, self.sizeBoard, self.pieceToCheck)
        if result != -1:
            return -1*howDeep if result == 1 else 1
        if piecesCountL >= self.sizeBoard*self.sizeBoard or howDeep <= 0:
            return 0
        
        if isMax:
            maxV = -100000
            obligatedVal = isObligatedMove(state, self.sizeBoard, self.pieceToCheck)
            if obligatedVal != -1:
                state[obligatedVal[0]][obligatedVal[1]] = 2
                eval = self.minimax(state, piecesCountL+1, howDeep-1, alpha, beta)
                maxV = max(eval, maxV)
                state[obligatedVal[0]][obligatedVal[1]] = 0
                alpha = max(alpha, eval)
                return maxV
            
            for x in range(self.sizeBoard):
                for y in range(self.sizeBoard):
                    if state[x][y] == 0:
                        state[x][y] = 2
                        eval = self.minimax(state, piecesCountL+1, howDeep-1, alpha, beta)
                        maxV = max(eval, maxV)
                        state[x][y] = 0
                        alpha = max(alpha, eval)
                        #if beta <= alpha:
                        #    return maxV
            return maxV
        else:
            minV = 100000
            obligatedVal = isObligatedMove(state, self.sizeBoard, piece = 2)
            if obligatedVal != -1:
                state[obligatedVal[0]][obligatedVal[1]] = 1
                eval = self.minimax(state, piecesCountL+1, howDeep-1, alpha, beta, True)
                minV = min(eval, minV)
                state[obligatedVal[0]][obligatedVal[1]] = 0
                beta = min(beta, eval)
                return minV
            
            for x in range(self.sizeBoard):
                for y in range(self.sizeBoard):
                    if state[x][y] == 0:
                        state[x][y] = 1
                        eval = self.minimax(state, piecesCountL+1, howDeep-1, alpha, beta, True)
                        minV = min(eval, minV)
                        state[x][y] = 0
                        beta = min(beta, eval)
                        #if beta <= alpha:
                        #    return minV  
            return minV
    def choosePiece(self, board, piecesCount):
            bestMove = [0,0]
            currentValue = -1000000
            bestValue = -1000000
            obligatedVal = isObligatedMove(board, self.sizeBoard, self.pieceToCheck, 2)
            if obligatedVal != -1:
                return obligatedVal
            obligatedVal = isObligatedMove(board, self.sizeBoard, self.pieceToCheck)
            if obligatedVal != -1:
                return obligatedVal
            
            for x in range(self.sizeBoard):
                for y in range(self.sizeBoard):
                    if board[x][y] == 0:
                        board[x][y] = 2
                        piecesCount += 1
                        currentValue = self.minimax(board, piecesCount)
                        piecesCount -= 1
                        board[x][y] = 0
                        if currentValue > bestValue:
                            bestMove = [x, y]
                            bestValue = currentValue
            return bestMove 

class IterativeAI:
    def __init__(self, sizeBoard, pieceToCheck, args):
        self.sizeBoard = sizeBoard
        self.pieceToCheck = pieceToCheck
        self.depth = args[0]
    def choosePiece(self, board, piecesCount):
        for i in range(9):
            if board[i//3][i%3] == 0:
                return [i//3, i%3]
        return [0,0]
    
class RandomAI:
    def __init__(self, sizeBoard, pieceToCheck, args):
        if (pieceToCheck != 3):
            print("pieceToCheck have to be 3");
        self.sizeBoard = sizeBoard
        self.pieceToCheck = pieceToCheck
    def choosePiece(self, board, piecesCount):
        available = []
        for i in range(9):
            if board[i//3][i%3] == 0:
                available.append(i)
        i = random.choice(available)
        return [i//3, i%3]
    
class DontCheckAI:
    def __init__(self, sizeBoard, pieceToCheck, args):
        if (pieceToCheck != 3):
            print("pieceToCheck have to be 3");
        self.sizeBoard = sizeBoard
        self.pieceToCheck = pieceToCheck
    def choosePiece(self, board, piecesCount):
        obligatedVal = isObligatedMove(board, self.sizeBoard, self.pieceToCheck, 2)
        if obligatedVal != -1:
            return obligatedVal
        obligatedVal = isObligatedMove(board, self.sizeBoard, self.pieceToCheck)
        if obligatedVal != -1:
            return obligatedVal
        i,j = random.randint(0,2),random.randint(0,2)
        while (board[i][j] != 0):
            i,j = random.randint(0,2),random.randint(0,2)
        return [i,j]

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

# NeuralAI uses a neural network (with weights as input) to choose the next move
class NeuralAI():
    def __init__(self, sizeBoard, pieceToCheck, args):
        self.weights = np.random.rand(9, 9)
        #self.biases = np.random.rand(9)
    def propagate(self, state):
        return softmax(np.dot(state, self.weights)) # + self.biases
    def choosePiece(self, board, piecesCount):
        state = np.array(board).reshape(1, 9)
        result = np.argmax(self.propagate(state))
        return [int(result/3), int(result)%3]

# Only for 3x3 boards
class MCTSAI:
    def __init__(self, sizeBoard, pieceToCheck, args):
        self.sizeBoard = sizeBoard
        self.pieceToCheck = pieceToCheck
        #self.depth = args[0]
    def choosePiece(self, board, piecesCount):
        return MCTS(board, 2, piecesCount, 1000)