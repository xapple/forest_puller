#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #

# First party modules #
from plumbing.cache import property_cached

# Third party modules #

###############################################################################
class GainsLossNetExtra:

    #------------------------------- Special ---------------------------------#
    @property_cached
    def soef(self):
        """
        Add the line that shows net increments estimated via the
        growing stock table in SOEF (table 1.2a).
        """
        # Import #
        import forest_puller.soef.concat
        # Load #
        area  = forest_puller.soef.concat.tables['forest_area'].copy()
        stock = forest_puller.soef.concat.tables['stock'].copy()
        # Get the area that matches the right category #
        area  = area.query("category == 'forest'")
        stock = stock.query("category == 'forest'")
        # Drop unused columns #
        area  = area.drop(columns=['category'])
        stock = stock.drop(columns=['category', 'conif_stock', 'broad_stock'])
        # Add the area to make one big dataframe #
        df = stock.left_join(area, on=['country', 'year'])
        # Drop missing values #
        df = df.dropna()
        # The growth reported here is the total stock, not the delta
        # So we need to operate a rolling subtraction and divide by years
        group           = df.groupby(['country'])
        df['net_diff']  = group['total_stock'].diff()
        df['year_diff'] = group['year'].diff()
        df['area_diff'] = group['area'].diff()
        df['growth']    = df['net_diff'] / df['year_diff']
        # Keep only those with values #
        df = df.query("growth==growth").copy()
        # Set the year in the middle #
        def year_in_middle(row): return row['year'] - row['year_diff']/2
        df['year'] = df.apply(year_in_middle, axis=1)
        # Set the area in the middle #
        def area_in_middle(row): return row['area'] - row['area_diff']/2
        df['area'] = df.apply(area_in_middle, axis=1)
        # Calculate the net per hectare #
        def compute_net_per_ha(row): return row['growth'] / row['area']
        df['extra'] = df.apply(compute_net_per_ha, axis=1)
        # Keep only the columns that interest us #
        df = df[['country', 'year', 'extra']].copy()
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property_cached
    def faostat(self):
        """
        Add the line that shows net increments estimated via the
        growing stock data in FRA. But show it on the FAOSTAT part
        of the graph.
        """
        # Import #
        import forest_puller.fra.concat
        # Load #
        area  = forest_puller.fra.concat.df.copy()
        stock = forest_puller.fra.concat.df.copy()
        # Get the area #
        area = area.query("category == 'Forest'")
        area = area[['country', 'year', 'value']].copy()
        area = area.rename(columns = {'value': 'area'})
        # Get the stock #
        stock = stock.query("category  == 'Total growing stock'")
        stock = stock.query("land_type == 'Forest'")
        stock = stock[['country', 'year', 'value']].copy()
        stock = stock.rename(columns = {'value': 'stock'})
        # Convert the stock from over bark to under bark #
        from forest_puller.viz.converted_to_tons import ConvertedTonsData
        factor = ConvertedTonsData.bark_correction_factor
        stock['stock'] *= factor
        # Add the area to make one big dataframe #
        df = stock.left_join(area, on=['country', 'year'])
        # Sort the dataframe so that years are ascending #
        df = df.sort_values(['country', 'year'])
        # Operate a rolling subtraction and divide by years
        group           = df.groupby(['country'])
        df['net_diff']  = group['stock'].diff()
        df['year_diff'] = group['year'].diff()
        df['area_diff'] = group['area'].diff()
        df['growth']    = df['net_diff'] / df['year_diff']
        # Keep only those with values (drop 1990) #
        df = df.query("growth==growth").copy()
        # Set the year in the middle #
        def year_in_middle(row): return row['year'] - row['year_diff']/2
        df['year'] = df.apply(year_in_middle, axis=1)
        # Set the area in the middle #
        def area_in_middle(row): return row['area'] - row['area_diff']/2
        df['area'] = df.apply(area_in_middle, axis=1)
        # Calculate the net per hectare #
        def compute_net_per_ha(row): return row['growth'] / row['area']
        df['extra'] = df.apply(compute_net_per_ha, axis=1)
        # Drop other columns #
        df = df[['country', 'year', 'extra']].copy()
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property_cached
    def hpffre_todo(self):
        """
        Add the line that shows net increments estimated via the
        growing stock data in HPFFRE.
        """
        # Import #
        #TODO

###############################################################################
# Create the singleton #
extra_data = GainsLossNetExtra()
