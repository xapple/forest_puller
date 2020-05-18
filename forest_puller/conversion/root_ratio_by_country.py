#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule like this:

    >>> from forest_puller.conversion.root_ratio_by_country import country_root_ratio
    >>> print(country_root_ratio.by_country_year)

"""

# Built-in modules #

# Internal modules #
from forest_puller.conversion.load_expansion_factor import root_coefs
from forest_puller.conversion.bcef_by_country import country_bcef

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import numpy


class CountryRootRatio:
    """This class uses the stock of above ground dry biomass in each country
    to choose the root to shoot ration R

    The choice of R the root to shoot ratio is based on the stock level
    expressed in tons of above-ground biomass (tons of dry biomass) obtained
    from the country_bcef.all_stock_abg_biomass method.

    The root to shoot ratio was loaded comes from Chapter 4 of the Forest Land
    2006 IPCC Guidelines for National Greenhouse Gas Inventories page 49, TABLE
    4.4 RATIO OF BELOW-GROUND  BIOMASS TO ABOVE-GROUND BIOMASS (R)
    https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_04_Ch4_Forest_Land.pdf
    """
    def get_one_root_coef(self, row):
        """Function to be applied to each row of the all_stock_abg_biomass data frame."""
        # If we get a NaN we return a NaN #
        if row['stock_per_ha'] != row['stock_per_ha']:
            return numpy.nan
        # Load #
        df = root_coefs
        # Select corresponding climatic zone #
        df = df.query(f"climatic_zone == '{row['climatic_zone']}'")
        # Select corresponding fores type#
        df = df.query(f"forest_type == '{row['forest_type']}'")
        # Select corresponding bounds on stock per hectare #
        df = df.query(f"lower < {row['stock_per_ha']} <= upper")
        # Make sure we have note more than one line #
        assert len(df) <= 1
        # Extract single float #
        result = df['ratio'].iloc[0]
        # Return #
        return result

    @property_cached
    def by_country_year(self):
        """
        This data frame contains the root to shoot ratio R for each country and
        leaf type. It uses the stock of above ground biomass expressed in tons
        of dry biomass to choose R.
        """
        # Data
        df = country_bcef.all_stock_abg_biomass.copy()
        # Filter out mixed forests
        df = df.query("forest_type != 'mixed'")
        # Add country information
        index = ['country']
        df = df.left_join(country_bcef.country_climates, on=index)
        # Add the root to shoot ratio #
        df['root_ratio'] = df.apply(self.get_one_root_coef, axis=1)
        # Multiply by the climatic coef
        df['root_ratio'] *= df['climatic_coef']
        # Group and sum over the climatic zones
        df = (df
              .groupby(['country', 'year', 'forest_type'])
              .agg({'root_ratio': 'sum',
                    'area': 'first'}))
        # Get the ratio of conifers against broadleaved #
        groups = df.groupby(['country', 'year'])
        df['area_total'] = groups['area'].transform('sum')
        df['leaf_type_prop'] = df['area'] / df['area_total']
        # Multiply by the ratio of the given leaf type #
        df['root_ratio'] *= df['leaf_type_prop']
        # Group and sum the root ratio
        df = (df
              .groupby(['country', 'year'])
              .agg({'root_ratio': 'sum'}))
        df = df.reset_index()
        # Return #
        return df

    def all_stock_total_biomass(self):
        """This data frame contains the whole stock expressed in total 
        above and below ground biomass in tons of dry matter.
        """

###############################################################################
# Create a singleton #
country_root_ratio = CountryRootRatio()

