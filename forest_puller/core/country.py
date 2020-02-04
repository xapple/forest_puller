#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas

###############################################################################
class Country:
    """Represents one country's dataset."""

    def __init__(self, iso2_code):
        # The reference ISO2 code #
        self.iso2_code = iso2_code

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

    #-------------------------------- Sources --------------------------------#
    @property
    def ipcc(self):
        from forest_puller.ipcc.country import countries
        return countries[self.iso2_code]

    @property
    def soef(self):
        from forest_puller.soef.country import countries
        return countries[self.iso2_code]

    @property
    def faostat(self):
        # Imports #
        from forest_puller.faostat.forestry.country import countries as c_forest
        from forest_puller.faostat.land.country     import countries as c_land
        # Two sub-data sources #
        attrs = {
            'forestry': c_forest[self.iso2_code],
            'land': c_land[self.iso2_code]
        }
        # Make a fake object with two attributes #
        return type('faostat', (object,), attrs)

    @property
    def hpffre(self):
        from forest_puller.hpffre.country import countries
        return countries[self.iso2_code]

    #-------------------------------- Other ----------------------------------#
    @property_cached
    def min_year_area(self):
        """This method is not finished."""
        # Load #
        ipcc    = self.ipcc.copy()
        soef    = self.soef.copy()
        faostat = self.faostat.land.copy()
        hpffre  = self.hpffre.copy()
        # Add source #
        ipcc.insert(0,    'source', 'ipcc')
        soef.insert(0,    'source', 'soef')
        faostat.insert(0, 'source', 'faostat')
        hpffre.insert(0,  'source', 'hpffre')
        # Combine #
        df = pandas.concat(ipcc, soef, faostat, hpffre)
        # Minimum #
        start_year = min(df['year'])
        # Return #
        return start_year