#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import cos, sin

import numpy as np
import pytest

from aeroframe.interpol.translate import get_deformed_mesh


@pytest.fixture
def target_mesh():
    mesh = np.array([
        [0, 1, 0],
        [1, 1, 0],
    ])
    return mesh


def test_mesh_deformation(target_mesh):
    """
    Test that beam-like deformation fields are transformed correctly
    """

    # ----- Test case: Pure translation of target point -----
    def_field = np.array([
        [0, 0, 0, 2, 2, 2, 0, 0, 0],
        [1, 0, 0, 4, 4, 4, 0, 0, 0],
    ])

    exp_def_mesh = np.array([
        [2, 3, 2],
        [5, 5, 4],
    ])

    comp_def_mesh = get_deformed_mesh(target_mesh, def_field)
    assert np.allclose(comp_def_mesh, exp_def_mesh) is True

    # ----- Test case: Translation and rotation tx -----
    for tx in np.linspace(0, np.pi, num=20):
        def_field = np.array([
            [0, 0, 0, 2, 2, 2, tx, 0, 0],
            [1, 0, 0, 4, 4, 4, 0, 0, 0],
        ])

        exp_def_mesh = np.array([
            [2, 3+cos(tx)-1, 2+sin(tx)],
            [5, 5, 4],
        ])

        comp_def_mesh = get_deformed_mesh(target_mesh, def_field)
        assert np.allclose(comp_def_mesh, exp_def_mesh) is True

    # ----- Test case: Translation and rotation tz -----
    for tz in np.linspace(0, np.pi, num=20):
        def_field = np.array([
            [0, 0, 0, 2, 2, 2, 0, 0, tz],
            [1, 0, 0, 4, 4, 4, 0, 0, 0],
        ])

        exp_def_mesh = np.array([
            [2-sin(tz), 3+(cos(tz)-1), 2],
            [5, 5, 4],
        ])

        comp_def_mesh = get_deformed_mesh(target_mesh, def_field)
        assert np.allclose(comp_def_mesh, exp_def_mesh)

    # ----- Test case: Translation and rotation in all directions -----
    for tx in np.linspace(0, np.pi/2, num=20):
        for ty in np.linspace(0, np.pi/2, num=20):
            for tz in np.linspace(0, np.pi/2, num=20):
                def_field = np.array([
                    [0, 0, 0, 2, 2, 2, tx, ty, tz],
                    [1, 0, 0, 4, 4, 4, 0, 0, 0],
                ])

                exp_def_mesh = np.array([
                    # [2-sin(tz)+(1-cos(ty)), 3+(cos(tx)-1)+(cos(tz)-1), 2+sin(tx)+sin(ty)],
                    [2-sin(tz), 3+(cos(tx)-1)+(cos(tz)-1), 2+sin(tx)],
                    [5, 5, 4],
                ])

                comp_def_mesh = get_deformed_mesh(target_mesh, def_field)
                assert np.allclose(comp_def_mesh, exp_def_mesh)
