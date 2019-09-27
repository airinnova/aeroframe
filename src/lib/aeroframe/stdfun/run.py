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
High-level wrappers for commonly used functions
"""

import logging

import commonlibs.logger as hlogger

from aeroframe.analyses.static import StaticAeroelasticity
from aeroframe.fileio.settings import Settings
from aeroframe import __prog_name__
from aeroframe.__version__ import __version__

logger = logging.getLogger(__name__)


class StdRunArgs:

    def __init__(self, verbose=False, debug=False, quiet=True,
                 clean=False, clean_only=False, dest=None):

        self.verbose = verbose
        self.debug = debug
        self.quiet = quiet

        self.clean = clean
        self.clean_only = clean_only

        # Root directory
        self.dest = dest


def standard_run(args):
    """
    High-level function to run a standard analysis

    Args:
        :args: (obj) Instance of form 'StdRunArgs'

    Returns:
        :results: (dict) Results from static analysis
    """

    # ===== Logging =====
    hlogger.init(log_filename="log.txt", level=args)
    logger = logging.getLogger()
    logger.info(hlogger.decorate(f"{__prog_name__} {__version__}"))

    # ===== Initialise =====
    settings = Settings(root_dir=args.dest)
    cfd_wrapper, stru_wrapper = settings.get_wrappers()

    # ===== Clean up before running a new analysis =====
    if args.clean or args.clean_only:
        logger.info("Removing old files...")
        cfd_wrapper.clean()
        stru_wrapper.clean()

        if args.clean_only:
            logger.info("Exiting...")
            return

    # ===== Run the aeroelastic analysis =====
    settings_static = settings.settings.get('general_settings', {}).get('static_loop', {})
    static = StaticAeroelasticity(cfd_wrapper, stru_wrapper, **settings_static)
    results = static.find_equilibrium()
    return results
