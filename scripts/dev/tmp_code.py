#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Development script to test some of the methods in `forest_puller`

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/dev/test_dev.py
"""

# Built-in modules #

# Third party modules #
import pandas
from tqdm import tqdm

# Set matplotlib to faceless mode #
import matplotlib
matplotlib.use('Agg')

###############################################################################
from forest_puller.tables.max_area_over_time import max_area_pub
print(max_area_pub.save())