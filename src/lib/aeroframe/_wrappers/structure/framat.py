#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AeroFrame wrapper for FramAT

* https://github.com/airinnova/framat
* Tested with version 0.3.0

See documentation for FramAT specifics
"""

# Author: Aaron Dettmann

from os.path import join
import json
import logging
import os
import re

import numpy as np
from aeroframe.templates.wrappers import StructureWrapper

from commonlibs.fileio.json import dump_pretty_json
from framat.fileio.utils import FileStructure
from framat.stdfun import standard_run, clean_project_dir, StdRunArgs

logger = logging.getLogger(__name__)

REGEX_MIRROR_IDENTIFIER = r"_m$"


class Wrapper(StructureWrapper):

    def __init__(self, root_path, shared, settings):
        super().__init__(root_path, shared, settings)

        # FramAT files
        self.own_files = {
            'model_file': join(self.root_path, settings.get('model_file', ''))
        }

        # Check that the model file exists
        if not os.path.isfile(self.own_files['model_file']):
            raise FileNotFoundError(f"FramAT model '{self.own_files['model_file']}' file not found")

    def run_analysis(self):
        """Run a FramAT analysis"""

        self._apply_loads_to_framat_model()

        # ----- Run the FramAT analysis -----
        results = standard_run(args=StdRunArgs(filename=self.own_files['model_file'], verbose=True))
        self.last_solution = results

        # ----- Share loads -----
        logger.info("Sharing loads...")
        frame = results['frame']
        self.shared.structure.def_fields = frame.deformation.get_displacement_fields(frame, n_sup=1000)

    def clean(self):
        """FramAT's clean method"""

        clean_project_dir(FileStructure(self.own_files['model_file']))

    def get_max_abs_diff(self):
        """
        Return the maximum absolute difference between the last two solutions

        Note:

            * It is assumed that the FEM mesh geometry does not change
        """

        # In the first iteration there is no previous analysis, i.e. nothing to compare with
        if self.solution_before_last is None:
            return 1

        # Get the maximum absolute difference
        U_last = self.last_solution['frame'].deformation.U
        U_before_last = self.solution_before_last['frame'].deformation.U
        U_abs_diff = np.amax(np.absolute((U_last - U_before_last)))
        return U_abs_diff

    def _apply_loads_to_framat_model(self):
        """Apply shared loads to FramAT model"""

        logger.info("Applying shared loads to structure...")

        # Load the FramAT model file
        model_file = self.own_files['model_file']
        with open(model_file, 'r') as fp:
            model = json.load(fp)

        # Update the free node loads in the model
        for component_uid, load_field in self.shared.cfd.load_fields.items():
            for i, beamline in enumerate(model['beamlines']):
                # Loads from a mirrored component 'BEAM_m' will be applied to 'BEAM'
                if beamline['uid'] == re.sub(REGEX_MIRROR_IDENTIFIER, '', component_uid):
                    beamline_idx = i
                    break
            else:
                raise RuntimeError(f"Component '{component_uid}' not found in structure model")

            # Add loads to the FramAT model file
            free_node_loads = []
            for entry in load_field:
                free_node_loads.append({'coord': list(entry[0:3]), 'load': list(entry[3:9])})

            # Loads acting on a mirrored side
            if component_uid.endswith('_m'):
                model['beamlines'][beamline_idx]['mirror_loads']['free_nodes'] = free_node_loads
            else:
                model['beamlines'][beamline_idx]['loads']['free_nodes'] = free_node_loads

        # Finally, update the structure file
        with open(self.own_files['model_file'], 'w') as fp:
            dump_pretty_json(model, fp)
