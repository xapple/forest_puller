#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

A script to export the LaTeX source code that displays the provisional
figure 2 of the manuscript, i.e. the full area comparison.

Typically you would run this file from a command line like this:

     python3 ~/deploy/forest_puller/scripts/viz/export_fig_2.py > figure.tex
"""

# Built-in modules #

# Third party modules #

# Internal modules #
from forest_puller import cache_dir

# First party modules #
from pymarktex.figures import LatexFigure, BareFigure

###############################################################################
# Monkey patch #
LatexFigure.abs_path = lambda s: '../' + s.path.rel_path_from(cache_dir)

###############################################################################
# Import #
from forest_puller.viz.manuscript.area_comparison import all_graphs, legend

# Initialize #
result = ""

# Loop every country #
for g in all_graphs: result += str(BareFigure(graph=g, width='\\textwidth'))

# Print #
print(result)

# Add the legend #
#print(BareFigure(graph=legend))
