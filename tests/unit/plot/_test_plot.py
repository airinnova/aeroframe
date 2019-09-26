#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aeroframe.fileio.serialise import load_json_def_fields
from aeroframe.plot.makeplot import plot_all


def_fields = load_json_def_fields('def_fields.json')
plot_all(def_fields)
