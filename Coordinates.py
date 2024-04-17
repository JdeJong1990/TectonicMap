import numpy as np

class Coordinates:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
    
    def to_relative_position(self):
        x = 1.0 + self.longitude/np.pi
        y = 0.5 - self.latitude/np.pi
        return RelativePosition(x, y)
    
class RelativePosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other): #Defines the subtraction between two RelativePosition instances.
        return RelativePosition(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other): #Defines the multiplication between a RelativePosition instance and an integer, float or double.
        if isinstance(other, (int, float)):
            return RelativePosition(self.x * other, self.y * other)
        else:
            raise TypeError("Unsupported operand type. You can only multiply RelativePosition by an integer or float.")
    
    def to_coordinate(self):
        longitude = np.pi * (self.x - 1.0)
        latitude = np.pi * (0.5 - self.y)
        coordinate = Coordinates(longitude, latitude)
        return coordinate
    
    def to_magnitude(self):
        return np.sqrt(self.x**2 + self.y**2)
    
class PixelPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other): #Defines the subtraction between two PixelPosition instances.
        return PixelPosition(self.x - other.x, self.y - other.y)
        
    def __mul__(self, other): #Defines the multiplication between a PixelPosition instance and an integer or float.
        if isinstance(other, (int, float)):
            return PixelPosition(self.x * other, self.y * other)
        else:
            raise TypeError("Unsupported operand type. You can only multiply PixelPosition by an integer or float.")


