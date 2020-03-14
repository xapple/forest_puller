#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.viz.inc_aggregate import inc_agg_ipcc
    >>> print(inc_agg_ipcc.df)
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir

# First party modules #
from plumbing.graphs import Graph
from plumbing.cache import property_cached

# Third party modules #
import pandas, matplotlib
from matplotlib import pyplot

###############################################################################
class IncAggregate(Graph):

    # Basic params #
    height  = 7
    width   = 10
    y_grid  = True
    x_label = 'Year'

    def add_main_legend(self, axes):
        items   = self.name_to_color.items()
        patches = [matplotlib.patches.Patch(color=v, label=k) for k,v in items]
        axes.legend(handles   = patches,
                    borderpad      = 1,
                    prop           = {'size': 12},
                    frameon        = True,
                    shadow         = True,
                    loc            = 'center left',
                    bbox_to_anchor = (1.03, 0.5))

    def draw(self, axes):
        self.line_plot(axes)

    def plot(self, **kw):
        # Plot #
        fig  = pyplot.figure()
        axes = fig.add_subplot(111)
        # Plot the line #
        self.draw(axes)
        # Force integer ticks on the x axis (no half years) #
        locator = matplotlib.ticker.MaxNLocator(integer=True)
        pyplot.gca().xaxis.set_major_locator(locator)
        # Leave space for the legend #
        fig.subplots_adjust(left=0.1, right=0.75, top=0.95)
        # Add legend #
        self.add_main_legend(axes)
        # Save #
        self.save_plot(**kw)
        # Return for display in notebooks for instance #
        return fig

###############################################################################
class IncAggregateIPCC(IncAggregate):
    """
    This graph will show the combined increments (loss, gain, net) of all
    countries together into one graph for the IPCC data source.
    """

    # Name #
    short_name = 'inc_aggregate_ipcc'

    # Colors #
    name_to_color = {'Net (Gain+Loss)': 'black'}

    @property
    def y_label(self):
        from forest_puller.viz.increments import GainsLossNetGraph
        return GainsLossNetGraph.source_to_y_label['ipcc']

    @property_cached
    def df(self):
        # Import #
        import forest_puller.ipcc.concat
        # Load #
        df = forest_puller.ipcc.concat.df.copy()
        # Common years #
        from forest_puller.ipcc.agg import source
        df = df.query("year in @source.common_years")
        # Filter #
        df = df.query("land_use == 'total_forest'").copy()
        # Columns #
        cols  = ['country', 'year', 'biomass_net_change', 'area']
        # Filter columns #
        df = df[cols]
        # Assert there are no NaNs #
        assert not df.isna().any().any()
        # Sum the countries and keep the years #
        df = df.groupby(['year']).agg({'area':               'sum',
                                       'biomass_net_change': 'sum'})
        # Compute per hectare values #
        df['net_per_ha'] = df['biomass_net_change'] / df['area']
        # Reset index #
        df = df.reset_index()
        # Return #
        return df

    def line_plot(self, axes, x='year', y='net_per_ha', **kw):
        axes.plot(self.df[x], self.df[y],
                  marker     = ".",
                  markersize = 10.0,
                  color      = 'black',
                  **kw)

###############################################################################
class IncAggregateSOEF(IncAggregate):
    """
    This graph will show the combined increments (loss, gain, net) of all
    countries together into one graph for the FAOSTAT data source.
    """

    # Name #
    short_name = 'inc_aggregate_soef'

    # Mapping of lines to colors #
    col_to_color  = {'gain_per_ha':      'green',
                     'loss_per_ha':      'red',
                     'net_per_ha':       'black'}
    name_to_color = {'Gains':            'green',
                     'Losses':           'red',
                     'Net (Gain+Loss)':  'black'}

    @property
    def y_label(self):
        from forest_puller.viz.increments import GainsLossNetGraph
        return GainsLossNetGraph.source_to_y_label['soef']

    @property_cached
    def df(self):
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
        df = area.left_join(fell, on=['country', 'year'])
        # Drop lines with missing values #
        df = df.dropna()
        # Pick countries #
        codes  = ['AT', 'BE', 'HR', 'CY', 'DK', 'FI',
                  'HU', 'IT', 'NL', 'RO', 'SI']
        df = df.query("country in @codes").copy()
        # Columns #
        cols  = ['year', 'area', 'gross_increment',
                 'natural_losses', 'fellings_total']
        # Filter columns #
        df = df[cols]
        # Aggregate #
        df = df.groupby(['year'])
        df = df.agg(pandas.DataFrame.sum, skipna=False)
        # Compute per hectare values #
        df['gain_per_ha'] = df['gross_increment']                         / df['area']
        df['loss_per_ha'] = (df['natural_losses'] + df['fellings_total']) / df['area']
        # By convention, losses should be negative values #
        df['loss_per_ha'] = - df['loss_per_ha']
        # The net #
        df['net_per_ha']  = df['gain_per_ha'] + df['loss_per_ha']
        # Reset index #
        df = df.reset_index()
        # Return #
        return df

    def draw(self, axes):
        self.line_plot(axes, y='gain_per_ha')
        self.line_plot(axes, y='loss_per_ha')
        self.line_plot(axes, y='net_per_ha')

    def line_plot(self, axes, x='year', y=None, **kw):
        axes.plot(self.df[x], self.df[y],
                  marker     = ".",
                  markersize = 10.0,
                  color      = self.col_to_color[y],
                  **kw)

###############################################################################
class IncAggregateFAOSTAT(IncAggregate):
    """
    This graph will show the losses of all
    countries together into one graph for the FAOSTAT data source.
    """

    # Name #
    short_name = 'inc_aggregate_faostat'

    # Colors #
    name_to_color = {'Losses': 'red'}

    @property
    def y_label(self):
        from forest_puller.viz.increments import GainsLossNetGraph
        return GainsLossNetGraph.source_to_y_label['faostat']

    @property_cached
    def df(self):
        # Import #
        import forest_puller.faostat.forestry.concat
        import forest_puller.faostat.land.concat
        # Load #
        fell = forest_puller.faostat.forestry.concat.df.copy()
        area = forest_puller.faostat.land.concat.df.copy()
        # Filter fell #
        fell = fell.query("element == 'Production'")
        fell = fell.query("unit == 'm3'")
        # Group fell #
        fell = (fell.groupby(['country', 'year'])
                .agg({'value': sum})
                .reset_index())
        # Filter area #
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
        # Assert there are no NaNs #
        assert not df.isna().any().any()
        # Sort the result #
        df = df.sort_values(['country', 'year'])
        # Compute common years #
        common_years = df.groupby('country').apply(lambda x: set(x.year))
        common_years = set.intersection(*common_years.values)
        # Filter by common years #
        df = df.query("year in @common_years")
        # Columns #
        cols  = ['year', 'area', 'loss']
        # Filter columns #
        df = df[cols]
        # Aggregate #
        df = df.groupby(['year'])
        df = df.agg(pandas.DataFrame.sum, skipna=False)
        # Compute per hectare values #
        df['loss_per_ha'] = df['loss'] / df['area']
        # By convention, losses should be negative values #
        df['loss_per_ha'] = - df['loss_per_ha']
        # Reset index #
        df = df.reset_index()
        # Return #
        return df

    def line_plot(self, axes, x='year', y='loss_per_ha', **kw):
        # Plot #
        axes.plot(self.df[x], self.df[y],
                  marker     = ".",
                  markersize = 10.0,
                  color      = 'red',
                  **kw)

###############################################################################
class IncAggregateCBM(IncAggregate):
    """
    This graph will show the combined increments (loss, gain, net) of all
    countries together into one graph for the EU-CBM data source.
    """

    # Name #
    short_name = 'inc_aggregate_cbm'

    # Mapping of lines to colors #
    col_to_color  = {'gain_per_ha':      'green',
                     'loss_per_ha':      'red',
                     'net_per_ha':       'black'}
    name_to_color = {'Gains':            'green',
                     'Losses':           'red',
                     'Net (Gain+Loss)':  'black'}

    @property
    def y_label(self):
        from forest_puller.viz.increments import GainsLossNetGraph
        return GainsLossNetGraph.source_to_y_label['eu-cbm']

    @property_cached
    def df(self):
        # Import #
        import forest_puller.cbm.concat
        # Load #
        df = forest_puller.cbm.concat.increments.copy()
        # Assert there are no NaNs #
        assert not df.isna().any().any()
        # Compute common years #
        common_years = df.groupby('country').apply(lambda x: set(x.year))
        common_years = set.intersection(*common_years.values)
        # Filter by common years #
        df = df.query("year in @common_years")
        # Filter columns #
        df = df.drop(columns='country')
        # Aggregate #
        df = df.groupby(['year'])
        df = df.agg(pandas.DataFrame.sum, skipna=False)
        # Reset index #
        df = df.reset_index()
        # Return #
        return df

    def draw(self, axes):
        self.line_plot(axes, y='gain_per_ha')
        self.line_plot(axes, y='loss_per_ha')
        self.line_plot(axes, y='net_per_ha')

    def line_plot(self, axes, x='year', y=None, **kw):
        axes.plot(self.df[x], self.df[y],
                  marker     = ".",
                  markersize = 10.0,
                  color      = self.col_to_color[y],
                  **kw)

###############################################################################
# Create the graphs #
export_dir = cache_dir + 'graphs/eu_tot/'
inc_agg_ipcc    = IncAggregateIPCC(base_dir = export_dir)
inc_agg_soef    = IncAggregateSOEF(base_dir = export_dir)
inc_agg_faostat = IncAggregateFAOSTAT(base_dir = export_dir)
inc_agg_cbm     = IncAggregateCBM(base_dir = export_dir)
