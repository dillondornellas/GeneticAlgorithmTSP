import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from capitals import things

# draw new frame
def draw_frame(sequence, fitness, gen, ax, fig):
    
    plt.cla()
    # creates to much lag adding detailed background
    #ax.stock_img()
    ax.coastlines()
    ax.set_global()

    # plot all travel lines
    for i in range(len(things) - 1):
        lats = [things[sequence[i]][1][0], things[sequence[i+1]][1][0]]
        lons = [things[sequence[i]][1][1], things[sequence[i+1]][1][1]]
        ax.plot(lons, lats, label='Great Circle', transform=ccrs.Geodetic())
    
    lats = [things[sequence[0]][1][0], things[sequence[-1]][1][0]]
    lons = [things[sequence[0]][1][1], things[sequence[-1]][1][1]]
    ax.plot(lons, lats, label='Great Circle', transform=ccrs.Geodetic())
    
    # set new title
    title = "Generation : " + str(gen) + " | Fitness : " + str(fitness)
    ax.set_title(title)

    # update canvas
    fig.canvas.draw()

# Scatter plot of all capitals
'''
for thing in things:
    ax.scatter(
        thing.coords[1],
        thing.coords[0],
        color='blue',
        s=2,
        transform = ccrs.PlateCarree()
    )
'''