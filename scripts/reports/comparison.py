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
from forest_puller.viz.increments import all_graphs
for graph in all_graphs: graph.plot(rerun=True)

from forest_puller.viz.increments import legend
legend.plot(rerun=True)

from forest_puller.core.continent import continent
print(continent.report())