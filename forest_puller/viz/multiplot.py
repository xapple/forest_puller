#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import warnings

# Internal modules #

# First party modules #
from plumbing.graphs import Graph
from plumbing.cache import property_cached

# Third party modules #
import matplotlib, numpy
from matplotlib import pyplot

###############################################################################
class Multiplot(Graph):
    """
    Similar to a FacetPlot, expect we don't use `seaborn` and do everything
    ourselves with `matplotlib`.
    """

    # Size of grid #
    nrows = 1
    ncols = 1

    # Defaults #
    share_y = True
    share_x = True

    @property_cached
    def fig_and_axes(self):
        # Synonyms #
        if self.share_x is True: self.share_x = 'all'
        if self.share_y is True: self.share_y = 'all'
        # Create #
        fig, axes = pyplot.subplots(nrows  = self.nrows,
                                    ncols  = self.ncols,
                                    sharex = self.share_x,
                                    sharey = self.share_y)
        # Return #
        return fig, axes

    @property
    def fig(self): return self.fig_and_axes[0]

    @property
    def axes(self): return self.fig_and_axes[1]

    #--------------- Conveniance ---------------------------------------------#
    def iterate_all_axes(self, fn):
        for axes in numpy.nditer(self.axes, flags=['refs_ok']): fn(axes)

    def x_grid_on(self, **kw):
        """Add horizontal lines on the x axis."""
        fn = lambda axes: axes.xaxis.grid(True, linestyle=':')
        self.iterate_all_axes(fn)

    def y_grid_on(self, **kw):
        """Add horizontal lines on the y axis."""
        pyplot.gca().yaxis.grid(True, linestyle=':')

    def hide_titles(self, **kw):
        """Remove the subplot titles."""
        pyplot.gca().title.set_visible(False)

    def y_max_two_decimals(self, **kw):
        """Force maximum two decimals for y axis."""
        str_formatter = matplotlib.ticker.FormatStrFormatter('%.2f')
        pyplot.gca().yaxis.set_major_formatter(str_formatter)

    def large_legend(self, x, **kw):
        """Put the title inside the graph and large."""
        df        = kw.pop("data")
        iso2_code = df[x].iloc[0]
        axes      = pyplot.gca()
        axes.text(0.08, 0.9, iso2_code, transform=axes.transAxes, ha="left", size=22)

    def add_main_legend(self, name_to_color=None):
        """Make a single box with the legend for the whole graph."""
        if name_to_color is None: name_to_color = self.name_to_color
        items   = name_to_color.items()
        patches = [matplotlib.patches.Patch(color=v, label=k) for k,v in items]
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            self.facet.add_legend(handles   = patches,
                                  borderpad = 1,
                                  prop      = {'size': 20},
                                  frameon   = True,
                                  shadow    = True,
                                  loc       = 'lower right')

    def y_center_origin(self, **kw):
        """
        Place the zero-intercept exactly the middle of the graph.
        This is not the same as doing:
        `axes.spines['left'].set_position('center')`
        """
        axes        = pyplot.gca()
        bottom, top = axes.get_ylim()
        highest     = max(abs(top), abs(bottom))
        axes.set_ylim(-highest, highest)
