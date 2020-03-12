#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.faostat.forestry.country import all_countries
    >>> print([(c.df_cache_path, c.df_cache_path.exists) for c in all_countries])
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir
from forest_puller.faostat.land.zip_file import zip_file
from forest_puller.common import country_codes

# First party modules #
from plumbing.cache import property_pickled_at

# Third party modules #

###############################################################################
class Country:
    """Represents one country's dataset."""

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
        return cache_dir + 'faostat/land/' + self.iso2_code + '.pickle'

    #----------------------------- Common years ------------------------------#
    @property
    def area_years(self):
        """
        Determine the years for which there is a data point for
        the area statistic in this country.
        Return a list of integers, e.g. [1999, 2000, 2001, 2004].
        """
        # Load #
        df = self.df
        # Filter #
        df = df.query('element == "Area"')
        df = df.query('item    == "Forest land"')
        df = df.query('flag    == "A"')
        # Process #
        years = df['year'].unique()
        # Return #
        return years

###############################################################################
# Create every country object #
all_countries = [Country(iso2) for iso2 in country_codes['iso2_code']]
countries     = {c.iso2_code: c for c in all_countries}
