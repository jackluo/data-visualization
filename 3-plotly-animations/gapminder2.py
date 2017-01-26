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

filename = "data/gapminder.csv"
chart_filename = "Gapminder " + str(datetime.now())

df = pd.read_csv(filename, encoding="utf-8-sig")
#df
#print(df.columns)

# Gets list of years
years = df["YEAR"].unique()
years = list(sorted(years.astype(str)))

# Bug with Grid parsing if dataset isn't sanitized, need to return NaN instead of empty []
#years = [str(i) for i in range(1962,2007)]


# In[]:
# Uploads Grid

grid_filename = chart_filename + " Grid"
columns = []

for i, year in enumerate(years):

    lons = df[df["YEAR"] == int(year)]["LON"].astype(float)
    lats = df[df["YEAR"] == int(year)]["LAT"].astype(float)
    texts = df[df["YEAR"] == int(year)]["STRCITY"].astype(str)

    columns.append(Column(lons, "x{}".format(i + 1)))
    columns.append(Column(lats, "y{}".format(i + 1)))
    columns.append(Column(texts, "text{}".format(i + 1)))

# Will throw error if file exists or path is not root
grid = Grid(columns)
py.grid_ops.upload(grid, grid_filename, auto_open=False)


# In[]:
# Creates data

trace1 = Scattermapbox(

    # GENERAL
    lonsrc = grid.get_column_reference("x1"),
    latsrc = grid.get_column_reference("y1"),
    textsrc = grid.get_column_reference("text1"),
    hoverinfo = "lon+lat+text",
    mode = "markers",

    marker = dict(
        size = 10,
        color = "#54D9F3",
        opacity = "0.6",
    ),

)


# In[]:
# Sets up slider and buttons

slider = dict(

    # GENERAL
    plotlycommand = "animate",
    values = years,
    initialValue = years[0],
    visible = True,

    # ARGUMENTS
    args = [
        "slider.value",
        dict(
            duration = 300,
            ease = "cubic-in-out",
        ),
    ],

)

sliders = dict(

    # GENERAL
    active = 0,
    steps = [],

    currentvalue = dict(
        font = dict(size = 16),
        prefix = "Year : ",
        xanchor = "right",
        visible = True,
    ),
    transition = dict(
        duration = 300,
        easing = "cubic-in-out",
    ),

    # PLACEMENT
    x = 0.1,
    y = 0,
    pad = dict(t = 40, b = 10),
    len = 0.9,
    xanchor = "left",
    yanchor = "top",

)

for year in years:

    slider_step = dict(

            # GENERAL
            method = "animate",
            value = year,
            label = year,

            # ARGUMENTS
            args = [
                [year],
                dict(
                    frame = dict(duration = 300, redraw = False),
                    transition = dict(duration = 300),
                    mode = "immediate",
                    ),
                ],

            )

    sliders["steps"].append(slider_step)


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
                    frame = dict(duration = 300, redraw = False),
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
                    frame = dict(duration = 0, redraw = False),
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
    title = "Growth of Walmart stores, 1962-2006",
    showlegend = False,
    hovermode = "closest",

    # ANIMATIONS
    slider = slider,
    sliders = [sliders],
    updatemenus = [updatemenus],

    # COLOR THEME
    plot_bgcolor = "#191A1A",
    paper_bgcolor = "#151515",

    # MAPBOX
    mapbox = dict(
        accesstoken = mapbox_access_token,
        center = dict(
            lon = -96.00,
            lat = 38.50,
        ),
        pitch = 0,
        zoom = 3.0,
        style = "dark",
    ),

)


# In[]:
# Creates frames

frames = []

for i, year in enumerate(years):
    frame = dict(
        data = [dict(lonsrc = grid.get_column_reference("x{}".format(i + 1)),
                     latsrc = grid.get_column_reference("y{}".format(i + 1)),
                     textsrc = grid.get_column_reference("text{}".format(i + 1)),
                     )],
        name = str(year),
    )
    frames.append(frame)


# In[]:
# Uploads animation

data = [trace1]
figure = dict(data=data, layout=layout, frames=frames)
py.icreate_animations(figure, filename=chart_filename, auto_open=False)
