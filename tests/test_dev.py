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

# Internal modules #
from forest_puller.soef.country import all_countries, countries

###############################################################################
country = countries['AT']
table   = country.forest_area
df      = table.df
