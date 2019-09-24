#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AeroFrame wrapper for PyTornado

* https://github.com/airinnova/pytornado
* Tested with version 0.5.0

See documentation for PyTornado specifics
"""

# Author: Aaron Dettmann

from os.path import join
from uuid import uuid4
import json
import os

import numpy as np
from commonlibs.fileio.json import dump_pretty_json
import pytornado.stdfun.run as pyt

from aeroframe.templates.wrappers import AeroWrapper
from aeroframe.fileio.serialise import dump_json_def_fields

# ---------
# TODO:
# - Generalise load sharing for multiple wings and mirrored wings
# ---------


class Wrapper(AeroWrapper):

    def __init__(self, root_path, shared, settings):
        super().__init__(root_path, shared, settings)

        # PyTornado files
        self.own_files = {}
        self.own_files['settings'] = join(self.root_path, settings.get('run', ''))
        self.own_files['deformation_dir'] = join(self.root_path, 'cfd', 'deformation')
        self.own_files['deformation'] = join(self.own_files['deformation_dir'], f'{uuid4()}.json')

        # Locate the PyTornado main settings file
        if not os.path.isfile(self.own_files['settings']):
            raise FileNotFoundError(f"PyTornado settings file '{self.own_files['settings']}' not found")

        # Create deformation folder and empty file
        if not os.path.exists(self.own_files['deformation_dir']):
            os.makedirs(self.own_files['deformation_dir'])
        open(self.own_files['deformation'], 'w').close()

        # Get the bound legs of the undeformed mesh
        self._toggle_deformation(turn_on=False)
        results = pyt.standard_run(args=pyt.StdRunArgs(run=self.own_files['settings']))
        bound_leg_midpoints = results['lattice'].bound_leg_midpoints
        self.points_of_attack_undeformed = bound_leg_midpoints

    def run_analysis(self, turn_off_deform=False):
        """
        Run the PyTornado analysis

        Args:
            :turn_off_deform: Flag which can be used to turn off all deformations
        """

        if turn_off_deform:
            self._toggle_deformation(turn_on=False)
        else:
            self._toggle_deformation(turn_on=True)
            dump_json_def_fields(self.own_files['deformation'], self.shared.structure.def_fields)

        # ----- Run the PyTornado analysis -----
        results = pyt.standard_run(args=pyt.StdRunArgs(run=self.own_files['settings']))
        self.last_solution = results  # Save the last solution

        # ----- Share load data -----
        # ==========
        # ==========
        # TODO:
        # + Make work for multiple wings
        # + Mirrored wings
        # ==========
        # ==========
        vlmdata = results['vlmdata']
        forces = np.array([vlmdata.panelwise[key] for key in ('fx', 'fy', 'fz')])
        load_data = np.block([self.points_of_attack_undeformed, forces.T, np.zeros_like(forces.T)])

        self.shared.cfd.loads['Wing'] = load_data
        # ==========
        # ==========

    def _toggle_deformation(self, *, turn_on=True):
        """
        Modify the PyTornado settings file and turn on/off the deformation

        Args:
            :turn_on: (bool) If True, deformation will be turned on, otherwise off
        """

        with open(self.own_files['settings'], 'r') as fp:
            settings = json.load(fp)

        deform_entry = os.path.basename(self.own_files['deformation']) if turn_on is True else None
        settings['deformation'] = deform_entry

        with open(self.own_files['settings'], 'w') as fp:
            dump_pretty_json(settings, fp)

    def clean(self):
        """
        PyTornado's clean method
        """

        pyt.clean_project_dir(pyt.get_settings(self.own_files['settings']))
