# In[]:
# Import required libraries

from datetime import datetime
import numpy as np

import plotly.plotly as py
from plotly.graph_objs import *
from plotly.grid_objs import Grid, Column


# In[]:
# Sine function
# https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

def sin(i):
    x = np.linspace(0, 2, 100)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    return x, y


# In[]:
# Upload Grid

chart_filename = "Sine " + str(datetime.now())
grid_filename = chart_filename + " Grid"
columns = []

# Actual animation function
for i in range(200):

    x, y = sin(i)

    columns.append(Column(x, "x{}".format(i + 1)))
    columns.append(Column(y, "y{}".format(i + 1)))

grid = Grid(columns)
py.grid_ops.upload(grid, grid_filename, auto_open=False)


# In[]:
# Create data

trace1 = Scatter(
    xsrc = grid.get_column_reference("x1"),
    ysrc = grid.get_column_reference("y1"),
    mode = "lines",
)


# In[]:
# Create layout

animation_time = 15

updatemenus = dict(
    type = "buttons",
    buttons=[
            dict(
                method = "animate",
                label = "Play",
                args = [None,
                        dict(frame = dict(duration = animation_time, redraw = False), mode = "immediate", fromcurrent = True),
                        ],
                ),
            dict(
                method = "animate",
                label = "Pause",
                args = [[None], # Note the list
                        dict(frame = dict(duration = 0, redraw = False), mode = "immediate"),
                        ],
                ),
            ],
)

layout = dict(updatemenus = [updatemenus])


# In[]:
# Create frames

frames = []

for i in range(200):
    frame = dict(
        data = [dict(xsrc = grid.get_column_reference("x{}".format(i+1)),
                     ysrc = grid.get_column_reference("y{}".format(i+1))
                     )],
        traces = [0],
    )
    frames.append(frame)


# In[]:
# Upload animation

figure = dict(data=[trace1], layout=layout, frames=frames)
py.icreate_animations(figure, filename=chart_filename, auto_open=False)
