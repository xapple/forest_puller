#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.manuscript.area_comparison import all_graphs
    >>> for g in all_graphs: g.plot(rerun=True)
    >>> from forest_puller.viz.manuscript.area_comparison import legend
    >>> legend.plot(rerun=True)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.area_comp import all_graphs as orig_graphs
from forest_puller.viz.area_comp import AreaComparison, AreaLegend
from forest_puller               import cache_dir

# First party modules #

# Third party modules #

###############################################################################
# Change the pdf destination path #
export_dir = cache_dir + 'graphs/manuscript/area/'

# Copy original graphs #
all_graphs = [AreaComparison(g.parent, export_dir) for g in orig_graphs]

# Remove the CBM line #
for g in all_graphs: g.sources = ('ipcc', 'soef', 'hpffre', 'faostat', 'fra')

# Copy the legend #
legend = AreaLegend(base_dir = export_dir)

# Remove the CBM line #
labels = AreaLegend.label_to_color.copy()
labels.pop('EU-CBM')
legend.label_to_color = labels