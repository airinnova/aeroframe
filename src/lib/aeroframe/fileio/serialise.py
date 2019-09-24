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
Serialise and deserialise objects
"""

import json

from commonlibs.fileio.json import dump_pretty_json
import numpy as np


def dump_json_def_fields(filename, def_fields):
    """
    Dump a JSON deformation field

    Args:
        :filename: (str) Output file name
        :def_fields: (array) Array of the displacement field
    """

    with open(filename, "w") as fp:
        dump_pretty_json(def_fields, fp)


def load_json_def_fields(filename):
    """
    Load a deformation field from a JSON file and return a deformation field

    Args:
        :filename: (str) Output file name

    Returns:
        :def_fields: (array) Array of the displacement field
    """

    with open(filename, "r") as fp:
        def_field_from_json = json.load(fp)

    def_fields = {}
    for component_name, comp_def_field in def_field_from_json.items():
        def_fields[component_name] = np.array(comp_def_field, dtype=float)

    return def_fields
