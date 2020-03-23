#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from plumbing.common import camel_to_snake

# First party modules #
from autopaths           import Path
from autopaths.file_path import FilePath
from plumbing.cache      import property_cached

# Third party modules #
import numpy

###############################################################################
class Table:
    """
    A table with different headers and values that is destined to be
    exported both to CSV and to TeX format, for instance for display in
    publications or manuscripts.
    """

    # Default options #
    formats      = ('csv', 'tex')
    index        = True
    bold_rows    = True
    na_rep       = '-'

    # Float formatting #
    float_format_csv = '%g'
    float_format_tex = '%g'

    # Extra formatting #
    capital_index = True
    upper_columns = False
    column_format = None
    escape_tex    = True

    def __init__(self, parent=None, base_dir=None, short_name=None):
        # Save parent if it was given #
        self.parent = parent
        # If we got a file #
        if isinstance(base_dir, FilePath):
            self.base_dir = base_dir.directory
            short_name    = base_dir.short_prefix
        else:
            self.base_dir = Path(base_dir)
        # Short name #
        if short_name: self.short_name = short_name
        # Use the parents name or the base class name #
        if not hasattr(self, 'short_name'):
            if hasattr(self.parent, 'short_name'):
                self.short_name = self.parent.short_name
            else:
                self.short_name = camel_to_snake(self.__class__.__name__)

    @property_cached
    def path(self):
        return Path(self.base_dir + self.short_name + '.tex')

    @property
    def csv_path(self): return self.path.replace_extension('csv')

    #-------------------------------- Other ----------------------------------#
    def split_thousands(self, number):
        """This method will determine how numbers are displayed in the table."""
        # Case is NaN #
        if numpy.isnan(number): return self.na_rep
        # Round #
        number = int(round(number))
        # Format #
        from plumbing.common import split_thousands
        number = split_thousands(number)
        # Return #
        return number

    def make_percent(self, row):
        # Remember where the NaNs are located #
        nans = row.isna()
        # Multiply for percentage #
        row *= 100
        # Express difference as a percentage #
        row = row.apply(lambda f: "%.1f%%" % f)
        # Restore NaNs #
        row[nans] = self.na_rep
        # Return #
        return row

    #--------------------------------- Save ----------------------------------#
    def save(self, **kw):
        # Load #
        df = self.df.copy()
        # Modify the index name#
        if self.capital_index and df.index.name is not None:
            df.index.name = df.index.name.capitalize()
        # Modify column names #
        if self.upper_columns: df.columns = df.columns.str.upper()
        # Possibility to overwrite path #
        if 'path' in kw: path = FilePath(kw['path'])
        else:            path = self.path
        # Special cases for float formatting #
        if self.float_format_tex == 'split_thousands':
            self.float_format_tex = self.split_thousands
        # Make sure the directory exists #
        self.base_dir.create_if_not_exists()
        # Latex version #
        if 'tex' in self.formats:
            df.to_latex(str(path),
                        float_format  = self.float_format_tex,
                        na_rep        = self.na_rep,
                        index         = self.index,
                        bold_rows     = self.bold_rows,
                        column_format = self.column_format,
                        escape        = self.escape_tex)
        # CSV version (plain text) #
        if 'csv' in self.formats:
            path = path.replace_extension('csv')
            df.to_csv(str(path),
                      float_format = self.float_format_csv,
                      index        = self.index)
        # Return the path #
        return path