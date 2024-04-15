
import matplotlib.pyplot as plt

from Poster import Poster
#%%
poster = Poster([1200 , 600])

# poster.globes.append(Globe(plate_index = 1)) 

poster.render()


plt.figure(3)
#plt.imshow(poster.masks.masks, cmap='gray')
plt.imshow(poster.poster_pixels)
plt.show()
# %%
