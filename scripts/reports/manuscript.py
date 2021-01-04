#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Script to generate all the figures that are later used in the manuscript.
The script also exports the data used in those figures.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/reports/manuscript.py

The figures are located in the $FOREST_PULLER_CACHE directory.
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir

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

# TODO: generates an error, see if avg_tons_pub is needed
#ImportError: cannot import name 'avg_tons_pub' from 'forest_puller.tables.average_growth' (/home/paul/repos/forest_puller/forest_puller/tables/average_growth.py)
#from forest_puller.tables.average_growth import avg_tons_pub
#print(avg_tons_pub.save())

# Save manuscript data for use in other statistical software
# TODO replace ~/downloads by an appropriate folder under cache_dir
from forest_puller.viz.increments_df import increments_data
increments_data.df.to_csv("~/downloads/gains_loss_net_mixed_units.csv", index=False)
from forest_puller.viz.converted_to_tons import converted_tons_data
converted_tons_data.df.to_csv("~/downloads/gains_loss_converted_to_tons.csv", index=False)

