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
#from forest_puller.cbm.concat import df as orig_eu_cbm

###############################################################################
#from forest_puller.core.continent import continent
#print(continent.first.min_year_area)

###############################################################################
#from forest_puller.viz.area import AreaComparison
#graph = AreaComparison(base_dir="~/test/forest_puller/")
#graph.plot()
#print(graph.path)

###############################################################################
from forest_puller.viz.area_aggregate import area_agg
area_agg.plot()
print(area_agg.path)

#from forest_puller.viz.area_aggregate import area_agg
#from forest_puller import cache_dir
#export_path = cache_dir + 'exports/area_agg_interim.csv'
#area_agg.data.to_csv(str(export_path))

#from forest_puller.ipcc.agg import source
#print(source.common_years)

#from forest_puller.faostat.land.agg import source
#print(source.common_years)


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

###############################################################################
#from forest_puller.viz.area import area_comp
#print(area_comp(rerun=False))
#
#from forest_puller.core.continent import continent
#print(continent.report())