#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.genus_barstack import genus_barstack_data
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.multiplot   import Multiplot
from forest_puller                 import cache_dir
from forest_puller.viz.solo_legend import SoloLegend

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas, numpy
from matplotlib import pyplot

###############################################################################
class GenusBarstackData:
    """
    Add a property to every SOEF country object.
    """

    @property_cached
    def countries(self):
        """We have one dataframe for every country."""
        # Load #
        from forest_puller.soef.country import countries
        # Add a property by monkey patching #
        for c in countries.values(): c.genus_comp = GenusComposition(c)
        # Return #
        return countries

###############################################################################
class GenusComposition:
    """
    Produces one dataframe for each country detailing
    the breakdown of the growing stock in terms of genera.
    Also responsible for plotting each individual subplot in the final graph.
    """

    def __init__(self, soef_country):
        # Parent #
        self.parent = soef_country
        # The reference ISO2 code #
        self.iso2_code = soef_country.iso2_code

    @property_cached
    def stock_comp_genus(self):
        # Import #
        from forest_puller.soef.composition import composition_data as comp_data
        # Load #
        df = comp_data.stock_comp.query("country==@self.iso2_code")
        # Join #
        df = df.left_join(comp_data.latin_mapping, on='latin_name')
        # Drop totals #
        df = df.query('rank!="total"')
        # Drop columns and reorder #
        cols_to_drop = ['latin_name', 'common_name', 'rank', 'species']
        cols_to_keep = ['country', 'year', 'genus', 'growing_stock']
        df = df.drop(columns=cols_to_drop)
        df = df[cols_to_keep]
        # Sort the dataframe #
        df = df.sort_values(by=['country', 'year', 'growing_stock'])
        # Return #
        return df

    @property_cached
    def stock_genus_year(self):
        # Load #
        df = self.stock_comp_genus
        # Join #
        df = df.pipe(pandas.pivot_table,
                     index   = ['year'],
                     columns = ['genus'],
                     values  = 'growing_stock',
                     aggfunc = numpy.sum)
        # Sort by average values #
        df = df.reindex(df.mean().sort_values(ascending=False).index, axis=1)
        # But put missing last #
        cols = df.columns.tolist()
        if 'missing' in cols:
            cols.remove('missing')
            cols.append('missing')
            df = df.reindex(columns=cols)
        # Return #
        return df

    @property_cached
    def genus_to_color(self):
        # Import #
        from plumbing.graphs import cool_colors
        # Load #
        df = self.stock_comp_genus
        # Join #
        df = df.pipe(pandas.pivot_table,
                     index   = ['year'],
                     columns = ['genus'],
                     values  = 'growing_stock',
                     aggfunc = numpy.sum)
        # Sort by average values #
        df = df.reindex(df.mean().sort_values(ascending=False).index, axis=1)
        # But put missing last #
        cols = df.columns.tolist()
        if 'missing' in cols:
            cols.remove('missing')
            cols.append('missing')
            df = df.reindex(columns=cols)
        # Return #
        return df

    year_to_index = {1990: 1,
                     2000: 2,
                     2005: 3,
                     2010: 4}

    def plot(self):
        # Load #
        df = self.stock_genus_year
        # Convert to fractions #
        df = df.div(df.sum(axis=1), axis=0)
        # Transpose #
        df = df.T
        # Number of bars and numbers of categories within bars #
        num_cats, num_bars = df.shape
        # Record the bottoms for each successive new bar #
        cum_size = numpy.zeros(num_bars)
        # Space each bar one unit apart from the next #
        x_locations = list(range(num_bars))
        # Loop #
        for i, row in df.iterrows():
            # Unpack #
            year   = row.name
            genera = row.index
            values = row.values
            # Plot #
            pyplot.bar(x_locations,
                       values,
                       bottom = cum_size)
            # Increase #
            cum_size += values

###############################################################################
class GenusBarstack(Multiplot):

    # Basic params #
    x_label    = 'Year'
    formats    = ('pdf',)
    share_y    = True
    share_x    = False
    height     = 5
    width      = 30

    # Size of grid #
    nrows = 1
    ncols = 5

    # Mapping of genera to colors #
    name_to_color = {}

    # The ISO2 codes of these countries #
    @property
    def short_name(self): return '_'.join(c.iso2_code for c in self.parent)

    def plot(self, **kwargs):
        # Plot every curve on every data source #
        for country, axes in zip(self.parent, self.axes):
            pyplot.sca(axes)
            country.genus_comp.plot()

        # Save #
        self.save_plot(**kwargs)

        # Convenience: return for display in notebooks for instance #
        return self.fig

###############################################################################
class GenusBarstackLegend(SoloLegend):
    pass

###############################################################################
# Add the required properties #
genus_barstack_data = GenusBarstackData()
c_vals = list(genus_barstack_data.countries.values())

# Sort countries into batches of a given size #
batch_size = GenusBarstack.ncols
batches    = [c_vals[i:i + batch_size] for i in range(0, len(c_vals), batch_size)]

# Constants #
export_dir = cache_dir + 'graphs/genus_barstack/'

# Create a multiplot for each batch of countries #
all_graphs = [GenusBarstack(b, export_dir) for b in batches]

# Create a separate standalone legend #
legend = GenusBarstackLegend(base_dir = export_dir)