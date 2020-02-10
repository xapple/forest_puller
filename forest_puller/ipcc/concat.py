#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> import forest_puller.ipcc.concat
    >>> print(forest_puller.ipcc.concat.df)
"""

# Built-in modules #

# Internal modules #
from forest_puller.ipcc.country import all_countries

# First party modules #

# Third party modules #
import pandas

##############################################################################
every_year = (y.year_country_cols for c in all_countries for y in c)
df = pandas.concat(every_year, ignore_index=True)
