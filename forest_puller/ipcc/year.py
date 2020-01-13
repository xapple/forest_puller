#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import re

# Internal modules #
from forest_puller.ipcc.headers import Headers

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas

###############################################################################
class Year:
    """Represents a specific year from a specific country's dataset."""

    def __init__(self, country, xls_file):
        """Record the parent and the file we have to parse."""
        # The parent country #
        self.country = country
        # The file that contains data for this year #
        self.xls_file = xls_file
        # The year itself from the file name #
        self.year = int(re.findall("^[A-Z]+_[0-9]+_([0-9]+)", xls_file.name)[0])
        # Position #

    def __repr__(self):
        return '%s %s of %s' % (self.__class__, self.year, self.country.iso2_code)

    # ---------------------------- Properties --------------------------------#
    @property_cached
    def raw_table_4a(self):
        """Table4.A as is without any modifications."""
        # Load table #
        df = pandas.read_excel(str(self.xls_file),
                               sheet_name = 'Table4.A',
                               header     = None,
                               na_values  = ['IE', 'NE', 'NO', 'NO,NE'])
        # Return #
        return df

    @property_cached
    def headers(self):
        """Parse the column names of the excel sheet."""
        return Headers(self)

    # Hard-code column names, easier #
    column_names = [
        'land_use',
        'subdivision',
        'area',
        'area_mineral',
        'area_organic',
        'gains_ratio',
        'losses_ratio',
        'net_change_ratio',
        'net_dead_ratio',
        'net_litter_ratio',
        'net_mineral_soil_ratio',
        'net_organic_soil_ratio',
        'gains',
        'losses',
        'net_change',
        'net_dead',
        'net_litter',
        'net_mineral_soils',
        'net_organic_soils',
        'net_co2',
    ]

    @property_cached
    def df(self):
        """
        Extract targeted information from 'Table4.A' into a pandas data frame.
        """
        # Look for the position of the first mostly empty row
        # at the end of the table
        selector      = self.raw_table_4a.isnull().sum(axis=1) > 18
        selector[0:9] = False
        selector      = selector.cumsum() == 0
        last_row      = max(selector.index[selector]) + 1
        # Take all lines after the header but before the last row #
        df = self.raw_table_4a.iloc[10:last_row]
        # Rename columns index #
        df.columns = self.column_names
        # Return #
        return df
