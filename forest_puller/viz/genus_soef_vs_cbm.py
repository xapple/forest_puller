#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.helper.gridspec_plot import GridspecPlot
from forest_puller                          import cache_dir

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas, numpy
from matplotlib import pyplot

###############################################################################

###############################################################################
class GenusPairedBarstack(GridspecPlot):
    """Plot several countries in a single graph using `gridspec` functionality."""

    # Size of outer grid #
    n_cols = 3
    n_rows = 1

    # Basic params #
    height     = 8
    width      = 30

    # Spacing between countries #
    cntry_spacer = 0.6

    @property
    def short_name(self):
        """All the ISO2 codes of the countries in the current batch."""
        return '_'.join(c for c in self.parent)

    @property_cached
    def fig(self):
        """The matplotlib.Figure object."""
        return pyplot.figure()

    @property_cached
    def widths(self):
        """
        Spacing between each country.
        Looks like [10.0, 0.6, 10.0, 0.6, 10.0]
        """
        base_width = self.width / self.n_cols
        result     = [base_width, self.cntry_spacer] * self.n_cols
        result.pop(-1)
        return result

    @property_cached
    def gridspec(self):
        """The matplotlib.gridspec.GridSpec object."""
        return self.fig.add_gridspec(nrows         = self.n_rows,
                                     ncols         = self.n_cols,
                                     width_ratios  = self.widths)

    @property_cached
    def countries(self):
        """One object per country."""
        return [CountryGenusComparison(self, i, c) for i, c in enumerate(self.parent)]

    def plot(self, **kwargs):
        # Save #
        self.save_plot(**kwargs)
        # Convenience: return for display in notebooks for instance #
        return self.fig

###############################################################################
class CountryGenusComparison:
    """
    Plotting methods for a single country.
    Produces a paired stacked bar chart of genera comparing several years
    across several data sources.
    """

    # Save the country code #
    def __init__(self, parent, num, iso2_code):
        self.parent    = parent
        self.num       = num
        self.iso2_code = iso2_code

    # Size of inner grid #
    n_cols = 4
    n_rows = 1

    # Which years are shown in which order #
    years = [1990, 2000, 2005, 2010]


    #ax1 = fig.add_subplot(gs[0, :])

    # Plot #
    def plot(self, **kwargs):
        pass

###############################################################################
# Import the object from our other graph #
from forest_puller.viz.genus_barstack import genus_barstack_data

# List of all countries #
codes = [c.iso2_code for c in genus_barstack_data.countries.values()]

# Sort countries into batches of a given size #
batch_size = GenusPairedBarstack.n_cols
batches    = [codes[i:i + batch_size] for i in range(0, len(codes), batch_size)]

# Where to save the graphs #
export_dir = cache_dir + 'graphs/genus_soef_vs_cbm/'

# Create a multiplot for each batch of countries #
all_graphs = [GenusPairedBarstack(batch, export_dir) for batch in batches]
