#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.viz.genus_aggregate import genus_agg
    >>> print(genus_agg.df)
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir

# First party modules #
from plumbing.graphs import Graph
from plumbing.cache import property_cached

# Third party modules #
import pandas, numpy
from matplotlib import pyplot

###############################################################################
class GenusAggregate(Graph):
    """
    This graph will show the breakdown of the growing stock (m^3) composition
    in terms of genera, for all countries combined together from the SOEF
    data source.
    """

    # Basic params #
    height  = 7
    width   = 10
    y_grid  = True

    # Name #
    short_name = 'genus_agg'

    @property_cached
    def df(self):
        # Import #
        from forest_puller.soef.composition import composition_data
        # Load #
        df = composition_data.stock_collapsed.copy()
        # Remove Portugal which didn't give info for 2010 #
        df = df.query('country != "PT"')
        # Filter rank #
        df = df.query('rank != "total"')
        # Filter year #
        df = df.query('year == 2010')
        # Columns #
        df = df[['country', 'year', 'genus', 'growing_stock']]
        # Assert there are no NaNs #
        assert not df.isna().any().any()
        # Aggregate #
        df = df.groupby(['genus'])
        df = df.agg(pandas.DataFrame.sum, skipna=False)
        df = df.reset_index()
        # Columns #
        df = df[['genus', 'growing_stock']]
        # Sort #
        df = df.sort_values('growing_stock', ascending=False)
        # Return #
        return df

    def plot(self, **kwargs):
        # Prepare #
        fig  = pyplot.figure()
        axes = fig.add_subplot(111)
        # Load #
        x = list(self.df['genus'])
        y = list(self.df['growing_stock'])
        # Put missing as the last #
        position    = x.index('missing')
        missing_str = x.pop(position)
        missing_val = y.pop(position)
        x.append(missing_str)
        y.append(missing_val)
        # Compute #
        x_enum = numpy.arange(len(x))
        # Pick colors #
        from forest_puller.viz.genus_soef_vs_cbm import genus_legend
        colors = [genus_legend.label_to_color.get(genus, 'gray') for genus in x]
        # Upper case genus #
        x = list(map(lambda s: s.capitalize(), x))
        # Plot #
        pyplot.bar(x_enum, y,
                   align     = 'center',
                   alpha     = 0.9,
                   color     = colors,
                   edgecolor = 'black')
        # Ticks on X #
        pyplot.xticks(x_enum, x)
        pyplot.setp(axes.xaxis.get_majorticklabels(), rotation=60)
        # Label on Y #
        pyplot.ylabel('Growing stock in cubic meters')
        # Leave space for the legend #
        fig.subplots_adjust(left=0.08, right=0.96, bottom=0.17, top=0.94)
        # Save #
        self.save_plot(**kwargs)
        # Return for display in notebooks for instance #
        return fig

###############################################################################
# Create the graph #
export_dir = cache_dir + 'graphs/eu_tot/'
genus_agg  = GenusAggregate(base_dir = export_dir)
