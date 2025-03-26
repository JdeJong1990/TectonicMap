"""
In this file we create the ambient occlusion for the shells on the background. 

"""
#%%
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

from scipy.ndimage import gaussian_filter

panel = 2
files = [0, 
         1,
         '..\\V1\\2_North_American\\2024-12-29_23-05-26_height_map.png',  
         3, 
         '..\\V1\\4_Eurasian_Somalilan_Indian\\2024-12-05_07-48-09_cast_shadow.png', 
         5, 
         6, 
         '..\\V1\\7_Australian\\2024-12-29_13-20-40_height_map.png']

height_limits = [
    [0.0, 0.0],         # Initial element with zeros
    [0.9999, 0.0],      # Pacific
    [0.4933, 0.0],      # North America
    [0.4481, -0.2602],  # Africa South America
    [0.4980, 0.0],      # Eurasian, Somalian, Indian
    [0.5497, 0.0],      # Antarctician
    [0.1048, -0.2893],  # Japan Indonesia
    [0.4366, 0.0],      # Australian
    [0.0053, -0.0236],  # Tiny islands past Indonesia
]

plate_names = [
    "Plate Zero",  
    "Pacific",  
    "North America",  
    "Africa South America",  
    "Eurasian, Somalian, Indian",  
    "Antarctician",  
    "Japan Indonesia",  
    "Australian",  
    "Tiny islands past Indonesia"  
]
relative_path = files[panel]
height_limit = height_limits[panel]
panel_name = plate_names[panel]

# •	Load in image

# Define paths
script_dir = os.path.dirname(__file__)  # Get the directory of the current script
image_path = os.path.abspath(os.path.join(script_dir, relative_path))

height_map = Image.open(relative_path)
height_map_np = np.array(height_map)/255

# •	Scale the data according to the table in this chapter
height_map_s = (height_map_np * (height_limit[0] - height_limit[1])) - height_limit[1]
print(f'Max of scaled map is {np.max(height_map_s):.04}')

# •	Run the data through the non-linear function, scale to desire
scaling_factor = 0.1

height_map_nl = height_map_s / (( height_map_s / scaling_factor)**3 + 1)

# •	Do 1 – (Low_pass – Hight_map)

blurred_height_map = gaussian_filter(height_map_nl, sigma=100)

occlusion_map = (blurred_height_map - height_map_nl)
occlusion_map = (occlusion_map + np.abs(occlusion_map))/2/0.04
occlusion_map = 1 - occlusion_map

# •	Save as image

# Create an RGB image from the clipped pixel data
image = Image.fromarray(occlusion_map, 'RGB')

image = image.transpose(Image.TRANSPOSE)

save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'images')

# if not os.path.exists(save_path):

#     os.makedirs(save_path)

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
full_save_path = os.path.join(save_path, f'{timestamp}_AO_{panel_name}.png')

#%% Save the image
image.save(full_save_path)

print('Image saved')

#  % %

TB_imaged = occlusion_map
fig1 = plt.figure(1)
ax = fig1.add_subplot(1,1,1)

ax.imshow(TB_imaged/np.max(TB_imaged), cmap="gray")

ax.axis("off")  # Hide axes

plt.show()
print(f'Max is: {np.max(TB_imaged)}')
# %%
