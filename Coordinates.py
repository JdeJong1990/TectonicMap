import numpy as np

class Coordinates:
    """
    Geographic coordinates in radians. 
    Longitude is in the range of -pi to pi, and latitude is in the range of -pi/2 to pi/2.
    """
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
    
    def to_relative_position(self):
        x = 1.0 + self.longitude/np.pi
        y = 0.5 - self.latitude/np.pi
        return RelativePosition(x, y)
    
class RelativePosition:
    """
    Relative coordinates in the range of x = [0, 2] and y = [0, 1].
    Ther origin is in the upper left corner.
    """
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
        # Convert the relative position to a coordinate in longitude and latitude
        longitude = np.pi * (self.x - 1.0)
        latitude = np.pi * (0.5 - self.y)
        coordinate = Coordinates(longitude, latitude)
        return coordinate
    
    def to_magnitude(self):
        return np.sqrt(self.x**2 + self.y**2)
    
class PixelPosition:
    """
    Coordinates in pixels, on a map with the origin in the upper left corner.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):  # Defines the addition between two PixelPosition instances.
        return PixelPosition(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other): #Defines the subtraction between two PixelPosition instances.
        return PixelPosition(self.x - other.x, self.y - other.y)
        
    def __mul__(self, other): #Defines the multiplication between a PixelPosition instance and an integer or float.
        if isinstance(other, (int, float)):
            return PixelPosition(self.x * other, self.y * other)
        else:
            raise TypeError("Unsupported operand type. You can only multiply PixelPosition by an integer or float.")

    def __str__(self):  # Defines the string representation for printing PixelPosition instances.
        return f"PixelPosition(x={self.x}, y={self.y})"


