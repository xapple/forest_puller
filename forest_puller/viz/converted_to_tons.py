#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.increments import converted_tons_data
    >>> print(converted_tons_data.ipcc)
"""

# Built-in modules #

# Internal modules #
from forest_puller.common        import country_codes
from forest_puller               import cache_dir
from forest_puller.viz.multiplot import Multiplot
from forest_puller import module_dir

# First party modules #
from plumbing.cache  import property_cached
from plumbing.graphs import Graph

# Third party modules #
import pandas, numpy
from matplotlib import pyplot

# Constants #
species_to_density = module_dir + 'extra_data/species_to_wood_density.csv'
species_to_density = pandas.read_csv(str(species_to_density))

# Strip white space #
for col in species_to_density.columns:
    species_to_density[col] = species_to_density[col].str.strip()

###############################################################################
class ConvertedTonsData:
    """
    Aggregate and prepare all the data frames that will be used in the
    'converted to tons' visualization.
    We will .... #TODO
    """

    #----------------------------- Data sources ------------------------------#
    @property_cached
    def species_fractions(self):
        """
        A dataframe containing the relative proportion of genera, in each country,
        where available.

        Interesting cases are:

            Carpinus betulus -> pinus
        """
        # Import #
        import forest_puller.soef.concat
        # Load #
        area = forest_puller.soef.concat.tables['stock_comp'].copy()
        # Load #
        df = forest_puller.ipcc.concat.df.copy()
        # Index name #

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
        # Add source #
        df.insert(0, 'source', "soef")
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
        forestry = forest_puller.faostat.forestry.concat.df.copy()
        land     = forest_puller.faostat.land.concat.df.copy()
        # Filter forestry #
        forestry = forestry.query("element == 'Production'")
        forestry = forestry.query("unit == 'm3'")
        # Group forestry #
        forestry = (forestry.groupby(['country', 'year'])
                    .agg({'value': sum})
                    .reset_index())
        # Filter land #
        land     = land.query('element == "Area"')
        land     = land.query('item    == "Forest land"')
        land     = land.query('flag    == "A"')
        # Keep columns #
        land     = land[['country', 'year', 'value']]
        # Rename columns #
        forestry = forestry.rename(columns = {'value': 'loss'})
        land     = land.rename(    columns = {'value': 'area'})
        # Add the area #
        df = forestry.inner_join(land, on=['country', 'year'])
        # Sort the result #
        df = df.sort_values(['country', 'year'])
        # Compute per hectare values #
        df['loss_per_ha'] = df['loss'] / df['area']
        # By convention, losses should be negative values #
        df['loss_per_ha'] = - df['loss_per_ha']
        # Add source #
        df.insert(0, 'source', 'faostat')
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
        group              = df.groupby(['country'])
        df['net_diff']     = group['growing_stock_volume_total'].diff()
        df['year_diff']    = group['year'].diff()
        df['net_per_year'] = df['net_diff']     / df['year_diff']
        df['net_per_ha']   = df['net_per_year'] / df['area']
        # The fellings however are per year already
        df = df.rename(columns = {'fellings_per_ha': 'loss_per_ha'})
        # By convention, losses should be negative values #
        df['loss_per_ha'] = - df['loss_per_ha']
        # Compute gain starting from the net #
        df['gain_per_ha'] = df['net_per_ha'] - df['loss_per_ha']
        # Remove all years that are in the future #
        df = df.query("year <= 2018")
        # Add source #
        df.insert(0, 'source', 'hpffre')
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    #------------------------------- Combine ---------------------------------#
    @property_cached
    def df(self):
        # Load all data sources #
        sources = [self.ipcc, self.soef, self.faostat, self.hpffre, self.eu_cbm]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Return #
        return df
###############################################################################
# Create the large df #
converted_tons_data = ConvertedTonsData()

# Create a facet for each country #
#export_dir = cache_dir + 'graphs/increments/'
#all_graphs = [GainsLossNetGraph(iso2, export_dir) for iso2 in country_codes['iso2_code']]
#countries  = {c.parent: c for c in all_graphs}

# Create a separate standalone legend #
#legend = GainsLossNetLegend(base_dir = cache_dir + 'graphs/increments/')