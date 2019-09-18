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
import os

import commonlibs.logger as hlogger

from aeroframe.analyses.static import StaticAeroelasticity
from aeroframe.data.shared import SharedData
import aeroframe.fileio as io
from aeroframe import __prog_name__

logger = logging.getLogger(__name__)


class StdRunArgs:

    def __init__(self):

        verbose = False
        debug = False
        quiet = False

        clean = False
        clean_only = False


def standard_run(args):
    """
    High-level function to run a standard analysis

    Args:
        :args: (obj) Instance of form 'StdRunArgs'
    """

    if args.verbose:
        level = 'info'
    elif args.debug:
        level = 'debug'
    elif args.quiet:
        level = 'quiet'
    else:
        level = 'default'

    # ===== Logging =====
    hlogger.init(log_filename="log.txt", level=level)
    logger = logging.getLogger()
    logger.info(hlogger.decorate(f"{__prog_name__}"))

    root_dir = os.path.dirname(args.dest)

    # ===== Initialise =====
    paths = io.FileStructure(root_dir=args.dest)
    general_settings = io.load_root_settings(paths).get('general_settings', {})

    cfd_lib, stru_lib = io.load_wrapper_libs(paths)
    cfd_wrapper = cfd_lib.AeroWrapper(paths)
    stru_wrapper = stru_lib.StructureWrapper(paths)

    #######################
    # shared_data = SharedData()
    # cfd_wrapper.shared_data = shared_data
    # stru_wrapper.shared_data = shared_data
    #######################

    # ===== Clean up before running a new analysis =====
    if args.clean or args.clean_only:
        logger.info("Removing old files...")
        cfd_wrapper.clean()
        stru_wrapper.clean()

        if args.clean_only:
            logger.info("Exiting...")
            return

    # ===== Run the aeroelastic analysis =====
    settings = general_settings.get('static_loop', {})
    static = StaticAeroelasticity(cfd_wrapper, stru_wrapper, **settings)
    static.find_equilibrium()
