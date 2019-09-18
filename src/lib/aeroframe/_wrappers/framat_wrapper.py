#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wrapper module for aeroframe
"""

# Author: Aaron Dettmann

from aeroframe.templates.wrappers import StructureWrapper

from framat.stdfun import standard_run, StdRunArgs


class Wrapper(StructureWrapper):

    def __init__(self, shared):
        super().__init__(shared)

    def run_analysis(self):
        """
        TODO
        """

        args = StdRunArgs(filename='structure/WindTunnelModel.json', verbose=True)
        results = standard_run(args=args)

        # TODO: perform PyTornado analysis
        # TODO: share loads
        # self.shared.structure.deformation = ...

    def clean(self):
        """
        TODO
        """
        ...

        # TODO




######
######
######

#import os
#import shutil

#import aeroframe.fileio as io

#from framat.helpers.iterators import pairwise
#from framat.stdfun import standard_run, StdRunArgs


#class StructureWrapper:

#    def __init__(self, aeroframe_files):
#        """
#        API for the "aeroframe" aeroelastic framework

#        Args:
#            :aeroframe_files: file structure of aeroframe program
#        """

#        self.aeroframe_files = aeroframe_files
#        self.exec_args = self.load_exec_settings()
#        self.model_filename = self.exec_args.filename
#        self.own_files = StructureWrapperFiles(aeroframe_files, self.model_filename)

#        # Solutions (note: solutions are frame structures)
#        self.solutions = []

#    @property
#    def last_solution(self):
#        """Return the last solution"""

#        return self.solutions[-1]

#    def goto_structure(self):
#        """
#        Change into the structure project folder
#        """

#        os.chdir(self.aeroframe_files.dirs['structure'])

#    def load_exec_settings(self):
#        """
#        Load the main execution settings

#        Returns:
#            :args: arguments which can be passed to 'run_analysis'
#        """

#        settings = io.load_root_settings(self.aeroframe_files)
#        settings = settings['structure_model']['exec_settings']

#        args = StdRunArgs()
#        args.filename = settings['filename']
#        args.verbose = settings['verbose']
#        args.debug = settings['debug']

#        return args

#    def run_analysis(self):
#        """
#        Run a full analysis

#        Note:
#            * Computed deformations are shared
#        """

#        self.goto_structure()
#        return_dict = standard_run(self.exec_args)
#        self.solutions.append(return_dict['frame'])
#        self.share_deformation()

#    def share_deformation(self):
#        """
#        Share the computed deformation
#        """

#        def_file = self.own_files.files['perimeter_lines']
#        shared_deformation = self.aeroframe_files.files['shared_def_file']

#        self.convert_perim_line_file(def_file)
#        shutil.copyfile(def_file, shared_deformation)

#    def check_convergence(self):
#        """
#        Return a relative difference between the deformations of the two analyses

#        Note:
#            * Deformations are evaluated at certain control points (here all
#              named nodes)

#        Returns:
#            :max_rel_diff: maximum relative difference between last and CG positions
#        """

#        max_rel_diff = 0

#        # There must be more than one solution to check for convergence
#        if len(self.solutions) > 1:
#            # Get the last and second last solution
#            sol_n1 = self.solutions[-1]
#            sol_n2 = self.solutions[-2]

#            for node_n1 in sol_n1.finder.nodes.by_uid.values():
#                # Get node from n2 solution with same name
#                node_n2 = sol_n2.finder.nodes.by_uid[node_n1.uid]

#                def_n1 = sol_n1.deformation.by_node_num(node_n1.num)
#                def_n2 = sol_n2.deformation.by_node_num(node_n2.num)

#                # Iterate through ux, uy, uz, tx, ty, tz
#                for def_prop_n1, def_prop_n2 in zip(def_n1, def_n2):
#                    diff = safe_rel_difference(def_prop_n2, def_prop_n1)

#                    if abs(diff) > max_rel_diff:
#                        max_rel_diff = diff

#            return max_rel_diff

#        return 1

#    @staticmethod
#    def convert_perim_line_file(filename):
#        """
#        Convert native deformation file shared file format

#        Notes:
#            * File will be modified on disk

#        Args:
#            :filename: name of file to modify
#        """

#        replacement_list = [
#            ['_m"', '"'],
#            ['"s"', '"eta"'],
#            ['"perimeter"', '"segment"'],
#            ['"beam"', '"wing"']
#        ]

#        io.sed_like_replace(filename, replacement_list)

#    def clean(self):
#        """
#        Remove old result file from a previous analysis
#        """

#        shutil.rmtree(self.own_files.dirs['project_results'], ignore_errors=True)


#class StructureWrapperFiles:

#    def __init__(self, aeroframe_files, model_filename):
#        """
#        Files pertinent to the structure code

#        Args:
#            :aeroframe_files: file structure of aeroframe program
#        """

#        self.aeroframe_files = aeroframe_files
#        stru_dir = self.aeroframe_files.dirs['structure']

#        # E.g. if the model_filename is "A380.json", the project_name is "A380"
#        self.project_name = os.path.splitext(model_filename)[0]

#        self.files = {
#            "perimeter_lines": os.path.join(stru_dir, f"{self.project_name}/results/perimeter_lines.json"),
#            "model_filename": os.path.join(stru_dir, f"{model_filename}.json")
#        }

#        self.dirs = {
#            "project_results": os.path.join(stru_dir,  self.project_name),
#        }


#def safe_rel_difference(old, new):
#    """
#    Safely return an indicator for the relative difference between two values

#    Note:
#        * The relative difference is:
#            * 0 if 'old' == 'new' == 0
#            * (new - old)/max( abs(old), abs(max) )

#    Args:
#        :old: old value
#        :new: new value

#    Returns:
#        :rel_diff: indicator for the relative difference
#    """

#    return 0 if old == new == 0 else (new - old)/max([abs(old), abs(new)])
