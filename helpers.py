def diagonalCheck(state, dir=False):
    piece = -1;
    if ((state[0][0] if dir else state[2][0]) >= 1):
        piece = (state[0][0] if dir else state[2][0])
    for i in range(3):
        if ((state[i][i] if dir else state[2-i][i]) != piece):
            return -1;
    return piece

def horizontalVerticalCheck(state, i, j, dir=False):
    piece = -1
    if state[i][j] >= 1:
        piece = state[i][j]
    for k in range(3):
        if (state[i+k if dir else i][j if dir else j+k] != piece):
            return -1;
    return piece

def isFinished(state):
    dig0 = diagonalCheck(state, False)
    if dig0 > -1:
        return dig0

    dig1 = diagonalCheck(state, True)
    if dig1 > -1:
        return dig1

    for i in range(3):
        pos = horizontalVerticalCheck(state, 0, i, True)
        if pos > -1:
            return pos
    for i in range(3):
        pos = horizontalVerticalCheck(state, i, 0, False)
        if pos > -1:
            return pos
    return -1
