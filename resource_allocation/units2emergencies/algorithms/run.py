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
import json, multiprocessing


def get_results(dataset):
    print(dataset)
    f = open(file="dataset/"+dataset, mode="r")
    data = json.load(f)
    f.close()
    input = Input.from_situation(data)
    res = []
    times = []
    print("PSO")
    prog = []
    for i in range(10):
        start = time.time()
        pso = PSO(input, iterations=10, population=20, verbose=True, step=10, save=False)
        pso.run()
        end = time.time()
        res.append(pso.getBestFitness())
        times.append(end-start)
        prog.append(pso.getProgress())
        
    progress = [statistics.mean([prog[x][i] for x in range(len(prog))]) for i in range(len(prog[0]))]
        
    try:
        prog_df = pd.read_csv("results/progress/"+dataset+".csv")
        prog_df['PSO'] = progress
    except:
        prog_df = pd.DataFrame(progress, columns = ['PSO'])
    
    prog_df.to_csv("results/progress/"+dataset+".csv")
    
    pso_result = {"situation": [dataset], "mean": [statistics.mean(res)], "std": [statistics.stdev(res)], "best": [max(res)], "worst": [min(res)], "avg_time": [statistics.mean(times)]}
    new = pd.DataFrame(pso_result, columns=["situation","mean", "std", "best", "worst", "avg_time"])
    try:
        pso_df = pd.read_csv("results/pso.csv")
        final = pd.concat(objs=[pso_df, new], axis=0).to_csv("results/pso.csv", index=False)
        final.to_csv("results/pso.csv", index=False)
    except:
        new.to_csv("results/pso.csv", index=False)
        
        
    
    res = []
    times = []
    print("GWO")
    prog = []
    for i in range(10):
        start = time.time()
        gwo = GWO(input, iterations=10, population=20, verbose=True, step=10, save=False)
        gwo.run()
        end = time.time()
        res.append(gwo.getBestFitness())
        prog.append(gwo.getProgress())
        times.append(end-start)
    progress = [statistics.mean([prog[x][i] for x in range(len(prog))]) for i in range(len(prog[0]))]
    prog_df = pd.read_csv("results/progress/"+dataset+".csv")
    prog_df['GWO'] = progress
    # except:
    #     prog_df = pd.DataFrame(progress, columns = ['GWO'])
    
    prog_df.to_csv("results/progress/"+dataset+".csv")
        
    gwo_result = {"situation": [dataset], "mean": [statistics.mean(res)], "std": [statistics.stdev(res)], "best": [max(res)], "worst": [min(res)], "avg_time": [statistics.mean(times)]}
    
    new = pd.DataFrame(gwo_result, columns=["situation", "mean", "std", "best", "worst", "avg_time"])
    try:
        gwo_df = pd.read_csv("results/gwo.csv")
        final = pd.concat(objs=[gwo_df, new], axis=0).to_csv("results/gwo.csv", index=False)
        final.to_csv("results/gwo.csv", index=False)
    except:
        new.to_csv("results/gwo.csv", index=False)








# if __name__ == '__main__':
#     multiprocessing.freeze_support()
#     datasets = os.listdir("dataset/")
#     datasets.sort()


#     a_pool = multiprocessing.Pool()

#     results = a_pool.map(func=get_results, iterable=datasets)


#     # Run `sum_up_to` 10 times simultaneously

#     print(results)

datasets = os.listdir("dataset/")
datasets.sort()
get_results(datasets[11])