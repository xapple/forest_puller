#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller.soef.country import all_countries

# First party modules #

# Third party modules #
import pandas

##############################################################################
table_names = ["forest_area", "age_dist", "fellings", "stock_comp"]
tables      = {}

for table_name in table_names:
    every_country = (getattr(c, table_name).country_cols for c in all_countries)
    tables[table_name] = pandas.concat(every_country, ignore_index=True)
