#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

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
class Headers:
    """
    Represents a specific list of column names for a given excel file.
    """

    def __init__(self, year):
        """
        Record the parent.
        """
        # The parent year #
        self.year = year

    def __repr__(self):
        return '%s of %s' % (self.__class__, self.year)

    # Here the numbers are parameters for the position of rows used for
    # the header. It is zero-indexed (i.e. offset of one compared to the
    # GUI excel row numbers)
    begin = 4
    end   = 9

    @property_cached
    def df(self):
        """
        Typically the result is something like:

            <class 'pandas.core.series.Series'>
            0                   land_use
            1                subdivision
            2                       area
            3               area_mineral
            4               area_organic
            5                gains_ratio
            6               losses_ratio
            [...]
        """
        # Raw header #
        df = self.year.raw_table_4a.iloc[self.begin:self.end]
        # Fill values, all NaNs become what is north of them #
        df = df.fillna(method='ffill')
        # Remove the index #
        df = df.reset_index(drop=True)
        # Take the fourth row (i.e. row no. 8 in excel GUI) #
        df = df.iloc[3]
        # Remove the name of the headers is 3 because of the original parsing #
        df.index.name = None
        # Remove all newlines #
        df = df.replace('\n', ' ', regex=True)
        # Add '_per_area' to the columns that are already divided
        # so we can distinguish them from the columns with carbon
        df.iloc[5:12] = df.iloc[5:12] + '_per_area'
        # Convert to short headers using col_name_map
        before = list(col_name_map['ipcc'])
        after  = list(col_name_map['forest_puller'])
        df     = df.replace(before, after)
        # Return #
        return df

