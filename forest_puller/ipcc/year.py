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
from forest_puller import module_dir

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas, numpy

# Load IPCC column name mapping to short names #
row_name_map = module_dir + 'extra_data/ipcc_rows.csv'
row_name_map = pandas.read_csv(str(row_name_map))

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
    # Values found in excel cells #
    na_values  = ['IE', 'NE', 'NO', 'NO,NE', 'NE,NO', 'NE,IE']

    @property_cached
    def raw_table_4a(self):
        """Table4.A as is without any modifications."""
        # Load table #
        df = pandas.read_excel(str(self.xls_file),
                               sheet_name = 'Table4.A',
                               header     = None,
                               na_values  = self.na_values)
        # Return #
        return df

    @property_cached
    def headers(self):
        """Parse the column names of the excel sheet."""
        return Headers(self)

    @property_cached
    def last_row(self):
        """Look for the position of the first mostly empty row at the end of the table."""
        i = 0
        for i, row in self.raw_table_4a.iterrows():
            if i < 10: continue
            if row.iloc[0] == '.': break
        return i

    @property_cached
    def df(self):
        """
        Extract targeted information from 'Table4.A' into a pandas data frame.
        """
        # Take all lines after the header but before the last row #
        df = self.raw_table_4a.iloc[9:self.last_row]
        # Rename columns index #
        df.columns = self.headers.df
        # Go through `land_use` and `subcategory` removing the repetitions
        for i,row in df.iterrows():
            cat, subcat = row['land_use'], row['subdivision']
            if subcat is numpy.NaN: current_cat     = cat
            elif subcat != cat:     raise Exception("Cat. and subcat. should never differ.")
            else:                   row['land_use'] = current_cat
        # Rename rows #
        df['land_use'] = df['land_use'].update(row_name_map.set_index('ipcc'))
        # Convert units (such that we never have kilo hectares, only hectares etc.) #
        pass
        # Return #
        return df
