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
Data fields
"""


def get_total_num_points(data_fields):
    """
    Return the total number of points in load or deformation fields

    Args:
        :data_fields: (dict) Either load or deformation fields

    Returns:
        :n_points: (int) Total number of points in all deformation fields
    """

    n_points = 0
    for data_field in data_fields.values():
        n_points += data_field.shape[0]
    return n_points
