#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.conversion.bcef_by_country import country_bcef
    >>> print(country_bcef.by_country_year)
"""

# Built-in modules #

# Internal modules #
from forest_puller.conversion.load_expansion_factor import df as bcef_info
from forest_puller.common import country_codes
from forest_puller import cache_dir

# First party modules #
from plumbing.cache import property_cached, property_pickled_at

# Third party modules #
import numpy

###############################################################################
class CountryBCEF:

    @property_cached
    def country_climates(self):
        """
        This dataframe looks like this:

               country  climatic_zone  climatic_coef
            0       AT         boreal            0.0
            1       AT      temperate            1.0
            2       AT  mediterranean            0.0
            3       BE         boreal            0.0
            4       BE      temperate            1.0
        """
        # Load #
        df = country_codes
        # Keep only some columns #
        columns = ['iso2_code', 'boreal', 'temperate', 'mediterranean']
        df = df[columns].copy()
        # Rename column #
        df = df.rename(columns={'iso2_code': 'country'})
        # Unpivot #
        df = df.melt(id_vars    = ['country'],
                     var_name   = 'climatic_zone',
                     value_name = 'climatic_coef')
        # Sort #
        df = df.sort_values('country')
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property
    def all_stock_area(self):
        """
        This data frame looks like this:

            country  year forest_type   area stock_per_ha
        0        AT  1990         con    ...          ...   
        1        AT  1990       broad    ...          ... 
        2        AT  1990       mixed    ...          ... 
        3        AT  2000         con    ...          ... 
        4        AT  2000       broad    ...          ... 
        ..      ...   ...         ...    ...          ...

        All columns are: 

            ['country', 'year', 'forest_type', 'area', 'stock_per_ha']

        """
        # Import #
        import forest_puller.soef.concat
        # Load #
        area  = forest_puller.soef.concat.tables['area_by_type'].copy()
        stock = forest_puller.soef.concat.tables['stock_by_type'].copy()
        # Remove null areas and make them NaNs #
        selector = area.area == 0
        area.loc[selector, 'area'] = numpy.NaN
        # Add the area to make one big dataframe #
        df = stock.left_join(area, on=['country', 'year', 'category'])
        # Rename category to forest_type #
        df = df.rename(columns={'category': 'forest_type'})
        # Compute stock by hectare #
        df['stock_per_ha'] = df['stock'] / df['area']
        # Now we don't need the stock column anymore #
        df = df.drop(columns=['stock'])
        return df

    @property
    def all_stock_area_by_climate(self):
        """
        This dataframe looks like this:

               country  year forest_type  area   stock_per_ha  climatic_zone  climatic_coef
           0        AT  1990         con   ...            ...         boreal            0.0
           1        AT  1990         con   ...            ...      temperate            1.0
           2        AT  1990         con   ...            ...  mediterranean            0.0
           3        AT  1990       broad   ...            ...         boreal            0.0
           4        AT  1990       broad   ...            ...      temperate            1.0

        Warning: the stock per area values are duplicated for each country and forest type   

        All columns are:

            ['country', 'year', 'forest_type', 'area', 'climatic_zone',
             'climatic_coef', 'stock_per_ha']
        """
        df = self.all_stock_area.copy()
        # Drop mixed forest #
        df = df.query("forest_type != 'mixed'")
        # Add country info #
        df = df.left_join(self.country_climates, on="country")
        # Return #
        return df

    def get_one_bcef(self, row, kind):
        """Function to be applied to each row of the previous dataframe."""
        # If we get a NaN we return a NaN #
        if row['stock_per_ha'] != row['stock_per_ha']: return numpy.nan
        # Load #
        df = bcef_info
        # Select corresponding climatic zone #
        df = df.query(f"climatic_zone == '{row['climatic_zone']}'")
        # Select corresponding fores type#
        df = df.query(f"forest_type == '{row['forest_type']}'")
        # Select corresponding bounds on stock per hectare #
        df = df.query(f"lower < {row['stock_per_ha']} <= upper")
        # Make sure we have note more than one line #
        assert len(df) <= 1
        # Extract single float #
        result = df['bcef' + kind].iloc[0]
        # Return #
        return result

    @property
    def with_bcef_coefs(self):
        """
        This dataframe is the same as above except we have added three
        columns. All columns are:

            ['country', 'year', 'forest_type', 'area', 'climatic_zone',
             'climatic_coef', 'bcefi', 'bcefr', 'bcefs']
        """
        # Load #
        df = self.all_stock_area_by_climate.copy()
        # Add three columns #
        df['bcefi'] = df.apply(lambda row: self.get_one_bcef(row, 'i'), axis=1)
        df['bcefr'] = df.apply(lambda row: self.get_one_bcef(row, 'r'), axis=1)
        df['bcefs'] = df.apply(lambda row: self.get_one_bcef(row, 's'), axis=1)
        # Now we don't need the stock_per_ha column anymore #
        df = df.drop(columns=['stock_per_ha'])
        # Return #
        return df

    @property_pickled_at('cache_path')
    def by_country_year(self):
        """
        This dataframe has three coefficients 'bcefi', 'bcefr', 'bcefs'
        for every country and for every SOEF year (except 2015).
        The dataframe looks like this:

                             bcefi     bcefr     bcefs
            country year
            AT      1990  0.600000  0.843959  0.764714
                    2000  0.574885  0.795115  0.720929
                    2005  0.573515  0.796485  0.722071
                    2010  0.572161  0.797839  0.723199
            BE      1990  0.000000  0.000000  0.000000
        """
        # Load #
        df = self.with_bcef_coefs.copy()
        # Multiply by the climatic situation #
        df['bcefi'] *= df['climatic_coef']
        df['bcefr'] *= df['climatic_coef']
        df['bcefs'] *= df['climatic_coef']
        # Now we don't need that column anymore #
        df = df.drop(columns=['climatic_coef'])
        # Group and sum each BCEF while keeping area #
        groups = df.groupby(['country', 'year', 'forest_type'])
        df     = groups.agg({'bcefi': 'sum',
                             'bcefr': 'sum',
                             'bcefs': 'sum',
                             'area':  'first'})
        # Get the ratio of conifers against broadleaved #
        groups           = df.groupby(['country', 'year'])
        df['area_total'] = groups['area'].transform('sum')
        df['tree_coef']  = df['area'] / df['area_total']
        # Multiply by the ratio of the given leaf type #
        df['bcefi'] *= df['tree_coef']
        df['bcefr'] *= df['tree_coef']
        df['bcefs'] *= df['tree_coef']
        # Group and sum each BCEF #
        groups = df.groupby(['country', 'year'])
        df     = groups.agg({'bcefi': 'sum',
                             'bcefr': 'sum',
                             'bcefs': 'sum'})
        df = df.reset_index()
        # Return #
        return df

    #--------------------------------- Cache ---------------------------------#
    @property
    def cache_path(self):
        """Specify where on the file system we will pickle the dataframe."""
        path = cache_dir + 'conversion/bcef.pickle'
        return path

###############################################################################
# Create a singleton #
country_bcef = CountryBCEF()
