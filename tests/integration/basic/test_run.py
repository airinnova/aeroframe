#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from aeroframe import __prog_name__

EXE = __prog_name__
HERE = os.path.abspath(os.path.dirname(__file__))


def test_run():
    """
    Make sure basic framework test runs without errors
    """

    proc = subprocess.run([f'{EXE}', 'run', '--dest', f"{HERE}", '-cv'])
    assert proc.returncode == 0


def test_init():
    ...
