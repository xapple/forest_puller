#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller.soef.table_parser import TableParser

# First party modules #
from plumbing.cache import property_cached, property_pickled_at

# Third party modules #
import pandas

###############################################################################
class AreaByType(TableParser):

    sheet_name    = "1.1"
    title         = "Table 1.1b: Forest area by forest types"
    short_name    = "area_by_type"
    header_len    = 3
    fixed_end_col = 5

    @property_cached
    def end_row(self):
        return self.start_row + 6

    @property_cached
    def header(self):
        """Return the years as integers."""
        # Load only the first few rows #
        df = self.cropped_sheet.iloc[0:self.header_len]
        # Last row is always just NaNs #
        df = df[1:-1].copy()
        # Sometimes we get years in the columns #
        df = df.apply(pandas.to_numeric, errors='ignore', downcast='integer')
        # Make as list #
        df = list(df.iloc[0])
        # Dropped category #
        df[0] = 'category'
        # Return #
        return df

    @property_pickled_at('df_cache_path')
    def df(self):
        """
        Special parsing, as the years are columns here.
        """
        # Load but skip the header #
        df = self.cropped_sheet.iloc[self.header_len:].copy()
        # Reset index #
        df = df.reset_index(drop=True)
        # Add columns #
        df.columns = self.header
        # Melt #
        df = df.melt(id_vars    = ['category'],
                     var_name   = 'year',
                     value_name = 'area')
        # Make the year numeric #
        df['year'] = df['year'].astype('int')
        # Make the area a float #
        df['area'] = df['area'].astype('float')
        # Make the area in hectares #
        df['area'] = df['area'] * 1000
        # Rename the rows #
        replacements = (('Predominantly coniferous forest',   'con'),
                        ('Predominantly broadleaved forest',  'broad'),
                        ('Mixed forest',                      'mixed'))
        # Rename all items (see docstring) #
        for orig, dest in replacements:
            df['category'] = df['category'].replace(to_replace = orig,
                                                    value      = dest)
        # Return #
        return df
