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
Wrapper base classes
"""

import logging

from aeroframe.data.shared import SharedData

logger = logging.getLogger(__name__)


class AeroWrapper:

    def __init__(self, aeroframe_files):
        """
        Setup routine

        Args:
            :aeroframe_files: file structure of aeroframe program

        Required attributes:
            :last_solution: some data structure with the last solution of the
                            CFD analysis (will be passed on once final solution
                            is found)
        """

        # Setup routines go here
        logger.info("Setup...")

        self.aeroframe_files = aeroframe_files

        # Shared data
        self.shared = SharedData()

        # Required
        self.last_solution = None

    def run_analysis(self, turn_off_deform=False):
        """
        Run a full analysis

        Note:
            * Computed loads are shared

        Args:
            :turn_off_deform: flag which can be used to turn off all deformations for a certain run
        """

        logger.info("Running analysis...")

        self.share_loads()

    def share_loads(self):
        logger.info("Sharing loads...")

    def clean(self):
        """
        Remove old result file from a previous analysis
        """

        logger.info("Cleaning...")


class StructureWrapper:

    def __init__(self, aeroframe_files):
        """
        Setup

        Args:
            :aeroframe_files: file structure of aeroframe program
        """

        # Setup routines go here
        logger.info("Setup...")

        self.aeroframe_files = aeroframe_files

        # Shared data
        self.shared = SharedData()

        # Required
        self.last_solution = None

    def run_analysis(self):
        """
        Run a full analysis

        Note:
            * Computed deformations are shared
        """

        logger.info("Running analysis...")

        self.share_deformations()

    def share_deformations(self):
        logger.info("Sharing deformations...")

    def check_convergence(self):
        """
        Return a relative difference between the deformations of the two analyses

        Note:
            * Deformations are evaluated at certain control points (here all
              named nodes)

        Returns:
            :max_rel_diff: maximum relative difference between last and CG positions
        """

        logger.info("Checking convergence...")
        return 1

    def clean(self):
        """
        Remove old result file from a previous analysis
        """

        logger.info("Cleaning...")
