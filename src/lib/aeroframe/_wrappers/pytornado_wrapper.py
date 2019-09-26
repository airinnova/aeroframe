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

        # Create a PyTornado deformation folder and a empty deformation file
        if not os.path.exists(self.own_files['deformation_dir']):
            os.makedirs(self.own_files['deformation_dir'])
        open(self.own_files['deformation'], 'w').close()

        # Get the bound leg midpoints of the undeformed (!) mesh
        self._toggle_deformation(turn_on=False)
        pytornado_results = pyt.standard_run(args=pyt.StdRunArgs(run=self.own_files['settings']))
        self.points_of_attack_undeformed = pytornado_results['lattice'].bound_leg_midpoints

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
        pytornado_results = pyt.standard_run(args=pyt.StdRunArgs(run=self.own_files['settings']))
        self.last_solution = pytornado_results  # Save the last solution

        # ----- Share load data -----
        self.shared.cfd.load_fields = self._get_load_fields(pytornado_results)

    def _toggle_deformation(self, *, turn_on=True):
        """
        Modify the PyTornado settings file and turn on/off the deformation

        Args:
            :turn_on: (bool) If True, deformations will be turned on, otherwise off
        """

        # Modify the PyTornado settings file
        with open(self.own_files['settings'], 'r') as fp:
            settings = json.load(fp)

        deform_entry = os.path.basename(self.own_files['deformation']) if turn_on is True else None
        settings['deformation'] = deform_entry

        with open(self.own_files['settings'], 'w') as fp:
            dump_pretty_json(settings, fp)

    def clean(self):
        """PyTornado's clean method"""

        pyt.clean_project_dir(pyt.get_settings(self.own_files['settings']))

    def _get_load_fields(self, pytornado_results):
        """
        Return AeroFrame load fields from PyTornado results

        Args:
            :pytornado_results: (obj) PyTornado results data structure

        Returns:
            :load_fields: (dict) AeroFrame load fields
        """

        vlmdata = pytornado_results['vlmdata']
        lattice = pytornado_results['lattice']

        # PyTornado API provides access to loads on main wing and on mirrored side
        bookkeeping_lists = (
            (lattice.bookkeeping_by_wing_uid, ''),
            (lattice.bookkeeping_by_wing_uid_mirror, '_m'),
        )

        load_fields = {}
        for (bookkeeping_list, suffix) in bookkeeping_lists:
            for wing_uid, panellist in bookkeeping_list.items():

                # Count number of panels
                num_pan = 0
                for entry in panellist:
                    num_pan += len(entry.pan_idx)

                # Add a first row of zeros in order to use 'append' method (will be removed below)
                load_field = np.zeros((1, 9))
                for entry in panellist:
                    # pan_idx: Panel index in PyTornado book keeping system
                    for pan_idx in entry.pan_idx:
                        load_field_entry = np.zeros((1, 9))
                        load_field_entry[0, 0:3] = self.points_of_attack_undeformed[pan_idx]
                        load_field_entry[0, 3] = vlmdata.panelwise['fx'][pan_idx]
                        load_field_entry[0, 4] = vlmdata.panelwise['fy'][pan_idx]
                        load_field_entry[0, 5] = vlmdata.panelwise['fz'][pan_idx]
                        load_field = np.append(load_field, load_field_entry, axis=0)

                load_fields[wing_uid + suffix] = load_field[1:, :]

        return load_fields
