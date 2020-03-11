#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.helper.color_rgb_code import color_legend
    >>> print(color_legend.plot(rerun=True))
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.genus_barstack import GenusBarstackLegend
from forest_puller                    import cache_dir

# First party modules #
from plumbing.cache import property_cached

# Third party modules #

###############################################################################
class ColorCodeLegend(GenusBarstackLegend):
    """
    So that we can view which color is which RGB code to
    reorganize them.
    """

    short_name = 'color_codes'

    @property_cached
    def cool_colors(self):
        # Import #
        import brewer2mpl
        # Base #
        result = brewer2mpl.get_map('Set1', 'qualitative', 8).mpl_colors
        result.reverse()
        # Pastels #
        result += brewer2mpl.get_map('Pastel2', 'qualitative', 8).mpl_colors
        # Missing 3 more #
        extras  = brewer2mpl.get_map('Set3', 'qualitative', 8).mpl_colors[4:7]
        result += extras
        # Return #
        return result

    @property_cached
    def labels(self):
        # Import #
        from forest_puller.other.tree_species_info import df as species_info
        # Load #
        genera = list(species_info['genus'].unique())
        genera.insert(0, 'missing')
        # Return #
        return genera

    @property_cached
    def label_to_color(self):
        colors = self.cool_colors[:len(self.labels)]
        names  = [' '.join(map(lambda f: '%.3f' % f, rgb)) for rgb in colors]
        return dict(zip(names, colors))

###############################################################################
export_dir = cache_dir + 'graphs/genus_barstack/'
color_legend = ColorCodeLegend(base_dir = export_dir)