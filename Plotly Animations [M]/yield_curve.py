import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *

df = pd.read_csv("data/yield_curve.csv")

xlist = list(df["x"].dropna())
ylist = list(df["y"].dropna())

del df["x"]
del df["y"]

zlist = []
for row in df.iterrows():
    index, data = row
    zlist.append(data.tolist())

trace1 = dict(

    x = xlist,
    y = ylist,
    z = zlist,

    lighting = {
        "ambient": 0.95,
        "diffuse": 0.99,
        "fresnel": 0.01,
        "roughness": 0.01,
        "specular": 0.01,
    },
    showscale = False,
    type = "surface",
    zmax = 9.18,
    zmin = 0,
    scene = "scene",

)

updatemenus = dict(

    # GENERAL
    type = "buttons",
    showactive = False,
    x = 0.1, #x = 1.1
    y = 0, #y = 1
    active = 99,
    bgcolor = "#000000",
    pad = dict(t = 60, r = 10),
    xanchor = "right",
    yanchor = "top",
    direction = "left",

    # BUTTONS
    buttons=[
        dict(
            method = "relayout",
            label = "Slide 1",

            # ARGUMENTS
            args = [
                {
                    "scene.camera.eye.x" : 1,
                    "scene.camera.eye.y" : 1,
                    "scene.camera.eye.z" : 1,
                    "title" : "TEST"
                },
            ],
        ),
        dict(
            method = "relayout",
            label = "Slide 2",

            # ARGUMENTS
            args = [
                {
                    "scene.aspectratio.x" : 10,
                    "scene.camera.eye": {'x': 0, 'y':0, 'z':0},
                    #"scene.camera.eye.x" : 0,
                    #"scene.camera.eye.y" : 0,
                    #"scene.camera.eye.z" : 0,
                    "title" : "Blabla"
                },
            ],
        ),
    ],

)

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
            "x": 0.5,
            "y": 0.5,
            "z": 0.5,
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

data = [trace1]
fig = dict(data=data, layout=layout)
plot_url = py.plot(fig, validate= False)
