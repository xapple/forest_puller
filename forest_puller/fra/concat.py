#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> import forest_puller.fra.concat
    >>> print(forest_puller.fra.concat.df)
"""

# Built-in modules #

# Internal modules #
from forest_puller.fra.country import all_countries
from forest_puller.fra import csv_file

# First party modules #

# Third party modules #
import pandas

##############################################################################
datasets = [
    'forest_chars',
    'forest_extent',
    'forest_establ',
    'growing_stock',
    'carbon_stock',
    'biomass_stock',
]

##############################################################################
all_raw = [getattr(csv_file, s).df for s in datasets]
all_raw = pandas.concat(all_raw)
all_raw = all_raw.reset_index(drop=True)

##############################################################################
every_country = (c.country_cols for c in all_countries)
df = pandas.concat(every_country, ignore_index=True)
