#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Script to automatically generate a latex formatted table from a pandas data frame.

Typically you would run this file from a command line like this:

    python3 ~/repos/forest_puller/scripts/latex/density_table.py > ~/repos/puller_pub/tables/density_table.tex

Or like this (locally):

    python3 /Users/sinclair/repos/sinclair/work/ispra_italy/repos/forest_puller/scripts/latex/density_table.py > /Users/sinclair/repos/sinclair/work/ispra_italy/repos/puller_pub/tables/density_table.tex
"""

# Built-in modules #
import sys

# Internal modules #
from forest_puller.soef.composition import composition_data

# First party modules #

# Third party modules #

###############################################################################
# Load #
df = composition_data.avg_densities.copy()

# Downcast to integer #
df['year'] = df['year'].apply(int)

# Specifying float_format produces errors, let's format ourselves #
df['avg_density']  = df['avg_density'].apply(lambda f: "%i" % f)

# Express frac_missing as a percentage #
df['frac_missing'] = df['frac_missing'] * 100
df['frac_missing'] = df['frac_missing'].apply(lambda f: "%i\\%%" % f)

# Pivot #
df = df.pivot(index='country', columns='year', values=['avg_density', 'frac_missing'])

# Rename columns #
df = df.rename(columns={'avg_density':  'Average density ($kg/m^3$)',
                        'frac_missing': 'Fraction missing'})

# Rename indexes #
df.index.name    = "Country"
df.columns.names = [None, 'Year']

# Generate LaTeX #
tex = df.to_latex(na_rep='-', escape=False)

# Add a little line and right align #
tex = tex.replace("lllllllll", "lrrrr|rrrr")

# Write to file #
sys.stdout.write(tex)
sys.stdout.flush()
