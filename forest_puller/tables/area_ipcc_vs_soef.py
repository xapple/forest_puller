#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.tables.area_ipcc_vs_soef import soef_vs_ipcc
    >>> print(soef_vs_ipcc.df)

To export the table:

    >>> from forest_puller.tables.area_ipcc_vs_soef import soef_vs_ipcc
    >>> print(soef_vs_ipcc.save())
"""

# Built-in modules #

# Internal modules #
from forest_puller        import cache_dir
from forest_puller.tables import Table

# First party modules #
from plumbing.cache  import property_cached

# Third party modules #

###############################################################################
class AreaSoefIpcc(Table):
    """
    Display the maximum forest area over time for IPCC and SOEF sources only.
    Add an extra column `diff_percent` defined as:

        (ipcc_area - soef_area) / soef_area * 100

    Sort the table by the `diff_percent` column.
    Values are in hectares.
    """

    # Parameters #
    short_name       = 'area_ipcc_vs_soef'
    float_format_tex = 'split_thousands'

    # Extra formatting #
    column_format = 'lrrr'

    #----------------------------- Data sources ------------------------------#
    @property_cached
    def df(self):
        # Import the data from the max_area table #
        from forest_puller.tables.max_area_over_time import max_area
        # Load #
        df = max_area.df.copy()
        # Filter columns #
        df = df[['ipcc', 'soef']]
        # Add extra column #
        df['difference'] = (df['ipcc'] - df['soef']) / df['soef']
        # Sort #
        df = df.sort_values('difference', ascending=False)
        # Express difference as a percentage #
        df['difference'] = self.make_percent(df['difference'])
        # Rename columns #
        df = df.rename(columns={'ipcc': 'IPCC', 'soef': 'SOEF'})
        # Return #
        return df

###############################################################################
# Create a singleton #
export_dir   = cache_dir + 'tables/'
soef_vs_ipcc = AreaSoefIpcc(base_dir = export_dir)
