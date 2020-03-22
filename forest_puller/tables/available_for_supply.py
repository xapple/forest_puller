#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.tables.available_for_supply import afws_comp
    >>> print(afws_comp.df)

To export the table:

    >>> from forest_puller.tables.available_for_supply import afws_comp
    >>> print(afws_comp.save())
"""

# Built-in modules #

# Internal modules #
from forest_puller        import cache_dir
from forest_puller.tables import Table

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas

###############################################################################
class AvailableForSupply(Table):
    """
    Creates a table that shows the total area for each country along with the
    proportion of that area which is "available for wood supply", for each given
    source that has this information (SOEF, HPFFRE), and for the year 2015.

    * For HPFFRE, the "FAWS" is compared to the sum of FAWS, FNAWS, FRAWS.
      NaNs are replaced by zero.

    * For SOEF, we add a column:     prop_aws = area_aws / forest_area
    """

    # Parameters #
    short_name    = 'avail_for_supply'
    column_format = 'lrrr'

    #----------------------------- Data sources ------------------------------#
    @property_cached
    def soef(self):
        # Import #
        import forest_puller.soef.concat
        # Load #
        df = forest_puller.soef.concat.tables['forest_area'].copy()
        # Filter year #
        df = df.query("year == 2015")
        # Filter category #
        df = df.query("category == 'forest' or category=='forest_avail_for_supply'")
        # Columns #
        df = df[['country', 'category', 'area']]
        # Pivot #
        df = df.pipe(pandas.pivot_table,
                     index   = ['country'],
                     columns = ['category'],
                     values  = 'area')
        # Calculate ratio #
        df['avail_ratio'] = df['forest_avail_for_supply'] / df['forest']
        # Return #
        return df

    @property_cached
    def hpffre(self):
        # Import #
        import forest_puller.hpffre.concat
        # Load #
        df = forest_puller.hpffre.concat.df.copy()
        # Filter for only the first scenario #
        df = df.query("scenario == 1")
        # Filter year #
        df = df.query("year == 2015")
        # Columns #
        df = df[['country', 'category', 'area']]
        # Split total and available for wood supply #
        total = df.groupby(['country']).agg({'area': 'sum'})
        avail = df.query("category == 'FAWS'").set_index('country')[['area']]
        # Reset all indexes #
        total = total.reset_index()
        avail = avail.reset_index()
        # Rename column #
        total = total.rename(columns={'area': 'total'})
        avail = avail.rename(columns={'area': 'avail'})
        # Join both together #
        df = total.left_join(avail, on='country')
        # Calculate ratio #
        df['avail_ratio'] = df['avail'] / df['total']
        # Set index #
        df = df.set_index('country')
        # Return #
        return df

    #------------------------------- Combine ---------------------------------#
    @property_cached
    def df(self):
        # Load #
        soef   = self.soef.copy()
        hpffre = self.hpffre.copy()
        # Filter columns #
        soef   = soef[['avail_ratio']]
        hpffre = hpffre[['avail_ratio']]
        # Rename columns #
        soef   = soef.rename(columns   = {'avail_ratio': 'soef_ratio'})
        hpffre = hpffre.rename(columns = {'avail_ratio': 'hpffre_ratio'})
        # Join both data sources together #
        df = soef.left_join(hpffre)
        # Express difference as a percentage #
        df['soef_ratio']   = self.make_percent(df['soef_ratio'])
        df['hpffre_ratio'] = self.make_percent(df['hpffre_ratio'])
        # Set index #
        df = df.set_index('country')
        # Return #
        return df

###############################################################################
# Create a singleton #
export_dir = cache_dir + 'tables/'
afws_comp  = AvailableForSupply(base_dir = export_dir)
