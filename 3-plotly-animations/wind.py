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

filename = "data/turbine_locations.csv"
chart_filename = "Wind turbines " + str(datetime.now())

df = pd.read_csv(filename, encoding="utf-8-sig")
#df
#print(df.columns)

# Filter -99999 (missing) years
# Replace -99999 blade lengths by NaN (their size will be dynamically determined for accuracy)
df = df[df["on_year_s"] != -99999]
df["blade_l"].replace(-99999, np.NaN, inplace=True)
#print(df["blade_l"])

# Remove site name "unknowns" (partial match, need regex = True)
df["site_name"].replace("unknown", "", regex=True)

# Gets list of years
years = df["on_year_s"].unique()
years = list(sorted(years.astype(str)))

# Groups by year and count number of turbines
ylist = df.groupby("on_year_s").count()["unique_id"]
ylist_cum = ylist.cumsum()

# Make running count of states
statecount = df.groupby("on_year_s")["state"].nunique()
statecount = list(statecount.astype(str))

# Gets max range for subplot (minimum set to 0, no y-axis jump)
max_range = max(ylist) * 1.25
max_range_cum = max(ylist_cum) * 1.25

min_range_year = 1981
max_range_year = 2014
max_range_blades = 60
max_range_states = 500
max_range_statecount = 40

# Converts list items to string
ylist = list(ylist.astype(str))
ylist_cum = list(ylist_cum.astype(str))


# In[]:
# Uploads all 2 Grids

# Since Grid has a size limit, it is good practice to upload multiple Grids for suplots in case of large datasets
grid_filename = chart_filename + " Grid"
grid_filename2 = grid_filename + "2"

columns = []
columns2 = []

blade_avgs = []

for i, year in enumerate(years):

    # Filter df for current year only
    current_year = df[df["on_year_s"] == int(year)]

    # Get average blade length for the year (ignores NaN values)
    blade_avg = current_year["blade_l"].astype(float).mean()

    # If whole average is NaN aveage blade length is that of last years
    if blade_avg != blade_avg:
        blade_avg = blade_avgs[-1]

    blade_avgs.append(blade_avg)

    # Replace the NaN by that average to not skew data
    current_year["blade_l"].fillna(blade_avg, inplace=True)

    lons = list(current_year["long_DD"].astype(float))
    lats = list(current_year["lat_DD"].astype(float))
    texts = list(current_year["site_name"].astype(str))
    sizes = list(current_year["blade_l"].astype(float))

    # Iteratively grows list to create running counts
    xvalues = years[:i + 1]
    yvalues = ylist[:i + 1]
    yvalues_cum = ylist_cum[:i + 1]

    # Idem for state count
    statevalues = statecount[:i + 1]

    # Get data for Choropleth inlay
    statelist = current_year.groupby("state").count()["unique_id"]
    states = list(statelist.index.astype(str))
    zvalues = list(statelist.astype(int))

    columns.append(Column(lons, "x{}".format(i + 1)))
    columns.append(Column(lats, "y{}".format(i + 1)))
    columns.append(Column(texts, "text{}".format(i + 1)))
    columns.append(Column(sizes, "size{}".format(i + 1)))

    columns2.append(Column(xvalues, "x{}".format(i + 1)))
    columns2.append(Column(yvalues, "y{}".format(i + 1)))
    columns2.append(Column(yvalues_cum, "y_cum{}".format(i + 1)))
    columns2.append(Column(blade_avgs, "blade_avg{}".format(i + 1)))
    columns2.append(Column(statevalues, "state{}".format(i + 1)))
    columns2.append(Column(states, "location{}".format(i + 1)))
    columns2.append(Column(zvalues, "z{}".format(i + 1)))

# Will throw error if file exists or path is not root
grid = Grid(columns)
py.grid_ops.upload(grid, grid_filename, auto_open=False)

grid2 = Grid(columns2)
py.grid_ops.upload(grid2, grid_filename2, auto_open=False)


# In[]:
# Creates data

viridis = [[0, "rgb(221,42,145)"], [0.3, "rgb(177,77,236)"], [0.4, "rgb(118,117,237)"],
            [0.65, "rgb(46,142,191)"], [0.8, "rgb(11,152,121)"], [1, "rgb(19,152,99)"]]

blackpink = [[0, "rgb(59,37,73)"], [0.35, "rgb(76,43,96)"], [0.6, "rgb(93,49,119)"],
            [0.6, "rgb(109,54,143)"], [0.7, "rgb(143,66,189)"], [1, "rgb(152,80,200)"]]

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

        # BASIC
        sizesrc = grid.get_column_reference("size1"),
        colorsrc = grid.get_column_reference("size1"),
        sizeref = 4,
        opacity = "0.6",

        # COLORSCALE
        cmin = 0,
        cmax = max_range_blades,
        autocolorscale = False,
        colorscale = viridis,
        colorbar = dict(
            title = "Turbine<br>blade<br>length (m)<br>",
        ),
    ),

)

# Non-cumulative count
trace2 = Scatter(

    # GENERAL
    xsrc = grid2.get_column_reference("x1"),
    ysrc = grid2.get_column_reference("y1"),
    mode = "lines+markers",
    hoverinfo = "x+y",

    # SPECS
    line = dict(
        color = "#17BECF",
    ),
    marker = dict(
        symbol = "cross-thin-open",
    ),
    xaxis = "x",
    yaxis = "y4",

)

# Cumulative count
trace3 = Scatter(

    # GENERAL
    xsrc = grid2.get_column_reference("x1"),
    ysrc = grid2.get_column_reference("y_cum1"),
    mode = "lines",
    fill = "tozeroy",
    hoverinfo = "x+y",

    # SPECS
    line = dict(
        color = "rgb(17,123,215)",
    ),
    xaxis = "x2",
    yaxis = "y3",

)

# Average blade length
trace4 = Scatter(

    # GENERAL
    xsrc = grid2.get_column_reference("x1"),
    ysrc = grid2.get_column_reference("blade_avg1"),
    mode = "markers",
    hoverinfo = "x+y",

    # SPECS
    marker = dict(
        color = "#FFB4EF",
        symbol = "diamond-open-dot",
    ),
    xaxis = "x3",
    yaxis = "y2",

)

# Cumulative secondary
trace5 = Scatter(

    # GENERAL
    xsrc = grid2.get_column_reference("x1"),
    ysrc = grid2.get_column_reference("state1"),
    mode = "lines",
    hoverinfo = "x+y",

    # SPECS
    line = dict(
        color = "#99D0AC",
        shape = "hvh",

    ),
    xaxis = "x4",
    yaxis = "y",

)

# States on choropleth
trace6 = Choropleth(

    # GENERAL
    locationssrc = grid2.get_column_reference("location1"),
    zsrc = grid2.get_column_reference("z1"),
    hoverinfo = "location+z",
    locationmode = "USA-states",

    # COLORSCALE
    zmin = 0,
    zmax = max_range_states,
    autocolorscale = False,
    colorscale = blackpink,
    showscale = False,

)

# Note that subplots are mapped to reversed yaxis (temporary solution, bugfix impending)


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

    title = "US Wind turbines, 1981-2014",

    # GENERAL LAYOUT
    width = 840,
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

    annotations = [
        dict(
            text = "Zoom in to see the ~ 50k <br>individual points",
            x = 0.01,
            y = 0.2,
            align = "left",
            showarrow = False,
            xref = "paper",
            yref = "paper",
        )
    ],

    images = [
        dict(
            source="http://2.bp.blogspot.com/-Ngg9gOXDnI4/Us2HY9LD9GI/AAAAAAAAAJw/O7_YtseZlZI/s1600/usgs_id_trans2.png",
            x = 0,
            y = 1.05,
            sizex = 0.10,
            sizey = 0.10,
            xref = "paper",
            yref = "paper",
            xanchor = "left",
            yanchor = "top"
      )
    ],

    # COLOR THEME
    plot_bgcolor = "#191A1A",
    paper_bgcolor = "#020202",

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
            y = [0.18, 0.77]
        ),
    ),

    # GEO PLOTS
    geo = dict(
        projection = dict(
            type = "albers usa",
            scale = 1,
            #rotation = dict(lat = 0, lon = 0, roll = 0),
        ),
        scope = "usa",
        showframe = False,
        resolution = "100",
        bgcolor = "rgba(0,0,0,0)",
        showland = True,
        landcolor = "rgb(25,25,26)",
        domain = dict(
            x = [0.82, 1],
            y = [0.20, 0.30]
        ),
    ),

    # AXIS (see current bug above)
    xaxis = dict(
        range = [min_range_year, max_range_year],
        domain = [0, 0.48],
        anchor = "y4",
        title = "Turbines/year",
        titlefont = dict(size = 12),
        tickfont = dict(size = 10),
    ),
    yaxis4 = dict(
        range = [0, max_range],
        domain = [0, 0.16],
        anchor = "x",
        tickfont = dict(size = 10),
    ),

    xaxis2 = dict(
        range = [min_range_year, max_range_year],
        domain = [0.52, 1],
        anchor = "y3",
        title = "Total turbines",
        titlefont = dict(size = 12),
        tickfont = dict(size = 10),
    ),
    yaxis3 = dict(
        range = [0, max_range_cum],
        domain = [0, 0.16],
        anchor = "x2",
        tickfont = dict(size = 10),
    ),

    xaxis3 = dict(
        range = [min_range_year, max_range_year],
        domain = [0, 0.48],
        anchor = "y2",
        side = "top",
        title = "Average turbine length",
        titlefont = dict(size = 12),
        tickfont = dict(size = 10),
    ),
    yaxis2 = dict(
        range = [0, max_range_blades],
        domain = [0.79, 0.95],
        side = "left",
        anchor = "x3",
        tickfont = dict(size = 12),
    ),

    xaxis4 = dict(
        range = [min_range_year, max_range_year],
        domain = [0.52, 1],
        anchor = "y",
        side = "top",
        title = "Number of states",
        titlefont = dict(size = 12),
        tickfont = dict(size = 10),
    ),
    yaxis1 = dict(
        range = [0, max_range_statecount],
        domain = [0.79, 0.95],
        anchor = "x4",
        tickfont = dict(size = 10),
    ),

)


# In[]:
# Creates frames

frames = []

for i, year in enumerate(years):

    # Create frame for each subplot
    frame_trace1 = dict(
        lonsrc = grid.get_column_reference("x{}".format(i + 1)),
        latsrc = grid.get_column_reference("y{}".format(i + 1)),
        textsrc = grid.get_column_reference("text{}".format(i + 1)),
        marker = dict(
            sizesrc = grid.get_column_reference("size{}".format(i + 1)),
            colorsrc = grid.get_column_reference("size{}".format(i + 1)),
        )
    )

    frame_trace2 = dict(
        xsrc = grid2.get_column_reference("x{}".format(i + 1)),
        ysrc = grid2.get_column_reference("y{}".format(i + 1)),
    )

    frame_trace3 = dict(
        xsrc = grid2.get_column_reference("x{}".format(i + 1)),
        ysrc = grid2.get_column_reference("y_cum{}".format(i + 1)),
    )

    frame_trace4 = dict(
        xsrc = grid2.get_column_reference("x{}".format(i + 1)),
        ysrc = grid2.get_column_reference("blade_avg{}".format(i + 1)),
    )

    frame_trace5 = dict(
        xsrc = grid2.get_column_reference("x{}".format(i + 1)),
        ysrc = grid2.get_column_reference("state{}".format(i + 1)),
    )

    frame_trace6 = dict(
        locationssrc = grid2.get_column_reference("location{}".format(i + 1)),
        zsrc = grid2.get_column_reference("z{}".format(i + 1)),
    )

    # [0,1,2] specifies the 3 subplots to apply frames to
    frame = dict(
        data = [frame_trace1, frame_trace2, frame_trace3, frame_trace4, frame_trace5, frame_trace6],
        name = year,
        traces = [0, 1, 2, 3, 4, 5],
    )

    frames.append(frame)


# In[]:
# Uploads animation

data = [trace1, trace2, trace3, trace4, trace5, trace6]
figure = dict(data=data, layout=layout, frames=frames)
py.icreate_animations(figure, filename=chart_filename, auto_open=False)
