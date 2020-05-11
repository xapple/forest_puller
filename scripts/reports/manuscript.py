#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Script to generate all the figures that are later used in the manuscript.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/reports/manuscript.py

Generated figures are located in:

    /home/paul/rp/puller_cache/graphs
"""

# Built-in modules #

# Third party modules #
from tqdm import tqdm
import matplotlib

# Set matplotlib to faceless mode #
matplotlib.use('Agg')

###############################################################################
from forest_puller.viz.manuscript.area_comparison import legend
legend.plot(rerun=True)

from forest_puller.viz.manuscript.area_comparison import all_graphs
for g in tqdm(all_graphs): g.plot(rerun=True)

from forest_puller.viz.manuscript.dynamics_comparison import all_graphs
for g in tqdm(all_graphs): g.plot(rerun=True)

