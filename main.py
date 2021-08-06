import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from capitals import things
from TSP_genetic import evolution, pop_size
from TSP_plot import draw_frame
import pandas as pd
import os

createVideo = True
index = 0
fitness_count = []

# CREATE CANVAS
plt.figure(figsize=(12,7))
ax = plt.axes(projection=ccrs.Robinson())
#ax.stock_img()
ax.coastlines()
ax.set_global()
fig = plt.gcf()
fig.show()
fig.canvas.draw()

# BEGIN EVOLUTION
for sequence, fitness, gen in evolution():
    title = "Generation : " + str(gen+1) + " | Fitness : " + str(fitness)
    print(title)

    # record fitness
    fitness_count.append(fitness)
    # draw frames
    if gen % 5 == 0:
        draw_frame(sequence, fitness, gen, ax, fig)
        # Generate images
        if createVideo == True:
            fname = 'TSP-{0:0=4d}.png'.format(index)
            fpath = 'E:/GitHub/Travel/images/data' + str(pop_size)
            fig.savefig(os.path.join(fpath, fname))        
            index += 1

# APPEND TO CSV
column = str(pop_size)
# create new dataframe
#df = pd.DataFrame(fitness_count, columns = [column])
# read in CSV
df = pd.read_csv("data.csv")
# add new column to DF
df[column] = fitness_count
# save new DF
df.to_csv("data.csv", index=False)