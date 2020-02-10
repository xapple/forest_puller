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
import forest_puller
from forest_puller.viz.facet import FacetPlot
from forest_puller.common    import country_codes
from forest_puller           import cache_dir

# First party modules #

# Third party modules #
import pandas
from matplotlib import pyplot

###############################################################################
class GainsLossNetData:

    #----------------------------- Data sources ------------------------------#
    @property
    def ipcc(self):
        # Import #
        import forest_puller.ipcc.concat
        # Load #
        df = forest_puller.ipcc.concat.df.copy()
        # Index #
        df = df.reset_index(drop=True)
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
        # Return #
        return df

    @property
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
        df['net_per_ha']  = (df['gain_per_ha']    - df['loss_per_ha'])    / df['area']
        # If there is no information at all, drop the line #
        df = df.query("gain_per_ha == gain_per_ha or "
                      "loss_per_ha == loss_per_ha or "
                      "net_per_ha  == net_per_ha")
        # Columns #
        df = df[['country', 'year', 'gain_per_ha', 'loss_per_ha', 'net_per_ha']]
        # Add source #
        df.insert(0, 'source', "soef")
        # Return #
        return df

    @property
    def faostat(self):
        # Load #
        df = forest_puller.faostat.forestry.concat.df.copy()
        # Filter #
        # Add source #
        df.insert(0, 'source', 'faostat')
        # Return #
        return df

    @property
    def hpffre(self):
        # Load #
        df = forest_puller.hpffre.concat.df.copy()
        # Filter #
        df = df.query("scenario == 1")
        # Add source #
        df.insert(0, 'source', "hpffre")
        # Return #
        return df

    @property
    def eu_cbm(self):
        # Load #
        df = forest_puller.cbm.concat.df.copy()
        # Add source #
        df.insert(0, 'source', 'eu-cbm')
        # Return #
        return df

    #------------------------------- Combine ---------------------------------#
    @property
    def df(self):
        # Load all data sources #
        sources = [self.ipcc, self.soef] #, self.faostat, self.hpffre, self.eu_cbm]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Add country long name #
        long_names = country_codes[['iso2_code', 'country']]
        long_names.columns = ['country', 'long_name']
        df = df.left_join(long_names, on=['country'])
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
    y_label = 'Test'

    name_to_color = {'gain_per_ha': 'green',
                     'loss_per_ha': 'red',
                     'net_per_ha':  'black'}

    source_to_y_label = {
        'ipcc': "Tons of carbon per hectare",
        'soef': "Cubic meters over bark per hectare",
    }

    @property
    def short_name(self): return self.parent

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
        # Plot every data source #
        self.facet.map_dataframe(self.line_plot, 'year', 'gain_per_ha', 'ipcc')
        self.facet.map_dataframe(self.line_plot, 'year', 'loss_per_ha', 'ipcc')
        self.facet.map_dataframe(self.line_plot, 'year', 'net_per_ha',  'ipcc')
        self.facet.map_dataframe(self.line_plot, 'year', 'gain_per_ha', 'soef')
        self.facet.map_dataframe(self.line_plot, 'year', 'loss_per_ha', 'soef')
        self.facet.map_dataframe(self.line_plot, 'year', 'net_per_ha',  'soef')

        # Adjust subplots #
        self.facet.map(self.y_grid_on)
        self.facet.map(self.hide_titles)
        self.facet.map(self.y_max_two_decimals)

        # Add a legend #
        self.add_main_legend()

        # Put the title inside the graph and large #
        self.facet.map_dataframe(self.large_legend, 'long_name')

        # Change the labels #
        self.facet.set_axis_labels(self.x_label, self.y_label)

        # Leave some space for the y axis labels #
        pyplot.subplots_adjust(left=0.025)

        # Save #
        self.save_plot(**kwargs)

        # Convenience: return for display in notebooks for instance #
        return self.facet

###############################################################################
# Create the large df #
gain_loss_net_data = GainsLossNetData()

# Create a facet for each country #
export_dir = cache_dir + 'graphs/increments/'
all_graphs = [GainsLossNetGraph(iso2, export_dir) for iso2 in country_codes['iso2_code']]
countries  = {c.parent: c for c in all_graphs}

