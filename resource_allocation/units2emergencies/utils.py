import numpy as np
import matplotlib.pyplot as plt
import tqdm
import random
import math, statistics
import json
# Severity: [1, 2, 3, 4, 5]
# Type: [1, 2, 3]
# Status: [1, 2, 3] :: [Available, In route, Returning]
# Distance: Using Benchmark Functions
# Amount of Personnel : int

import datetime
import decimal


# Signum Function
def sgn(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1

# Function to calculate euclidian distance between 2 points
def euclidian_distance(point1, point2):
    """
    Distance

    Args:
        point1 (tuple): point1
        point2 (tuple): point2

    Returns:
        [float]: distance
    """    
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

class EmergencyServiceLocation:
    
    def __init__(self, point, Etype, personnel_avaliable, n_units, unit_severities):
        self.point = point
        self.Etype = Etype
        self.personnel_avaliable = personnel_avaliable
        self.n_units = n_units
        self.available = []
        self.in_route = []
        self.returning = []
        self.unit_severities = unit_severities
        self.unitsFromSeverity()
        
    def addUnits(self, units):
        self.available.extend(units)
        
    def unitsFromSeverity(self):
        for i in self.unit_severities:
            self.available.append(Unit(self, self.Etype, 4, i))
    
    def to_json(self):
        return {
            "point": self.point,
            "Etype": self.Etype,
            "personnel_avaliable": self.personnel_avaliable,
            "n_units": self.n_units,
            "unit_severities": self.unit_severities.tolist()
        }

class Unit:

    def __init__(self, serviceLocation, Etype, max_personnel, severity_limit):
        self.home = serviceLocation
        self.Etype = Etype
        self.max_personnel = max_personnel
        self.severity_limit = severity_limit
    

class Emergency:
    
    def __init__(self, point, Etype, severity):
        self.point = point
        self.severity = severity
        self.Etype = Etype
        
    def to_json(self):
        return {
            "point": self.point,
            "severity": self.severity,
            "Etype": self.Etype
        }
    

class Input:
    
    def __init__(self, emergencies, service_locations, units, reserve=0.2, eTypes = []):
        self.emergencies = emergencies
        self.service_locations = service_locations
        self.units = units
        self.eTypes = eTypes
        self.reserve = reserve
        self.emergencyMap = {}
        self.unitMap = {}
        for emergency in emergencies:
            try:
                self.emergencyMap[emergency.Etype].append(emergency)
            except:
                self.emergencyMap[emergency.Etype] = [emergency]
        for unit in units:
            try:
                self.unitMap[unit.Etype].append(unit)
            except:
                self.unitMap[unit.Etype] = [unit]
        # self.originalVector = originalVector
        '''
        Other Approach: origVector: vector of size units, contains n None values, where n is len(unuts)-len(emergencies). Then simple optimization.
        '''
        
    # Method to create Input object from situation dict
    @classmethod
    def from_situation(cls, situation):
        # load the json file
        json_data = situation
        # load the json data into objects
        json_emergencies = json_data["emergencies"]
        json_service_locations = json_data["service_locations"]
        # json_units = json_data["units"]
        json_reserve = json_data["reserve"]
        json_eTypes = json_data["eTypes"]
        # create the emergency objects
        emergency_objs = [Emergency(**json_emergencies[i]) for i in range(len(json_emergencies))]
        # create the service location objects
        service_location_objs = [EmergencyServiceLocation(**json_service_locations[i]) for i in range(len(json_service_locations))]
        # create the unit objects
        unit_objs = []
        for loc in service_location_objs:
            unit_objs.extend(loc.available)
        # create the input object
        return cls(
            emergencies = emergency_objs,
            service_locations = service_location_objs,
            units = unit_objs,
            reserve = json_reserve,
            eTypes = json_eTypes,
        )
        
    def to_json(self):
        all_emergencies = []
        for e in self.emergencies:
            all_emergencies.append(e.to_json())
            
        all_locs = []
        for loc in self.service_locations:
            all_locs.append(loc.to_json())
        
        return {"emergencies": all_emergencies, "service_locations": all_locs, "reserve": self.reserve, "eTypes": self.eTypes}
        

        
    # @staticmethod
    # # Input Object from JSON file
    # def from_json(path):
        # Load JSON file
        json_data = load_json(path)
        # Initialize data
        emergencies = []
        service_locations = []
        units = []
        eTypes = []
        # Iterate through JSON file and create objects
        for i in range(len(json_data['emergencies'])):
            emergencies.append(Emergency(json_data['emergencies'][i][0], json_data['emergencies'][i][1], json_data['emergencies'][i][2]))
        for i in range(len(json_data['service_locations'])):
            service_locations.append(EmergencyServiceLocation(json_data['service_locations'][i], json_data['eTypes'][i], json_data['personnel_avaliable'][i], json_data['n_units'][i]))
        for i in range(len(json_data['units'])):
            units.append(Unit(service_locations[json_data['units'][i][0]], json_data['units'][i][1], json_data['units'][i][2], json_data['units'][i][3]))
        
        # Initialize Input Object
        return Input(emergencies, service_locations, units, json_data['reserve'], json_data['eTypes'])

        
        
        
    @staticmethod
    def get_random_situation(n_emergencies, n_service_locations, n_personnel, n_units = 5, x = (-100, 100), y = (-100, 100), verbose = False, etypes=3):
        """
        TODO: Needs to be modified
        Random Landscape

        Args:
            n_emergencies ([int]): Number of Emergencies
            n_service_locations ([int]): Number of Service Locations
            n_personnel ([int]): Number of personnel
            n_units (int, optional): Number of units. Defaults to 5.
            x (tuple, optional): x-axis limits. Defaults to (-100, 100).
            y (tuple, optional): y-axis limits. Defaults to (-100, 100).

        Returns:
            [Input]: Situation for optimial resource allocation
        """        
        service_locations = []
        emergencies = []
        eTypes = []
        units = []
        if verbose:
            r = tqdm.trange(n_emergencies)
        else:
            r = range(n_emergencies)
        
        for _ in r:
            etype = np.random.randint(1, etypes)
            emergencies.append(Emergency(point=(np.random.randint(x[0], x[1]),np.random.randint(y[0], y[1])), Etype=etype, severity=np.random.randint(1, 5)))
            eTypes.append(etype)
        eTypes = list(set(eTypes))
        
        if verbose:
            r = tqdm.trange(n_service_locations, leave = False)
        else:
            r = range(n_service_locations)
        
        for _ in r:
            service_locations.append(EmergencyServiceLocation(point=(np.random.randint(x[0], x[1]),np.random.randint(y[0], y[1])), Etype=np.random.randint(1, etypes), personnel_avaliable=np.random.randint(2, n_personnel), n_units=np.random.randint(1, n_units), unit_severities=np.random.randint(1, 5, size=n_units)))
        
        if verbose:
            r = tqdm.tqdm(service_locations, leave = False)
        else:
            r = service_locations
        
        for loc in r:
            loc_units = []
            for _ in range(loc.n_units):
                loc_units.append(Unit(serviceLocation=loc, Etype=loc.Etype, max_personnel=np.random.randint(1, loc.personnel_avaliable), severity_limit=np.random.randint(1, 5)))
            loc.addUnits(loc_units)
            units.extend(loc_units)

        return Input(emergencies=emergencies, service_locations=service_locations, units=units, eTypes=eTypes)
    
    def plot(self) :
        '''
        Function to plot points
        '''
        x = []
        y = []

        for i in range(len(self.service_locations)):
            # Use matplotlib to plot x, y of each point
            x.append(self.service_locations[i].point[0])
            y.append(self.service_locations[i].point[1])
            # plt.plot(self.service_locations[i].point[0], self.service_locations[i].point[1],'bo', label='Service Locations')
        plt.scatter(x, y, c='b', label='Service Locations', marker='o')
        
        x = []
        y = []
        for i in range(len(self.emergencies)):
            # Use matplotlib to plot x, y of each point
            x.append(self.emergencies[i].point[0])
            y.append(self.emergencies[i].point[1])
            # plt.plot(self.emergencies[i].point[0], self.emergencies[i].point[1], 'rv', label='Emergencies')
        plt.scatter(x, y, c='r', label='Emergencies', marker='v')
        plt.legend()

        # plt.tight_layout(rect=[0,0,0.75,1])

        plt.show()
    
class Distribution:
    
    def __init__(self, input_situation, **kwargs):
        self.input_situation = input_situation
        self.alloted_units = []
        self.vectors = {}
        self.allocatedUnits = {}
        for i in input_situation.eTypes:
            self.vectors[i] = np.random.uniform(-10, 10, len(input_situation.emergencyMap[i]))
            self.allocatedUnits[i] = random.sample(input_situation.unitMap[i], len(input_situation.emergencyMap[i]))
        # self.sequence_vector = kwargs.pop('sequence_vector', np.random.uniform(-10, 10, len(input_situation.emergencies)))
        # self.alloted_units = kwargs.pop('alloted_units', random.sample(input_situation.units, len(input_situation.emergencies)))
        # self.vector = self.getVector()
        self.allotment = self.getVectors()
        
    # def reset(self):
    #     self.alloted_units = random.sample(self.input_situation.units, len(self.input_situation.emergencies))
        
    def checkConstraints(self):
        for i in range(len(self.vector)):
            if self.input_situation.emergencies[i].Etype != self.alloted_units[i].Etype:
                return False
            
        # # TODO: Add check for reserve
        # severities = []
        # for i in range(len(self.input_situation.emergencies)):
        #     severities.append(self.input_situation.emergencies[i].severity)
        # mean = statistics.mean(severities)
        # std = statistics.stdev(severities)
        
        
        return True
            

        
    def getVectors(self):
        """
        Applies the SPV rule and returns a list of units allocated in order to the emergencies in the input_situation

        Returns:
            [list]: sequence vector
        """        
        dist = {}
        for i in self.input_situation.eTypes:
                sorted_indices = np.argsort(self.vectors[i])
                for j in sorted_indices:
                    
                    try:    
                        dist[i].append(self.allocatedUnits[i][j])
                    except:
                        dist[i] = []
                        dist[i].append(self.allocatedUnits[i][j])
        
        return dist
    
    def fitness(self):
        """
        Function to calculate fitness of the Distribution
        To be minimized
        Constraints:
            1. Number of units alloted must be equal to number of Emergencies
            2. Each emergency must be assigned to a unit
            3. Each active unit must be assigned to one unique emergency
            
            Use ratio of more severe emergencies to determine exact reserve threshold

        Returns:
            [float]: Fitness of the distribution
        """     
        dist_dict = {}
        severity_diff_dict = {}
        dist_factor = 0
        severity_factor = 0
        # for unit in self.allotment:
        #     dist_dict[unit] = euclidian_distance(unit.home.point, self.allotment[unit].point)
        #     dist_factor += dist_dict[unit] * (unit.severity_limit - self.allotment[unit].severity)
        
        for i in self.input_situation.eTypes:
            # Allotment of one etype
            for j in range(len(self.allotment[i])):
                unit = self.allotment[i][j]
                distance = euclidian_distance(unit.home.point, self.input_situation.emergencyMap[i][j].point)
                dist_factor += distance * (math.e ** (self.input_situation.emergencyMap[i][j].severity - unit.severity_limit))
        
        
        
        # distribution = self.vector
        # for i in range(len(distribution)):
        #     dist_dict[distribution[i]] = euclidian_distance(distribution[i].home.point, self.input_situation.emergencies[i].point)
            
        #     severity_diff_dict[distribution[i]] = self.input_situation.emergencies[i].severity - distribution[i].severity_limit
            
        #     dist_factor += dist_dict[distribution[i]] * (math.e ** (self.input_situation.emergencies[i].severity -  distribution[i].severity_limit))
        #     # print(self.input_situation.emergencies[i].Etype, distribution[i].Etype)
        #     if self.input_situation.emergencies[i].Etype != distribution[i].Etype:
        #         dist_factor = float('inf')
        #         break
            '''
            e = 5
            u = 3
            
            diff = e - u = 2
            e ^ diff = e ^ 2
            
            e = 3
            u = 5
            
            e^-2, e^-1, e^0, e^1, e^2
            
            '''
            
        # print(dist_factor)
        return dist_factor
    
    def updateVector(self):
        self.allotment = self.getVectors()
    
    def plot(self, save=False, path=''):
        markers = [["ro", "bo"], ["rv", "bv"]]
        for i in range(len(self.input_situation.service_locations)):
            # Use matplotlib to plot x, y of each point
            plt.plot(self.input_situation.service_locations[i].point[0], self.input_situation.service_locations[i].point[1], markers[0][self.input_situation.service_locations[i].Etype-1])
        for i in range(len(self.input_situation.emergencies)):
            # Use matplotlib to plot x, y of each point
            plt.plot(self.input_situation.emergencies[i].point[0], self.input_situation.emergencies[i].point[1], markers[1][self.input_situation.emergencies[i].Etype-1])
        
        for i in self.input_situation.eTypes:
            for j in range(len(self.allotment[i])):
                unit = self.allotment[i][j]
                x_val = [unit.home.point[0], self.input_situation.emergencyMap[i][j].point[0]]
                y_val = [unit.home.point[1], self.input_situation.emergencyMap[i][j].point[1]]
                # Use matplotlib to plot x, y of each point
                plt.plot(x_val, y_val)
                # plt.text(x_val, y_val, str(i))
                
        
        
        # for i in range(len(self.vector)):
        #     x_val = [self.vector[i].home.point[0], self.input_situation.emergencies[i].point[0]]
        #     y_val = [self.vector[i].home.point[1], self.input_situation.emergencies[i].point[1]]
        #     # Use matplotlib to plot x, y of each point
        #     plt.plot(x_val, y_val)
        #     # plt.text(x_val, y_val, str(i))
        if save:
            plt.savefig(path)
        else:
            plt.show()
        plt.close()
      
    
    
    def plotOld(self, save=False, path=''):
        markers = [["ro", "bo"], ["rv", "bv"]]
        for i in range(len(self.input_situation.service_locations)):
            # Use matplotlib to plot x, y of each point
            plt.plot(self.input_situation.service_locations[i].point[0], self.input_situation.service_locations[i].point[1], markers[0][self.input_situation.service_locations[i].Etype-1])
        for i in range(len(self.input_situation.emergencies)):
            # Use matplotlib to plot x, y of each point
            plt.plot(self.input_situation.emergencies[i].point[0], self.input_situation.emergencies[i].point[1], markers[1][self.input_situation.emergencies[i].Etype-1])
        
        for i in range(len(self.vector)):
            x_val = [self.vector[i].home.point[0], self.input_situation.emergencies[i].point[0]]
            y_val = [self.vector[i].home.point[1], self.input_situation.emergencies[i].point[1]]
            # Use matplotlib to plot x, y of each point
            plt.plot(x_val, y_val)
            # plt.text(x_val, y_val, str(i))
        if save:
            plt.savefig(path)
        else:
            plt.show()
        plt.close()
        
# input_a = Input.get_random_situation(n_emergencies=10, n_service_locations=10, n_units=10, n_personnel=10)
# # Dist = Distribution(input_a)
# # # jsonD = json.dumps(input_a.__dict__)
# # # print(jsonD)
# # # for i in range(len(Dist.input_situation.emergencies)):
# # #     print(Dist.input_situation.emergencies[i], ' : ', Dist.vector[i])
    
# # # print(Dist.fitness())
# # list1 = []
# # for i in range(100):
# #     Dist = Distribution(input_a)
# #     list1.append(Dist.fitness()[0])
    
# # print(min(list1))
# # print(statistics.mean(list1))

# for emergency in input_a.emergencies:
#     print(emergency.__dict__)

# print("dfas")
# i = 0
# for loc in input_a.service_locations:
#     print("START UNITS for " + str(i))
#     for unit in loc.available:
#         print(unit.__dict__)
#     print("END UNITS ")
#     print(loc.__dict__)
    
# # print("dfas")

# # for unit in input_a.units:
# #     print(unit.__dict__)

# print(json.dumps(input_a.__dict__, default=lambda o: o.__dict__))

# input_a = Input.from_situation(situation)
# input_a.plot()
# # for i in range(100):
# list1 = []
# for i in range(1000):
#     Dist = Distribution(input_a)
#     list1.append(Dist.fitness())
    
# print(min(list1))
# print(statistics.mean(list1))


'''
Example of approaches
units = [4]
emergencies = [a, b]
centers = 2
center 1 = [1, 2]
center 2 =[3, 4]

Case 1
each particle = [1, 2] # 10 null values
We are allocating units to emergencies

Case 2
units = [1 ,2, 3, 4]
each particle = [a, null, b, null]
We are allocating emergencies to units
'''