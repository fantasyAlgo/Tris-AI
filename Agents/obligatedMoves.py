def diagonalPreCheck(state, pos, dir=False, toDoCheck = 3, piece = 1):
    missingPosXY = []
    numCheck = False
    for i in range(toDoCheck):
        if ((state[pos[0]+i][pos[1]+i] if dir else state[pos[0]-i][pos[1]+i]) != piece):
            if (not numCheck and (state[pos[0]+i][pos[1]+i] if dir else state[pos[0]-i][pos[1]+i]) == 0):
                missingPosXY = [pos[0]+i, pos[1]+i] if dir else [pos[0]-i, pos[1]+i]
                numCheck = True
            else: return [-1, -1]
    return missingPosXY

def horizontalVerticalPreCheck(state, i, j, dir=False, toDoCheck = 3, piece = 1):
    missingPosXY = []
    numCheck = False
    for k in range(toDoCheck):
        if (state[i+k if dir else i][j if dir else j+k] != piece):
            #print(f"{i}, {j} in this time, with state {state[i+k if dir else i][j if dir else j+k]}")
            if (not numCheck and state[i+k if dir else i][j if dir else j+k] == 0):
                missingPosXY = [i+k if dir else i, j if dir else j+k]
                numCheck = True
            else: return [-1, -1]
    return missingPosXY

def isObligatedMove(state, sizeBoard=3, toDoCheck = 3, piece = 1):
    for i in range(sizeBoard-toDoCheck+1):
        for j in range(sizeBoard-toDoCheck+1):
            dig0 = diagonalPreCheck(state, [sizeBoard-1-i,j], False, toDoCheck, piece)
            dig1 = diagonalPreCheck(state, [i,j], True, toDoCheck, piece)
            if len(dig0) > 1 and dig0[0] > -1:
                return dig0
            if len(dig1) > 1 and dig1[0] > -1:
                return dig1

    for i in range(sizeBoard):
        for j in range(sizeBoard-toDoCheck+1):
            dig0 = horizontalVerticalPreCheck(state, j, i, True, toDoCheck, piece)
            dig1 = horizontalVerticalPreCheck(state, i, j, False, toDoCheck, piece)
            if len(dig0) > 1 and dig0[0] > -1:
                return dig0
            if len(dig1) > 1 and dig1[0] > -1:
                return dig1
    return -1