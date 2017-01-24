# In[]:
# Imports required libraries

from datetime import datetime
import numpy as np
from scipy.spatial.distance import pdist, squareform

import plotly.plotly as py
from plotly.graph_objs import *
from plotly.grid_objs import Grid, Column


# In[]:
# ParticleBox class
# https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

class ParticleBox(object):
    """Orbits class

    init_state is an [N x 4] array, where N is the number of particles:
       [[x1, y1, vx1, vy1],
        [x2, y2, vx2, vy2],
        ...               ]

    bounds is the size of the box: [xmin, xmax, ymin, ymax]
    """
    def __init__(self,
                 init_state = [[1, 0, 0, -1],
                               [-0.5, 0.5, 0.5, 0.5],
                               [-0.5, -0.5, -0.5, 0.5]],
                 bounds = [-2, 2, -2, 2],
                 size = 0.04,
                 M = 0.05,
                 G = 9.8):
        self.init_state = np.asarray(init_state, dtype=float)
        self.M = M * np.ones(self.init_state.shape[0])
        self.size = size
        self.state = self.init_state.copy()
        self.time_elapsed = 0
        self.bounds = bounds
        self.G = G

    def step(self, dt):
        """step once by dt seconds"""
        self.time_elapsed += dt

        # update positions
        self.state[:, :2] += dt * self.state[:, 2:]

        # find pairs of particles undergoing a collision
        D = squareform(pdist(self.state[:, :2]))
        ind1, ind2 = np.where(D < 2 * self.size)
        unique = (ind1 < ind2)
        ind1 = ind1[unique]
        ind2 = ind2[unique]

        # update velocities of colliding pairs
        for i1, i2 in zip(ind1, ind2):
            # mass
            m1 = self.M[i1]
            m2 = self.M[i2]

            # location vector
            r1 = self.state[i1, :2]
            r2 = self.state[i2, :2]

            # velocity vector
            v1 = self.state[i1, 2:]
            v2 = self.state[i2, 2:]

            # relative location & velocity vectors
            r_rel = r1 - r2
            v_rel = v1 - v2

            # momentum vector of the center of mass
            v_cm = (m1 * v1 + m2 * v2) / (m1 + m2)

            # collisions of spheres reflect v_rel over r_rel
            rr_rel = np.dot(r_rel, r_rel)
            vr_rel = np.dot(v_rel, r_rel)
            v_rel = 2 * r_rel * vr_rel / rr_rel - v_rel

            # assign new velocities
            self.state[i1, 2:] = v_cm + v_rel * m2 / (m1 + m2)
            self.state[i2, 2:] = v_cm - v_rel * m1 / (m1 + m2)

        # check for crossing boundary
        crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)
        crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.size)
        crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.size)
        crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.size)

        self.state[crossed_x1, 0] = self.bounds[0] + self.size
        self.state[crossed_x2, 0] = self.bounds[1] - self.size

        self.state[crossed_y1, 1] = self.bounds[2] + self.size
        self.state[crossed_y2, 1] = self.bounds[3] - self.size

        self.state[crossed_x1 | crossed_x2, 2] *= -1
        self.state[crossed_y1 | crossed_y2, 3] *= -1

        # add gravity
        self.state[:, 3] -= self.M * self.G * dt


# In[]:
# Sets up initial state

np.random.seed(0)
init_state = -0.5 + np.random.random((50, 4))
init_state[:, :2] *= 3.9

box = ParticleBox(init_state, size=0.04)
dt = 1. / 30 # 30fps


# In[]:
# Uploads Grid and performs animation

chart_filename = "Particles " + str(datetime.now())
grid_filename = chart_filename + " Grid"
columns = []

# Actual animation function
for i in range(600):

    box.step(dt)
    x, y = box.state[:, 0], box.state[:, 1]
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
    mode = "markers",
)


# In[]:
# Creates layout

animation_time = 10
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
    xaxis = dict(range = [-3.2, 3.2]),
    yaxis = dict(range = [-2.4, 2.4]),
    updatemenus = [updatemenus],
)


# In[]:
# Creates frames

frames = []

for i in range(600):
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
