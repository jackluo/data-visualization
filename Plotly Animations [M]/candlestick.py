# In[]:
# Imports required libraries

from datetime import datetime
import numpy as np
import pandas as pd
import pandas_datareader.data as web

import plotly.plotly as py
from plotly.graph_objs import *


# In[]:
# Selects ticker, date range and other options

ticker = "GS"
date_start = "2014-01-01"
date_end = "2016-12-31"

#increasing_color = "green"
#decreasing_color = "red"

#months = 24
#hard_yzero = False
#log_yaxis = False
#color = "green"
#color = "#13A0FD"


# In[]:
# Fetches and mangles data

chart_filename = ticker + " " + date_start + " to " + date_end
grid_filename = chart_filename + " Grid"

df = web.get_data_yahoo(ticker, date_start, date_end)


# In[]:
# Creates Candlestick

trace1 = Candlestick(

    # GENERAL
    x = df.index,
    open = df["Open"],
    high = df["High"],
    low = df["Low"],
    close = df["Close"],
    name = ticker,

    increasing = dict( line = dict( color = "green") ),
    decreasing = dict( line = dict( color = "red" ) ),

    # OPTIONAL
    #opacity = "0.2",
    #visible = "legendonly",
    #legendgroup = "group1",
    #connectgaps = True,
    #xaxis = "x2",
    #overlaying = "y",
    yaxis = "y",

)


# In[]:
# Creates layout

layout = Layout(

    title = "",

    # GENERAL LAYOUT
    width = 1280,
    height = 720,
    autosize = True,
    font = dict(
        family = "Overpass",
        size = 12,
    ),
    margin = dict(
        t = 40,
        l = 40,
        b = 40,
        r = 40,
        pad = 0,
    ),

    # OPTIONAL
    #showlegend = False,
    #hovermode = "closest",
    #shapes = shapes,
    #annotations = annotations,
    #images = images,

    # ANIMATIONS
    #slider = slider,
    #sliders = [sliders],
    #updatemenus = [updatemenus],

    # COLOR THEME
    #plot_bgcolor = "#151515", #"#191A1A",
    #paper_bgcolor = "#020202",
    #plot_bgcolor = "#F5F5F5",
    #paper_bgcolor = "#F5F5F5",

    # LEGEND
    legend = dict(
    x = 1.02,
    y = 1,
    #font = dict(size = 10),
    #tracegroupgap = 20,
    #orientation = "h",
    #traceorder = "reversed",
    ),

    # LINEAR PLOTS
    xaxis = dict(

        # RANGE
        #rangemode = "tozero",
        #range = ,
        #nticks = , #OR
        #tick0 = , #AND
        #dtick = ,

        # TICKS
        #tickprefix = "$",
        #ticksuffix = "%",
        #tickangle = "45",
        #tickfont = dict(size = 10),
        #showticklabels = False,

        # OTHER
        #type = "log",
        #domain = [0, 0.48],
        #showline = False,
        #showgrid = False,
        #zeroline = False,
        #side = "right",
        #anchor = "x(n)",
        #titlefont = dict(size = 12),

        # RANGE SELECTOR
        rangeselector = dict(
            visible = True,
            #activecolor = "#F5F5F5",
            #bordercolor = "#F5F5F5",
            bgcolor = "#CCCCCC",

            # Buttons
            buttons = [
                dict(
                    count = 1,
                    step = "day", # "year", "day", "hour" etc
                    stepmode = "backward", # stepmode = "backward"
                    label = "1D"
                ),
                dict(
                    count = 5,
                    step = "day", # "year", "day", "hour" etc
                    stepmode = "backwrad", # stepmode = "backward"
                    label = "5D"
                ),
                dict(
                    count = 1,
                    step = "month", # "year", "day", "hour" etc
                    stepmode = "backward", # stepmode = "backward"
                    label = "1M"
                ),
                dict(
                    count = 3,
                    step = "month", # "year", "day", "hour" etc
                    stepmode = "backward", # stepmode = "backward"
                    label = "3M"
                ),
                dict(
                    count = 6,
                    step = "month", # "year", "day", "hour" etc
                    stepmode = "backward", # stepmode = "backward"
                    label = "6M"
                ),
                dict(
                    count = 1,
                    step = "year", # "year", "day", "hour" etc
                    stepmode = "backward", # stepmode = "backward"
                    label = "1Y"
                ),
                dict(
                    count = 2,
                    step = "year", # "year", "day", "hour" etc
                    stepmode = "backward", # stepmode = "backward"
                    label = "2Y"
                ),
                dict(
                    count = 5,
                    step = "year", # "year", "day", "hour" etc
                    stepmode = "backward", # stepmode = "backward"
                    label = "5Y"
                ),
                dict(
                    count = 1,
                    step = "all", # "year", "day", "hour" etc
                    stepmode = "backward", # stepmode = "backward"
                    label = "MAX"
                ),
                dict(
                    count = 1,
                    step = "year", # "year", "day", "hour" etc
                    stepmode = "todate", # stepmode = "backward"
                    label = "YTD"
                ),
            ]
        )

    ),
    yaxis = dict(

        # RANGE
        #rangemode = "tozero",
        #range = ,
        #nticks = , #OR
        #tick0 = , #AND
        #dtick = ,

        # TICKS
        #tickprefix = "$",
        #ticksuffix = "%",
        #tickangle = "45",
        #tickfont = dict(size = 10),
        #showticklabels = False,

        # OTHER
        #type = "log",
        #domain = [0, 0.48],
        #showline = False,
        #showgrid = False,
        #zeroline = False,
        #side = "right",
        #anchor = "x(n)",
        #titlefont = dict(size = 12),
    ),
    # xaxis, xaxis2, xaxis3, etc...

    # BAR PLOTS
    barmode = "group",
    #barmode = "stack",
    #barmode = "relative",


)

data = [trace1]

figure = dict(data = data, layout = layout)
py.plot(figure, filename="A", overwrite=True)
