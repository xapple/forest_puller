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
        """
        Special parsing for the table of growing_stock as years are now columns.
        The units are specified in million m³ over bark.
        """
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
        df = df.melt(id_vars    = ['rank', 'latin_name', 'common_name'],
                     var_name   = 'year',
                     value_name = 'growing_stock')
        # Make numeric #
        df['growing_stock'] = df['growing_stock'].apply(pandas.to_numeric, errors="coerce", downcast='float')
        # Turn into cubic meters, not millions of cubic meters #
        df['growing_stock'] = df['growing_stock'] * 1e6
        # Remove empty values #
        df = df.query("growing_stock==growing_stock").copy()
        # Sanitize names #
        df.iloc[:,0:2] = df.iloc[:,0:2].applymap(self.sanitize)
        # Sanitize the rank column #
        df['rank'] = df['rank'].apply(self.sanitize_rank)
        # Return #
        return df

    def sanitize(self, text):
        # Eliminate trailing spaces #
        text = text.strip(' ,')
        # Eliminate newlines #
        text = text.replace('\n', ' ')
        # Return #
        return text

    def sanitize_rank(self, text):
        if text[0].isnumeric():
            return int(text[:-2])
        else:
            return text

    @property
    def indexed(self):
        """Same as `self.df` but with an index on the first columns."""
        return self.df.set_index(['rank', 'year'])
