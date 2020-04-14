#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

A script to export the LaTeX source code that displays the provisional
figure 3 of the manuscript, i.e. the full increments (dynamics) comparison.

Typically you would run this file from a command line like this:

     python3 ~/deploy/forest_puller/scripts/viz/export_fig_3.py > figure.tex
"""

# Built-in modules #

# Third party modules #

# Internal modules #
from forest_puller.common import country_codes
from forest_puller import cache_dir

# First party modules #
from pymarktex.figures import LatexFigure, BareFigure

###############################################################################
# Monkey patch #
LatexFigure.abs_path = lambda s: '../' + s.path.rel_path_from(cache_dir)

###############################################################################
# Import #
from forest_puller.viz.increments import countries, legend

# Initialize #
result = ""

# Loop every country #
for iso2_code in country_codes['iso2_code']:
    g = countries[iso2_code]
    result += str(BareFigure(graph=g, width='\\textwidth'))

# Print #
print(result)

# Add the legend #
#print(BareFigure(graph=legend))
