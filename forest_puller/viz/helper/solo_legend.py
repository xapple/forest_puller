#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.increments import gain_loss_net_data
    >>> print(gain_loss_net_data.ipcc)
"""

# Built-in modules #

# Internal modules #

# First party modules #
from plumbing.graphs import Graph

# Third party modules #
import numpy, matplotlib
from matplotlib import pyplot

###############################################################################
class SoloLegend(Graph):
    """
    A figure that contains no plot, only a legend, for composition purposes
    with the other graphs.
    """

    short_name = "legend"
    n_col      = 1
    capitalize = True

    @property
    def label_to_color(self):
        raise NotImplementedError()

    def plot(self, **kwargs):
        # Plot #
        fig  = pyplot.figure()
        axes = fig.add_subplot(111)
        # Create lines #
        items = self.label_to_color.items()
        # Modify the labels #
        if self.capitalize: items = [(k.capitalize(), v) for k,v in items]
        # Create the patches #
        patches = [matplotlib.patches.Patch(color=v, label=k) for k,v in items]
        # Suppress a warning #
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            leg = fig.legend(handles   = patches,
                             borderpad = 1,
                             prop      = {'size': 20},
                             frameon   = True,
                             shadow    = True,
                             loc       = 'center',
                             ncol      = self.n_col,
                             fancybox  = True)
        # Remove the axes #
        axes.axis('off')
        # Find the bounding box to remove useless white space #
        fig.canvas.draw()
        expand = [-10, -10, 10, 10]
        bbox   = leg.get_window_extent()
        bbox   = bbox.from_extents(*(bbox.extents + numpy.array(expand)))
        bbox   = bbox.transformed(fig.dpi_scale_trans.inverted())
        # Save #
        self.dpi  = 'figure'
        self.bbox = bbox
        self.save_plot(**kwargs)
        # Return for display in notebooks for instance #
        return fig