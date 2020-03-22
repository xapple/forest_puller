#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.tables.average_growth import avg_inc
    >>> print(avg_inc.df)

To export the tables:

    >>> from forest_puller.tables.average_growth import avg_inc, avg_tons
    >>> print(avg_inc.save())
    >>> print(avg_tons.save())
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
def pivot_increments(df):
    # Group #
    group = df.groupby(['country', 'source'])
    # Average #
    result = group.aggregate({'gain_per_ha': 'mean',
                              'loss_per_ha': 'mean'})
    # Pivot #
    result = result.pipe(pandas.pivot_table,
                 index   = ['country'],
                 columns = ['source'],
                 values  = ['gain_per_ha', 'loss_per_ha'])
    # Cosmetic changes level 1 #
    result = result.rename(columns={'gain_per_ha': 'Gains per hectare',
                                    'loss_per_ha': 'Losses per hectare'})
    # Cosmetic changes level 2 #
    sources = {'ipcc':    'IPCC',
               'soef':    'SOEF',
               'faostat': 'FAO',
               'hpffre':  'HFRE',
               'eu-cbm':  'CBM'}
    result = result.rename(columns=sources)
    # Cosmetic changes level 3 #
    result = result.rename_axis([None, "Source"], axis="columns")
    # Return #
    return result

###############################################################################
class AverageIncrements(Table):
    """
    Table with average gains and losses over all years available.
    Units are heterogeneous.
    """

    # Parameters #
    short_name       = 'average_increments'
    float_format_tex = '%.2f'
    column_format    = 'lrrrr|rrrrr'

    @property_cached
    def df(self):
        # Import #
        from forest_puller.viz.increments import gain_loss_net_data
        # Return #
        return pivot_increments(gain_loss_net_data.df)

###############################################################################
class AverageIncsToTons(Table):
    """
    Table with average gains and losses over all years available.
    Units are converted to tons.
    """

    # Parameters #
    short_name       = 'average_inc_to_tons'
    float_format_tex = '%.2f'
    column_format    = 'lrrrr|rrrrr'

    @property_cached
    def df(self):
        # Import #
        from forest_puller.viz.converted_to_tons import converted_tons_data
        # Return #
        return pivot_increments(converted_tons_data.df)

###############################################################################
# Create singletons #
export_dir = cache_dir + 'tables/'
avg_inc  = AverageIncrements(base_dir = export_dir)
avg_tons = AverageIncsToTons(base_dir = export_dir)
