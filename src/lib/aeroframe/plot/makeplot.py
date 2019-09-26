#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019 Airinnova AB and the AeroFrame authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Authors:
# * Aaron Dettmann

"""
Plot tools
"""

import logging

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from aeroframe.data.datafields import get_total_num_points

logger = logging.getLogger(__name__)


# 3D plots

def plot_all(data_fields, density=1.0):
    """
    Visualise a load or deformation fields

    Args:
        :data_fields: (dict) Either load or deformation fields
        :density: (float) Data density (plot approx. x percent of the data)
    """

    fig, ax = _init_3D_plot()
    _set_limits(ax, data_fields)
    _plot_data_fields(ax, data_fields, density=density)

    plt.show()
    plt.close('all')


def _init_3D_plot():
    """
    Initialise a 3D plot and return the matplotlib 'figure' and 'axes' object

    Returns:
        :fig: (obj) Matplotlib figure object
        :ax: (obj) Matplotlib axes object
    """

    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    return fig, ax


def _set_limits(ax, data_fields):
    """
    Adjust the plot limits for an axis object

    Args:
        :ax: (obj) Matplotlib axes object
        :data_fields: (dict) Either load or deformation fields
    """

    limits = {
        'x': [-0.01, 0.01],
        'y': [-0.01, 0.01],
        'z': [-0.01, 0.01],
    }

    for data_field in data_fields.values():
        xyz = data_field[:, 0:3]

        for coord, idx in zip('xyz', (0, 1, 2)):
            min_in_data = np.amin(xyz[:, idx])
            max_in_data = np.amax(xyz[:, idx])

            if min_in_data < limits[coord][0]:
                limits[coord][0] = min_in_data

            if max_in_data > limits[coord][1]:
                limits[coord][1] = max_in_data

    # Adjust the limits
    ax.set_xlim(*limits['x'])
    ax.set_ylim(*limits['y'])
    ax.set_zlim(*limits['z'])
    ax.set_aspect('equal')
    _set_equal_aspect_3D(ax)


def _set_equal_aspect_3D(ax):
    """
    Set aspect ratio of plot correctly

    Args:
        :ax: (obj) Matplotlib axes object
    """
    # See https://stackoverflow.com/a/19248731

    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:, 1] - extents[:, 0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)


def _plot_data_fields(ax, data_fields, density=1.0):
    """
    Add data fields to an axis plot object

    Plot:
        :ax: (obj) Matplotlib axes object
        :data_fields: (dict) Either load or deformation fields
        :density: (float) Data density (plot approx. x percent of the data)
    """

    if not 0 < density <= 1:
        raise ValueError("'density' must be in range (0, 1]")

    # Plot  every nth point
    nth = int(1/density)

    for uid, data_field in data_fields.items():
        sliced_data_field = data_field[::nth, 0:3]
        x = sliced_data_field[:, 0]
        y = sliced_data_field[:, 1]
        z = sliced_data_field[:, 2]

        if uid.endswith('_m'):
            color = 'grey'
        else:
            color = 'maroon'

        ax.scatter(x, y, z, color=color)
