#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import cos, sin

import numpy as np
import pytest

from aeroframe.interpol.translate import translate_from_line_to_line


@pytest.fixture
def simple_target_line():
    target_line = np.array([
        [0, 1, 0],
        [1, 1, 0],
    ])
    return target_line


def test_line_line(simple_target_line):
    """
    Test that beam-like deformation fields are transformed correctly
    """

    # ----- Test case: Pure translation of target point -----
    def_field = np.array([
        [0, 0, 0, 2, 2, 2, 0, 0, 0],
        [1, 0, 0, 4, 4, 4, 0, 0, 0],
    ])


    exp_def_field_on_target = np.array([
        [0, 1, 0, 2, 2, 2, 0, 0, 0],
        [1, 1, 0, 4, 4, 4, 0, 0, 0],
    ])

    comp_def_field_on_target = translate_from_line_to_line(def_field, simple_target_line)
    assert np.testing.assert_equal(comp_def_field_on_target, exp_def_field_on_target) is None

    # ----- Test case: Translation and rotation tx -----
    for tx in np.linspace(0, np.pi, num=20):
        def_field = np.array([
            [0, 0, 0, 2, 2, 2, tx, 0, 0],
            [1, 0, 0, 4, 4, 4, 0, 0, 0],
        ])

        exp_def_field_on_target = np.array([
            [0, 1, 0, 2, 2-(1-cos(tx)), 2+sin(tx), tx, 0, 0],
            [1, 1, 0, 4, 4, 4, 0, 0, 0],
        ])

        comp_def_field_on_target = translate_from_line_to_line(def_field, simple_target_line)
        assert np.allclose(comp_def_field_on_target, exp_def_field_on_target)

    # ----- Test case: Translation and rotation tz -----
    for tz in np.linspace(0, np.pi, num=20):
        def_field = np.array([
            [0, 0, 0, 2, 2, 2, 0, 0, tz],
            [1, 0, 0, 4, 4, 4, 0, 0, 0],
        ])

        exp_def_field_on_target = np.array([
            [0, 1, 0, 2-sin(tz), 2-(1-cos(tz)), 2, 0, 0, tz],
            [1, 1, 0, 4, 4, 4, 0, 0, 0],
        ])

        comp_def_field_on_target = translate_from_line_to_line(def_field, simple_target_line)
        assert np.allclose(comp_def_field_on_target, exp_def_field_on_target)

    # # ----- Test case: Translation and rotation in all directions -----
    for tx in np.linspace(0, np.pi/2, num=20):
        for ty in np.linspace(0, np.pi/2, num=20):
            for tz in np.linspace(0, np.pi/2, num=20):
                def_field = np.array([
                    [0, 0, 0, 2, 2, 2, tx, ty, tz],
                    [1, 0, 0, 4, 4, 4, 0, 0, 0],
                ])
                exp_def_field_on_target = np.array([
                    [0, 1, 0, 2-sin(tz), 2-(1-cos(tx))-(1-cos(tz)), 2+sin(tx), tx, ty, tz],
                    [1, 1, 0, 4, 4, 4, 0, 0, 0],
                ])

                comp_def_field_on_target = translate_from_line_to_line(def_field, simple_target_line)
                assert np.allclose(comp_def_field_on_target, exp_def_field_on_target)
