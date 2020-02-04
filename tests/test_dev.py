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
from tqdm import tqdm

# Internal modules #
#from forest_puller.soef.country import all_countries, countries

###############################################################################
#from forest_puller.core.continent import continent
#print(continent.first.min_year_area)

###############################################################################
from forest_puller.viz.area import AreaComparison
graph = AreaComparison(base_dir="~/test/forest_puller/")
graph.plot()
print(graph.path)

###############################################################################
#from forest_puller.hpffre.country import all_countries, countries
#for c in tqdm(all_countries):
#    c.df

###############################################################################
#from forest_puller.faostat.land.zip_file import zip_file
#print(zip_file.raw_csv)

###############################################################################
#from forest_puller.faostat.land.country import all_countries, countries
#at = countries['AT']