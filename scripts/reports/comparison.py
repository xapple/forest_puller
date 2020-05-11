#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Script to generate the 'comparison.pdf' report.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/reports/comparison.py
"""

# Built-in modules #

# Third party modules #
import matplotlib

# Set matplotlib to faceless mode #
matplotlib.use('Agg')

###############################################################################
# Area comparison #
from forest_puller.viz.area_comp import all_graphs
for g in all_graphs: print(g.plot(rerun=True))

from forest_puller.viz.area_comp import legend
print(legend.plot(rerun=True))

#-----------------------------------------------------------------------------#
# Increments #
from forest_puller.viz.increments import all_graphs
for graph in all_graphs: print(graph.plot(rerun=True))

from forest_puller.viz.increments import legend
print(legend.plot(rerun=True))

#-----------------------------------------------------------------------------#
# Converted to tons #
from forest_puller.viz.converted_to_tons import all_graphs
for graph in all_graphs: print(graph.plot(rerun=True))

from forest_puller.viz.converted_to_tons import legend
print(legend.plot(rerun=True))

#-----------------------------------------------------------------------------#
# Genus breakdown #
from forest_puller.viz.genus_barstack import all_graphs
for g in all_graphs[:]: print(g.plot(rerun=True))

from forest_puller.viz.genus_barstack import genus_legend
print(genus_legend.plot(rerun=True))

#-----------------------------------------------------------------------------#
# Genus SOEF vs EU-CBM #
from forest_puller.viz.genus_soef_vs_cbm import all_graphs
for g in all_graphs[:]: print(g.plot(rerun=True))

from forest_puller.viz.genus_soef_vs_cbm import genus_legend
print(genus_legend.plot(rerun=True))

#-----------------------------------------------------------------------------#
# Aggregates #
from forest_puller.viz.area_aggregate import area_agg
print(area_agg.plot(rerun=True))

from forest_puller.viz.inc_aggregate import inc_agg_ipcc
print(inc_agg_ipcc.plot(rerun=True))

from forest_puller.viz.inc_aggregate import inc_agg_soef
print(inc_agg_soef.plot(rerun=True))

from forest_puller.viz.inc_aggregate import inc_agg_faostat
print(inc_agg_faostat.plot(rerun=True))

from forest_puller.viz.genus_aggregate import genus_agg
print(genus_agg.plot(rerun=True))

#-----------------------------------------------------------------------------#
# Tables #
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

#-----------------------------------------------------------------------------#
# Correlations #
from forest_puller.viz.correlation import all_graphs
for graph in all_graphs: print(graph.plot(rerun=True))

###############################################################################
# Report #
from forest_puller.core.continent import continent
print(continent.report())