#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Script to automatically generate a latex formatted table from a pandas data frame.

Typically you would run this file from a command line like this:

    ipython3 -i -- ~/deploy/forest_puller/scripts/latex/density_table.py

Or like this:

    ipython3 -i -- ~/repos/forest_puller/scripts/latex/density_table.py

"""

# Built-in modules #

# Internal modules #
from forest_puller.soef.composition import composition_data

# First party modules #
from autopaths import Path

# Third party modules #

###############################################################################
# Load #
df = composition_data.avg_densities.copy()

# Downcast to integer #
df['year'] = df['year'].apply(int)
# Make frac missing in percent
df['frac_missing'] = df['frac_missing'] * 100

# Pivot #
df = df.pivot(index = 'country', columns='year', values=['avg_density', 'frac_missing'])

# Rename columns
df = df.rename(columns={'avg_density':'Average density ($kg/m^3$)',
                        'frac_missing':'Fraction missing (percent)'})

# Pick the title #
label = 'average_density'
caption = 'Weighted average density by country'

# Generate LaTeX #
tex = df.to_latex(float_format = "%.0f",
                  na_rep       = '',
                  escape       = False,
                  label        = label,
                  caption      = caption)

# Pick the destination #
#path = Path("/Users/sinclair/repos/sinclair/work/ispra_italy/repos/puller_pub/tables/density_table.tex")
# TODO: pass path as an argument
path = Path("~/repos/puller_pub/manuscript/tables/density_table.tex")

# Add a little line #
tex = tex.replace("lrrrrrrrr", "lrrrr|rrrr")

# Write to file #
with open(path, 'w') as handle: handle.write(tex)
