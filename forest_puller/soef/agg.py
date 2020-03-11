#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.faostat.land.agg import source
    >>> print(source.common_years)
"""

# Built-in modules #

# Internal modules #

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas

###############################################################################
class AggSOEF:
    """
    Represents one data source and contains all countries for that
    particular data source.
    """

    def __getitem__(self, key): return [c for c in self.countries if c.iso2_code == key][0]

    def __iter__(self): return iter(self.countries)

    def __len__(self):  return len(self.countries)

    def __init__(self):
        pass

    @property
    def countries(self):
        from forest_puller.soef.country import countries
        return countries

    @property
    def first(self):
        return self.countries[0]

    #----------------------------- Common years ------------------------------#
    @property_cached
    def common_years(self):
        """
        Determine the years for which there is a data point in every single
        country of this data source.
        Return a list of integers, e.g. [1999, 2000, 2001, 2004].
        """
        # Initialize #
        table_names = ["forest_area", "age_dist", "fellings"]
        tables      = {}
        # Loop #
        for table_name in table_names:
            all_tables  = (getattr(c, table_name) for c in self.countries.values())
            avail_years = (set(t.df['year']) for t in all_tables)
            years       = sorted(list(set.intersection(*avail_years)))
            tables[table_name] = years
        # Return #
        return tables

    #-------------------------------- Tables ---------------------------------#
    @property_cached
    def forest_area(self):
        # Import #
        from forest_puller.soef.concat import tables
        # Load #
        df = tables['forest_area'].copy()
        # Get the common years #
        common_years = self.common_years['forest_area']
        # Filter #
        df = df.query("year in @common_years")
        # This only works for the 'forest_area' table #
        df = df.query("category == 'forest'")
        # Check there are no NaNs #
        assert not df.isna().any().any()
        # Keep only two columns #
        df = df[['year', 'area']]
        # Sum the countries and keep the years #
        df = df.groupby(['year']).agg({'area': 'sum'})
        # We don't want the year as an index #
        df = df.reset_index()
        # Return #
        return df

###############################################################################
source = AggSOEF()