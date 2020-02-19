#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

A script to print the countries sorted by area (within the IPCC source).

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/viz/show_highest_area.py
"""

# Built-in modules #

# Third party modules #

# Internal modules #
from forest_puller.ipcc.country import countries

###############################################################################
def get_area(c):
    """Get the total forest area of a IPCC country object for the last year."""
    return c.last_year.indexed.loc['total_forest', 'area'][0]

###############################################################################
area_sort = sorted([c for c in countries.values()], key=get_area, reverse=True)
highest   = [c.iso2_code for c in area_sort[:5]]

###############################################################################
print(highest)