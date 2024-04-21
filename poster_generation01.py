#%%
import matplotlib.pyplot as plt

from Poster import Poster
#%%
poster = Poster([1200 , 600])

# poster.globes.append(Globe(plate_index = 1)) 

poster.render()
poster.save_image()

#%%
#plt.ion()
plt.figure(3)
#plt.imshow(poster.masks.masks, cmap='gray')
#plt.imshow(poster.poster_pixels[:,:,2])
plt.imshow(poster.height_map, cmap='gray', alpha=0.5)
plt.show()

# %%
