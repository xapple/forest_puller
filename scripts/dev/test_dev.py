#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Development script to test some of the methods in `forest_puller`

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/dev/test_dev.py
"""

# Built-in modules #
from pprint import pprint

# Third party modules #
import pandas
from tqdm import tqdm

###############################################################################
#from forest_puller.tables.max_area_over_time import max_area
#print(max_area.save())

#from forest_puller.core.continent import continent
#print(continent.report())

###############################################################################
from forest_puller.fra.country import all_countries
for country in tqdm(all_countries):
    del country.df
    df = country.df

from forest_puller.tables.max_area_over_time import max_area
print(max_area.save())

from forest_puller.tables.area_ipcc_vs_soef import soef_vs_ipcc
print(soef_vs_ipcc.save())

from forest_puller.tables.available_for_supply import afws_comp
print(afws_comp.save())

from forest_puller.tables.average_growth import avg_inc, avg_tons
print(avg_inc.save())
print(avg_tons.save())

from forest_puller.tables.density_table import wood_density
print(wood_density.save())
