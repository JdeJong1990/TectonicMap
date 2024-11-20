import numpy as np
import matplotlib.pyplot as plt

def point_to_line_distance(pixel_position, l1, l2):
    """
    Calculates the distance between a 2D point (pixel_position) and an infinite line
    defined by two points l1 and l2.
    
    :param pixel_position: 2D numpy array representing the coordinates of the point.
    :param l1: 2D numpy array representing the first point on the line.
    :param l2: 2D numpy array representing the second point on the line.
    :return: The distance from pixel_position to the infinite line.
    """
    direction = l2 - l1
    direction = direction / np.linalg.norm(direction)  # Normalize the direction vector
    l1_to_pixel = pixel_position - l1
    projection_length = np.dot(l1_to_pixel, direction)
    projection_vector = projection_length * direction
    distance_vector = l1_to_pixel - projection_vector
    return np.linalg.norm(distance_vector)

def generate_loxodrome_image(resolution, radius):
    """
    Generates a 2D image where the gray value represents the distance to the nearest loxodrome line,
    with anchor points arranged in a circle around the center of the image.
    
    :param resolution: Tuple (width, height) of the image.
    :param radius: Radius of the circle in which the anchor points are placed.
    :return: 2D numpy array representing the distance map.
    """
    width, height = resolution
    image = np.zeros((height, width))  # Image where gray value will be stored
    
    # Center of the image
    center = np.array([width // 2, height // 2])
    
    # Define 8 anchor points in a circle
    num_points = 8
    angles_circle = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    anchor_points = [center + np.array([np.cos(angle), np.sin(angle)]) * radius for angle in angles_circle]
    
    # Define 16 directions per anchor, evenly spaced between 0 and pi radians
    angles_rose = np.linspace(0, np.pi, 16)
    
    # Create a grid of pixel positions
    for y in range(height):
        print(height - y)
        for x in range(width):
            pixel_position = np.array([x, y])
            min_distance = np.inf
            
            # Loop over all anchor points and calculate the distance to each loxodrome line
            for anchor in anchor_points:
                anchor = np.array(anchor)
                for angle in angles_rose:
                    # Calculate the second point on the loxodrome using the angle
                    l2 = anchor + np.array([np.cos(angle), np.sin(angle)]) * max(width, height)
                    # Compute the distance from the pixel to the line
                    distance = point_to_line_distance(pixel_position, anchor, l2)
                    if distance < min_distance:
                        min_distance = distance
            
            # Assign the distance as the pixel value (inverse to create a visible gradient)
            image[y, x] = min_distance
    
    # Normalize the image to the range [0, 1]
    image = image / np.max(image)
    
    return image

# Example code
resolution = (50, 50)
radius = min(resolution) // 4  # Radius of the circular arrangement of anchor points
loxodrome_image = generate_loxodrome_image(resolution, radius)

# Plot the generated image
plt.imshow(loxodrome_image, cmap='gray', interpolation='nearest')
plt.title('Loxodrome Distance Map with Circular Anchor Points')
plt.colorbar(label='Distance to Nearest Line')
plt.show()
