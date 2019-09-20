#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wrapper module for aeroframe
"""

# Author: Aaron Dettmann

import json
import os
from uuid import uuid4

import numpy as np
from commonlibs.fileio.json import dump_pretty_json
import pytornado.stdfun.run as pyt

from aeroframe.templates.wrappers import AeroWrapper
from aeroframe.interpol.translate import translate_from_line_to_line


# ---------
# TODO:
# - generalise for multiple wings
# - Make sure aircraft is undeformed
# ---------

class Wrapper(AeroWrapper):

    def __init__(self, root_path, shared, settings):
        super().__init__(root_path, shared, settings)

        # File
        self.own_files = {}
        self.own_files['settings'] = os.path.join(self.root_path, settings.get('run', ''))
        self.own_files['deformation'] = os.path.join(self.root_path, 'cfd', 'deformation', f'{uuid4()}.json')

        # Locate the PyTornado main settings file
        if not os.path.isfile(self.own_files['settings']):
            raise FileNotFoundError(f"PyTornado settings file '{self.own_files['settings']}' not found")

        # Create empyt deformation file
        open(self.own_files['deformation'], 'w').close()

        # Get the bound legs of the undeformed mesh
        self._toggle_deformation(turn_on=False)
        results = pyt.standard_run(args=pyt.StdRunArgs(run=self.own_files['settings']))
        bound_leg_midpoints = results['lattice'].bound_leg_midpoints
        self.points_of_attack_undeformed = bound_leg_midpoints

        # ======================================
        # ======================================
        # ======================================
        model_file = 'cfd/aircraft/WindTunnelModel.json'
        with open(model_file, "r") as fp:
            model = json.load(fp)

        vertices = model['wings'][0]['segments'][0]['vertices']
        a = np.array(vertices['a'])
        b = np.array(vertices['b'])
        self.le_line = np.array((a, (a+b)/2, b))
        # ======================================
        # ======================================
        # ======================================

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

        # Fetch deformation field
        def_field = self.shared.structure.deformations.get('Wing', None)
        if def_field is not None:
            le_def_field = translate_from_line_to_line(def_field, target_line=self.le_line)

            # Write to file
            write_def_field_for_pytornado(self.own_files['deformation'], def_field)

        args = pyt.StdRunArgs(run='cfd/settings/WindTunnelModel.json', verbose=True)
        results = pyt.standard_run(args)

        # ---------
        # See PyTornado documentation
        vlmdata = results['vlmdata']

        forces = np.array([vlmdata.panelwise[key] for key in ('fx', 'fy', 'fz')])
        load_data = np.block([self.points_of_attack_undeformed, forces.T])

        # Share loads
        self.shared.cfd.loads['main_wing'] = load_data
        # ---------

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


def write_def_field_for_pytornado(output_file, def_field):
    """
    TODO
    """

    output = [
        {
            'wing': 'Wing',
            'segment': 'WingSegment1',
            'mirror': False,
            'deform': [
                {
                    'eta': 0,
                    'deform': list(def_field[0, 3:9]),
                },
                {
                    'eta': 0.5,
                    'deform': list(def_field[1, 3:9]),
                },
                {
                    'eta': 1,
                    'deform': list(def_field[2, 3:9]),
                },
            ],
        }
    ]
