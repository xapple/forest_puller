#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.tables.density_table import wood_density
    >>> print(wood_density.df)

To export the table:

    >>> from forest_puller.tables.density_table import wood_density
    >>> print(wood_density.save())
"""

# Built-in modules #

# Internal modules #
from forest_puller        import cache_dir
from forest_puller.tables import Table

# First party modules #
from plumbing.cache  import property_cached

# Third party modules #
import pandas

###############################################################################
class WoodDensity(Table):
    """
    Display the average wood density as it is used to convert volumes to masses.
    """

    # Parameters #
    short_name    = 'wood_density'
    column_format = 'lrrrr|rrrr'
    escape_tex    = False

    @property_cached
    def df(self):
        # Import #
        from forest_puller.soef.composition import composition_data
        # Load #
        df = composition_data.avg_densities.copy()
        # Downcast to integer #
        df['year'] = df['year'].apply(int)
        # Specifying float_format produces errors, let's format ourselves #
        df['avg_density']  = df['avg_density'].apply(lambda f: "%i" % f)
        # Express frac_missing as a percentage #
        df['frac_missing'] = df['frac_missing'] * 100
        df['frac_missing'] = df['frac_missing'].apply(lambda f: "%i\\%%" % f)
        # Pivot #
        df = df.pivot(index='country', columns='year', values=['avg_density', 'frac_missing'])
        # Rename columns #
        df = df.rename(columns={'avg_density':  'Average density ($kg/m^3$)',
                                'frac_missing': 'Fraction missing'})
        # Rename indexes #
        df.index.name    = "Country"
        df.columns.names = [None, 'Year']
        # Return #
        return df

###############################################################################
# Create a singleton #
export_dir   = cache_dir + 'tables/'
wood_density = WoodDensity(base_dir = export_dir)
