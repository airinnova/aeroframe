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
Shared data
"""

import logging

logger = logging.getLogger(__name__)


class SharedData:

    def __init__(self):
        """
        Data shared from the CFD analysis

        Attr:
            :cfd: Data shared from CFD analysis
            :structure: Data shared from structure analysis
        """

        self.cfd = _CFDData()
        self.structure = _StructureData()

class _CFDData:

    def __init__(self):
        """
        CFD data

        Attr:
            :load_fields: Forces computed from the CFD analysis

        Note:

        Forces computed by a CFD solver and shared here must follow a
        strict format:

            * 'self.load_fields' must be a dictionary. Each key must be a UID for
              the structural element on which the loads are acting.

            * The values must be Numpy arrays of the following format:

                x1, y1, z1, fx1, fy1, fz1
                x2, y2, z2, fx2, fy2, fz2
                ...
                xN, yN, zN, fxN, fyN, fzN

              I.e. for each structural element there can be an array with size
              6 x N where N is the number of discrete forces belonging to the
              structural element.

              xi, yi, zi are Cartesian coordinates where force i acts
              fxi, fyi, fzi are elements of a force vector acting at position i

            * If there are no loads acting on a component, the value can be None
        """

        self.load_fields = {}

class _StructureData:

    def __init__(self):
        """
        Data shared from the structure analysis

        Note:

        Deformations computed by a structure solver and shared here
        must follow a strict format:

            * 'self.def_fields' must be a dictionary. Each key must be a UID for
              the structural element on which the deformations belong.

            * The values must be Numpy arrays of the following format:

                x1, y1, z1, ux1, uy1, uz1, tx1, ty1, tz1,
                x2, y2, z2, ux2, uy2, uz2, tx2, ty2, tz2,
                ...
                xN, yN, zN, uxN, uyN, uzN, txN, tyN, tzN,

              I.e. for each structural element there can be an array with size
              9 x N where N is the number of discrete deformation points
              belonging to the structural element.

              xi, yi, zi are Cartesian coordinates where force i acts
              uxi, uyi, uzi are displacments in x, y and z directions
              txi, tyi, tzi are rotations in x, y and z directions
        """

        self.def_fields = {}
