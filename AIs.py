from helpers import isFinished
from obligatedMoves import isObligatedMove
def minimax(state, piecesCountL=0, depth=4, sizeBoard=1, alpha=0, beta=0, isMax=False):
    result = isFinished(state, sizeBoard)
    if result != -1:
        return -1*depth if result == 1 else 1
    if piecesCountL >= sizeBoard*sizeBoard or depth == 0:
        return 0
    
    if isMax:
        maxV = -100000
        obligatedVal = isObligatedMove(state, sizeBoard)
        if obligatedVal != -1:
            state[obligatedVal[0]][obligatedVal[1]] = 2
            maxV = max(minimax(state, piecesCountL+1, depth-1, sizeBoard, alpha, beta), maxV)
            state[obligatedVal[0]][obligatedVal[1]] = 0
            return maxV
        
        for x in range(sizeBoard):
            for y in range(sizeBoard):
                if state[x][y] == 0:
                    state[x][y] = 2
                    eval = minimax(state, piecesCountL+1, depth-1, sizeBoard, alpha, beta)
                    maxV = max(eval, maxV)
                    state[x][y] = 0
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        return maxV
        return maxV
    else:
        minV = 100000
        obligatedVal = isObligatedMove(state, sizeBoard, piece = 2)
        if obligatedVal != -1:
            state[obligatedVal[0]][obligatedVal[1]] = 1
            minV = min(minimax(state, piecesCountL+1, depth-1, sizeBoard, alpha, beta, True), minV)
            state[obligatedVal[0]][obligatedVal[1]] = 0
            return minV
        
        for x in range(sizeBoard):
            for y in range(sizeBoard):
                if state[x][y] == 0:
                    state[x][y] = 1
                    eval = minimax(state, piecesCountL+1, depth-1, sizeBoard, alpha, beta, True)
                    minV = min(eval, minV)
                    state[x][y] = 0
                    beta = min(beta, eval)
                    if beta <= alpha:
                        return minV  
        return minV
    
def choosePiece(board, piecesCount, howDeep, sizeBoard = 3):
    bestMove = [0,0]
    currentValue = -1000000
    bestValue = -1000000
    obligatedVal = isObligatedMove(board, sizeBoard)
    if obligatedVal != -1:
        return obligatedVal
    for x in range(sizeBoard):
        for y in range(sizeBoard):
            if board[x][y] == 0:
                board[x][y] = 2
                piecesCount += 1
                currentValue = minimax(board, piecesCount, howDeep, sizeBoard)
                piecesCount -= 1
                board[x][y] = 0
                if currentValue > bestValue:
                    bestMove = [x, y]
                    bestValue = currentValue
    return bestMove
