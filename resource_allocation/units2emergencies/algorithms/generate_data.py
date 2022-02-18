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
import json 

all_specs = [    
    (100, 50, 2, 5),
    (100, 50, 4, 5),
    (100, 50, 5, 5),
    (500, 100, 3, 6),
    (500, 100, 4, 6),
    (500, 100, 5, 7),
    (500, 100, 5, 6),
    (500, 100, 7, 6),
    (1000, 200, 2, 9),
    (1000, 200, 3, 9),
    (1000, 200, 4, 9),
    (1000, 200, 5, 10),
    (1000, 200, 6, 10),
    (1000, 300, 3, 5),    
    (1000, 300, 3, 6),  
    (1000, 400, 3, 6),  
    (2000, 400, 3,15),    
    (2000, 400, 4,15),    
    (2000, 400, 5,15),    
    (2000, 400, 6,15),    
]
for i in tqdm.trange(len(all_specs)):
    input = Input.get_random_situation(n_emergencies=all_specs[i][0], n_service_locations=all_specs[i][1], n_personnel=10, n_units=all_specs[i][3], etypes=all_specs[i][2])
    
    
    with open("dataset/situation_"+ str(i+1) + ".json", "w") as f:
        json.dump(input.to_json(), f, indent=4)
    