#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
import forest_puller
from forest_puller import cache_dir

# First party modules #
from plumbing.graphs import Graph

# Third party modules #
import seaborn
from matplotlib import pyplot

###############################################################################
class AreaAggregate(Graph):

    short_name = 'area_aggregate'
    y_grid  = True
    x_label = "Years"
    y_label = "Area in million hectares"

    #----------------------------- Data sources ------------------------------#
    @property
    def area_ipcc(self):
        # Load #
        area_ipcc = -1
        # Filter #
        area_ipcc = area_ipcc.query("land_use == 'total_forest'")
        # Columns #
        area_ipcc = area_ipcc[['country', 'year', 'area']]
        # Add source #
        area_ipcc.insert(0, 'source', "ipcc")
        # Return #
        return area_ipcc

    @property
    def area_soef(self):
        # Load #
        area_soef = -1
        # Filter #
        area_soef = area_soef.query("category == 'forest'")
        # Columns #
        area_soef = area_soef[['country', 'year', 'area']]
        # Add source #
        area_soef.insert(0, 'source', "soef")
        # Return #
        return area_soef

    @property
    def area_faostat(self):
        # Load #
        area_faos = -1
        # Filter #
        area_faos = area_faos.query('element == "Area"')
        area_faos = area_faos.query('item    == "Forest land"')
        area_faos = area_faos.query('flag    == "A"')
        # Columns #
        area_faos = area_faos[['country', 'year', 'value']]
        area_faos.columns   = ['country', 'year', 'area']
        # Add source #
        area_faos.insert(0, 'source', 'faostat')
        # Return #
        return area_faos

    @property
    def area_eu_cbm(self):
        # Load #
        area_cbm = -1
        # Add source #
        area_cbm.insert(0, 'source', 'eu-cbm')
        # Return #
        return area_cbm

    @property
    def data(self):
        """
        Importing the other graph at: `forest_puller.viz.area.area_comp`
        and using it's data frame to aggregate and sum doesn't work because
        one has to filter on the available years. One possible alternative
        approach is df.groupby([source,year]).agg(n=count).query(n==26)
        """
        pass
        # Return #
        return df

    def plot(self, **kwargs):
        # Load #
        df = self.data
        # Plot #
        pyplot.plot(df['year'], df['area'],
                    marker     = ".",
                    markersize = 10.0,
                    color      = 'k',
                    **kwargs)
        # Save #
        self.save_plot(**kwargs)
        # Return for display in notebooks for instance #
        return g

###############################################################################
area_agg = AreaAggregate(base_dir = cache_dir + 'graphs/')
