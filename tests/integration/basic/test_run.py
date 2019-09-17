#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

HERE = os.path.abspath(os.path.dirname(__file__))
DUMMY_SETTING_FILE = os.path.join(HERE, 'aeroframe_settings.json')


def test_run():
    os.system(f"aeroframe -cv {DUMMY_SETTING_FILE}")
