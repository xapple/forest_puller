#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.genus_barstack import genus_barstack_data
    >>> print(genus_barstack_data.df)
"""

# Built-in modules #

# Internal modules #
from forest_puller.common          import country_codes
from forest_puller.viz.multiplot   import Multiplot
from forest_puller                 import cache_dir
from forest_puller.viz.solo_legend import SoloLegend

# First party modules #
from plumbing.cache  import property_cached

# Third party modules #

###############################################################################
class GenusBarstackData:
    """
    Lorem ipsum
    """

    @property_cached
    def df(self):
        # Load #
        pass
        # Return #
        return df

###############################################################################
class GenusBarstackGraph(Multiplot):

    # Size of grid #
    nrows = 5

###############################################################################
class GenusBarstackLegend(SoloLegend):
    pass

###############################################################################
# Create the large df #
genus_barstack_data = GenusBarstackData()

# Sort countries into batches  #
batch_size = GenusBarstackGraph.nrows
countries  = [iso2 for iso2 in country_codes['iso2_code']]
batches    = [countries[i:i + batch_size] for i in range(0, len(countries), batch_size)]

# Create a multiplot for each batch of countries #
export_dir = cache_dir + 'graphs/genus_barstack/'
all_graphs = [GenusBarstackGraph(iso2, export_dir) for iso2 in batches]
countries  = {tuple(c.parent): c for c in all_graphs}

# Create a separate standalone legend #
legend = GenusBarstackLegend(base_dir = export_dir)