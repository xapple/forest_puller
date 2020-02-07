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
from forest_puller.viz import name_to_color

# First party modules #
from plumbing.graphs import Graph
from plumbing.cache import property_cached

# Third party modules #
import seaborn, pandas
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
        # Import #
        from forest_puller.ipcc.agg import source
        # Load #
        df = source.df.copy()
        # Columns #
        df = df[['year', 'area']]
        # Add source #
        df.insert(0, 'source', "ipcc")
        # Return #
        return df

    @property
    def area_soef(self):
        # Import #
        from forest_puller.soef.agg import source
        # Load #
        df = source.tables['forest_area'].copy()
        # Add source #
        df.insert(0, 'source', 'soef')
        # Return #
        return df

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

    @property_cached
    def data(self):
        """
        Importing the other graph at: `forest_puller.viz.area.area_comp`
        and using it's data frame to aggregate and sum doesn't work because
        one has to filter on the available years. One possible alternative
        approach is df.groupby([source,year]).agg(n=count).query(n==26)
        """
        # Load all data sources #
        sources = [self.area_ipcc, self.area_soef]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Adjust to million hectares #
        df['area'] /= 1e6
        # Return #
        return df

    def plot(self, **kwargs):
        # Plot #
        fig  = pyplot.figure()
        axes = fig.add_subplot(111)

        # Functions #
        def line_plot(x, y, source, **kw):
            data = self.data.query("source == '%s'" % source)
            axes.plot(data[x], data[y],
                      marker     = ".",
                      markersize = 10.0,
                      color      = name_to_color[source.upper()],
                      **kw)

        # Plot every data source #
        line_plot('year', 'area', 'ipcc')
        line_plot('year', 'area', 'soef')
        #line_plot('year', 'area', 'faostat')
        #line_plot('year', 'area', 'eu-cbm')

        # Save #
        self.save_plot(**kwargs)

        # Return for display in notebooks for instance #
        return fig

###############################################################################
area_agg = AreaAggregate(base_dir = cache_dir + 'graphs/')
