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
High-level wrappers for setup
"""

import sys

from aeroframe.fileio.settings import Settings, PATHS


class ArgsSetup:

    def __init__(self):

        dest = os.getcwd()
        force = False


def setup_project(args):
    """
    Setup a project directory

    Args:
        :args: (obj) Instance of form 'ArgsSetup'
    """

    paths = Settings(root_dir=args.dest, make_dirs=True)

    try:
        paths.init_emtpy_settings_file(overwrite=args.force)
    except FileExistsError:
        err_msg = f"Settings file '{PATHS.FILES.DEFAULT_SETTINGS}' exists.\n" + \
                   "Will not overwrite, unless forced (hint: --force)"
        print(err_msg, sep='')
        sys.exit(1)
