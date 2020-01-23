#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas, numpy

###############################################################################
class TableParser:
    """
    Is responsible for finding and parsing a table that is contained somewhere
    within an excel sheet. It will try to identify where the embedded table
    starts and where it ends. It will auto-detect the column headers too and
    return a correctly formatted pandas data frame.
    """

    sheet_name = "" # Subclass these attributes
    title      = "" # Subclass these attributes
    short_name = "" # Subclass these attributes
    header_len = -1 # Subclass these attributes

    def __init__(self, country):
        # Save the parent #
        self.country = country
        # Convenience short cuts #
        self.xls_file  = self.country.xls_file
        self.iso2_code = self.country.iso2_code

    @property_cached
    def full_sheet(self):
        """Return the full sheet containing one or several tables."""
        return pandas.read_excel(str(self.xls_file),
                                 sheet_name = self.sheet_name,
                                 header     = None)

    def raise_exception(self, message):
        """Print a nice message for when we need to raise an exception."""
        message += "\n Table title '%s' of sheet '%s' of country '%s'"
        message  = message % (self.title, self.sheet_name, self.iso2_code)
        message += "\n The exact file is location at: '%s'"
        message  = message % self.xls_file
        raise Exception(message)

    #------------------------------- Location --------------------------------#
    @property_cached
    def start_row(self):
        """Determine where the table of interest starts within the sheet."""
        # Get the first cell that matches the title #
        for i, row in self.full_sheet.iterrows():
            if row[0] == self.title: return i+1
        self.raise_exception("Could not find the start row of the table.")

    @property_cached
    def end_row(self):
        """Determine where the table of interest ends within the sheet."""
        # Get the first completely empty row #
        # Within at least 3 rows after the header #
        for i, row in self.full_sheet.iterrows():
            if i <= self.start_row + 3:       continue
            if all(row.fillna(-999) == -999): return i
        self.raise_exception("Could not find the end row of the table.")

    @property
    def start_col(self):
        """Determine where the table of interest starts within the sheet."""
        return 0

    @property_cached
    def end_col(self):
        """Determine where the table of interest ends within the sheet."""
        # Find the first completely empty column #
        df = self.full_sheet.iloc[self.start_row:self.end_row]
        for i, name in enumerate(df.columns):
            column = df[name]
            if all(column.fillna(-999) == -999): return i
        return len(df.columns)

    @property_cached
    def cropped_sheet(self):
        """Returns a slice of the full sheet based on start and end rows."""
        # Load #
        df = self.full_sheet
        # Make a sub-sheet #
        df = df.iloc[self.start_row:self.end_row, self.start_col:self.end_col]
        # Return #
        return df

    #--------------------------------- Main ----------------------------------#
    @property_cached
    def header(self):
        """Return the column names for the final data frame."""
        # Load only the first few rows #
        df = self.cropped_sheet.iloc[0:self.header_len]
        # Last row is just NaNs #
        df = df[:-1].copy()
        # Fill from left to right (not top to bottom) #
        df = df.T.fillna(method='ffill').T
        # Remaining NaNs are uninteresting #
        df = df.fillna('')
        # Concatenate from top to bottom #
        return pandas.Series(' '.join(row.tolist()) for i, row in df.T.iterrows())

    @property_cached
    def merged_category(self):
        """Category should be merged with all cells for every group of years."""
        # Load but skip the header #
        df = self.cropped_sheet.iloc[self.header_len:].copy()
        # Reset index #
        df = df.reset_index(drop=True)
        # Initialize #
        seen  = set()
        start = 0
        text  = ""
        # Loop #
        for i, row in df.iterrows():
            # Parse new row #
            cat = row.iloc[0]
            val = row.iloc[1]
            # Have we hit a new category? #
            if val in seen:
                df.iloc[start:i, 0] = text
                seen  = set()
                start = i+1
                text  = ""
            # Accumulate category text #
            if cat is not numpy.nan: text += str(cat)
            # Add value to seen #
            seen.add(val)
        # Last group #
        df.iloc[start:, 0] = text
        # Return #
        return df

    #@property_pickled_at('df_cache_path')
    @property
    def df(self):
        """Return the table of interest correctly parsed and formatted."""
        # Load #
        df = self.merged_category
        # Add columns #
        df.columns = self.header
        # Return #
        return df

    #--------------------------------- Cache ---------------------------------#
    @property
    def df_cache_path(self):
        """Specify where on the file system we will pickle the df property."""
        path  = cache_dir + 'soef/df/' + self.country.iso2_code + '/'
        path += self.short_name + '.pickle'
        return path

    #--------------------------- Helper methods ------------------------------#

###############################################################################
class ForestArea(TableParser):
    """
    This table is interesting because blah blah.
    """

    sheet_name = "1.1"
    title = "Table 1.1a: Forest area"
    short_name = "forest_area"
    header_len = 2

#-----------------------------------------------------------------------------#
class AgeDist(TableParser):
    """
    This table is interesting because blah blah.
    """

    sheet_name = "1.3a"
    title = "Table 1.3a1: Age class distribution (area of even-aged stands)"
    short_name = "age_dist"
    header_len = 3

#-----------------------------------------------------------------------------#
class Fellings(TableParser):
    """
    This table is interesting because blah blah.
    """

    sheet_name = "3.1"
    title = "Table 3.1: Increment and fellings"
    short_name = "fellings"
    header_len = 4
