import numpy as np
import matplotlib.pyplot as plt
# Severity: [1, 2, 3, 4, 5]
# Type: [1, 2, 3]
# Status: [1, 2, 3] :: [Available, In route, Returning]
# Distance: Using Benchmark Functions
# Amount of Personnel : int

class EmergencyServiceLocation:
    
    def __init__(self, point, Etype, personnel_avaliable, n_units):
        self.point = point
        self.Etype = Etype
        self.personnel_avaliable = personnel_avaliable
        self.n_units = n_units
        self.available = []
        self.in_route = []
        self.returning = []
        
    def addUnits(self, units):
        self.available.extend(units)

class Unit:

    def __init__(self, serviceLocation, Etype, max_personnel, severity_limit):
        self.home = serviceLocation
        self.Etype = Etype
        self.max_personnel = max_personnel
        self.severity_limit = severity_limit
    
        
        
class Emergency:
    
    def __init__(self, point, Etype, severity):
        self.point = point
        self.Severity = severity
        self.Etype = Etype
    

class Input:
    
    def __init__(self, emergencies, service_locations, units):
        self.emergencies = emergencies
        self.service_locations = service_locations
        self.units = units
        
    @staticmethod
    def get_random_situation(n_emergencies, n_service_locations, n_personnel, n_units = 5, x = (-100, 100), y = (-100, 100)):
        """
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
        units = []
        
        for _ in range(n_emergencies):
            emergencies.append(Emergency(point=(np.random.randint(x[0], x[1]),np.random.randint(y[0], y[1])), Etype=np.random.randint(1, 3), severity=np.random.randint(1, 5)))

        for _ in range(n_service_locations):
            service_locations.append(EmergencyServiceLocation(point=(np.random.randint(x[0], x[1]),np.random.randint(y[0], y[1])), Etype=np.random.randint(1, 3), personnel_avaliable=np.random.randint(2, n_personnel), n_units=np.random.randint(1, n_units)))
            
        for loc in service_locations:
            loc_units = []
            for _ in range(loc.n_units):
                loc_units.append(Unit(serviceLocation=loc, Etype=np.random.randint(1, 3), max_personnel=np.random.randint(1, loc.personnel_avaliable), severity_limit=np.random.randint(1, 5)))
            loc.addUnits(loc_units)
            units.extend(loc_units)

        return Input(emergencies=emergencies, service_locations=service_locations, units=units)
    
    def plot(self) :
        '''
        Function to plot points
        '''
        for i in range(len(self.service_locations)):
            # Use matplotlib to plot x, y of each point
            plt.plot(self.service_locations[i].point[0], self.service_locations[i].point[1], 'bo')
        for i in range(len(self.emergencies)):
            # Use matplotlib to plot x, y of each point
            plt.plot(self.emergencies[i].point[0], self.emergencies[i].point[1], 'r+')
                
        plt.show()
    
class Distribution:
    
    def __init__(self, input_situation, random = True):
        self.allotment = {}
        if len(input_situation.units) < len(input_situation.emergencies):
            # TODO: Chage this to handle this exception
            raise Exception("Number of units is less than number of emergencies")
        
        if random:
            temp_emergencies = input_situation.emergencies.copy()
            for unit in input_situation.units:
                if len(temp_emergencies) == 0:
                    break
                x = temp_emergencies.pop(np.random.randint(0, len(temp_emergencies)))
                self.allotment[unit] = x
                
        
        
        
input_a = Input.get_random_situation(n_emergencies=10, n_service_locations=10, n_units=10, n_personnel=10)
Dist = Distribution(input_a)
print(Dist.allotment)