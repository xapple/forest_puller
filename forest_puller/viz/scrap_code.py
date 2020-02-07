#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.viz.increments import increments
    >>> increments.plot()
    >>> print(increments.path)
"""

# Built-in modules #
import math, warnings

# Internal modules #
import forest_puller
import forest_puller.ipcc.concat
import forest_puller.soef.concat
import forest_puller.faostat.land.concat
import forest_puller.hpffre.concat
import forest_puller.cbm.concat
from forest_puller import cache_dir
from forest_puller.common import country_codes
from forest_puller.viz import name_to_color

# First party modules #
from plumbing.graphs import Graph

# Third party modules #
import seaborn, matplotlib, pandas
from matplotlib import pyplot
from matplotlib import ticker

###############################################################################
class IncrementsComparison(Graph):

    short_name = 'increments_comparison'
    facet_var  = "country"

    #----------------------------- Data sources ------------------------------#
    @property
    def inc_ipcc(self):
        # Load #
        area_ipcc = forest_puller.ipcc.concat.df.copy()
        # Index #
        area_ipcc = area_ipcc.reset_index(drop=True)
        del area_ipcc.columns.name
        # Filter #
        area_ipcc = area_ipcc.query("land_use == 'total_forest'")
        # Columns #
        area_ipcc = area_ipcc[['country', 'year', 'inc']]
        # Add source #
        area_ipcc.insert(0, 'source', "ipcc")
        # Return #
        return area_ipcc

    @property
    def inc_soef(self):
        # Load #
        area_soef = forest_puller.soef.concat.tables['forest_area'].copy()
        # Filter #
        area_soef = area_soef.query("category == 'forest'")
        # Columns #
        area_soef = area_soef[['country', 'year', 'area']]
        # Add source #
        area_soef.insert(0, 'source', "soef")
        # Return #
        return area_soef

    @property
    def inc_faostat(self):
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
    def inc_hpffre(self):
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
    def inc_eu_cbm(self):
        # Load #
        area_cbm = forest_puller.cbm.concat.df.copy()
        # Add source #
        area_cbm.insert(0, 'source', 'eu-cbm')
        # Return #
        return area_cbm

    #----------------------------- Visualization -----------------------------#
    @property
    def data(self):
        # Load all data sources #
        sources = [self.inc_ipcc,
                   self.inc_soef,
                   self.inc_faostat,
                   self.inc_hpffre,
                   self.inc_eu_cbm]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Add country long name #
        long_names = country_codes[['iso2_code', 'country']]
        long_names.columns = ['country', 'long_name']
        df = df.left_join(long_names, on=['country'])
        # Adjust to million hectares #
        df['area'] /= 1e6
        # Return #
        return df



###############################################################################
class GainsLossNet(Graph):

    x_label = "Year"

    def plot(self, **kwargs):
        # Number of columns #
        col_wrap = math.ceil(len(self.data[self.facet_var].unique()) / 9.0) + 1

        # Facet grid #
        p = seaborn.FacetGrid(data     = self.data,
                              col      = self.facet_var,
                              sharey   = False,
                              col_wrap = col_wrap,
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
class GainsLossNetIPCC(GainsLossNet):
    y_label = "Tons of carbon per hectare"

class GainsLossNetSOEF(GainsLossNet):
    y_label = "Cubic meters over bark per hectare"

class GainsLossNetFOATSTAT(GainsLossNet):
    y_label = "x"

class GainsLossNetHPFFRE(GainsLossNet):
    y_label = "x"

class GainsLossNetEUCBM(GainsLossNet):
    y_label = "x"

###############################################################################
graph_dir = cache_dir + 'graphs/'

# One graph per source #
ipcc    = GainsLossNetIPCC(base_dir=graph_dir)
soef    = GainsLossNetSOEF(base_dir=graph_dir)
foastat = GainsLossNetFOATSTAT(base_dir=graph_dir)
hpffre  = GainsLossNetHPFFRE(base_dir=graph_dir)
eu_cbm  = GainsLossNetEUCBM(base_dir=graph_dir)


###############################################################################
###############################################################################
###############################################################################
class GainsLossNetData:

    def __init__(self):
        pass

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
class GainsLossNetGraph(Graph):

    @property
    def plot(self):
        pass