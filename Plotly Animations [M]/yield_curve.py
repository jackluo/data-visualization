# In[]:
# Imports required libraries

from datetime import datetime
import numpy as np
import pandas as pd

import plotly.plotly as py
from plotly.graph_objs import *
from plotly.grid_objs import Grid, Column


# In[]:
# Selects data

filename = "data/yield_curve.csv" # Already sanitized for Plotly
chart_filename = "Yield curve " + str(datetime.now())

df = pd.read_csv(filename, encoding="utf-8-sig")
#df
#print(df.columns)


# In[]:
# Uploads Grid

grid_filename = chart_filename + " Grid"
columns = []

xcol = [1, 2, 3]
ycol = [1, 2, 3]
zcol = [[1,2,3], [4,5,6], [7,8,9]]
#xcol = list(df["x"])
#ycol = list(df["y"])

columns.append(Column(xcol, "x"))
columns.append(Column(ycol, "y"))
columns.append(Column(zcol, "z"))

#zcols = []
#for i in range(11):
#    zcol = list(df["z[{}]".format(i)])
#    columns.append(Column(zcol, "z[{}]".format(i)))
#    zcols.append(zcol)

# Will throw error if file exists or path is not root
grid = Grid(columns)
py.grid_ops.upload(grid, grid_filename, auto_open=False)


# In[]:
# Creates data

trace1 = Surface(

    # GENERAL
    x = grid.get_column_reference("x"),
    y = grid.get_column_reference("y"),
    z = grid.get_column_reference("z"),

)


# In[]:
# Sets up slider and buttons


updatemenus = dict(

    # GENERAL
    type = "buttons",
    showactive = False,
    x = 0.1, #x = 1.1
    y = 0, #y = 1
    pad = dict(t = 60, r = 10),
    xanchor = "right",
    yanchor = "top",
    direction = "left",

    # BUTTONS
    buttons=[
        dict(
            method = "animate",
            label = "Play",

            # PLAY
            args = [
                None,
                dict(
                    frame = dict(duration = 300, redraw = True),
                    fromcurrent = True,
                    transition = dict(duration = 50, easing = "quadratic-in-out"), # easing = "cubic-in-out"
                    mode = "immediate",
                    ),
                ],
            ),
        dict(
            method = "animate",
            label = "Pause",

            # PAUSE
            args = [
                [None], # Note the list
                dict(
                    frame = dict(duration = 0, redraw = True),
                    mode = "immediate",
                    transition = dict(duration = 0),
                    ),
                ],
            ),
        ],

)


# In[]:
# Creates layout

layout = dict(

    # GENERAL LAYOUT
    width = 1080,
    height = 720,
    autosize = True,
    font = dict(
        family = 'Overpass',
        size = 12,
        color = "#CCCCCC",
    ),
    margin = dict(
        t = 80,
        l = 80,
        b = 80,
        r = 80,
        pad = 2,
    ),
    title = "US Treasury Yield Curve",
    showlegend = False,
    hovermode = "closest",

    # ANIMATIONS
    updatemenus = [updatemenus],

    # COLOR THEME
    #plot_bgcolor = "#191A1A",
    #paper_bgcolor = "#151515",

    # SCENE
    scene = dict(
        aspectmode = "manual",
        aspectratio = dict(x = 1, y = 4, z = 2),
        camera = {
          "center": {
            "x": 0,
            "y": 0,
            "z": 0
          },
          "eye": {
            "x": -1,
            "y": -1,
            "z": 1,
          },
          "up": {
            "x": 0,
            "y": 0,
            "z": 1
          }
        },
        xaxis = {
              "showgrid": True,
              "title": "",
              "type": "category",
              "zeroline": False
            },
        yaxis = {
              "showgrid": True,
              "title": "",
              "type": "date",
              "zeroline": False
            },
    )

)


# In[]:
# Creates frames

frames = []
years = range(5)

for i, year in enumerate(years):

    #frame_trace1 = dict(
    #    xsrc = grid.get_column_reference("x"),
    #    ysrc = grid.get_column_reference("y"),
    #    zsrc = grid.get_column_reference("z"),
    #)

    frame = dict(
        #data = [frame_trace1],
        traces = [0],
        layout = dict(
            title = "ZZZ",
            scene = dict(
                aspectmode = "manual",
                aspectratio = dict(x = 2, y = 4, z = 2),
                camera = {
                  "eye": {
                    "x": -10,
                    "y": -10,
                    "z": 1,
                  },
                },
            )
        )
    )
    frames.append(frame)


# In[]:
# Uploads animation

data = [trace1]
figure = dict(data=data, layout=layout, frames=frames)
#py.iplot(figure)
py.icreate_animations(figure, filename=chart_filename, auto_open=False)
