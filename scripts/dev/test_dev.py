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

from forest_puller.viz.correlation import all_graphs
for graph in all_graphs: print(graph.plot(rerun=True))

from forest_puller.core.continent import continent
print(continent.report())
