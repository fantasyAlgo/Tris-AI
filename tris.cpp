#include <iostream>
#include <utility>
#include <vector>
using namespace std;

int N = 3;
//int matrix[3][3] = {{0}};
vector<vector<int>> matrix(4, vector<int>(4));
int piecesCount = 0;

const int howDeep = 7;
void printTris(){
    for (int i = 0; i < 3; i++) {
        cout << "| ";
        for (int j = 0; j < 3; j++){
            if (matrix[i][j] == 0)
                cout << "*" << " ";
            if (matrix[i][j] == 1)
                cout << "X" << " ";
            if (matrix[i][j] == 2)
                cout << "O" << " ";
        }
        cout << "|" << endl;
    }
}

void printTris(vector<vector<int>> state){
    for (int i = 0; i < 3; i++) {
        cout << "| ";
        for (int j = 0; j < 3; j++){
            if (state[i][j] == 0)
                cout << "*" << " ";
            if (state[i][j] == 1)
                cout << "X" << " ";
            if (state[i][j] == 2)
                cout << "O" << " ";
        }
        cout << "|" << endl;
    }
}

int diagonalCheck(vector<vector<int>> state, bool dir = 0){
    int piece = -1;
    if ((dir ? state[0][0] : state[2][0]) >= 1)
        piece = (dir ? state[0][0] : state[2][0]);

    for (int i = 0; i < 3; i++){
        if ((dir ? state[i][i] : state[2-i][i]) != piece)
            return -1;
    }
    return piece;
}

// This function assume that either i or j is a 0, i.e i,j is in the border (for the 3x3 case)
// dir = false is hor, otherwise vertical 
int horizontalVerticalCheck(vector<vector<int>> state, int i, int j, bool dir = false){
    int piece = -1;
    if (state[i][j] >= 1) piece = state[i][j];
    for (int k = 0; k < 3; k++){
        if (state[dir ? i+k : i][dir ? j : j+k] != piece) return -1;
    }
    return piece;
}
int isFinished(vector<vector<int>> state){
    int dig0 = diagonalCheck(state, 0);
    if (dig0 > -1) return dig0;

    int dig1 = diagonalCheck(state, 1);
    if (dig1 > -1) return dig1;

    int pos;
    for (int i = 0; i < 3; i++){
        pos = horizontalVerticalCheck(state, 0, i, 1);
        if (pos > -1) return pos;
    }
    for (int i = 0; i < 3; i++){
        pos = horizontalVerticalCheck(state, i, 0, 0);
        if (pos > -1) return pos;
    }
    return -1;
}


// To-do in vs
int minimax(vector<vector<int>> state, int piecesCount = 0, int depth = 4, bool maxPlayer = 0){
    if (piecesCount >= 9 || depth == 0)
        return 0;
    int result = isFinished(state);
    //printTris(state);
    if (result != -1)
        return (result == 1 ? -1*(9-piecesCount+1) : 1);

    if (maxPlayer){
        int maxV = -100000;
        for (int x = 0; x < 3; x++){
            for (int y = 0; y < 3; y++){
                if (state[x][y] == 0){
                    state[x][y] = 2;
                    maxV = max(minimax(state, piecesCount+1, depth-1, 0), maxV);
                    state[x][y] = 0;
                }
            }
        }
        return maxV;
    }else{
        int minV = 100000;
        for (int x = 0; x < 3; x++){
            for (int y = 0; y < 3; y++){
                if (state[x][y] == 0){
                    state[x][y] = 1;
                    minV = min(minimax(state, piecesCount+1, depth-1, 1), minV);
                    state[x][y] = 0;
                }
            }
        }
        return minV;
    }
}
void choosePiece(){
    pair <int, int> bestMove;
    int currentValue;
    int bestValue = -1000000;
    for (int x = 0; x < 3; x++){
        for (int y = 0; y < 3; y++){
            if (matrix[x][y] == 0){
                matrix[x][y] = 2;
                piecesCount += 1;
                currentValue = minimax(matrix, piecesCount, howDeep, 0);
                piecesCount -= 1;
                matrix[x][y] = 0;
                //cout << bestMove.first << ", " << bestMove.second << ", val: " << currentValue << endl;
                if (currentValue > bestValue){
                    bestMove = {x,y};
                    bestValue = currentValue;
                }
            }
        }
    }
    cout << "value: " << bestValue << endl;
    matrix[bestMove.first][bestMove.second] = 2;
}
int main(){
    int i, j;
    printTris();
    // isFinished(matrix) == -1
    while (isFinished(matrix) == -1 && piecesCount < 9){
        cout << "Choose the piece in i-j coord:" << endl;
        cin >> i >> j;
        matrix[i][j] = 1;
        piecesCount += 1;
        if (piecesCount < 9 && isFinished(matrix) == -1)
            choosePiece();
        printTris();
        piecesCount += 1;
    }
    int gameEnd = isFinished(matrix);
    if (gameEnd != -1)
        cout << "Player " << (gameEnd == 1 ? "X" : "O") << " has won!" << endl;
    if (piecesCount >= 9)
        cout << "Draw!" << endl;
}
