#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> import forest_puller.cbm.concat
    >>> df = forest_puller.cbm.concat.area
    >>> print(df)
"""

# Built-in modules #

# Internal modules #
from forest_puller.cbm.country import all_countries

# First party modules #

# Third party modules #
import pandas

##############################################################################
every_country = (c.area_country_cols for c in all_countries)
area = pandas.concat(every_country, ignore_index=True)

every_country = (c.increments_country_cols for c in all_countries)
increments = pandas.concat(every_country, ignore_index=True)
