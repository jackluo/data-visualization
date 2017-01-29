# In[]:
# Imports required libraries

from datetime import datetime

import numpy as np
import pandas as pd
import pandas_datareader.data as web

import plotly.plotly as py
from plotly.graph_objs import *
from plotly.grid_objs import Grid, Column


# In[]:
# Selects ticker, date range and other options

tickers = ["SPY", "GOOG", "AAPL"] # Input a list of tickers
date_start = "2014-01-01" # Start date to fetch
date_end = "2016-12-31" # End date to fetch

months = 24 # Sets how many ticks to display
hard_yzero = False # Should plot go to hard zero?
relative = True # Relative (%) change on graph, ensures multiple stocks start at same place
log_yaxis = False # Log axis for large timeframes


# In[]:
# Fetches and mangles data

chart_filename = "Stocks " + str(datetime.now())
grid_filename = chart_filename + " Grid"

dfs = {}
max_prices = {}
min_prices = {}

for ticker in tickers:
    df = web.get_data_yahoo(ticker, date_start, date_end)
    #df.columns

    if relative:
        first_price = df["Adj Close"][0] # First ticker price set as reference
        df["Rel Close"] = df["Adj Close"].apply(lambda x: x/first_price * 100)
        price = df["Rel Close"]
    else:
        price = df["Adj Close"]

    max_price = max(price.astype(float))
    min_price = min(price.astype(float))

    max_prices[ticker] = max_price
    min_prices[ticker] = min_price
    dfs[ticker] = df

# Dynamically sets max and minimum ranges (latter only if hard zero not enabled)
global_max_price = max(max_prices.values())
global_min_price = max(min_prices.values())
max_yrange = global_max_price + 0.15 * (global_max_price - global_min_price)

if not hard_yzero:
    min_yrange = global_min_price - 0.15 * (global_max_price - global_min_price)
else:
    min_yrange = 0


# In[]:
# Uploads Grid

columns = []

for ticker, df in dfs.items():

    if relative:
        price = df["Rel Close"]
    else:
        price = df["Adj Close"]

    for i in range(len(df.index)):
        columns.append(Column(df.index[:i + 1], str(ticker) + "x{}".format(i + 1)))
        columns.append(Column(price[:i + 1], str(ticker) + "y{}".format(i + 1)))

# Will throw error if file exists or path is not root
for column in columns: print(column)
grid = Grid(columns)
py.grid_ops.upload(grid, grid_filename, auto_open=False)


# In[]:
# Creates data

trace1 = Scatter(

    # GENERAL
    xsrc = grid.get_column_reference("x1"),
    ysrc = grid.get_column_reference("y1"),
    hoverinfo = "x+y+name",
    mode = "lines",
    name = ticker,

    # SPECS
    line = dict(
        color = color,
        #width = "2",
        #dash = "4",
    ),

)


# In[]:
# Creates layout

# Just copy paste this, not much to modify
updatemenus = dict(

    # GENERAL PLACEMENT
    type = "buttons",
    #showactive = False,
    x = 1.1,
    y = 1,
    xanchor = "right",
    yanchor = "top",
    pad = dict(t = 0, r = 10),

    # BUTTONS
    buttons=[
            dict(
                method = "animate",
                label = "Play",

                # PLAY
                args = [None,
                        dict(
                            frame = dict(duration = 10, redraw = False),
                            transition = dict(duration = 10, easing = "quadratic-in-out"),
                            fromcurrent = True,
                            mode = "immediate",
                            ),
                        ],
                ),
            dict(
                method = "animate",
                label = "Pause",

                # PAUSE
                args = [[None], # Note the list
                        dict(
                            frame = dict(duration = 0, redraw = False),
                            mode = "immediate",
                            ),
                        ],
                ),
            ],
)

layout = Layout(

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
        pad = dict(t=2, l=2, b=2, r=10),
    ),
    title="",

    # OPTIONAL
    showlegend = False,
    updatemenus = [updatemenus],
    #hovermode = "closest",

    # COLOR THEME
    plot_bgcolor = "#F5F5F5",
    paper_bgcolor = "#F5F5F5",

    # LINEAR PLOTS
    xaxis = dict(

        # RANGE
        range = [date_start, date_end],
        nticks = months,

        # TICKS
        tickangle = "45",
        #tickfont = dict(size = 10),

        # OTHER
        #showgrid = False,
        #zeroline = False,
    ),
    yaxis = dict(

        # RANGE
        range = [min_yrange, max_yrange],

        # TICKS
        tickprefix = "$",
        #tickfont = dict(size = 10),

        # OTHER
        #type = "log",
        #showgrid = False,
        #zeroline = False,
    ),

)

if log_yaxis: yaxis["type"] = "log"


# In[]:
# Creates frames

frames = []

for i in range(len(df.index)):
    frame = dict(
        data = [dict(xsrc = grid.get_column_reference("x{}".format(i+1)),
                     ysrc = grid.get_column_reference("y{}".format(i+1))
                     )],
        traces = [0],
    )
    frames.append(frame)


# In[]:
# Uploads animation

layout.title = ticker + " Daily Adjusted Close, " + date_start + " to " + date_end

# Will throw error if file exists or path is not root
data = [trace1]
figure = Figure(data=data, layout=layout, frames=frames)
py.icreate_animations(figure, filename=chart_filename, auto_open=False)
