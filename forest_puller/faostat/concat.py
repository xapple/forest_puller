#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller.faostat.country import all_countries

# First party modules #

# Third party modules #
import pandas

##############################################################################
every_country = (c.df for c in all_countries)
df = pandas.concat(every_country)
