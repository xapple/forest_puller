#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.


Typically you can use this submodule this like:

    >>> from forest_puller.viz.increments import gain_loss_net_data
    >>> print(gain_loss_net_data.ipcc)
"""

# Built-in modules #
import math, warnings

# Internal modules #
import forest_puller
import forest_puller.ipcc.concat
import forest_puller.soef.concat
from forest_puller.common import country_codes

# First party modules #
from plumbing.graphs import Graph

# Third party modules #
import seaborn, matplotlib, pandas
from matplotlib import pyplot
from matplotlib import ticker

# Constants #
source_to_y_label = {
    'ipcc': "Tons of carbon per hectare",
    'soef': "Cubic meters over bark per hectare",
}

###############################################################################
class GainsLossNetData:

    def __init__(self):
        pass

    #----------------------------- Data sources ------------------------------#
    @property
    def ipcc(self):
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
        # Load #
        area = forest_puller.soef.concat.tables['forest_area'].copy()
        fell = forest_puller.soef.concat.tables['fellings'].copy()
        # Keep only the columns we want #
        info_cols = ['gross_increment', 'natural_losses', 'fellings_total']
        fell      = fell[['country', 'year'] + info_cols]
        # If there is no information at all, drop the line #
        fell = fell.query("gross_increment == gross_increment or "
                          "natural_losses  == natural_losses  or "
                          "fellings_total  == fellings_total")
        # Get the area that matches the right category #
        area = area.query("category == 'forest_avail_for_supply'")
        area = area.drop(columns=['category'])
        # Add the area #
        df = fell.left_join(area, on=['country', 'year'])
        # If we didn't get the area for that line, drop the line #
        df = df.query("area == area")
        # Compute per hectare values #
        df['gain_per_ha'] = df['gross_increment']                         / df['area']
        df['loss_per_ha'] = (df['natural_losses'] + df['fellings_total']) / df['area']
        df['net_per_ha']  = (df['gain_per_ha']    - df['loss_per_ha'])    / df['area']
        # Columns #
        df = df[['country', 'year', 'gain_per_ha', 'loss_per_ha', 'net_per_ha']]
        # Add source #
        df.insert(0, 'source', "soef")
        # Return #
        return df

    @property
    def faostat(self):
        # Load #
        area_faos = forest_puller.faostat.forestry.concat.df.copy()
        # Filter #
        area_faos = area_faos.query('element == "Area"')
        area_faos = area_faos.query('item    == "Forest land"')
        area_faos = area_faos.query('flag    == "A"')
        # Columns #
        area_faos = area_faos[['country', 'year', 'value']]
        area_faos.columns   = ['country', 'year', 'area']
        # Add source #
        area_faos.insert(0, 'source', 'faostat')
        # Return #
        return area_faos

    @property
    def hpffre(self):
        """
        We are not going to plot the future projections,
        Instead we are just gonna take one point and extend it
        to the present year.
        """
        # Load #
        area_hpff = forest_puller.hpffre.concat.df.copy()
        # Filter #
        area_hpff = area_hpff.query("scenario == 1")
        # Sum all the different categories #
        area_hpff = (area_hpff
                     .groupby(['country', 'year'])
                     .agg({'area': sum})
                     .reset_index())
        # Columns #
        area_hpff = area_hpff[['country', 'year', 'area']]
        # Take minimum year for each country #
        selector  = area_hpff.groupby('country')['year'].idxmin()
        area_hpff = area_hpff.loc[selector]
        # Extend the line to the end year #
        other     = pandas.concat([self.area_ipcc, self.area_soef], ignore_index=True)
        selector  = other.groupby('country')['year'].idxmax()
        other     = other.loc[selector][['country', 'year']]
        other     = other.left_join(area_hpff[['area', 'country']], on='country')
        other     = other.dropna()
        area_hpff = pandas.concat((area_hpff, other), ignore_index=True)
        # Add source #
        area_hpff.insert(0, 'source', "hpffre")
        # Return #
        return area_hpff

    @property
    def eu_cbm(self):
        # Load #
        area_cbm = forest_puller.cbm.concat.df.copy()
        # Add source #
        area_cbm.insert(0, 'source', 'eu-cbm')
        # Return #
        return area_cbm

    #----------------------------- Concatenation ------------------------------#
    @property
    def df(self):
        # Load all data sources #
        sources = [self.ipcc,
                   self.soef,
                   self.faostat,
                   self.hpffre,
                   self.eu_cbm]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Add country long name #
        long_names = country_codes[['iso2_code', 'country']]
        long_names.columns = ['country', 'long_name']
        df = df.left_join(long_names, on=['country'])
        # Return #
        return df

###############################################################################
class GainsLossNetGraphPerPage(Graph):

    facet_col = 'source'
    facet_row = 'country'

    def plot(self, **kwargs):
        # Facet grid #
        p = seaborn.FacetGrid(data     = self.df,
                              row      = self.facet_row,
                              col      = self.facet_col,
                              sharey   = False,
                              height   = 6.0)

        # Colors #
        name_to_color = {'Gains':  'green',
                         'Losses': 'red',
                         'Net':    'black'}

        # Functions #
        def line_plot(x, y, source, **kwargs):
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
                        color      = name_to_color[source.upper()],
                        **kwargs)

        # Plot every data source #
        p.map_dataframe(line_plot, 'year', 'inc', 'gain')
        p.map_dataframe(line_plot, 'year', 'inc', 'loss')
        p.map_dataframe(line_plot, 'year', 'inc', 'net')

        # Add horizontal lines on the x axis #
        def grid_on(**kw):
            pyplot.gca().xaxis.grid(True, linestyle=':')
        p.map(grid_on)

        # Change the titles #
        def hide_titles(**kw):
            pyplot.gca().title.set_visible(False)
        p.map(hide_titles)

        # Force maximum two decimals for y axis #
        def formatter(**kw):
            str_formatter = matplotlib.ticker.FormatStrFormatter('%.2f')
            pyplot.gca().yaxis.set_major_formatter(str_formatter)
        p.map(formatter)

        # Add a legend #
        patches = [matplotlib.patches.Patch(color=v, label=k) for k,v in name_to_color.items()]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            p.add_legend(handles   = patches,
                         borderpad = 1,
                         prop      = {'size': 20},
                         frameon   = True,
                         shadow    = True,
                         loc       = 'lower right')

        # Put the title inside the graph and large #
        def large_legend(x, **kw):
            df = kw.pop("data")
            iso2_code = df[x].iloc[0]
            axes = pyplot.gca()
            axes.text(0.08, 0.9, iso2_code, transform=axes.transAxes, ha="left", size=22)
        p.map_dataframe(large_legend, 'long_name')

        # Change the labels #
        p.set_axis_labels(self.x_label, self.y_label)

        # Leave some space for the y axis labels #
        pyplot.subplots_adjust(left=0.025)

        # Save #
        self.save_plot(**kwargs)

        # Convenience: return for display in notebooks for instance #
        return p

###############################################################################
# Create the large df #
gain_loss_net_data = GainsLossNetData()

# Seperate by pages #
#pages = []
#
#country_per_page = 7
#count_pages = math.ceil(len(countries) / country_per_page)
#
#for page_num in range(0, count_pages):
#    klass = type('page_%i' % page_num, {}, {})
#    pages.append()

