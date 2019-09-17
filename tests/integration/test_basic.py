#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aeroframe.__version__ as v


def test_version():
    assert isinstance(v.__version__, str)
    assert isinstance(v.VERSION, tuple)
