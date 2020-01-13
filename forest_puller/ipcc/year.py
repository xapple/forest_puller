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
from forest_puller import module_dir

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas

# Load IPCC column name mapping to short names #
col_name_map = module_dir + 'extra_data/ipcc_columns.csv'
col_name_map = pandas.read_csv(str(col_name_map))

###############################################################################
class Year:
    """
    Represents a specific year from a specific country's dataset.

    Here the numbers are parameters for the position of rows used for
    the header. It is zero-indexed (i.e. offset of one compared to the
    GUI excel row numbers)
    """

    begin_head = 4
    end_head   = 9

    def __init__(self, country, xls_file):
        """
        Record the parent and the file we have to parse.
        """
        # The parent country #
        self.country = country
        # The file that contains data for this year #
        self.xls_file = xls_file
        # The year itself from the file name #
        self.year = int(re.findall("^[A-Z]+_[0-9]+_([0-9]+)", xls_file.name)[0])
        # Position #

    def __repr__(self):
        return '%s %s of %s' % (self.__class__, self.year, self.country.iso2_code)

    # ------------------------------- Other ----------------------------------#
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
    def column_names(self):
        # Raw header #
        df = self.raw_table_4a.iloc[self.begin_head:self.end_head]
        # Fill values #
        df = df.fillna(method='ffill')
        df = df.reset_index(drop=True)
        # Add information on per area columns in t C /ha
        # so they have different name than the kt C columns
        df.iloc[3, 5:12] = df.iloc[3,5:12] + '_per_area'
        # Convert to short headers
        # Check column names for the reason why this doesn't work properly
        df = df.iloc[3].replace(list(col_name_map['ipcc']),
                                list(col_name_map['forest_puller']))
        # Return #
        return df

    @property_cached
    def df(self):
        """Extract targeted information from 'Table4.A' into a pandas data frame."""
        # Look for the position of the first mostly empty row
        # at the end of the table
        selector = self.raw_table_4a.isnull().sum(axis=1) > 18
        selector[0:self.end_head] = False
        selector = selector.cumsum() == 0
        last_row = max(selector.index[selector])
        # Take all lines after the header but before the last row #
        df = self.raw_table_4a.iloc[self.end_head + 1:last_row + 1]
        # Rename columns index #
        df.columns = self.column_names
        # Return #
        return df
