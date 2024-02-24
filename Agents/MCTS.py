import numpy as np
import random
from Agents.helpers import *
from Agents.Node import *
from Agents.obligatedMoves import *
import copy

def randomMove(state):
    available = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                available.append([i,j])
    if available == []:
        return -1
    return random.choice(available)

def rollout(node):
    move = []
    initPiece = node.piece;
    piece = 1+initPiece%2;
    currentState = copy.deepcopy(node.state)
    pieceCount = node.piecesCount;
    result = 0;
    while True:
        result = isFinished(currentState)
        if result != -1 or pieceCount >= 9: break;
        oblMoveP = isObligatedMove(currentState, 3, 3, piece)
        oblMoveE = isObligatedMove(currentState, 3, 3, 1+piece%2)
        if oblMoveP != -1:
            currentState[oblMoveP[0]][oblMoveP[1]] = piece
        elif oblMoveE != -1:
            currentState[oblMoveE[0]][oblMoveE[1]] = piece
        else:
            move = randomMove(currentState)
            currentState[move[0]][move[1]] = piece
        piece = 1+piece%2;
        pieceCount += 1
    if result == -1: return 0
    return 1 if result == initPiece else -1


def MCTS(state, piece, piecesCount, maxIter=100):
    root = Node(0,0,state, 0, piecesCount, piece, None)
    root.expand()
    for _ in range(maxIter):
        node = root
        while len(node.children) > 0:
            node = node.bestChild()
        if node.visit_count > 0:
            node.expand()
            node = node.bestChild()
        value = rollout(node)
        node.backpropagate(value)

    best = root.children[0]
    for child in root.children:
        if child.value/child.visit_count > best.value/best.visit_count:
            best = child
    return best.action



def takeInputMove():
    inp = input("Enter the move: ")
    listInp = inp.split(" ")
    return [int(listInp[0]), int(listInp[1])]

def tryingMove(state, piece, piecesCount):
    move = MCTS(state, piece, piecesCount, 100)
    state[move[0]][move[1]] = piece
    print(move)

if __name__ == '__main__':
    trying = True
    if trying:
        board = [
            [1,0,0],
            [1,2,0],
            [2,0,0]
        ]
        tryingMove(board, 1, 4)
        exit()
    
    # Trying to play a game
    state = np.zeros((3,3))
    piece = 1
    piecesCount = 0
    while True:
        if piece == 2:
            print(state)
        if piecesCount%2 == 0:
            move = MCTS(state, piece, piecesCount)
        else:
            move = takeInputMove()
        state[move[0]][move[1]] = piece
        piecesCount += 1
        if isFinished(state) != -1 or piecesCount >= 9:
            break
        piece = 1+piece%2
    print(state)