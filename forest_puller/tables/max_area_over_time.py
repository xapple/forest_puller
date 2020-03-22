#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.tables.max_area_over_time import max_area
    >>> print(max_area.df)

To export the table:

    >>> from forest_puller.tables.max_area_over_time import max_area
    >>> print(max_area.save())
"""

# Built-in modules #

# Internal modules #
from forest_puller        import cache_dir
from forest_puller.tables import Table
from forest_puller.common import country_codes

# First party modules #
from plumbing.cache  import property_cached

# Third party modules #
import pandas

###############################################################################
class MaxArea(Table):
    """
    Display, for each source, and for each country, the maximum forest area
    over time (usually this occurs in the last year of the dataset but not always).
    Data sources are displayed as different columns, and countries as rows.
    Values are in hectares.
    """

    # Parameters #
    short_name       = 'max_area'
    float_format_tex = 'split_thousands'

    # Extra formatting #
    upper_columns = True

    #----------------------------- Data sources ------------------------------#
    @property_cached
    def df(self):
        # Each source we want to include #
        source_names = ['ipcc', 'soef', 'faostat', 'hpffre', 'eu_cbm']
        # Import the data from the area graph #
        from forest_puller.viz.area import area_data
        # Put each dataframe in a list #
        dfs = [getattr(area_data, source) for source in source_names]
        # Function to group each one by country and do max on area #
        fn = lambda d: d.groupby('country').aggregate({'area': 'max'})
        # Apply that function to each source #
        dfs = [fn(df) for df in dfs]
        # Reset index #
        dfs = [df.reset_index() for df in dfs]
        # Rename the column to include the source #
        dfs = [df.rename(columns={'area': name}) for df, name in zip(dfs, source_names)]
        # Make a list of countries we want included #
        codes = [iso2 for iso2 in country_codes['iso2_code']]
        # Start with an empty dataframe #
        result = pandas.DataFrame(codes, columns=['country'])
        # Join each data source #
        for df in dfs: result = result.left_join(df, on='country')
        # Set the index #
        result = result.set_index('country')
        # Return #
        return result

###############################################################################
# Create a singleton #
export_dir = cache_dir + 'tables/'
max_area   = MaxArea(base_dir = export_dir)
