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

###############################################################################
# Area comparison #
from forest_puller.viz.area import area_comp
print(area_comp.plot(rerun=True))

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

###############################################################################
# Report #
from forest_puller.core.continent import continent
print(continent.report())