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

logger = logging.getLogger(__name__)


class GenericWrapper:

    def __init__(self, root_path, shared, settings):
        """
        Wrapper base class

        Args:
            :root_path: Path to the project root directory
            :shared: Instance of 'SharedData'
            :settings: Specific execution settings

        Attr:
            :last_solution: Some data structure with the last analysis solution
                            (will be passed on once final solution is found)
        """

        logger.info("Initialising wrapper...")

        self.root_path = root_path
        self.shared = shared
        self.settings = settings

        self._last_solution = None

    @property
    def last_solution(self):
        return self._last_solution

    @last_solution.setter
    def last_solution(self, last_solution):
        self._last_solution = last_solution

    def run_analysis(self):
        """
        Run a full analysis and share data
        """

        logger.info("Running analysis...")
        logger.info("Sharing data...")

    def clean(self):
        """
        Remove old/temporary files from a previous analysis
        """

        logger.info("Cleaning...")


class AeroWrapper(GenericWrapper):

    def __init__(self, root_path, shared, settings):
        """
        Wrapper for the CFD solver

        Args:
            :root_path: Path to the project root directory
            :shared: Instance of 'SharedData'
            :settings: Specific execution settings
        """

        super().__init__(root_path, shared, settings)
        logger.info("Initialising CFD wrapper...")

    def run_analysis(self, turn_off_deform=False):
        """
        Run a full CFD analysis

        Args:
            :turn_off_deform: Flag which can be used to turn off all
                              deformations for a certain run
        """

        super().run_analysis()


class StructureWrapper(GenericWrapper):

    def __init__(self, root_path, shared, settings):
        """
        Wrapper for the structure solver

        Args:
            :root_path: Path to the project root directory
            :shared: Instance of 'SharedData'
            :settings: Specific execution settings
        """

        super().__init__(root_path, shared, settings)
        logger.info("Initialising structure wrapper...")

        # The structure wrapper should keep track of the last two solutions
        self._solution_before_last = None

    @property
    def last_solution(self):
        return self._last_solution

    @last_solution.setter
    def last_solution(self, last_solution):
        self._solution_before_last = self._last_solution
        self._last_solution = last_solution

    @property
    def solution_before_last(self):
        return self._solution_before_last

    def get_max_abs_diff(self):
        """
        Return the absolute difference between the deformations of the two analyses

        Note:
            * Deformations are evaluated at certain control points (here all
              named nodes)

        Returns:
            :max_abs_diff: (float) Maximum absolute difference
        """

        logger.info("Checking convergence...")
        return 1
