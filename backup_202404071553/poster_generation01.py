#%%
from Poster import Poster

poster = Poster([200 , 100])

# poster.globes.append(Globe(plate_index = 1)) 

poster.render()

import matplotlib.pyplot as plt
plt.figure(3)
plt.imshow(poster.poster_pixels)
plt.show()
# %%
