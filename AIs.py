from helpers import isFinished
from obligatedMoves import isObligatedMove
def minimax(state, piecesCountL=0, depth=4, sizeBoard=1, isMax=True):
    result = isFinished(state, sizeBoard)

    if result != -1:
        return -1*depth if result == 1 else 1
    if piecesCountL >= sizeBoard*sizeBoard or depth == 0:
        return 0

    if isMax:
        maxV = -100000
        for x in range(sizeBoard):
            for y in range(sizeBoard):
                if state[x][y] == 0:
                    state[x][y] = 2
                    maxV = max(minimax(state, piecesCountL+1, depth-1, sizeBoard, False), maxV)
                    state[x][y] = 0
        return maxV
    else:
        minV = 100000
        for x in range(sizeBoard):
            for y in range(sizeBoard):
                if state[x][y] == 0:
                    state[x][y] = 1
                    minV = min(minimax(state, piecesCountL+1, depth-1, sizeBoard, True), minV)
                    state[x][y] = 0
        return minV
    
def choosePiece(board, piecesCount, howDeep, sizeBoard = 3):
    bestMove = [0,0]
    currentValue = -1000000
    bestValue = -1000000
    for x in range(sizeBoard):
        for y in range(sizeBoard):
            if board[x][y] == 0:
                board[x][y] = 2
                piecesCount += 1
                currentValue = minimax(board, piecesCount, howDeep, sizeBoard, False)
                piecesCount -= 1
                board[x][y] = 0
                if currentValue > bestValue:
                    bestMove = [x, y]
                    bestValue = currentValue
    return bestMove
