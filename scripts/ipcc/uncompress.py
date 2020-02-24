#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

For every country: uncompress the zip file(s) that were downloaded from the
IPCC website and place the result it in a directory.

Manual intervention: delete the strange multi year "HUN" file
Manual intervention: "ES" zip file corrupted, but works on macOS.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/ipcc/uncompress.py
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