#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import os

import numpy as np
import pytest

import aeroframe.fileio.serialise as s


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


def check_if_def_fields_same(actual, desired):
    """
    Check if a deformation field 'actual' matches a deformation field 'desired'

    Args:
        :actual: (array) Actual deformation field
        :desired: (array) Desired deformation field
    """

    for act_key, act_val in actual.items():
        des_val = desired[act_key]
        assert np.array_equal(act_val, des_val)


def test_json_dump(example_def_field):
    """
    Test that JSON serialisation is lossless
    """

    tmp_file = tempfile.mkstemp()[1]

    s.dump_json_def_fields(tmp_file, example_def_field)
    deserialised_def_fields = s.load_json_def_fields(tmp_file)
    check_if_def_fields_same(deserialised_def_fields, example_def_field)

    os.remove(tmp_file)
