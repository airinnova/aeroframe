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
Static aeroelasticity
"""

import logging

from commonlibs.logger import decorate

logger = logging.getLogger(__name__)


class StaticAeroelasticity:

    def __init__(self, cfd_wrapper, stru_wrapper,
                 max_iterations=10, rel_conv_lim=0.05):
        """
        Static aeroelastic analysis

        Attributes:
            :cfd: CFD wrapper class
            :structure: structure wrapper class
            :max_iters: maximum number of iterations
            :rel_conv_lim: relative convergence limit

        Note:
            * The analysis is considered converged if the deformation between
              last two analyses is smaller than the relative convergence limit
        """

        self.cfd = cfd_wrapper
        self.stru = stru_wrapper
        self.max_iters = max_iterations
        self.rel_conv_lim = rel_conv_lim

    def find_equilibrium(self):
        """
        Find a static equilibrium

        Note:
            This function iteratively computes deflections and loads until
            the deflection has converged or a maximum number of iterations
            is reached

        Returns:
            :results: dictionary with results provided by the CFD and structure modules
        """

        logger.info("Initialising loop...")
        logger.info("Load analysis without deformation...")
        self.cfd.run_analysis(turn_off_deform=True)

        n = 1
        has_converged = False
        while True:
            logger.info(decorate(f"===== Loop {n} =====", '\n', 3, 2))

            logger.info("--> Structure analysis...")
            self.stru.run_analysis()

            logger.info("--> Load analysis...")
            self.cfd.run_analysis()

            n += 1

            max_rel_def_diff = self.stru.get_max_rel_diff()
            logger.info(f"The maximum rel. difference is {(100*max_rel_def_diff):.2f} %")

            if abs(max_rel_def_diff) < self.rel_conv_lim:
                logger.info(f"Solution has converged (loop {n})...")
                has_converged = True
                break
            elif n > self.max_iters:
                logger.warning(f"Maximum number of iterations ({self.max_iters}) reached. Aborting.")
                break

        results = {
            "loop": n-1,
            "has_converged": has_converged,
            "cfd": self.cfd.last_solution,
            "structure": self.stru.last_solution,
        }

        return results
