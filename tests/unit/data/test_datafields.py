#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pytest

from aeroframe.data.datafields import get_total_num_points


@pytest.fixture
def example_def_field():
    """
    Example random deformation field
    """

    def_field = {}
    def_field['Wing'] = np.random.rand(20, 9)
    def_field['Fuselage'] = np.random.rand(20, 9)
    def_field['HorizTail'] = np.random.rand(20, 9)

    return def_field


def test_get_total_num(example_def_field):
    """
    Test function 'get_total_num_points()'
    """

    n_tot = get_total_num_points(example_def_field)
    assert n_tot == 60
