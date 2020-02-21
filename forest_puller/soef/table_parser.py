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
from forest_puller import cache_dir, module_dir
from forest_puller.common import convert_row_names

# First party modules #
from plumbing.cache import property_cached, property_pickled_at

# Third party modules #
import pandas, numpy

# Load column name mapping to short names #
col_name_map = module_dir + 'extra_data/soef_columns.csv'
col_name_map = pandas.read_csv(str(col_name_map))

# Load row name mapping to short names #
row_name_map = module_dir + 'extra_data/soef_rows.csv'
row_name_map = pandas.read_csv(str(row_name_map))

###############################################################################
class TableParser:
    """
    Is responsible for finding and parsing a table that is contained somewhere
    within an excel sheet. It will try to identify where the embedded table
    starts and where it ends. It will auto-detect the column headers too and
    return a correctly formatted pandas data frame.
    """

    sheet_name    = "" # Subclass these attributes
    title         = "" # Subclass these attributes
    short_name    = "" # Subclass these attributes
    header_len    = -1 # Subclass these attributes
    fixed_end_col = None
    fixed_end_row = None
    start_offset  = None

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
                                 header     = None,
                                 na_values  = ["n.a.", "n./a.", "n. a. "])

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
        # You can manually add an offset to this value in the attributes #
        offset = 0 if self.start_offset is None else self.start_offset
        # Get the first cell that matches the title #
        for i, row in self.full_sheet.iterrows():
            if row[0] == self.title: return i+1+offset
        self.raise_exception("Could not find the start row of the table.")

    @property_cached
    def end_row(self):
        """Determine where the table of interest ends within the sheet."""
        # You can manually override this in the attributes #
        if self.fixed_end_row is not None: return self.fixed_end_row
        # Get the first completely empty row #
        # that is within at least 3 rows after the header #
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
        # You can manually override this in the attributes #
        if self.fixed_end_col is not None: return self.fixed_end_col
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
        # Last row is always just NaNs #
        df = df[:-1].copy()
        # Fill from left to right (not top to bottom) #
        df = df.T.fillna(method='ffill').T
        # Remaining NaNs are uninteresting #
        df = df.fillna('')
        # Concatenate from top to bottom #
        df = list(' '.join(map(str,row.tolist())) for i, row in df.T.iterrows())
        # Remove any new lines #
        df = [col.replace("\n", " ").strip() for col in df]
        # Sometimes there is a useless space in '1 000' #
        df = [re.sub('1 000', '1000', col) for col in df]
        # Apply custom fixes if one is specified #
        df = self.header_fix(df)
        # Rename the fields to their short-version #
        before = list(col_name_map['soef'])
        after  = list(col_name_map['forest_puller'])
        df     = pandas.Series(df).replace(before, after)
        # Sometimes we get years in the columns #
        df = df.apply(pandas.to_numeric, errors='ignore', downcast='integer')
        # Return #
        return df

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

    @property_pickled_at('df_cache_path')
    def df(self):
        """Return the table of interest correctly parsed and formatted."""
        # Load #
        df = self.merged_category
        # Add columns #
        df.columns = self.header
        # Convert to short headers using col_name_map #
        df = convert_row_names(df, row_name_map, col_name_map, 'soef')
        # The year column should be cast to integer #
        if 'year' in df.columns: df['year'] = pandas.to_numeric(df['year'])
        # Return #
        return df

    @property
    def indexed(self):
        """Same as `self.df` but with an index on the first columns."""
        return self.df.set_index(['category'])

    @property
    def country_cols(self):
        """Same as `self.df` but we add a column with the current country (e.g. 'AT')."""
        # Load #
        df = self.df.copy()
        # Add column #
        df.insert(0, 'country', self.country.iso2_code)
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
    def header_fix(self, df): return df

###############################################################################
class ForestArea(TableParser):

    sheet_name    = "1.1"
    title         = "Table 1.1a: Forest area"
    short_name    = "forest_area"
    header_len    = 2
    fixed_end_col = 3

#-----------------------------------------------------------------------------#
class AgeDist(TableParser):

    sheet_name    = "1.3a"
    title         = "Table 1.3a1: Age class distribution (area of even-aged stands)"
    short_name    = "age_dist"
    header_len    = 3
    fixed_end_col = 7
    fixed_end_row = 30

    def header_fix(self, df):
        """Fix some inconsistencies that are non-concordant between countries."""
        # Fix the second element to be standardized #
        df[2] = "Total area (1000 ha)"
        # Return #
        return df

#-----------------------------------------------------------------------------#
class Fellings(TableParser):

    sheet_name    = "3.1"
    title         = "Table 3.1: Increment and fellings"
    short_name    = "fellings"
    header_len    = 4
    fixed_end_col = 7
    fixed_end_row = 15