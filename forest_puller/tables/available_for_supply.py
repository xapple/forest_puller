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
      (AWS = Forest Available)
      (FR = Forest Restricted)
      (FN = Forest Not Available)

    * For SOEF, we add a column:     prop_aws = area_aws / forest_area
    """

    # Parameters #
    short_name    = 'avail_for_supply'
    column_format = 'lr|rr'

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
        # Pivot #
        df = df.pipe(pandas.pivot_table,
                     index   = ['country'],
                     columns = ['category'],
                     values  = ['area'])
        # We end up with a dual level column index #
        df.columns = df.columns.get_level_values(1)
        # Total #
        df['total'] = df.sum(axis=1)
        # Calculate ratio #
        df['ratio_aws'] = df['FAWS'] / df['total']
        # Calculate ratio #
        df['ratio_raws'] = (df['FAWS'] + df['FRAWS']) / df['total']
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
        hpffre = hpffre[['ratio_aws', 'ratio_raws']]
        # Join both data sources together #
        df = soef.left_join(hpffre)
        # Set index #
        df = df.set_index('country')
        # Remove name #
        df.columns.name = None
        # Multi-index #
        df.columns = pandas.MultiIndex.from_tuples([('SOEF',   'AWS'),
                                                    ('HPFFRE', 'AWS'),
                                                    ('HPFFRE', 'AWS+FRAWS')])
        # Express difference as a percentage #
        df = df.apply(self.make_percent)
        # Return #
        return df

###############################################################################
# Create a singleton #
export_dir = cache_dir + 'tables/'
afws_comp  = AvailableForSupply(base_dir = export_dir)
