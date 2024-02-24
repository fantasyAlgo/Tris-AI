import numpy as np
import copy

def UCBValue(node, parent_visit_count, c=2.0):
    if node.visit_count == 0:
        return float('inf')
    return node.value + c*np.sqrt(2*np.log(parent_visit_count)/node.visit_count)
class Node:
    prior = 0
    value = 0
    children = []
    action = 0
    state = 0
    parent = 0
    piecesCount = 0;
    visit_count = 0
    def __init__(self, prior,value,state, pos, piecesCount, piece, parent):
        self.prior = prior
        self.value = value
        self.visit_count = 0
        self.children = []
        self.action = pos
        self.state = state
        self.piece = piece
        self.parent = parent
        self.piecesCount = piecesCount
    def expand(self):
        #print("Expanding")
        #if self.parent != None:
        #    print(self.parent.state)
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    self.state[i][j] = 1+self.piece%2
                    #print(self.state, self.piecesCount+1)
                    self.children.append(Node(0,0, copy.deepcopy(self.state), [i,j], self.piecesCount+1, 1+self.piece%2, self))
                    self.state[i][j] = 0
        #print(len(self.children))

    def backpropagate(self, value):
        self.value += value
        self.visit_count += 1
        if self.parent != None:
            self.parent.backpropagate(-value)

    def bestChild(self):
        if (self.children == []): return self
        best = self.children[0]
        for child in self.children:
            if UCBValue(child, self.visit_count) > UCBValue(best, self.visit_count):
                best = child
        return best