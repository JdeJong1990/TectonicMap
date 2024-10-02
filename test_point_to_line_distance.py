import numpy as np

def point_to_line_distance(pixel_position, l1, l2):
    """
    Calculates the distance between a 2D point (pixel_position) and an infinite line
    defined by two points l1 and l2.
    
    :param pixel_position: 2D numpy array representing the coordinates of the point.
    :param l1: 2D numpy array representing the first point on the line.
    :param l2: 2D numpy array representing the second point on the line.
    :return: The distance from pixel_position to the infinite line.
    """
    # Direction vector from l1 to l2
    direction = l2 - l1
    direction = direction / np.linalg.norm(direction)  # Normalize the direction vector
    
    # Vector from l1 to pixel_position
    l1_to_pixel = pixel_position - l1
    
    # Project the l1_to_pixel vector onto the direction of the line
    projection_length = np.dot(l1_to_pixel, direction)
    projection_vector = projection_length * direction
    
    # The distance is the norm of the difference between l1_to_pixel and the projection
    distance_vector = l1_to_pixel - projection_vector
    distance = np.linalg.norm(distance_vector)
    
    return distance


# Example usage
pixel_position = np.array([2, 3])
l1 = np.array([0, 0])
l2 = np.array([4, 4])

distance = point_to_line_distance(pixel_position, l1, l2)
print(f"Distance to the line: {distance}")
