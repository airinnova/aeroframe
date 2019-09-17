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


class FileStructure:

    """Aeroframe file structure"""

    def __init__(self, settings_file, root_dir=None, make_dirs=True):
        """
        Setup the project directories and main files

        All files and directories stored as absolute paths
        """

        self.dirs = {
            "cfd": "cfd",
            "structure": "structure",
            "shared": "_shared",
            "shared_from_cfd": "_shared/from_cfd",
            "shared_from_structure": "_shared/from_structure",
        }

        self.files = {
            "root_settings": settings_file,
            "shared_def_file": "_shared/from_structure/deformation.json"
        }

        if root_dir is not None:
            self.root = os.path.abspath(root_dir)
        else:
            self.root = os.path.abspath(os.getcwd())

        # Make absolute paths
        for dir_id in self.dirs.keys():
            self.dirs[dir_id] = os.path.join(self.root, self.dirs[dir_id])

            if make_dirs and not os.path.exists(self.dirs[dir_id]):
                    os.makedirs(self.dirs[dir_id])

        for file_id in self.files.keys():
            self.files[file_id] = os.path.join(self.root, self.files[file_id])


def load_root_settings(aeroframe_files):
    """
    Load and return the root settings file

    Args:
        :aeroframe_files: file structure of aeroframe program
    """

    with open(aeroframe_files.files["root_settings"], "r") as fp:
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
