#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #

# First party modules #

# Third party modules #
import brewer2mpl

# Colors #
colors = brewer2mpl.get_map('Set1', 'qualitative', 5).mpl_colors
name_to_color = {'IPCC':      colors[0],
                 'SOEF':      colors[1],
                 'HPFFRE':    colors[2],
                 'FAOSTAT':   colors[3],
                 'EU-CBM':    colors[4]}
