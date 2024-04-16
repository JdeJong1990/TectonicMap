#%%
import matplotlib.pyplot as plt
my_masks = PlateMasks()

try:
    from Plate import Plate
except:
    pass

#%%
plate_index = 13

print('start making plate and find center')

my_plate = Plate(my_masks.masks==plate_index)

center = my_plate.center_coordinate
print("center determined by Plate class: ", center)

[longitude, latitude] = center

def coordinate_to_pixel(longitude, latitude):
    x = (longitude+np.pi)/2/np.pi*4454
    y = -(latitude-np.pi/2)/np.pi*2227
    x = x%4454
    return x, y

plt.figure(2)
map = np.transpose(my_masks.masks==plate_index)
plt.imshow(map, cmap='gray')

x, y = coordinate_to_pixel(longitude, latitude)
plt.scatter(x,y, color='r', s=10)

plt.show()

print("second image shown")
# %%
plt.figure(1)
plt.imshow(my_masks.masks, cmap='gray')
plt.show()
print('first image shown')
# %%
