import cartopy.crs as ccrs
import cartopy
import matplotlib.pyplot as plt
from capitals import things
from TSP_genetic import evolution

sequence = evolution()
print(sequence)

def draw_frame(sequence):
    plt.figure(figsize=(12,7))
    ax = plt.axes(projection=ccrs.Robinson())
    ax.stock_img()
    ax.add_feature(cartopy.feature.BORDERS, linestyle =':')
    ax.coastlines()
    ax.set_global()
    for thing in things:
        ax.scatter(
            thing.coords[1],
            thing.coords[0],
            color='blue',
            s=2,
            transform = ccrs.PlateCarree()
        )
    
    for i in range(len(things) - 1):
        lats = [things[sequence[i]][1][0], things[sequence[i+1]][1][0]]
        lons = [things[sequence[i]][1][1], things[sequence[i+1]][1][1]]
        ax.plot(lons, lats, label='Great Circle', transform=ccrs.Geodetic())
    
    lats = [things[sequence[0]][1][0], things[sequence[-1]][1][0]]
    lons = [things[sequence[0]][1][1], things[sequence[-1]][1][1]]
    ax.plot(lons, lats, label='Great Circle', transform=ccrs.Geodetic())
    
    ax.set_title('Ottawa')
    #plt.pause(0.05)
    plt.show()


draw_frame(sequence)