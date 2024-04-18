
import matplotlib.pyplot as plt

from Poster import Poster
#%%
poster = Poster([240 , 120])

# poster.globes.append(Globe(plate_index = 1)) 

poster.render()

#%%
#plt.figure(3)
#plt.imshow(poster.masks.masks, cmap='gray')
#plt.imshow(poster.poster_pixels[:,:,0])
#plt.show()
