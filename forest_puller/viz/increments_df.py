#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule like this:

    >>> from forest_puller.viz.increments_df import increments_data
    >>> print(increments_data.df)
"""

# Built-in modules #

# Internal modules #

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas

###############################################################################
class GainsLossNetData:
    """
    Aggregate and prepare all the data frames that will be used in the
    increments plot.
    """

    #----------------------------- Data sources ------------------------------#
    @property_cached
    def ipcc(self):
        # Import #
        import forest_puller.ipcc.concat
        # Load #
        df = forest_puller.ipcc.concat.df.copy()
        # Index name #
        df.columns.name = None
        # Filter #
        df = df.query("land_use == 'total_forest'").copy()
        # Compute per hectare values #
        df['gain_per_ha'] = df['biomass_gains']      / df['area']
        df['loss_per_ha'] = df['biomass_losses']     / df['area']
        df['net_per_ha']  = df['biomass_net_change'] / df['area']
        # Columns #
        df = df[['country', 'year', 'gain_per_ha', 'loss_per_ha', 'net_per_ha']]
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property_cached
    def soef(self):
        # Import #
        import forest_puller.soef.concat
        # Load #
        area = forest_puller.soef.concat.tables['forest_area'].copy()
        fell = forest_puller.soef.concat.tables['fellings'].copy()
        # Keep only the columns we want #
        info_cols = ['gross_increment', 'natural_losses', 'fellings_total']
        fell      = fell[['country', 'year'] + info_cols]
        # Get the area that matches the right category #
        area = area.query("category == 'forest_avail_for_supply'")
        area = area.drop(columns=['category'])
        # Add the area #
        df = fell.left_join(area, on=['country', 'year'])
        # Compute per hectare values #
        df['gain_per_ha'] = df['gross_increment']                         / df['area']
        df['loss_per_ha'] = (df['natural_losses'] + df['fellings_total']) / df['area']
        # By convention, losses should be negative values #
        df['loss_per_ha'] = - df['loss_per_ha']
        # The net #
        df['net_per_ha']  = df['gain_per_ha'] + df['loss_per_ha']
        # If there is no information at all, drop the line #
        df = df.query("gain_per_ha == gain_per_ha or "
                      "loss_per_ha == loss_per_ha or "
                      "net_per_ha  == net_per_ha")
        # Columns #
        df = df[['country', 'year', 'gain_per_ha', 'loss_per_ha', 'net_per_ha']]
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property_cached
    def faostat(self):
        # Import #
        import forest_puller.faostat.forestry.concat
        import forest_puller.faostat.land.concat
        # Load #
        fell = forest_puller.faostat.forestry.concat.df.copy()
        area = forest_puller.faostat.land.concat.df.copy()
        # Filter forestry #
        fell = fell.query("element == 'Production'")
        fell = fell.query("unit == 'm3'")
        # Group forestry #
        fell = (fell.groupby(['country', 'year'])
                .agg({'value': sum})
                .reset_index())
        # Filter land #
        area = area.query('element == "Area"')
        area = area.query('item    == "Forest land"')
        area = area.query('flag    == "A"')
        # Keep columns #
        area = area[['country', 'year', 'value']]
        # Rename columns #
        fell = fell.rename(columns = {'value': 'loss'})
        area = area.rename(columns = {'value': 'area'})
        # Add the area #
        df = fell.inner_join(area, on=['country', 'year'])
        # Sort the result #
        df = df.sort_values(['country', 'year'])
        # Compute per hectare values #
        df['loss_per_ha'] = df['loss'] / df['area']
        # By convention, losses should be negative values #
        df['loss_per_ha'] = - df['loss_per_ha']
        # Drop the other columns #
        df = df.drop(columns=['area', 'loss'])
        # Reset index #
        df = df.reset_index(drop=True)
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
        # Sum all the different categories #
        df = (df
              .groupby(['country', 'year'])
              .agg({'fellings_per_ha':            'sum',
                    'growing_stock_volume_total': 'sum',
                    'area':                       'sum',})
              .reset_index())
        # The growth reported here is the total stock, not the delta
        # So we need to operate a rolling subtraction and divide by years
        group           = df.groupby(['country'])
        df['net_diff']  = group['growing_stock_volume_total'].diff()
        df['year_diff'] = group['year'].diff()
        df['area_diff'] = group['area'].diff()
        df['growth']    = df['net_diff'] / df['year_diff']
        # Set the year in the middle #
        def year_in_middle(row): return row['year'] - row['year_diff']/2
        df['year'] = df.apply(year_in_middle, axis=1)
        # Set the area in the middle #
        def area_in_middle(row): return row['area'] - row['area_diff']/2
        df['area'] = df.apply(area_in_middle, axis=1)
        # Calculate the net per hectare #
        def compute_net_per_ha(row): return row['growth'] / row['area']
        df['net_per_ha'] = df.apply(compute_net_per_ha, axis=1)
        # The fellings however are per year already #
        df = df.rename(columns = {'fellings_per_ha': 'loss_per_ha'})
        # By convention, losses should be negative values #
        df['loss_per_ha'] = - df['loss_per_ha']
        # Remove all years that are in the future #
        df = df.query("year <= 2018")
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property_cached
    def df(self):
        # Copy the data frames
        ipcc = self.ipcc.copy()
        soef = self.soef.copy()
        faostat = self.faostat.copy()
        hpffre = self.hpffre.copy()

        # Add source information
        ipcc.insert(0, 'source', "ipcc")
        soef.insert(0, 'source', "soef")
        faostat.insert(0, 'source', "fao")
        hpffre.insert(0, 'source', "hpffre")

        # Add unit information
        ipcc.insert(0, 'unit', "tons")
        soef.insert(0, 'unit', "m3 ob")
        faostat.insert(0, 'unit', "m3 ub")
        hpffre.insert(0, 'unit', "m3 ob")


        # Combine all data sources #
        sources = [ipcc, soef, faostat, hpffre]
        df = pandas.concat(sources, ignore_index=True)
        return df

###############################################################################
# Create the singleton #
increments_data = GainsLossNetData()
