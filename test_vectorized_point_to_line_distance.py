import numpy as np
import matplotlib.pyplot as plt

def vectorized_point_to_line_distance(grid_x, grid_y, l1, l2):
    """
    Vectorized calculation of the distance from a grid of points to a line defined by two points l1 and l2.
    
    :param grid_x: 2D numpy array of x-coordinates of the grid.
    :param grid_y: 2D numpy array of y-coordinates of the grid.
    :param l1: 2D numpy array representing the first point on the line.
    :param l2: 2D numpy array representing the second point on the line.
    :return: 2D numpy array representing the distances from each point to the line.
    """
    direction = l2 - l1
    direction = direction / np.linalg.norm(direction)  # Normalize the direction vector
    
    l1_to_pixel_x = grid_x - l1[0]
    l1_to_pixel_y = grid_y - l1[1]
    
    projection_length = l1_to_pixel_x * direction[0] + l1_to_pixel_y * direction[1]
    projection_x = projection_length * direction[0]
    projection_y = projection_length * direction[1]
    
    distance_x = l1_to_pixel_x - projection_x
    distance_y = l1_to_pixel_y - projection_y
    
    return np.sqrt(distance_x**2 + distance_y**2)

def generate_loxodrome_image_fast(resolution):
    """
    Generates a 2D image where the gray value represents the distance to the nearest loxodrome line,
    with anchor points arranged in a circle around the center of the image. This version avoids looping
    over individual pixels by using vectorized operations.
    
    :param resolution: Tuple (width, height) of the image.
    :param radius: Radius of the circle in which the anchor points are placed.
    :return: 2D numpy array representing the distance map.
    """
    width, height = resolution
    radius = np.min([width, height]) // 2 
    image = np.full((height, width), np.inf)  # Initialize with large values for minimum comparison
    
    # Center of the image
    center = np.array([width // 2, height // 2])
    
    # Define 8 anchor points in a circle
    num_points = 16
    angles_circle = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    anchor_points = [center + np.array([np.cos(angle), np.sin(angle)]) * radius for angle in angles_circle]
    
    # Define 16 directions per anchor, evenly spaced between 0 and pi radians
    angles_rose = np.linspace(0, np.pi, 16 + 1)
    
    # Create a grid of pixel positions
    grid_y, grid_x = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
    
    # Loop over all anchor points and calculate the distance to each loxodrome line
    for anchor in anchor_points:
        anchor = np.array(anchor)
        print("Looping over anchor points")
        for angle in angles_rose:
            # Calculate the second point on the loxodrome using the angle
            l2 = anchor + np.array([np.cos(angle), np.sin(angle)]) * max(width, height)
            
            # Compute the distance from the grid to the line
            distances = vectorized_point_to_line_distance(grid_x, grid_y, anchor, l2)
            
            # Update the image with the minimum distance for each pixel
            image = np.minimum(image, distances)
    
    # Apply linear mapping to the image
    threshold = np.min([width, height]) / 2000
    image = np.clip((image - threshold) , 0, 1)

    # Normalize the image to the range [0, 1]
    image = image / np.max(image)
    return image

# Example code
resolution = (2000, 1000)
loxodrome_image = generate_loxodrome_image_fast(resolution)

# Plot the generated image
plt.imshow(loxodrome_image, cmap='gray', interpolation='nearest')
plt.title('Loxodrome Distance Map')
plt.colorbar()
plt.show()
