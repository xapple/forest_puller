#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

A script to export some graphs in SVG format for inclusion in the README
and showcasing.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/viz/export_increments_svg.py

This takes about 1 minute and 30 seconds to run.
"""

# Built-in modules #

# Third party modules #
from tqdm import tqdm

# Internal modules #
from forest_puller.viz.increments import countries

# Constants #
highest = ['SE', 'FR', 'FI', 'ES', 'DE']

###############################################################################
# Select highest #
graphs  = {iso2: countries[iso2] for iso2 in highest}

# Set them to SVG #
for g in graphs.values(): g.formats = ('svg',)

# Remove a source #
for g in graphs.values():
    df = g.df.copy()
    df = df.query("source != 'eu-cbm'").copy()
    g.df = df

# Put the legend on the first one #
list(graphs.values())[0].display_legend = True

###############################################################################
# Plot all graphs #
for graph in tqdm(graphs.values()): graph.plot(rerun=True)
