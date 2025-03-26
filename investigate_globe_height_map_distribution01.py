
#%%
import matplotlib.pyplot as plt
import numpy as np


# Example 2D numpy array for demonstration
# Replace this with your actual poster.height_map
# poster.height_map = np.array([[...]])

# Flatten the 2D array and filter out zero elements

# plates =  [7, 30, 31, 37, 42, 44]

height_map = poster.globes[1].height_map
height_map = height_map[height_map != 0]

non_zero_elements = height_map[np.nonzero(height_map)]

mean_non_zero = np.mean(non_zero_elements)
max_non_zero = np.max(non_zero_elements)
minimum_value = mean_non_zero - 5*(max_non_zero - mean_non_zero)

# Plot the histogram with 50 bins
plt.hist(height_map, bins=50, edgecolor='black', alpha=0.75)
plt.axvline(x=minimum_value, color='red', linestyle='--', label='Mean/2')
plt.axvline(x=mean_non_zero, color='k', linestyle='--', label='Mean value')

# Add labels and title
plt.title('Histogram of Nonzero Height Map Values')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()
plt.show()
