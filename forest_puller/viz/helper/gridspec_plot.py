#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.helper.multiplot import Multiplot

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import matplotlib, numpy
from matplotlib import pyplot

###############################################################################
class GridspecPlot(Multiplot):
    """
    Wrapper for the `matplotlib` gridspec functionality.
    See https://matplotlib.org/3.1.3/tutorials/intermediate/gridspec.html
    """

    # Size of outer grid #
    n_rows = 1
    n_cols = 1

    # Defaults #
    height = None
    width  = None

    @property_cached
    def fig_and_axes(self):
        # Synonyms #
        if self.share_x is True: self.share_x = 'all'
        if self.share_y is True: self.share_y = 'all'
        # Figure size #
        width  = self.n_cols * 5 if self.width  is None else self.width
        height = self.n_rows * 5 if self.height is None else self.height
        # Create #
        fig, axes = pyplot.subplots(nrows   = self.n_rows,
                                    ncols   = self.n_cols,
                                    sharex  = self.share_x,
                                    sharey  = self.share_y,
                                    figsize = (width, height))
        # Return #
        return fig, axes

    @property
    def fig(self): return self.fig_and_axes[0]

    @property
    def axes(self): return self.fig_and_axes[1]

    #--------------------------- Convenience ---------------------------------#
    def iterate_all_axes(self, fn):
        for axes in numpy.nditer(self.axes, flags=['refs_ok']): fn(axes[()])