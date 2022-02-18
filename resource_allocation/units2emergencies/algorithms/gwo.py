import sys, os
sys.path.insert(1, '../')
import time, tqdm
import copy
import numpy as np
import pandas as pd
from operator import attrgetter
from utils import Emergency, EmergencyServiceLocation, Distribution, Input, Unit
from situations import situation1, situation2

# function to load a json file as a dict
def load_json(path):
    with open(path) as json_file:
        json_data = json.load(json_file)
    return json_data

class Wolf:
    def __init__(self, input_situation):
        # current solution
        self.distribution = Distribution(input_situation)
        self.fitness = self.distribution.fitness()

        # self.pbest_value = float('inf')
        # self.pbest_solution = self.distribution
        # self.velocity = {} 
        # for i in self.distribution.input_situation.eTypes:
        #     try:
        #         self.velocity[i] = np.zeros(len(self.distribution.vectors[i]))
        #     except:
        #         self.velocity[i] = [np.zeros(len(self.distribution.vectors[i]))]

class GWO:
    def __init__(self, input_situation, iterations, population, verbose=True, step=10, save=False):
        self.iterations = iterations  # max of iterations
        self.population = population  # size population
        self.verbose = verbose
        self.step = step
        self.progress = []
        self.input_situation = input_situation
        self.save=save
        
        wolves = []
        if not self.verbose:
            r = range(population)
        else:
            r = tqdm.trange(population, desc='Initializing')
        for _ in r:
            wolves.append(Wolf(self.input_situation))
            
        self.wolves = wolves
        self.wolves.sort(key=attrgetter('fitness'), reverse=True)
        self.alpha, self.beta, self.gamma = copy.copy(self.wolves[:3])
        print("Initial alpha fitness = ", self.alpha.fitness)
        self.progress = []    
        
    def run(self):
        if self.verbose:
            r = tqdm.trange(self.iterations)
        else:
            r = range(self.iterations)
            
        for iter in r:
            # calculate a
            a = 2 - iter * (2 / self.iterations)
            
            for j in range(len(self.wolves)):
                for i in self.wolves[j].distribution.input_situation.eTypes: 
                
                    A1, A2, A3 = a * (2 * np.random.random() - 1), a * (2 * np.random.random() - 1), a * (2 * np.random.random() - 1)
                    C1, C2, C3 = 2 * np.random.random(), 2*np.random.random(), 2*np.random.random()
                    dim = len(self.wolves[j].distribution.vectors[i])
                    
                    X1 = [0.0 for i in range(dim)]
                    X2 = [0.0 for i in range(dim)]
                    X3 = [0.0 for i in range(dim)]
                    Xnew = [0.0 for i in range(dim)]
                    # print(self.alpha.distribution.vectors[i][0])
                    for k in range(dim):
                        X1[k] = self.alpha.distribution.vectors[i][k] - A1 * abs(C1 - self.alpha.distribution.vectors[i][k] - self.wolves[i].distribution.vectors[i][k])
                        X2[k] = self.beta.distribution.vectors[i][k] - A2 * abs(C2 -  self.beta.distribution.vectors[i][k] - self.wolves[i].distribution.vectors[i][k])
                        X3[k] = self.gamma.distribution.vectors[i][k] - A3 * abs(C3 - self.gamma.distribution.vectors[i][k] - self.wolves[i].distribution.vectors[i][k])
                        Xnew[k]+= X1[k] + X2[k] + X3[k]
                    
                    # if r == print(Xnew)
                    for l in range(dim):
                        Xnew[l]/=3.0
                        
                    # print(Xnew)
                    candidate = copy.copy(self.wolves[j])
                    
                    candidate.distribution.vectors[i] = Xnew
                    candidate.distribution.updateVector()
                    candidate_fitness = candidate.distribution.fitness()
                    
                    if candidate_fitness > self.wolves[j].fitness:
                        self.wolves[j] = candidate
                        self.wolves[j].fitness = candidate_fitness
                    
                    
            self.wolves.sort(key=attrgetter('fitness'), reverse=True)
            self.alpha, self.beta, self.gamma = copy.copy(self.wolves[:3])
            self.progress.append(self.alpha.fitness)
                
                
    def getBestFitness(self):
        # return self.gbest_solution.sequence_vector
        return self.alpha.fitness
    
    def getBest(self):
        return self.alpha

    def getProgress(self):
        return self.progress