import sys, os
sys.path.insert(1, '../')
import time, tqdm
import copy
import numpy as np
import pandas as pd
from operator import attrgetter
from utils import Emergency, EmergencyServiceLocation, Distribution, Input, Unit
from situations import situation1, situation2
from pso import PSO
from gwo import GWO
import statistics


input_a = Input.from_situation(situation1)
# n_emergencies=500
# n_service_locations=150
# n_personnel=10
# n_units=10
# etypes=5
# # input_a = Input.get_random_situation(n_emergencies=n_emergencies, n_service_locations=n_service_locations, n_personnel=n_personnel, n_units=n_units, x = (-1000, 1000), y = (-1000, 1000), etypes=etypes)
# print(n_emergencies, n_service_locations, etypes)


# for i in range(1):
#     results = []

#     for _ in tqdm.trange(10):
#         pso = PSO(input_a, iterations=100, population=200, save=False, verbose=False)
#         pso.run()
#         # print(pso.getBest())
#         # print(pso.getBestFitness())
#         results.append(pso.getBestFitness())
        
#     # df = pd.DataFrame(results)
#     # df.to_csv('results.csv')
#     print("Worst= ", max(results))
#     print("Best= ", min(results))
#     print("Avg= ", statistics.mean(results))
#     print("Std= ", statistics.stdev(results))

gwo = GWO(input_a, iterations=1000, population=200, save=False, verbose=True)
gwo.run()

print(gwo.getBestFitness())

pso = PSO(input_a, iterations=1000, population=200, save=False, verbose=True)
pso.run()
print(pso.getBestFitness())