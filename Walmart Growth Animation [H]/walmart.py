# In[]:
# Import required libraries

from datetime import datetime
import numpy as np
import pandas as pd

import plotly.plotly as py
from plotly.graph_objs import *
from plotly.grid_objs import Grid, Column

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjaXhzYTB0bHcwOHNoMnFtOWZ3YWdreDB3In0.pjROwb9_CEuyKPE-x0lRUw'


# In[]:
# Select data

filename = "data/walmart_store_openings.csv"
chart_filename = "Walmart " + str(datetime.now())

df = pd.read_csv(filename, encoding = "utf-8-sig")
#df
#print(df.columns)

# Gets list of years
years = df["YEAR"].unique()
years = list(sorted(years.astype(str)))

# Bug with Grid parsing if dataset isn't sanitized, need to return NaN instead of empty []
#years = [str(i) for i in range(1962,2007)]

# Groups by year and count number of stores
ylist = df.groupby("YEAR").count()["storenum"].astype(int)
ylist_cum = ylist.cumsum()

# Gets max range for subplot (minimum set to 0, no y-axis jump)
max_range = max(ylist) * 1.15
max_range_cum = max(ylist_cum) * 1.15

# Converts list items to string
ylist = list(ylist.astype(str))
ylist_cum = list(ylist_cum.astype(str))


# In[]:
# Upload all 2 Grids

# Since Grid has a size limit, it is good practice to upload multiple Grids for suplots in case of large datasets
grid_filename = chart_filename + " Grid"
grid_filename2 = grid_filename + "2"

columns = []
columns2 = []

for i, year in enumerate(years):

    # Filter df for current year only
    current_year = df[df["YEAR"] == int(year)]

    lons = list(current_year["LON"].astype(float))
    lats = list(current_year["LAT"].astype(float))
    texts = list(current_year["STRCITY"].astype(str))

    # Iteratively grows list to create running counts
    xvalues = years[:i + 1]
    yvalues = ylist[:i + 1]
    yvalues_cum = ylist_cum[:i + 1]

    columns.append(Column(lons, "x{}".format(i + 1)))
    columns.append(Column(lats, "y{}".format(i + 1)))
    columns.append(Column(texts, "text{}".format(i + 1)))

    columns2.append(Column(xvalues, "x{}".format(i + 1)))
    columns2.append(Column(yvalues, "y{}".format(i + 1)))
    columns2.append(Column(yvalues_cum, "y_cum{}".format(i + 1)))

# Will throw error if file exists or path is not root
grid = Grid(columns)
py.grid_ops.upload(grid, grid_filename, auto_open=False)

grid2 = Grid(columns2)
py.grid_ops.upload(grid2, grid_filename2, auto_open=False)



# In[]:
# Create data

# Main trace
trace1 = Scattermapbox(

    # GENERAL
    lonsrc = grid.get_column_reference("x1"),
    latsrc = grid.get_column_reference("y1"),
    textsrc = grid.get_column_reference("text1"),
    mode = "markers",
    hoverinfo = "lon+lat+text",

    # SPECS
    marker = dict(
        size = 10,
        color = "#54D9F3",
        opacity = "0.6",
    ),
)

# Non-cumulative secondary
trace2 = Scatter(

    # GENERAL
    xsrc = grid2.get_column_reference("x1"),
    ysrc = grid2.get_column_reference("y1"),
    mode = "lines+markers",
    hoverinfo = "x+y",

    # SPECS
    line = dict(
        color = "#4ADFD0",
    ),
    marker = dict(
        symbol = "cross-thin-open",
    ),
    xaxis = "x",
    yaxis = "y2",

)

# Cumulative secondary
trace3 = Scatter(

    # GENERAL
    xsrc = grid2.get_column_reference("x1"),
    ysrc = grid2.get_column_reference("y_cum1"),
    mode = "lines",
    fill = "tozeroy",
    hoverinfo = "x+y",

    # SPECS
    line = dict(
        color = "#1CA9E2",
    ),
    xaxis = "x2",
    yaxis = "y",

)

# Note that subplots are mapped to reversed yaxis (temporary solution, bugfix impending)


# In[]:
# Set up slider and buttons

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
    xanchor = 'right',
    yanchor = 'top',
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
                    frame = dict(duration = 300, redraw = True), # False quicker but disables animations
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
                    frame = dict(duration = 0, redraw = True), # Idem
                    mode = "immediate",
                    transition = dict(duration = 0),
                    ),
                ],
            ),
        ],

)


# In[]:
# Create layout

layout = dict(

    title = "Growth of Walmart stores, 1962-2006",

    # GENERAL LAYOUT
    width = 960,
    height = 720,
    autosize = True,
    font = dict(
        family = "Overpass",
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
        zoom = 3.0,
        style = "dark",
        domain = dict(
            x = [0, 1],
            y = [0.24, 1]
        ),
    ),

    # AXIS (see current bug above)
    xaxis = dict(
        range = ["1962", "2006"],
        domain = [0, 0.48],
        anchor = "y2",
        title = "Stores/year",
    ),
    yaxis2 = dict(
        range = [0, max_range],
        domain = [0, 0.20],
        anchor = "x",
    ),

    xaxis2 = dict(
        range = ["1962", "2006"],
        domain = [0.53, 1],
        anchor = "y",
        title = "Total stores",
    ),
    yaxis = dict(
        range = [0, max_range_cum],
        domain = [0, 0.20],
        anchor = "x2",
    ),

)


# In[]:
# Create frames

frames = []

for i, year in enumerate(years):

    # Create frame for each subplot
    frame_trace1 = dict(
        lonsrc = grid.get_column_reference("x{}".format(i + 1)),
        latsrc = grid.get_column_reference("y{}".format(i + 1)),
        textsrc = grid.get_column_reference("text{}".format(i + 1)),
    )

    frame_trace2 = dict(
        xsrc = grid2.get_column_reference("x{}".format(i + 1)),
        ysrc = grid2.get_column_reference("y{}".format(i + 1)),
    )

    frame_trace3 = dict(
        xsrc = grid2.get_column_reference("x{}".format(i + 1)),
        ysrc = grid2.get_column_reference("y_cum{}".format(i + 1)),
    )

    # No Grid upload needed since not plot data
    frame_layout = dict(
        annotations = [
            dict(
                text = year + " stores: {:>4}".format(ylist[i]) + "<br>" + "Total stores: {:>4}".format(ylist_cum[i]),
                x = 1,
                y = 0.98,
                font = dict(size = 16),
                xanchor = "right",
                showarrow = False,
                xref = "paper",
                yref = "paper",
            )
        ]
    )

    # [0,1,2] specifies the 3 subplots to apply frames to
    frame = dict(
        data = [frame_trace1, frame_trace2, frame_trace3],
        name = year,
        traces = [0, 1, 2],
        layout = frame_layout, # Need redraw = True to refresh
    )

    frames.append(frame)


# In[]:
# Upload animation

data = [trace1, trace2, trace3]
figure = dict(data=data, layout=layout, frames=frames)
py.icreate_animations(figure, filename=chart_filename, auto_open=False)
