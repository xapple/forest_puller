#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #

# First party modules #
from plumbing.cache import property_cached, property_pickled_at

# Third party modules #
import pandas

###############################################################################
class CompositionData:
    """
    Post-processing of the "growing_stock" table to compute, for instance,
    the relative proportion of genera, in each country, where available,
    as well as their corresponding wood densities.
    """

    @property_cached
    def xx(self):
        pass