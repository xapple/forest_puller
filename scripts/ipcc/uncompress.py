#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

For every country: uncompress the zip file(s) that were downloaded from the
IPCC website and place the result it in a directory.
"""

# Built-in modules #

# Third party modules #
from tqdm import tqdm

# Internal modules #
from forest_puller.ipcc.country import all_countries

###############################################################################
country = all_countries[0]

for country in tqdm(all_countries):
    if country.iso2_code == 'ES': continue
    country.uncompress()