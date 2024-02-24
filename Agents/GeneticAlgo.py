# Genetic Algorithm to train a neural network to play the game of tris

import numpy as np
import MCTS.AIs as AIs
import random
from MCTS.AIs import NeuralAI
from main import TrisNxN, fight
from tqdm import tqdm
    
class GeneticAlgo:
    def __init__(self, num_sample, mut_rate=0.1):
        self.Ais = [NeuralAI(3,3, []) for i in range(num_sample)]
        self.tris = TrisNxN(800, 3, 3, False, AIs.RandomAI, NeuralAI, 0, 0)
        self.num_sample = num_sample
        self.mut_rate = mut_rate
        self.fitnessArray = np.zeros(num_sample)

    def fitness(self, sample):
        self.tris.playerAI = self.Ais[sample]
        #print("Setting playerAI...")
        play = fight(self.tris, 100)
        #print("Playing...")
        return (play[1]-play[0])/100
    
    def selection(self):
        size = len(self.Ais)
        self.fitnessArray = [self.fitness(i) for i in range(size)]
        self.Ais = [self.Ais[i] for i in np.argsort(self.fitnessArray)]
        self.Ais = self.Ais[int(len(self.Ais)*0.5):]

    def crossover(self):
        children = []
        size = len(self.Ais)
        for i in range(size//2):
            parent1 = random.choice(self.Ais)
            parent2 = random.choice(self.Ais)
            flattenedWeights1 = parent1.weights.flatten()
            flattenedWeights2 = parent2.weights.flatten()
            split = random.randint(0, len(flattenedWeights1))
            newWeights1 = np.concatenate((flattenedWeights1[:split] , flattenedWeights2[split:]))
            newWeights2 = np.concatenate((flattenedWeights2[:split] , flattenedWeights1[split:]))

            child1 = NeuralAI(3, 3, [])
            child1.weights = newWeights1.reshape(9, 9)
            child2 = NeuralAI(3, 3, [])
            child2.weights = newWeights2.reshape(9, 9)

            children.append(child1)
            children.append(child2)
        self.Ais = self.Ais + children
        
    def mutation(self):
        for i in range(self.num_sample):
            if random.random() < self.mut_rate:
                point = random.randint(0, 80)
                self.Ais[i].weights[point//9][point%9] = np.random.rand(1)[0]

    def train(self, num_generations):
        for i in tqdm(range(num_generations)):
            self.selection()
            self.crossover()
            self.mutation()
            #print(np.max(self.fitnessArray))
            if len(self.Ais) <= 1:
                break

if __name__ == '__main__':
    algo = GeneticAlgo(200)
    l = 0.0
    algo.train(1000)
    np.save('weights.npy', algo.Ais[np.argmax(algo.fitnessArray)].weights)
    #tris = TrisNxN(800, 3, 3, True, AIs.RandomAI, NeuralAI)
    #tris.timeSleep = 0.4
    #tris.playerAI = algo.Ais[np.argmax(algo.fitnessArray)]
    #print(fight(tris, 10))
    