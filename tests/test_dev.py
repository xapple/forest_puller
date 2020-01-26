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
import pandas

# Internal modules #
from forest_puller.soef.country import all_countries, countries

###############################################################################
table_names = ["forest_area", "age_dist", "fellings"]

for table_name in table_names:
    print("\n\n--------- %s ----------" % table_name.upper())
    for country in all_countries:
        print("Country: %s" % country)
        table = getattr(country, table_name).df
        cols = table.columns
