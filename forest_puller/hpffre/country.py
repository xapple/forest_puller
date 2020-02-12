#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.hpffre.country import all_countries
    >>> print([(c.df_cache_path, c.df_cache_path.exists) for c in all_countries])
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir, module_dir
from forest_puller.hpffre.zip_file import zip_file
from forest_puller.common import convert_units
from forest_puller.common import country_codes

# First party modules #
from plumbing.cache import property_pickled_at

# Third party modules #
import pandas

# Load column name mapping to short names #
col_name_map = module_dir + 'extra_data/hpffre_columns.csv'
col_name_map = pandas.read_csv(str(col_name_map))

###############################################################################
class Country:
    """Represents one country's dataset.

    From the excel file of dataset:

    * _Growing stock_: Total stemwood volume measured over bark. Stemwood = Part of tree
      stem from the felling cut to the tree top with the branches removed, including bark.
    * _Fellings_: Total stemwood volume of trees felled in thinnings, selection or final cuttings.
    """

    def __init__(self, iso2_code):
        # The reference ISO2 code #
        self.iso2_code = iso2_code

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

    @property_pickled_at('df_cache_path')
    def df(self):
        """Return rows that concern this country."""
        # Load #
        df = zip_file.df
        # Select rows for country #
        selector = df['country'] == self.iso2_code
        df       = df[selector]
        # We don't need the country column anymore #
        df = df.drop(columns=['country'])
        # We don't need the old index anymore #
        df = df.reset_index(drop=True)
        # Convert the units using col_name_map #
        df = convert_units(df, col_name_map)
        # Return #
        return df

    @property
    def country_cols(self):
        """Same as `self.df` but we add a column with the current country (e.g. 'AT')."""
        # Load #
        df = self.df.copy()
        # Add column #
        df.insert(0, 'country', self.iso2_code)
        # Return #
        return df

    #--------------------------------- Cache ---------------------------------#
    @property
    def df_cache_path(self):
        """Specify where on the file system we will pickle the df property."""
        return cache_dir + 'hpffre/df/' + self.iso2_code + '.pickle'

###############################################################################
# Create every country object #
missing       = ['BG', 'LU', 'HR', 'GR', 'PL', 'NL']
all_codes     = [iso2 for iso2 in country_codes['iso2_code'] if iso2 not in missing]
all_countries = [Country(iso2) for iso2 in all_codes]
countries     = {c.iso2_code: c for c in all_countries}
