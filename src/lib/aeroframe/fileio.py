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

import re
import json
import importlib
import os

from commonlibs.fileio.paths import ProjectPaths
from commonlibs.fileio.json import dump_pretty_json
from commonlibs.dicts.schemadicts import get_default_value_dict


class PATHS:

    class FILES:

        DEFAULT_SETTINGS = 'aeroframe_settings.json'

    class DIRS:

        CFD = 'cfd'
        STRUCTURE = 'structure'
        SHARED_FROM_CFD = 'from_cfd'
        SHARED_FROM_STRUCTURE = 'from_structure'

    class GROUPS:

        INIT = 'init'
        CFD = 'cfd'
        STRUCTURE = 'structure'

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


class FileStructure:

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


def load_root_settings(aeroframe_files):
    """
    Load and return the root settings file

    Args:
        :aeroframe_files: file structure of aeroframe program
    """

    with open(aeroframe_files.paths("f_root_settings"), "r") as fp:
        settings = json.load(fp)

    return settings


def load_wrapper_libs(aeroframe_files):
    """
    Load wrapper modules dynamically

    Args:
        :aeroframe_files: file structure of aeroframe program
    """

    settings = load_root_settings(aeroframe_files)
    cfd = importlib.import_module(settings['cfd_model']['wrapper'])
    stru = importlib.import_module(settings['structure_model']['wrapper'])

    return cfd, stru


def sed_like_replace(filename, replacement_list):
    """
    Replace expressions in a "sed"-like style

    Args:
        :filename: name of file to modify
        :replacement_list: list of lists, each entry with ["old", "new"]
    """

    with open(filename, "r") as fp:
        lines = fp.readlines()

    with open(filename, "w") as fp:
        for line in lines:
            mod_line = string_replace(replacement_list, line)
            fp.write(mod_line)


def string_replace(replacement_list, string):
    """
    Replace multiple expressions in a string

    Args:
        :replacement_list: list of lists, each entry with ["old", "new"]
        :string: string to modify

    Returns:
        :mod_string: modified string
    """

    for replacement in replacement_list:
        orig, new = replacement
        string = re.sub(orig, new, string)

    return string


def is_string_in_file(string, filepath):
    """
    Check if a string is in a file

    Args:
        :string: string to search for
        :filepath: path of file

    Returns:
        :is_found: True if found, False otherwise
    """

    if string in open(filepath).read():
        return True

    return False
