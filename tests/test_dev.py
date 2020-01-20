#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Development script to test some of the methods in `forest_puller`

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/tests/test_dev.py
"""

# Built-in modules #

# Third party modules #
from tqdm import tqdm

# Internal modules #
from forest_puller.ipcc.country import all_countries

###############################################################################
for c in tqdm(all_countries):
    for y in c:
        y.sanity_check()