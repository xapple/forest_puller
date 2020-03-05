#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.genus_barstack import genus_barstack_data
    >>> country = genus_barstack_data.countries['FR']
    >>> print(country.genus_comp.stock_comp_genus)
    >>> print(country.genus_comp.sort_cols)
    >>> print(country.genus_comp.stock_genus_by_year)

Or if you want to look at the legend:

    >>> from forest_puller.viz.genus_barstack import genus_legend
    >>> print(genus_legend.label_to_color)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.multiplot   import Multiplot
from forest_puller                 import cache_dir
from forest_puller.viz.solo_legend import SoloLegend
from forest_puller.common          import country_codes

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas, numpy
from matplotlib import pyplot

###############################################################################
