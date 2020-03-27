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
from forest_puller.common               import country_codes
from forest_puller                      import cache_dir
from forest_puller.viz.helper.multiplot import Multiplot

# First party modules #
from plumbing.cache  import property_cached
from plumbing.graphs import Graph

# Third party modules #
import pandas, numpy
from matplotlib import pyplot

###############################################################################
class GainsLossNetData:
    """
    Aggregate and prepare all the data frames that will be used in the increments
    plot.
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
        df = forest_puller.cbm.concat.increments.copy()
        # Add source #
        df.insert(0, 'source', 'eu-cbm')
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    #------------------------------- Special ---------------------------------#
    @property_cached
    def soef_stock(self):
        """
        Add the line that shows net increments estimated via the
        growing stock table in SOEF.
        """
        # Import #
        import forest_puller.soef.concat
        # Load #
        area  = forest_puller.soef.concat.tables['forest_area'].copy()
        stock = forest_puller.soef.concat.tables['stock_comp'].copy()
        # Get the area that matches the right category #
        area = area.query("category == 'forest_avail_for_supply'")
        area = area.drop(columns=['category'])
        # Get only the stock that represents the total #
        stock = stock.query("rank=='total'")
        # Add the area to make one big dataframe #
        df = stock.left_join(area, on=['country', 'year'])
        # The growth reported here is the total stock, not the delta
        # So we need to operate a rolling subtraction and divide by years
        group           = df.groupby(['country', 'rank'])
        df['net_diff']  = group['growing_stock'].diff()
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
        df['net_per_ha'] = df.apply(compute_net_per_ha, axis=1)
        # Keep only the columns that interest us #
        df = df[['country', 'year', 'net_per_ha']].copy()
        # Add source #
        df.insert(0, 'source', 'soef')
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
class GainsLossNetGraph(Multiplot):
    """
    This facet plot will produce five graphs, one per data source, for a
    given country.
    """

    # Basic params #
    x_label    = 'Year'
    formats    = ('pdf',)

    # Size of grid #
    n_rows = 1
    n_cols = 5

    # Cosmetic params #
    display_legend = False
    share_y        = False
    share_x        = True
    height         = 5
    width          = 30

    # Optional extras #
    add_soef_line  = True

    # Mapping of lines to colors #
    name_to_color = {'gain_per_ha': 'green',
                     'loss_per_ha': 'red',
                     'net_per_ha':  'black'}

    # Mapping of unit to each source #
    source_to_y_label = {
        'ipcc':    "Tons of carbon per hectare",
        'soef':    "Cubic meters over bark per hectare",
        'faostat': "Cubic meters under bark per hectare",
        'hpffre':  "Cubic meters over bark per hectare",
        'eu-cbm':  "Tons of carbon per hectare",
    }

    # The ISO2 code of the country #
    @property
    def short_name(self): return self.parent

    @property
    def country_name(self):
        # Load name mappings #
        row = country_codes.loc[country_codes['iso2_code'] == self.parent]
        row = row.iloc[0]
        # Return the long name #
        return row['country']

    @property
    def all_data(self):
        """A link to the dataframe containing all countries."""
        return gain_loss_net_data.df

    @property_cached
    def df(self):
        """Take only data that concerns the current country from the big dataframe."""
        return self.all_data.query("country == @self.parent").copy()

    @property_cached
    def soef_stock(self):
        """Take the data for the special SOEF extra line."""
        return gain_loss_net_data.soef_stock.query("country == @self.parent").copy()

    @property_cached
    def source_to_axes(self):
        return dict(zip(self.source_to_y_label.keys(), self.axes))

    def line_plot(self, df, axes, source, curve, **kw):
        # Filter for the source #
        df = df.query("source == '%s'" % source)
        # Add arguments #
        if 'marker' not in kw:     kw['marker'] = '.'
        if 'markersize' not in kw: kw['markersize'] = 10
        if 'color' not in kw:      kw['color'] = self.name_to_color[curve]
        # Plot #
        axes.plot(df['year'], df[curve], **kw)

    def plot(self, **kwargs):
        # Plot every curve on every data source #
        for source, axes in self.source_to_axes.items():
            for curve in ('gain_per_ha', 'loss_per_ha', 'net_per_ha'):
                self.line_plot(self.df, axes, source, curve)

        # We also want the special extra SOEF stock line #
        if self.add_soef_line:
            self.line_plot(self.soef_stock, self.source_to_axes['soef'],
                           'soef', 'net_per_ha', marker='+', linestyle='--')

        # Adjust details on the subplots #
        self.y_grid_on()
        self.y_max_two_decimals()

        # Hide the default titles #
        self.hide_titles()

        # Center the Y axis origin  #
        self.y_center_origin()

        # Change the X labels #
        self.set_x_labels(self.x_label)

        # Remove ugly box around figures #
        self.remove_frame()

        # Add the custom title  #
        for source, axes in self.source_to_axes.items():
            title  = self.country_name + '  (from ' + source.upper() + ')'
            axes.text(0.05, 1.05, title, transform=axes.transAxes, ha="left", size=18)

        # Set the custom Y labels #
        for source, axes in self.source_to_axes.items():
            axes.set_ylabel(self.source_to_y_label[source], fontsize=13)

        # Leave some space for the y axis labels and custom titles #
        pyplot.subplots_adjust(wspace=0.3, top=0.9, left=0.04, right=0.985, bottom=0.1)

        # Save #
        self.save_plot(**kwargs)

        # Convenience: return for display in notebooks for instance #
        return self.fig

###############################################################################
class GainsLossNetLegend(Graph):
    """
    A figure that contains no plot, only a legend, for composition purposes
    with the other graphs.
    """

    # Parameters #
    short_name    = "legend"
    add_soef_line = True

    # Names #
    title_to_color = {'Gains':            'green',
                      'Losses':           'red',
                      'Net (Gain+Loss)':  'black'}

    def plot(self, **kwargs):
        # Plot #
        fig  = pyplot.figure()
        axes = fig.add_subplot(111)
        # Create lines #
        from matplotlib.lines import Line2D
        items = self.title_to_color.items()
        kw    = {'linewidth': 10, 'linestyle': '-'}
        lines = [Line2D([0], [0], color=v, label=k, **kw) for k,v in items]
        # Add a special line #
        if self.add_soef_line:
            kw.update({'color': 'black', 'label': 'Net estimated', 'linestyle': ':'})
            lines += [Line2D([0], [0], **kw)]
        # Suppress a warning #
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            leg = fig.legend(handles   = lines,
                             borderpad = 1,
                             prop      = {'size': 20},
                             frameon   = True,
                             shadow    = True,
                             loc       = 'center')
        # Remove the axes #
        axes.axis('off')
        # Find the bounding box to remove useless white space #
        fig.canvas.draw()
        expand = [-10, -10, 10, 10]
        bbox   = leg.get_window_extent()
        bbox   = bbox.from_extents(*(bbox.extents + numpy.array(expand)))
        bbox   = bbox.transformed(fig.dpi_scale_trans.inverted())
        # Save #
        self.dpi  = 'figure'
        self.bbox = bbox
        self.save_plot(**kwargs)
        # Return for display in notebooks for instance #
        return fig

###############################################################################
# Create the large df #
gain_loss_net_data = GainsLossNetData()

# Create a facet for each country #
export_dir = cache_dir + 'graphs/increments/'
all_graphs = [GainsLossNetGraph(iso2, export_dir) for iso2 in country_codes['iso2_code']]
countries  = {c.parent: c for c in all_graphs}

# Create a separate standalone legend #
legend = GainsLossNetLegend(base_dir = export_dir)