
# PSO No inertia

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

c1 = 2
c2 = 2

class Particle:

    def __init__(self, input_situation):
        # current solution
        self.distribution = Distribution(input_situation)

        self.pbest_value = float('inf')
        self.pbest_solution = self.distribution
        self.stagnancy = 0
        self.velocity = {} 
        for i in self.distribution.input_situation.eTypes:
            try:
                self.velocity[i] = np.zeros(len(self.distribution.vectors[i]))
            except:
                self.velocity[i] = [np.zeros(len(self.distribution.vectors[i]))]


    # def __str__(self):
    #     return ("My order is  " + str(self.SequenceVector(self)) + " my pbest is " + str(self.SequenceVector(self.pbest_solution, self.reads)))

    def move(self):
        for i in self.distribution.input_situation.eTypes:
            self.distribution.vectors[i] = self.distribution.vectors[i] + self.velocity[i]
        
        # self.distribution.sequence_vector = self.distribution.sequence_vector + self.velocity
        self.distribution.updateVector()


class PSO:

    def __init__(self, input_situation, iterations, population, verbose=True, step=10, save=False):
        self.iterations = iterations  # max of iterations
        self.population = population  # size population
        self.verbose = verbose
        self.step = step
        self.progress = []
        self.input_situation = input_situation
        self.save=save

        # initialized with a group of random particles (solutions)
        particles = []
        if self.verbose:
            r = range(population)
        else:
            r = tqdm.trange(population, desc='Initializing')
        for _ in range(population):
            particles.append(Particle(self.input_situation))

        # checks if exists any solution
        if not particles:
            print('Initial population empty! Try run the algorithm again...')
            sys.exit(1)

        # creates the particles
        self.particles = particles

        # updates "population"
        self.population = len(self.particles)
        self.gbest_value = float('inf')
        self.gbest_solution = Particle(self.input_situation).distribution

    def print_particles(self):
        for particle in self.particles:
            print(particle)


    def set_pbest(self):
        # Minimize
        for particle in self.particles:
            fitness_cadidate = particle.distribution.fitness()
            if(particle.pbest_value > fitness_cadidate):
                particle.pbest_value = fitness_cadidate
                particle.pbest_solution = particle.distribution
            else:
                particle.stagnancy += 1
                
        # print(particle.pbest_solution.fitness())

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = particle.distribution.fitness()
            if(self.gbest_value > best_fitness_cadidate):
                self.gbest_value = best_fitness_cadidate
                self.gbest_solution = particle.distribution

    def move_particles(self):
        for particle in self.particles:
            for i in particle.distribution.input_situation.eTypes: 
                a = particle.velocity[i]  # No Inertia
                b = (c1*np.random.random()) * \
                    (particle.pbest_solution.vectors[i] - particle.distribution.vectors[i])  # Cognitive
                # print(b)
                c = (np.random.random()*c2) * \
                    (self.gbest_solution.vectors[i] - particle.distribution.vectors[i])  # Social
                particle.velocity[i] = a+b+c
            particle.move()

    def run(self):

        # for each time step (iteration)
        if self.verbose:
            r = tqdm.trange(self.iterations)
        else:
            r = range(self.iterations)
            
        for step in r:
            self.set_pbest()
            self.set_gbest()
            self.progress.append(self.gbest_value)
            self.move_particles()
            if self.save:
                self.getBest().plot(save=True, path=str(step)+'.png')

    # def getString(self):
    #     a = (Particle.SequenceVector(self.gbest_solution, self.reads))
    #     # b = (self.score(Particle.SequenceVector(self.gbest_solution, self.reads)))
    #     # print('gbest: {} | cost: {}\n'.format(a, b) )
    #     return a

    # def getScore(self):
    #     b = (self.score(Particle.SequenceVector(self.gbest_solution, self.reads)))
    #     return b
    
    def getBestFitness(self):
        # return self.gbest_solution.sequence_vector
        return self.gbest_value
    
    def getBest(self):
        return self.gbest_solution

    def getProgress(self):
        return self.progress



# # print(reads)

# pso = PSO(reads1, iterations=10, population=100)
# pso.run()
# pso.getString()

# # shows the global best particle
# a = (Particle.SequenceVector(pso.gbest_solution, pso.reads))
# b = (pso.score(Particle.SequenceVector(pso.gbest_solution, pso.reads)))
# print('gbest: {} | cost: {}\n'.format(a, b) )

# print("Final Sequence::",consensus(a))

input_a = Input.from_situation(situation1)
# input_a = Input.get_random_situation(100, 50, 10, x = (-1000, 1000), y = (-1000, 1000))
# input_a.plot()
pso = PSO(input_a, iterations=100, population=10, save=False)
pso.run()
print(pso.getBest())
print(pso.getBestFitness())
# pso.getBest().plot()

import pandas as pd
df = pd.DataFrame(pso.getProgress())
df.to_csv('progress.csv')
# df.plot()