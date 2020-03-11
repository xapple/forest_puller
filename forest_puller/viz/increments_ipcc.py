#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller           import cache_dir
from forest_puller.viz.increments import GainsLossNetGraph

# First party modules #

# Third party modules #
from matplotlib import pyplot

###############################################################################
class IncrementsIPCC(GainsLossNetGraph):
    """
    This graph will show the gains loss and net increments for all countries
    by making one sub-plot for each country on a facet plot.
    However it will focus on only one source: IPCC to avoid making a
    visualization that would be too large.
    """

    facet_var  = "country"

    @property
    def y_label(self): return self.source_to_y_label['ipcc']

    @property
    def df(self):
        # Load #
        df = gain_loss_net_data.df
        # Filter #
        df = df.query("country == @self.parent").copy()
        # Return #
        return df

    def plot(self, **kwargs):
        # Plot each curve #
        for curve in ('gain_per_ha', 'loss_per_ha', 'net_per_ha'):
            self.facet.map_dataframe(self.line_plot, 'year', curve, 'ipcc')
        # Adjust subplots #
        self.facet.map(self.y_grid_on)
        self.facet.map(self.hide_titles)
        self.facet.map(self.y_max_two_decimals)
        # Add a legend #
        self.add_main_legend()
        # Put the title inside the graph and large #
        self.facet.map_dataframe(self.large_legend, 'long_name')
        # Change the labels #
        self.facet.set_axis_labels(self.x_label, self.y_label)
        # Leave some space for the y axis labels #
        pyplot.subplots_adjust(left=0.025)
        # Save #
        self.save_plot(**kwargs)
        # Convenience: return for display in notebooks for instance #
        return self.facet

###############################################################################
# Create the large df #
increments_ipcc = IncrementsIPCC()

# Load the other graph's data #
from forest_puller.viz.increments import gain_loss_net_data

# Create the graph #
export_dir = cache_dir + 'graphs/'
area_comp  = IncrementsIPCC(gain_loss_net_data, export_dir)