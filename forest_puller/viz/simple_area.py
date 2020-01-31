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

# First party modules #
from plumbing.graphs import Graph

# Third party modules #
import seaborn
from matplotlib import pyplot

###############################################################################
class AreaComparison(Graph):
    short_name = 'area_comparison'
    sep     = ('y',)
    y_grid  = True
    y_label = "XXX"

    @property
    def data(self):
        # IPCC #
        area_ipcc = 0000

        return x

    def plot(self, **kwargs):
        # Plot #
        g = seaborn.barplot(x="forest_type", y="mass_1e6", hue="scenario",
                            palette='colorblind', data=self.data)
        # Lines #
        pyplot.gca().yaxis.grid(True, linestyle=':')
        # Save #
        self.save_plot(**kwargs)
        # Return for display in notebooks for instance #
        return g

