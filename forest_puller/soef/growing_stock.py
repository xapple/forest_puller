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

###############################################################################
class GrowingStockComp(TableParser):

    sheet_name    = "1.2"
    title         = "Table 1.2c: Growing stock composition"
    short_name    = "stock_comp"
    header_len    = 2
    fixed_end_col = 7
    start_offset  = 1

    @property_cached
    def end_row(self):
        for i, row in self.full_sheet.iterrows():
            if i <= self.start_row + 3:         continue
            if row.iloc[0].startswith("Note:"): return i
        self.raise_exception("Could not find the end row of the table.")

    @property_pickled_at('df_cache_path')
    def df(self):
        """Return the table of interest correctly parsed and formatted."""
        # Load but skip the header #
        df = self.cropped_sheet.iloc[self.header_len:].copy()
        # Reset index #
        df = df.reset_index(drop=True)
        # Add columns #
        df.columns = self.header
        # Last row 'remaining' and 'total' #
        df.iloc[-1, 0:3] = 'total'
        df.iloc[-2, 0:3] = 'remaining'
        # Melt #
        df = df.melt(id_vars    = ['rank', 'species', 'common_name'],
                     var_name   = 'year',
                     value_name = 'growing_stock')
        # Remove empty values #
        df = df.query("growing_stock==growing_stock").copy()
        # Sanitize names #
        df.iloc[:,0:2] = df.iloc[:,0:2].applymap(self.sanitize)
        # Return #
        return df

    def sanitize(self, text):
        # Load #
        result = text
        # Eliminate trailing spaces #
        result = result.strip(' ,')
        # Eliminate newlines #
        result = result.replace('\n', ' ')
        # Return #
        return result
