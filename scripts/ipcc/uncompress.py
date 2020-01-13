#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

For every country: uncompress the zip file(s) that were downloaded from the
IPCC website and place the result it in a directory.

The final file structure will look like this:

/puller_cache/ipcc/xls/AT:
16M Jan 12 18:15 aut-2019-crf-15apr19.zip

/puller_cache/ipcc/xls/DK:
17M Jan 12 18:15 dnm-2019-crf-12apr19.zip
14M Jan 12 18:15 dke-2019-crf-12apr19.zip
15M Jan 12 18:15 dnk-2019-crf-12apr19.zip
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