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
Interpolate discretised load and deformation data between FEM and CFD meshes
"""

import numpy as np
from commonlibs.math.vectors import rotate_vector_around_axis

X_AXIS = np.array([1, 0, 0])
Y_AXIS = np.array([0, 1, 0])
Z_AXIS = np.array([0, 0, 1])


def get_closest_def_field_entry(p2, def_field):
    """
    Return the deformation field entry closest to a point p2

    Args:
        :p2: (array) Some point in space [x, y, z]
        :def_field: (array) Array of the displacement field

    Returns:
        :def_field: (array) closest deformation field entry (1, 9)-vector

    Note:

        * Closest is here defines as the minimal Euclidean norm
    """

    # TODO: Interpolate displacement field between discrete points

    distances = np.linalg.norm(def_field[:, 0:3] - p2.reshape((1, 3)), axis=1)
    idx_closest = np.where(distances == np.amin(distances))[0][0]
    return def_field[idx_closest, :]


def get_deformed_point(p2, def_field):
    """
    Interpolate the position of a field point 'p2' based on a deformation field

    Args:
        :point: (array) Some field point in space [x, y, z]
        :def_field_entry: (array) A single row entry (1 x 9)

    Returns:
        :def_field_entry_on_target: (array) (1 x 9)
    """

    p1_def_field_entry = get_closest_def_field_entry(p2, def_field)

    p1 = p1_def_field_entry[0:3]
    p2_def = p1_def_field_entry[3:9]  # Rotation and translation at p1

    r = np.array(p2 - p1, dtype=float)
    rx = rotate_vector_around_axis(r, X_AXIS, p1_def_field_entry[6])
    ry = rotate_vector_around_axis(r, Y_AXIS, p1_def_field_entry[7])
    rz = rotate_vector_around_axis(r, Z_AXIS, p1_def_field_entry[8])
    p2_def[0:3] += (rx-r) + (ry-r) + (rz-r)

    ##########
    # See Raimer et al. 2010 (may be a sufficient approx.)
    # p2_def[0:3] += np.cross(p1_def_field_entry[6:9], r)
    ##########

    return p2+p2_def[0:3]


def get_deformed_mesh(mesh, def_field):
    """
    Interpolate the position of multiple field points
    based on a given deformation field

    Args:
        :mesh: Array of size (N x 3) with initial mesh coordinates

    Returns:
        :def_mesh: Array of size (N x 3) with deformed mesh coordinates
    """

    def_field = np.array(def_field, dtype=float)
    mesh = np.array(mesh, dtype=float)

    def_mesh = np.zeros_like(mesh)
    for i, point in enumerate(mesh, start=0):
        p2 = get_deformed_point(point, def_field)
        def_mesh[i, :] = p2
    return def_mesh


# def translate_from_line_to_line(def_field, target_line):
#     """
#     Return the deformation field of a target line based on a
#     line-like deformation field

#     Args:
#         :def_field: (array) Array of the displacement field
#         :target_line: (array) Array with discrete points forming the target line

#     Returns:
#         :def_field_on_target: (array) Displacement field on the target line

#     Notes:

#         * It is assumed that there is a *rigid* connection between the
#           original line and the target line
#     """

#     # ----- Check input data -----
#     if not isinstance(def_field, np.ndarray):
#         raise TypeError("'def_field' must be a Numpy array")

#     if not isinstance(target_line, np.ndarray):
#         raise TypeError("'target_line' must be a Numpy array")

#     if len(def_field.shape) != 2 and def_field.shape[1] == 9:
#         raise ValueError("'target_line' must be of shape (N, 9)")

#     if len(target_line.shape) != 2 and target_line.shape[1] == 3:
#         raise ValueError("'target_line' must be of shape (N, 3)")

#     # ----- Always use float arrays -----
#     def_field = np.array(def_field, dtype=float)
#     target_line = np.array(target_line, dtype=float)

#     def_field_on_target = np.zeros((target_line.shape[0], 9))
#     for i, p2 in enumerate(target_line):
#         def_field_on_target[i, :] = interpol_p2_deformation(p2, def_field)

#     return def_field_on_target
