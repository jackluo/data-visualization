# In[]:
# Imports required libraries

from datetime import datetime
import numpy as np
from numpy import sin, cos
import scipy.integrate as integrate

import plotly.plotly as py
from plotly.graph_objs import *
from plotly.grid_objs import Grid, Column


# In[]:
# Pendulum class
# https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

class DoublePendulum(object):
    """Double Pendulum Class

    init_state is [theta1, omega1, theta2, omega2] in degrees,
    where theta1, omega1 is the angular position and velocity of the first
    pendulum arm, and theta2, omega2 is that of the second pendulum arm
    """
    def __init__(self,
                 init_state = [120, 0, -20, 0],
                 L1=1.0,  # length of pendulum 1 in m
                 L2=1.0,  # length of pendulum 2 in m
                 M1=1.0,  # mass of pendulum 1 in kg
                 M2=1.0,  # mass of pendulum 2 in kg
                 G=9.8,  # acceleration due to gravity, in m/s^2
                 origin=(0, 0)):
        self.init_state = np.asarray(init_state, dtype='float')
        self.params = (L1, L2, M1, M2, G)
        self.origin = origin
        self.time_elapsed = 0

        self.state = self.init_state * np.pi / 180.

    def position(self):
        """compute the current x,y positions of the pendulum arms"""
        (L1, L2, M1, M2, G) = self.params

        x = np.cumsum([self.origin[0],
                       L1 * sin(self.state[0]),
                       L2 * sin(self.state[2])])
        y = np.cumsum([self.origin[1],
                       -L1 * cos(self.state[0]),
                       -L2 * cos(self.state[2])])
        return x, y

    def energy(self):
        """compute the energy of the current state"""
        (L1, L2, M1, M2, G) = self.params

        x = np.cumsum([L1 * sin(self.state[0]),
                       L2 * sin(self.state[2])])
        y = np.cumsum([-L1 * cos(self.state[0]),
                       -L2 * cos(self.state[2])])
        vx = np.cumsum([L1 * self.state[1] * cos(self.state[0]),
                        L2 * self.state[3] * cos(self.state[2])])
        vy = np.cumsum([L1 * self.state[1] * sin(self.state[0]),
                        L2 * self.state[3] * sin(self.state[2])])

        U = G * (M1 * y[0] + M2 * y[1])
        K = 0.5 * (M1 * np.dot(vx, vx) + M2 * np.dot(vy, vy))

        return U + K

    def dstate_dt(self, state, t):
        """compute the derivative of the given state"""
        (M1, M2, L1, L2, G) = self.params

        dydx = np.zeros_like(state)
        dydx[0] = state[1]
        dydx[2] = state[3]

        cos_delta = cos(state[2] - state[0])
        sin_delta = sin(state[2] - state[0])

        den1 = (M1 + M2) * L1 - M2 * L1 * cos_delta * cos_delta
        dydx[1] = (M2 * L1 * state[1] * state[1] * sin_delta * cos_delta
                   + M2 * G * sin(state[2]) * cos_delta
                   + M2 * L2 * state[3] * state[3] * sin_delta
                   - (M1 + M2) * G * sin(state[0])) / den1

        den2 = (L2 / L1) * den1
        dydx[3] = (-M2 * L2 * state[3] * state[3] * sin_delta * cos_delta
                   + (M1 + M2) * G * sin(state[0]) * cos_delta
                   - (M1 + M2) * L1 * state[1] * state[1] * sin_delta
                   - (M1 + M2) * G * sin(state[2])) / den2

        return dydx

    def step(self, dt):
        """execute one time step of length dt and update state"""
        self.state = integrate.odeint(self.dstate_dt, self.state, [0, dt])[1]
        self.time_elapsed += dt


# In[]:
# Sets up pendulum

pendulum = DoublePendulum([180., 0.0, -20., 0.0])
dt = 1./30 # 30 fps


# In[]:
# Uploads Grid

chart_filename = "Pendulum " + str(datetime.now())
grid_filename = chart_filename + " Grid"
columns = []

# Actual animation function
for i in range(500):

    pendulum.step(dt)
    x, y = pendulum.position()
    x = list(x)
    y = list(y)

    columns.append(Column(x, "x{}".format(i + 1)))
    columns.append(Column(y, "y{}".format(i + 1)))

grid = Grid(columns)
py.grid_ops.upload(grid, grid_filename, auto_open=False)


# In[]:
# Creates data

trace1 = Scatter(
    xsrc = grid.get_column_reference("x1"),
    ysrc = grid.get_column_reference("y1"),
    mode = "lines+markers",
)


# In[]:
# Creates layout

animation_time = 20
transition_time = 10

updatemenus = dict(
    type = "buttons",
    buttons=[
        dict(
            method = "animate",
            label = "Play",
            args = [None,
                    dict(
                        frame = dict(duration = animation_time, redraw = False),
                        transition = dict(duration = transition_time, easing = "quadratic-in-out"),
                        mode = "immediate"
                    ),
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

layout = dict(
    width = 720,
    height = 720,
    xaxis = dict(range = [-2, 2]),
    yaxis = dict(range = [-2, 2]),
    hovermode = closest,
    updatemenus = [updatemenus],
)


# In[]:
# Creates frames

frames = []

for i in range(500):
    frame = dict(
        data = [dict(xsrc = grid.get_column_reference("x{}".format(i+1)),
                     ysrc = grid.get_column_reference("y{}".format(i+1))
                     )],
        traces = [0],
    )
    frames.append(frame)


# In[]:
# Uploads animation

figure = dict(data=[trace1], layout=layout, frames=frames)
py.icreate_animations(figure, filename=chart_filename, auto_open=False)
