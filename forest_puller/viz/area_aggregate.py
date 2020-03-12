#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.viz.area_aggregate import area_agg_data
    >>> print(area_agg_data.area_ipcc)

To generate the plot:

    >>> from forest_puller.viz.area_aggregate import area_agg
    >>> area_agg.plot(rerun=True)
    >>> print(area_agg.path)
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir

# First party modules #
from plumbing.graphs import Graph
from plumbing.cache import property_cached

# Third party modules #
import pandas, brewer2mpl, matplotlib
from matplotlib import pyplot

###############################################################################
class AreaAggregateData:
    """
    Prepare all aggregated by year dataframes.
    """

    #----------------------------- Data sources ------------------------------#
    @property
    def area_ipcc(self):
        # Import #
        from forest_puller.ipcc.agg import source
        # Load #
        df = source.df.copy()
        # Take only columns that interest us #
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
        df = source.forest_area.copy()
        # Add source #
        df.insert(0, 'source', 'soef')
        # Return #
        return df

    @property
    def area_faostat(self):
        # Import #
        from forest_puller.faostat.land.agg import source
        # Load #
        df = source.forest_area.copy()
        # Add source #
        df.insert(0, 'source', 'faostat')
        # Return #
        return df

    @property
    def area_eu_cbm(self):
        # Import #
        from forest_puller.cbm.agg import source
        # Load #
        df = source.forest_area.copy()
        # Add source #
        df.insert(0, 'source', 'eu-cbm')
        # Return #
        return df

    #---------------------------- Data combined ------------------------------#
    @property_cached
    def df(self):
        """
        Importing the other graph at: `forest_puller.viz.area.area_comp`
        and using its data frame to aggregate and sum doesn't work because
        one has to filter on the available years. One possible alternative
        approach is some long dataframe processing starting with:

            df.groupby([source,year]).agg(n=count).query(n==27)

        This is not the road we have chosen here.
        """
        # Load all data sources #
        sources = [self.area_ipcc, self.area_soef, self.area_faostat,
                   self.area_eu_cbm]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Adjust to million hectares #
        df['area'] /= 1e6
        # Return #
        return df

###############################################################################
class AreaAggregate(Graph):
    """
    This graph will show the combined forested area by summing all countries
    together into one graph.
    """

    # Size #
    height = 7
    width  = 10

    # Basic params #
    short_name = 'area_aggregate'
    y_grid  = True
    x_label = "Years"
    y_label = "Area in million hectares"

    # Colors #
    colors = brewer2mpl.get_map('Set1', 'qualitative', 5).mpl_colors
    name_to_color = {'IPCC':    colors[0],
                     'SOEF':    colors[1],
                     'HPFFRE':  colors[2],
                     'FAOSTAT': colors[3],
                     'EU-CBM':  colors[4]}

    def line_plot(self, axes, x, y, source, **kw):
        # Filter by source #
        data = area_agg_data.df.query("source == '%s'" % source)
        # Plot #
        axes.plot(data[x], data[y],
                  marker     = ".",
                  markersize = 10.0,
                  color      = self.name_to_color[source.upper()],
                  **kw)

    def add_main_legend(self, axes):
        items   = self.name_to_color.items()
        patches = [matplotlib.patches.Patch(color=v, label=k) for k,v in items]
        axes.legend(handles   = patches,
                    borderpad      = 1,
                    prop           = {'size': 12},
                    frameon        = True,
                    shadow         = True,
                    loc            = 'center left',
                    bbox_to_anchor = (1.03, 0.5))

    def plot(self, **kwargs):
        # Plot #
        fig  = pyplot.figure()
        axes = fig.add_subplot(111)

        # Plot every data source #
        self.line_plot(axes, 'year', 'area', 'ipcc')
        self.line_plot(axes, 'year', 'area', 'soef')
        self.line_plot(axes, 'year', 'area', 'faostat')
        self.line_plot(axes, 'year', 'area', 'eu-cbm')

        # Leave space for the legend #
        fig.subplots_adjust(left=0.1, right=0.8, top=0.95)

        # Add legend #
        self.add_main_legend(axes)

        # Save #
        self.save_plot(**kwargs)

        # Return for display in notebooks for instance #
        return fig

###############################################################################
# Create the large df with all sources #
area_agg_data = AreaAggregateData()

# Create the graph #
export_dir = cache_dir + 'graphs/eu_tot/'
area_agg = AreaAggregate(base_dir = export_dir)
