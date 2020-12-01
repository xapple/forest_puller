#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule like this:

    >>> from forest_puller.viz.manuscript.dynamics_mass import all_graphs
    >>> for g in all_graphs: g.plot(rerun=True)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.converted_to_tons import all_graphs as orig_graphs
from forest_puller.viz.converted_to_tons import ConvertedTonsGraph
from forest_puller                       import cache_dir

# First party modules #

# Third party modules #

###############################################################################
# Change the pdf destination path #
export_dir = cache_dir + 'graphs/manuscript/dynamics_mass/'

# Copy original graphs #
all_graphs = [ConvertedTonsGraph(g.parent, export_dir) for g in orig_graphs]

# Remove the fifth axes #
for g in all_graphs: g.n_cols = 4
for g in all_graphs: g.height = 6