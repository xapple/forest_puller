#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Script to check what years are available for which country in `forest_puller.ipcc`

Typically you would run this file from a command line like this:

     ipython3 -i -- /deploy/forest_puller/scripts/ipcc/display_start_end_years.py
"""

# Built-in modules #

# Third party modules #
from tqdm import tqdm

# Internal modules #
from forest_puller.ipcc.country import all_countries

###############################################################################
for country in tqdm(all_countries): country.uncompress()