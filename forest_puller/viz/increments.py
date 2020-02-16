#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.increments import gain_loss_net_data
    >>> print(gain_loss_net_data.ipcc)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.facet import FacetPlot
from forest_puller.common    import country_codes
from forest_puller           import cache_dir

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas
from matplotlib import pyplot

###############################################################################
class GainsLossNetData:

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
        # Add source #
        df.insert(0, 'source', "ipcc")
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

    @property_cached
    def eu_cbm(self):
        # Import #
        import forest_puller.cbm.concat
        # Load #
        df = forest_puller.cbm.concat.area.copy()
        # Temporary #TODO #
        df['gain_per_ha'] = df['area'] / 2e6
        df['loss_per_ha'] = df['area'] / 3e6
        df['net_per_ha']  = df['area'] / 5e6
        df = df.drop(columns=['area'])
        # Add source #
        df.insert(0, 'source', 'eu-cbm')
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
class GainsLossNetGraph(FacetPlot):

    facet_col  = 'source'
    facet_row  = 'country'

    formats    = ('pdf',)

    facet_var  = "source"
    col_wrap   = 5

    x_label = 'Year'

    display_legend = False

    share_y = False
    share_x = True

    name_to_color = {'gain_per_ha': 'green',
                     'loss_per_ha': 'red',
                     'net_per_ha':  'black'}

    source_to_y_label = {
        'ipcc':    "Tons of carbon per hectare",
        'soef':    "Cubic meters over bark per hectare",
        'faostat': "Cubic meters under bark per hectare",
        'hpffre':  "Cubic meters of stemwood over bark per hectare",
        'eu-cbm':  "Lorem ipsum dolor sit amet",
    }

    @property
    def short_name(self): return self.parent

    @property
    def country_name(self):
        # Load name mappings #
        row = country_codes.loc[country_codes['iso2_code'] == self.parent]
        row = row.iloc[0]
        # Return long name #
        return row['country']

    @property
    def df(self):
        # Load #
        df = gain_loss_net_data.df
        # Filter #
        df = df.query("country == @self.parent").copy()
        # Return #
        return df

    def line_plot(self, x, y, source, **kwargs):
        # Remove the color we get #
        kwargs.pop("color")
        # Get the data frame #
        df = kwargs.pop("data")
        # Filter the source #
        df = df.query("source == '%s'" % source)
        # Plot #
        pyplot.plot(df[x], df[y],
                    marker     = ".",
                    markersize = 10.0,
                    color      = self.name_to_color[y],
                    **kwargs)

    def plot(self, **kwargs):
        # Plot every curve on every data source #
        for curve in ('gain_per_ha', 'loss_per_ha', 'net_per_ha'):
            for source in ('ipcc', 'soef', 'faostat', 'hpffre', 'eu-cbm'):
                self.facet.map_dataframe(self.line_plot, 'year', curve, source)

        # Adjust details on the subplots #
        self.facet.map(self.y_grid_on)
        self.facet.map(self.y_max_two_decimals)

        # Hide the default titles #
        self.facet.map(self.hide_titles)

        # Center the Y axis origin  #
        self.facet.map(self.y_center_origin)

        # Add the custom title  #
        self.facet.map(self.custom_title, 'source')

        # Change the X labels #
        self.facet.set_axis_labels(self.x_label, 'Test')

        # Set the custom Y labels (hackish, no better way found in seaborn) #
        label_and_axes = zip(self.source_to_y_label.values(), self.facet.axes)
        for label, ax in label_and_axes: ax.set_ylabel(label, fontsize=13)

        # Add a legend if requested #
        legend_titles = {'Gains':            'green',
                         'Losses':           'red',
                         'Net (Gain+Loss)':  'black'}
        if self.display_legend: self.add_main_legend(legend_titles)

        # Leave some space for the y axis labels and custom titles #
        pyplot.subplots_adjust(top=0.89, left=0.025, wspace=0.2)

        # Save #
        self.save_plot(**kwargs)
        # Convenience: return for display in notebooks for instance #
        return self.facet

    def custom_title(self, source, **kw):
        """Add the custom title for each subplot."""
        source = source.iloc[0]
        title  = self.country_name + '     (from ' + source.upper() + ')'
        axes   = pyplot.gca()
        axes.text(0.05, 1.05, title, transform=axes.transAxes, ha="left", size=20)

###############################################################################
# Create the large df #
gain_loss_net_data = GainsLossNetData()

# Create a facet for each country #
export_dir = cache_dir + 'graphs/increments/'
all_graphs = [GainsLossNetGraph(iso2, export_dir) for iso2 in country_codes['iso2_code']]
countries  = {c.parent: c for c in all_graphs}

# Add legend only on the last graph #
all_graphs[-1].display_legend = True
