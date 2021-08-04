import cartopy.crs as ccrs
import cartopy
import matplotlib.pyplot as plt
from TSP_genetic import evolution
from capitals import things

plt.figure(figsize=(12,7))
ax = plt.axes(projection=ccrs.Robinson())
ax.stock_img()

for thing in things:
    ax.scatter(
        thing.coords[1],
        thing.coords[0],
        color='blue',
        s=2,
        transform = ccrs.PlateCarree()
    )
    '''plt.text(
        thing.coords[1],
        thing.coords[0], 
        thing.name, 
        transform = ccrs.PlateCarree(),
        fontsize=7
    )'''

ax.add_feature(cartopy.feature.BORDERS)
ax.coastlines()
ax.set_global()
plt.show()