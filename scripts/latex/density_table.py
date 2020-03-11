#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Script to automatically generate a latex formatted table from a pandas data frame.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/latex/density_table.py
"""

# Built-in modules #

# Internal modules #
from forest_puller.soef.composition import composition_data

# First party modules #
from autopaths import Path

# Third party modules #
import pandas

###############################################################################
# Load #
df = composition_data.avg_densities.copy()

# Downcast to integer #
df['year'] = df['year'].apply(pandas.to_numeric, errors="coerce", downcast='integer')

# Pivot #
avg_densities_wide = df.pivot(index = 'country', columns='year', values=['avg_density', 'frac_missing'])

# Pick the title #
label = 'Weighted average density by country'

# Generate LaTeX #
tex = avg_densities_wide.to_latex(float_format = "%.3f",
                                  na_rep       = '',
                                  label        = label)

# Pick the destination #
#path = Path("/Users/sinclair/repos/sinclair/work/ispra_italy/repos/puller_pub/tables/density_table.tex")
path = Path("~/repos/puller_pub/tables/density_table.tex")

# Add a little line #
tex = tex.replace("lrrrrrrrr", "lrrrr|rrrr")

# Write to file #
with open(path, 'w') as handle: handle.write(tex)
