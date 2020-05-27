#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Script to generate all the figures that are later used in the manuscript.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/reports/manuscript.py

The figures are located in the $FOREST_PULLER_CACHE directory.
"""

# Built-in modules #

# Third party modules #
from tqdm import tqdm
import matplotlib

# Set matplotlib to faceless mode #
matplotlib.use('Agg')

###############################################################################
from forest_puller.viz.manuscript.area_comparison import legend
print(legend.plot(rerun=True))

from forest_puller.viz.manuscript.area_comparison import all_graphs
for g in tqdm(all_graphs): g.plot(rerun=True)

#-----------------------------------------------------------------------------#
from forest_puller.viz.increments import legend
print(legend.plot(rerun=True))

from forest_puller.viz.manuscript.dynamics_volume import all_graphs
for g in tqdm(all_graphs): g.plot(rerun=True)

#-----------------------------------------------------------------------------#
from forest_puller.viz.converted_to_tons import legend
print(legend.plot(rerun=True))

from forest_puller.viz.manuscript.dynamics_mass import all_graphs
for g in tqdm(all_graphs): g.plot(rerun=True)

###############################################################################
from forest_puller.tables.max_area_over_time import max_area
print(max_area.save())

from forest_puller.tables.available_for_supply import afws_comp
print(afws_comp.save())