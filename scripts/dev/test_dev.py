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
#from forest_puller.viz.manuscript.area_comparison import all_graphs
#for g in tqdm(all_graphs): g.plot(rerun=True)
#from forest_puller.viz.manuscript.area_comparison import legend
#legend.plot(rerun=True)

#from forest_puller.viz.manuscript.dynamics_comparison import all_graphs
#for g in tqdm(all_graphs): g.plot(rerun=True)

#from forest_puller.viz.increments import countries
#countries['DK'].plot(rerun=True)

#from forest_puller.viz.correlation import all_graphs
#for graph in all_graphs: print(graph.plot(rerun=True))

#from forest_puller.core.continent import continent
#print(continent.report())

#from forest_puller.soef.country import all_countries, countries
#
#for country in all_countries:
#    print("--------- %s ----------" % country.iso2_code)
#    if country.iso2_code != 'EE': continue
#    del country.stock.df
#    df = country.stock.df
#    print(df)
#
#from forest_puller.soef.country import all_countries, countries
#country = countries['EE']
#table5 = country.stock.indexed
#print(table5)

#from forest_puller.viz.increments import all_graphs
#for graph in all_graphs: print(graph.plot(rerun=True))
#
#from forest_puller.viz.increments import legend
#print(legend.plot(rerun=True))
#
#from forest_puller.core.continent import continent
#print(continent.report())

#from forest_puller.conversion.load_expansion_factor import df
#print(df)

#from forest_puller.conversion.bcef_by_country import country_bcef
#print(country_bcef.by_country_year)

#from forest_puller.conversion.bcef_by_country import country_bcef
#del country_bcef.by_country_year
#print(country_bcef.all_stock_abg_biomass)

#from forest_puller.tests.conversion.test_bcef_by_country import test_bcef_intrpld
#print(test_bcef_intrpld())

#from forest_puller.tests.conversion.test_root_ratio import test_root_intrpld
#print(test_root_intrpld())

#from forest_puller.conversion.root_ratio_by_country import country_root_ratio
#print(country_root_ratio.by_country_year)

#from forest_puller.viz.converted_to_tons import converted_tons_data
#print(converted_tons_data.faostat)

#from forest_puller.viz.increments import all_graphs
#for graph in all_graphs: print(graph.plot(rerun=True))
#from forest_puller.viz.converted_to_tons import all_graphs
#for graph in all_graphs: print(graph.plot(rerun=True))
#from forest_puller.viz.converted_to_tons import legend
#print(legend.plot(rerun=True))
#from forest_puller.core.continent import continent
#print(continent.report())

from forest_puller.tables.max_area_over_time import max_area_pub
print(max_area_pub.save())
