#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Development script to test some of the methods in `forest_puller`

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/tests/test_dev.py
"""

# Built-in modules #
from pprint import pprint

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
#from forest_puller.viz.area import area_comp
#area_comp.plot()
#print(area_comp.path)

###############################################################################
#from forest_puller.viz.area_aggregate import area_agg
#area_agg.plot(rerun=True)
#print(area_agg.path)

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
#print(area_comp(rerun=True))
#print(type(area_comp.facet))

###############################################################################
#from forest_puller.viz.increments import gain_loss_net_data
#print(gain_loss_net_data.ipcc)

#from forest_puller.viz.increments import all_graphs
#g = all_graphs[0]
#g.plot(rerun=True)
#print(g.path)

#from forest_puller.viz.increments import all_graphs
#for graph in all_graphs: graph.plot(rerun=True)

#from forest_puller.core.continent import continent
#print(continent.report())

#from forest_puller.viz.increments import legend
#legend.plot(rerun=True)
#print(legend.path)

###############################################################################
#from forest_puller.soef.country import all_countries

#for country in all_countries:
#    del country.stock_comp.df
#    df = country.stock_comp.df
#    print("--------- %s ----------" % country.iso2_code)
#    print(df)

###############################################################################
#from forest_puller.soef.composition import composition_data
#del composition_data.avg_dnsty_intrpld
#interpolated = composition_data.avg_dnsty_intrpld

#from forest_puller.viz.converted_to_tons import all_graphs
#for graph in all_graphs: graph.plot(rerun=True)

#from forest_puller.viz.converted_to_tons import legend
#legend.plot(rerun=True)

#from forest_puller.core.continent import continent
#print(continent.report())

###############################################################################
#from forest_puller.viz.genus_barstack import all_graphs
#for g in all_graphs[:]: g.plot(rerun=True)
#
#from forest_puller.viz.genus_barstack import genus_legend
#genus_legend.plot(rerun=True)
#
#from forest_puller.core.continent import continent
#print(continent.report())

################################################################################
#from forest_puller.viz.color_rgb_code import color_legend
#color_legend.plot(rerun=True)

###############################################################################
#from forest_puller.viz.genus_soef_vs_cbm import all_graphs
#for g in all_graphs[:]: g.plot(rerun=True)
#
#from forest_puller.viz.genus_soef_vs_cbm import genus_legend
#genus_legend.plot(rerun=True)
#
#from forest_puller.core.continent import continent
#print(continent.report())

###############################################################################
#from forest_puller.viz.genus_barstack import genus_legend
#pprint(genus_legend.label_to_color)
#pprint(genus_legend.label_to_color_old)

###############################################################################
#from forest_puller.viz.area_aggregate import area_agg
#area_agg.plot(rerun=True)
#from forest_puller.viz.inc_aggregate import inc_agg_ipcc
#inc_agg_ipcc.plot(rerun=True)
#from forest_puller.viz.inc_aggregate import inc_agg_soef
#inc_agg_soef.plot(rerun=True)
#from forest_puller.viz.inc_aggregate import inc_agg_faostat
#inc_agg_faostat.plot(rerun=True)
#from forest_puller.viz.genus_aggregate import genus_agg
#genus_agg.plot(rerun=True)
#
#from forest_puller.core.continent import continent
#print(continent.report())

###############################################################################
#from forest_puller.tables.max_area_over_time import max_area
#print(max_area.save())

#from forest_puller.tables.area_ipcc_vs_soef import soef_vs_ipcc
#print(soef_vs_ipcc.save())

#from forest_puller.tables.available_for_supply import afws_comp
#print(afws_comp.save())

from forest_puller.tables.average_growth import avg_inc, avg_tons
print(avg_inc.save())
print(avg_tons.save())

from forest_puller.core.continent import continent
print(continent.report())
