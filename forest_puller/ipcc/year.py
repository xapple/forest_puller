#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import re

# Internal modules #
from forest_puller.ipcc.headers import Headers
from forest_puller import cache_dir, module_dir

# First party modules #
from plumbing.cache import property_cached, property_pickled_at

# Third party modules #
import pandas, numpy

# Load IPCC row and column names mapping to short names #
col_name_map = module_dir + 'extra_data/ipcc_columns.csv'
col_name_map = pandas.read_csv(str(col_name_map))

# Load row name mapping to short names #
row_name_map = module_dir + 'extra_data/ipcc_rows.csv'
row_name_map = pandas.read_csv(str(row_name_map))

##############################################################################
class Year:
    """
    Represents a specific year from a specific country's dataset and gives
    access to all the data of that year.

        The final file structure will look like this:

        /puller_cache/ipcc/df/AT:
            1990.pickle
            1991.pickle
            1992.pickle
            1993.pickle
            1994.pickle
            ...

        /puller_cache/ipcc/df/BE:
            1990.pickle
            1991.pickle
            1992.pickle
            ...
    """

    def __init__(self, country, xls_file):
        """Record the parent and the file we have to parse."""
        # The parent country #
        self.country = country
        # The file that contains data for this year #
        self.xls_file = xls_file
        # The year itself from the file name #
        self.year = int(re.findall("^[A-Z]+_[0-9]+_([0-9]+)", xls_file.name)[0])

    def __repr__(self):
        return '%s %s of %s' % (self.__class__, self.year, self.country.iso2_code)

    # ---------------------------- Properties --------------------------------#
    # Values found in excel cells #
    na_values  = [
        'IE',    'NE',    'NO',
                 'IE,NE', 'IE,NO', 'IE,NA',
        'NE,IE',          'NE,NO',
        'NO,IE', 'NO,NE',          'NO,NA',
        'NA,NO',
        'NE,NA,NO', 'NO,IE,NA', 'NO,NE,NA', 'NE,NO,IE'
    ]

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
        """Look for the position of the first row that contains a period as only
        content."""
        i = 0
        for i, row in self.raw_table_4a.iterrows():
            if i < 10: continue
            if row.iloc[0] == '.': break
        return i

    @property_pickled_at('df_cache_path')
    def df(self):
        """Extract targeted information from 'Table4.A' into a pandas data frame."""
        # Take all lines after the header but before the last row #
        df = self.raw_table_4a.iloc[9:self.last_row]
        # Rename columns index #
        df.columns = self.headers.df
        # Go through `land_use` and `subcategory` removing the repetitions #
        for i,row in df.iterrows():
            cat, subcat = row['land_use'], row['subdivision']
            if subcat is numpy.NaN: current_cat     = cat
            elif subcat != cat:     raise Exception("Cat. and subcat. should never differ.")
            else:                   row['land_use'] = current_cat
        # Convert to short titles using row_name_map #
        before = list(row_name_map['ipcc'])
        after  = list(row_name_map['forest_puller'])
        df     = df.replace(before, after)
        # Convert units (such that we never have kilo hectares, only hectares etc.) #
        for i, row in col_name_map.iterrows():
            col_name, ratio = row['forest_puller'], row['unit_convert_ratio']
            if numpy.isnan(ratio): continue
            if df[col_name].dtype != 'float64': raise Exception("Non-float in the df.")
            df[col_name] = df[col_name] * ratio
        # Reset the index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property_cached
    def df_cache_path(self):
        """Specify where on the file system we will pickle the df property."""
        path  = cache_dir + 'ipcc/df/' + self.country.iso2_code + '/'
        path += str(self.year) + '.pickle'
        return path

    @property_cached
    def indexed(self):
        """
        Same as `self.df` but with an index on the first and second columns.
        Also we put empty strings instead of NaNs in the subdivision column.
        """
        # Load #
        df = self.df.copy()
        # Empty string #
        df['subdivision'] = df['subdivision'].fillna('')
        # Index #
        df = df.set_index(['land_use', 'subdivision'])
        # Return #
        return df

    @property
    def year_country_cols(self):
        """
        Same as `self.df` but we add a column with the current year (e.g. 1990)
        and a column with the current country (e.g. 'AT').
        """
        # Load #
        df = self.df.copy()
        # Add columns #
        df.insert(0, 'year',    self.year)
        df.insert(0, 'country', self.country.iso2_code)
        # Return #
        return df

    # ------------------------------ Methods ---------------------------------#
    def sanity_check(self):
        """Recompute the total row to check that everything adds up."""
        # Load table and set index #
        df = self.df.set_index('land_use')
        # Drop the per area columns which can't be summed #
        df = df.loc[:, ~df.columns.str.endswith('_ratio')]
        # Get the totals row #
        expected = df.loc['total_forest'].fillna(0.0)
        # Remove that very same total rows from the df #
        df = df.drop('total_forest')
        # Sum every subdivison's total (where there are NaNs) #
        df = df[pandas.isna(df['subdivision'])]
        # But not the converted recap total which is redundant #
        df = df.drop('land_to_forest')
        # Recompute the totals #
        totals = df.sum()
        # Compare #
        all_close = numpy.testing.assert_allclose
        all_close(expected, totals, rtol=1e-10)
        # Return #
        return True
