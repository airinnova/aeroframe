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
File IO
"""

import json
import importlib
import os

from commonlibs.fileio.paths import ProjectPaths
from commonlibs.fileio.json import dump_pretty_json
from commonlibs.dicts.schemadicts import get_default_value_dict

from aeroframe.data.shared import SharedData


DEFAULT_SETTINGS_DICT = {
    'general_settings': {
        'type': dict,
        'schema': {
            'static_loop': {
                'type': dict,
                'schema': {
                    'max_iterations': {'type': int, '>': 1, 'default': 15},
                    'rel_conv_lim': {'type': float, '>': 0, '<': 1, 'default': 0.05},
                },
            },
        },
    },
    'cfd_model': {
        'type': dict,
        'schema': {
            'wrapper': {'type': str, 'default': 'aeroframe.templates.cfdwrapper'},
            'exec_settings': {'type': dict}
        },
    },
    'structure_model': {
        'type': dict,
        'schema': {
            'wrapper': {'type': str, 'default': 'aeroframe.templates.structurewrapper'},
            'exec_settings': {'type': dict}
        },
    },
}


class PATHS:

    class FILES:

        DEFAULT_SETTINGS = 'aeroframe_settings.json'

    class DIRS:

        CFD = 'cfd'
        STRUCTURE = 'structure'

    class GROUPS:

        INIT = 'init'
        CFD = 'cfd'
        STRUCTURE = 'structure'

class Settings:

    def __init__(self, root_dir=None, make_dirs=True):
        """
        Aeroframe file structure

        Note:
            * If 'root_dir' is None, the root directory, we use 'os.getcwd()'

        Args:
            :root_dir: (str,path) Project root folder
            :make_dirs: (bool) If True, make directories of group 'init'
        """

        if root_dir is None:
            root_dir = os.getcwd()

# ==============================
        self.settings = None

        self.cfd_wrapper = None
        self.stru_wrapper = None
# ==============================

        self.paths = ProjectPaths(root_dir)

        # ----- Directories -----
        self.paths.add_path(
            uid='d_cfd',
            path=PATHS.DIRS.CFD,
            uid_groups=(PATHS.GROUPS.INIT, PATHS.GROUPS.CFD)
        )

        self.paths.add_path(
            uid='d_structure',
            path=PATHS.DIRS.STRUCTURE,
            uid_groups=(PATHS.GROUPS.INIT, PATHS.GROUPS.STRUCTURE)
        )

        # ----- Files -----
        self.paths.add_path(
            uid='f_root_settings',
            path=PATHS.FILES.DEFAULT_SETTINGS
        )

        if make_dirs:
            self.init_dirs()

    def init_dirs(self):
        """
        Create directories belonging to 'init' group
        """

        self.paths.make_dirs_for_groups(uid_groups='init', is_dir=True)

    def init_emtpy_settings_file(self, overwrite=False):
        """
        Create a settings file with default values

        Args:
            :overwrite: (bool) If True, overwrite an existing settings file
        """

        settings_file = self.paths("f_root_settings")

        if not overwrite and settings_file.exists():
            raise FileExistsError(f"Path '{settings_file}' exists. Will not overwrite.")

        with open(settings_file, "w") as fp:
            settings_dict = get_default_value_dict(DEFAULT_SETTINGS_DICT)
            dump_pretty_json(settings_dict, fp)

# ==============================
# ==============================
    def load_root_settings(self):
        """
        Load and return the root settings file

        Args:
            :aeroframe_files: file structure of aeroframe program
        """

        with open(self.paths("f_root_settings"), "r") as fp:
            self.settings = json.load(fp)

    def get_wrappers(self):
        """
        Load wrapper modules dynamically

        Args:
            :aeroframe_files: file structure of aeroframe program
        """

        self.load_root_settings()

        self.cfd_lib = importlib.import_module(self.settings['cfd_model']['wrapper'])
        self.stru_lib = importlib.import_module(self.settings['structure_model']['wrapper'])

        root_path = root_path = self.paths('root')
        cfd_settings = self.settings['cfd_model'].get('exec_settings', {})
        stru_settings = self.settings['structure_model'].get('exec_settings', {})

        # Wrapper must share same instance of 'SharedData()'
        shared_data = SharedData()
        cfd_wrapper = self.cfd_lib.Wrapper(root_path, shared_data, cfd_settings)
        stru_wrapper = self.stru_lib.Wrapper(root_path, shared_data, stru_settings)
        return cfd_wrapper, stru_wrapper
# ==============================
# ==============================
