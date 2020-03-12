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

###############################################################################
class FaostatLandAgg:
    """
    Represents one data source and contains all countries for that
    particular data source. In this case faostat land.
    """

    def __getitem__(self, key): return [c for c in self.countries if c.iso2_code == key][0]

    def __iter__(self): return iter(self.countries)

    def __len__(self):  return len(self.countries)

    def __init__(self):
        pass

    @property
    def countries(self):
        from forest_puller.faostat.land.country import countries
        return countries

    @property
    def first(self):
        return self.countries[0]

    #----------------------------- Common years ------------------------------#
    @property_cached
    def common_years_area(self):
        """
        Determine the years for which there is a data point in every single
        country of this data source for the area statistic.
        Return a list of integers, e.g. [1999, 2000, 2001, 2004].
        """
        # Every country's available years #
        avail_years = (set(c.area_years) for c in self.countries.values())
        # Intersection of all country's years #
        years = set.intersection(*avail_years)
        # Convert to a list #
        years = sorted(list(years))
        # Return #
        return years

    #-------------------------------- Tables ---------------------------------#
    @property_cached
    def forest_area(self):
        # Import #
        import forest_puller.faostat.land.concat
        # Load #
        df = forest_puller.faostat.land.concat.df.copy()
        # Filter years #
        df = df.query("year in @self.common_years_area")
        # Filter #
        df = df.query('element == "Area"')
        df = df.query('item    == "Forest land"')
        df = df.query('flag    == "A"')
        # The value now is the area #
        df = df.rename(columns={'value': 'area'})
        # Keep only two columns #
        df = df[['year', 'area']]
        # Check there are no NaNs #
        assert not df.isna().any().any()
        # Sum the countries and keep the years #
        df = df.groupby(['year']).agg({'area': 'sum'})
        # We don't want the year as an index #
        df = df.reset_index()
        # Return #
        return df

###############################################################################
source = FaostatLandAgg()