def diagonalCheck(state, pos, dir=False, toDoCheck = 3):
    piece = -1
    j = 0
    if (state[pos[0]][pos[1]] >= 1):
        j = 1
        piece = state[pos[0]][pos[1]]
    for i in range(j, toDoCheck):
        if ((state[pos[0]+i][pos[1]+i] if dir else state[pos[0]-i][pos[1]+i]) != piece):
            return -1
    return piece

def horizontalVerticalCheck(state, i, j, dir=False, toDoCheck = 3):
    piece = -1
    if state[i][j] >= 1:
        piece = state[i][j]
    for k in range(toDoCheck):
        if (state[i+k if dir else i][j if dir else j+k] != piece):
            return -1
    return piece

def isFinished(state, sizeBoard=3, toDoCheck = 3):
    for i in range(sizeBoard-toDoCheck+1):
        for j in range(sizeBoard-toDoCheck+1):
            dig0 = diagonalCheck(state, [sizeBoard-1-i,j], False, toDoCheck)
            dig1 = diagonalCheck(state, [i,j], True, toDoCheck)
            if dig0 > -1:
                return dig0
            if dig1 > -1:
                return dig1

    for i in range(sizeBoard):
        for j in range(sizeBoard-toDoCheck+1):
            pos0 = horizontalVerticalCheck(state, j, i, True, toDoCheck)
            pos1 = horizontalVerticalCheck(state, i, j, False, toDoCheck)
            if pos0 > -1:
                return pos0
            if pos1 > -1:
                return pos1
    return -1