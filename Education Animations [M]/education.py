# In[]:
# Imports required libraries

from datetime import datetime
import numpy as np
import pandas as pd

import plotly.plotly as py
from plotly.graph_objs import *
from plotly.grid_objs import Grid, Column

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjaXhzYTB0bHcwOHNoMnFtOWZ3YWdreDB3In0.pjROwb9_CEuyKPE-x0lRUw'


# In[]:
# Selects data

filename = "data/mean-years-of-schooling.csv"
chart_filename = "Education " + str(datetime.now())

df = pd.read_csv(filename, encoding="utf-8-sig")

# Pivots Table (Very important!)
#df = df.pivot(index="Year", columns="Country", values="Total_YearsSchool – Lee-Lee (2016)")
df = df.pivot(index="Year", columns="Country", values="Barro Lee Education Dataset: Educational Attainment (average years of total education)")
#df

# Gets list of years
years = df.index.unique()
years = list(sorted(years.astype(str)))


# In[]:
# Uploads Grid

grid_filename = chart_filename + " Grid"
columns = []

for i, year in enumerate(years):

    # Filter df for current year only
    current_year = df[df.index == int(year)]

    # Get countries and their years ([0] since .valures returns a list of numpy arrays)
    countries = list(current_year.columns.astype(str))
    zvalues = list(current_year.values.astype(float)[0])
    #print(countries, zvalues)

    columns.append(Column(countries, "location{}".format(i + 1)))
    columns.append(Column(zvalues, "z{}".format(i + 1)))

    #print(countries,zvalues)

# Will throw error if file exists or path is not root
grid = Grid(columns)
py.grid_ops.upload(grid, grid_filename, auto_open=False)


# In[]:
# Creates data

yellowblue = [[0, "rgb(255,255,204)"], [0.35, "rgb(161,218,180)"], [0.5, "rgb(65,182,196)"],
            [0.6, "rgb(44,127,184)"], [0.7, "rgb(8,104,172)"], [1, "rgb(37,52,148)"]]

# Main trace
trace1 = Choropleth(

    # GENERAL
    locationssrc = grid.get_column_reference("location1"),
    zsrc = grid.get_column_reference("z1"),
    hoverinfo = "location+z",
    locationmode = "country names",

    # COLORSCALE
    zmin = 0,
    zmax = 14,
    autocolorscale = False,
    colorscale = yellowblue,
    showscale = True,
    colorbar = dict(
        title = "Years<br>",
        nticks = 14,
    ),

)


# In[]:
# Sets up slider and buttons

animation_time = 1000
transition_time = 300
slider_transition_time = 300

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
            duration = animation_time,
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
        duration = slider_transition_time,
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
                    frame = dict(duration = animation_time, redraw = False),
                    transition = dict(duration = slider_transition_time),
                    mode = "immediate",
                    ),
                ],

            )

    sliders["steps"].append(slider_step)


updatemenus = dict(

    # GENERAL
    type = "buttons",
    #showactive = False,
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
                    frame = dict(duration = animation_time, redraw = False), # False quicker but disables animations
                    fromcurrent = True,
                    transition = dict(duration = transition_time, easing = "quadratic-in-out"), # easing = "cubic-in-out"
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
                    frame = dict(duration = 0, redraw = False), # Idem
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

    title = "Mean years of schooling, 1950-2005",

    # GENERAL LAYOUT
    width = 1080,
    height = 720,
    autosize = True,
    font = dict(
        family = "Overpass",
        size = 12,
    ),
    margin = dict(
        t = 80,
        l = 80,
        b = 80,
        r = 80,
        pad = 2,
    ),
    showlegend = False,
    hovermode = "closest",

    # ANIMATIONS
    slider = slider,
    sliders = [sliders],
    updatemenus = [updatemenus],

    annotations = [
        dict(
            text = 'Source: <a href="https://ourworldindata.org/grapher/mean-years-of-schooling">Our World in Data (Barron Lee dataset)</a>',
            x = 0.01,
            y = -0.08,
            align = "left",
            showarrow = False,
            xref = "paper",
            yref = "paper",
        )
    ],

    # COLOR THEME
    plot_bgcolor = "#F5F5F5",
    paper_bgcolor = "#F5F5F5",

    # GEO PLOTS
    geo = dict(

        #GENERAL
        projection = dict(
            type = "natural earth",
            scale = 1,
            #rotation = dict(lat = 0, lon = 0, roll = 0),
        ),
        scope = "world",
        showframe = False,
        bgcolor = "#ECF6FC",

        # CONFIG
        showcountries = True,
        countrywidth = 0.5,
        showocean = True,
        oceancolor = "#ECF6FC",
        showland = True,
        landcolor = "#ADACAC",
        showcoastlines = True,
        coastlinewidth = 0.5,

    ),

)


# In[]:
# Creates frames

frames = []

for i, year in enumerate(years):

    # Create frame for each subplot
    frame_trace1 = dict(
        locationssrc = grid.get_column_reference("location{}".format(i + 1)),
        zsrc = grid.get_column_reference("z{}".format(i + 1)),
    )

    frame = dict(
        data = [frame_trace1],
        name = year,
        traces = [0],
    )

    frames.append(frame)


# In[]:
# Uploads animation

data = [trace1]
figure = dict(data=data, layout=layout, frames=frames)
py.icreate_animations(figure, filename=chart_filename, auto_open=False)
