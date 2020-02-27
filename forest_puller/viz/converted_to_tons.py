#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.converted_to_tons import converted_tons_data
    >>> print(converted_tons_data.ipcc)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.multiplot import Multiplot
from forest_puller import module_dir
from forest_puller.viz.increments import gain_loss_net_data

# First party modules #
from plumbing.cache  import property_cached

# Third party modules #
import pandas, numpy
from matplotlib import pyplot

###############################################################################
class ConvertedTonsData:
    """
    Aggregate and prepare all the dataframes that will be used in the
    'converted to tons' visualization.

    * Start with: one cubic meter (in each country in each year).
    * Obtain: the density in [tons / m^3] more precisely [oven-dry tonnes of C per moist m^3].
    * Multiply the volume with the density to obtain [tons].
    * Multiply the result with the bark correction factor to obtain over/under bark.
    * The result is now in tons of carbon per hectare.
    """

    #----------------------------- Data sources ------------------------------#
    @property
    def avg_densities(self):
        """Convenience shortcut to the avg_densities dataframe."""
        from forest_puller.soef.composition import composition_data
        return composition_data.avg_densities

    #------------------------ Data sources modified --------------------------#
    @property_cached
    def ipcc(self):
        # Load #
        df = gain_loss_net_data.ipcc.copy()
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property_cached
    def faostat(self):
        # Load #
        df = gain_loss_net_data.faostat.copy()
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property_cached
    def hpffre(self):
        # Load #
        df = gain_loss_net_data.hpffre.copy()
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    #----------------------- Data sources unmodified -------------------------#
    @property
    def soef(self):
        # Load #
        df = gain_loss_net_data.soef
        # Return #
        return df

    @property
    def eu_cbm(self):
        # Load #
        df = gain_loss_net_data.eu_cbm
        # Return #
        return df

    #------------------------------- Combine ---------------------------------#
    @property_cached
    def df(self):
        # Load all data sources #
        sources = [self.ipcc, self.soef, self.faostat, self.hpffre, self.eu_cbm]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Return #
        return df

###############################################################################
# Create the large df #
converted_tons_data = ConvertedTonsData()

# Create a facet for each country #
#export_dir = cache_dir + 'graphs/increments/'
#all_codes  = country_codes['iso2_code']
#all_graphs = [ConvertedTonsGraph(iso2, export_dir) for iso2 in all_codes]
#countries  = {c.parent: c for c in all_graphs}

# Create a separate standalone legend #
#legend = GainsLossNetLegend(base_dir = cache_dir + 'graphs/increments/')