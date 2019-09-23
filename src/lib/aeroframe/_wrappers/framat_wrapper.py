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

import numpy as np
from aeroframe.templates.wrappers import StructureWrapper

from commonlibs.fileio.json import dump_pretty_json
from framat.fileio.utils import FileStructure
from framat.stdfun import standard_run, clean_project_dir, StdRunArgs

logger = logging.getLogger(__name__)


class Wrapper(StructureWrapper):

    def __init__(self, root_path, shared, settings):
        super().__init__(root_path, shared, settings)

        self.own_files = {}
        self.own_files['model_file'] = join(self.root_path, settings.get('model_file', ''))

        # Check that the model file exists
        if not os.path.isfile(self.own_files['model_file']):
            raise FileNotFoundError(f"FramAT model '{self.own_files['model_file']}' file not found")

    def run_analysis(self):
        self._apply_loads_to_framat_model()

        args = StdRunArgs(filename=self.own_files['model_file'], verbose=True)
        results = standard_run(args=args)

        self.last_solution = results

        # ----- Share loads -----
        logger.info("Sharing loads...")
        frame = results['frame']
        self.shared.structure.deformations = frame.deformation.get_displacement_fields(frame, n_sup=500)

    def clean(self):
        """
        FramAT's clean method
        """

        clean_project_dir(FileStructure(self.own_files['model_file']))

    def get_max_abs_diff(self):
        """
        Return the maximum absolute difference between the last two solutions

        Note:

            * It is assumed that the FEM mesh geometry does not change
        """

        if self.solution_before_last is None:
            return 1

        frame_last = self.last_solution['frame']
        frame_before_last = self.solution_before_last['frame']
        U_last = frame_last.deformation.U
        U_before_last = frame_before_last.deformation.U
        U_abs_diff = np.amax(np.absolute((U_last - U_before_last)))

        print(U_abs_diff)
        return U_abs_diff

    def _apply_loads_to_framat_model(self):
        """
        Apply shared loads to FramAT model
        """

        logger.info("Applying shared loads to structure...")

        # Load the FramAT model file
        model_file = self.own_files['model_file']
        with open(model_file, 'r') as fp:
            model = json.load(fp)

        # Update the free node loads in the model
        for component, load_field in self.shared.cfd.loads.items():
            for i, beamline in enumerate(model['beamlines']):
                if beamline['uid'] == component:
                    beamline_idx = i
                    break
            else:
                raise RuntimeError(f"Component '{component}' not found in structure model")

            # Add loads to model
            free_node_loads = []
            for entry in load_field:
                free_node_loads.append({'coord': list(entry[0:3]), 'load': list(entry[3:9])})
            model['beamlines'][beamline_idx]['loads']['free_nodes'] = free_node_loads

        # Finally, update the structure file
        with open(self.own_files['model_file'], 'w') as fp:
            dump_pretty_json(model, fp)
