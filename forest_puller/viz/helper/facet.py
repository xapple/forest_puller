#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import math, warnings

# Internal modules #

# First party modules #
from plumbing.graphs import Graph
from plumbing.cache import property_cached

# Third party modules #
import matplotlib, brewer2mpl, seaborn
from matplotlib import pyplot
from matplotlib import ticker

###############################################################################
class FacetPlot(Graph):

    # Defaults #
    share_y = True
    share_x = True

    # Colors #
    colors = brewer2mpl.get_map('Set1', 'qualitative', 5).mpl_colors
    name_to_color = {'IPCC':    colors[0],
                     'SOEF':    colors[1],
                     'HPFFRE':  colors[2],
                     'FAOSTAT': colors[3],
                     'EU-CBM':  colors[4]}

    @property_cached
    def facet(self):
        """The seaborn plot object."""
        # Default values #
        arguments = dict(data     = self.df,
                         col      = self.facet_var,
                         sharey   = self.share_y,
                         sharex   = self.share_x,
                         col_wrap = self.col_wrap,
                         height   = 6.0,
                         dropna   = False)
        # Are we doing a one dimensional or two dimensional plot #
        if hasattr(self, 'facet_var'): arguments['col'] = self.facet_var
        else: arguments.update({'col': self.col_var, 'row': self.row_var})
        # Return #
        return seaborn.FacetGrid(**arguments)

    @property
    def col_wrap(self):
        """Calculate the number of columns."""
        return math.ceil(len(self.df[self.facet_var].unique()) / 9.0) + 1

    def line_plot(self, x, y, source, **kwargs):
        # Remove the color we get #
        kwargs.pop("color")
        # Get the data frame #
        df = kwargs.pop("data")
        # Filter the source #
        df = df.query("source == '%s'" % source)
        # Plot #
        pyplot.plot(df[x], df[y],
                    marker     = ".",
                    markersize = 10.0,
                    color      = self.name_to_color[source.upper()],
                    **kwargs)

    def x_grid_on(self, **kw):
        """Add horizontal lines on the x axis."""
        pyplot.gca().xaxis.grid(True, linestyle=':')

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

    def large_title(self, x, **kw):
        """Put the title inside the graph and large."""
        df        = kw.pop("data")
        iso2_code = df[x].iloc[0]
        axes      = pyplot.gca()
        axes.text(0.08, 0.9, iso2_code, transform=axes.transAxes, ha="left", size=22)

    def add_main_legend(self, name_to_color=None):
        """Make a box with the legend for all plots."""
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
