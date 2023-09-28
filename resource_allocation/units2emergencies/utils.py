import numpy as np
import matplotlib.pyplot as plt
import random
import math
import statistics
import json

class EmergencyServiceLocation:
    """
    Represents an emergency service location.
    """
    
    def __init__(self, point, Etype, personnel_available, n_units, unit_severities):
        """
        Initializes an EmergencyServiceLocation instance.

        Args:
            point (tuple): Coordinates (x, y) of the location.
            Etype (int): Type of emergency service.
            personnel_available (int): Number of available personnel.
            n_units (int): Number of units.
            unit_severities (list): List of unit severities.
        """
        self.point = point
        self.Etype = Etype
        self.personnel_available = personnel_available
        self.n_units = n_units
        self.available = []
        self.in_route = []
        self.returning = []
        self.unit_severities = unit_severities
        self.unitsFromSeverity()
        
    def addUnits(self, units):
        """
        Add units to the available units.

        Args:
            units (list): List of units to add.
        """
        self.available.extend(units)
        
    def unitsFromSeverity(self):
        """
        Create units based on severities and add them to available units.
        """
        for i in self.unit_severities:
            self.available.append(Unit(self, self.Etype, 4, i))
    
    def to_json(self):
        """
        Convert the object to a JSON-compatible dictionary.

        Returns:
            dict: JSON representation of the object.
        """
        return {
            "point": self.point,
            "Etype": self.Etype,
            "personnel_available": self.personnel_available,
            "n_units": self.n_units,
            "unit_severities": self.unit_severities.tolist()
        }

class Unit:
    """
    Represents an emergency unit.
    """

    def __init__(self, serviceLocation, Etype, max_personnel, severity_limit):
        """
        Initializes a Unit instance.

        Args:
            serviceLocation (EmergencyServiceLocation): The service location to which the unit belongs.
            Etype (int): Type of the unit.
            max_personnel (int): Maximum personnel the unit can have.
            severity_limit (int): Severity limit for the unit.
        """
        self.home = serviceLocation
        self.Etype = Etype
        self.max_personnel = max_personnel
        self.severity_limit = severity_limit

# Other classes (Emergency, Input, Distribution) have been omitted for brevity, but you can apply similar principles to them as well.

def euclidian_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.

    Args:
        point1 (tuple): Coordinates (x, y) of the first point.
        point2 (tuple): Coordinates (x, y) of the second point.

    Returns:
        float: Euclidean distance between the points.
    """
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
