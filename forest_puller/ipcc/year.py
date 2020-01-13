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
    """

    def __init__(self, country, xls_file):
        # The parent country #
        self.country = country
        # The file that contains data for this year #
        self.xls_file = xls_file
        # The year itself from the file name #
        self.year = int(re.findall("^[A-Z]+_[0-9]+_([0-9]+)", xls_file.name)[0])

    def __repr__(self):
        return '%s %s of %s' % (self.__class__, self.year, self.country.iso2_code)

    # ------------------------------- Other ----------------------------------#
    @property_cached
    def raw_table_4a(self):
        """Table4.A without any modifications."""
        # Load table #
        df = pandas.read_excel(str(self.xls_file),
                               sheet_name = 'Table4.A',
                               header     = None,
                               na_values  = ['IE', 'NE', 'NO', 'NO,NE'])
        # Return #
        return df

    @property_cached
    def header(self):
        """
        Parameters for the position of rows used for the header.
        It is zero-indexed (i.e. offset of one compared to the
        GUI excel row numbers)
        """
        # Position #
        begin_head = 4
        end_head   = 9
        header     = self.raw_table_4a.iloc[begin_head:end_head]
        # Fill values #
        header = header.fillna(method='ffill')
        header = header.reset_index(drop=True)
        # Add information on per area columns in t C /ha
        # so they have different name than the kt C columns
        header.iloc[3, 5:12] = header.iloc[3,5:12] + '_per_area'
        # Convert to short headers
        # Check column names for the reason why this doesn't work properly
        header = header.iloc[3].replace(list(col_name_map['ipcc']),
                                        list(col_name_map['forest_puller']))
        # Return #
        return header

    @property_cached
    def df(self):
        """Extract targeted information from 'Table4.A' into a pandas data frame."""
        # Extract table body
        # Look for the position of the first mostly empty row
        # at the end of the table in order to remove all links after that
        selector = self.raw_table_4a.isnull().sum(axis=1) > 18
        selector[0:end_head] = False
        selector = selector.cumsum() == 0
        last_row = max(selector.index[selector])
        df       = self.raw_table_4a.iloc[end_head+1:last_row+1]
        # Rename columns #
        df.columns = self.header
        # Return #
        return df
