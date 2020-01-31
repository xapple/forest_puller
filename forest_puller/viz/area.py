#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.viz.area import AreaComparison
    >>> graph = AreaComparison()
    >>> graph.plot()
"""

# Built-in modules #
import math, warnings

# Internal modules #
import forest_puller
import forest_puller.ipcc.concat
from forest_puller import module_dir

# First party modules #
from plumbing.graphs import Graph

# Third party modules #
import seaborn, matplotlib, brewer2mpl, pandas
from matplotlib import pyplot
from matplotlib import ticker

# Load country codes #
country_codes = module_dir + 'extra_data/country_codes.csv'
country_codes = pandas.read_csv(str(country_codes))

###############################################################################
class AreaComparison(Graph):
    short_name = 'area_comparison'
    facet_var  = "country"

    @property
    def area_ipcc(self):
        # Load #
        area_ipcc = forest_puller.ipcc.concat.df.copy()
        # Index #
        area_ipcc = area_ipcc.reset_index(drop=True)
        del area_ipcc.columns.name
        # Filter #
        area_ipcc = area_ipcc.query("land_use == 'total_forest'")
        # Columns #
        area_ipcc = area_ipcc[['country', 'year', 'area']]
        # Add source #
        area_ipcc.insert(0, 'source', "ipcc")
        # Return #
        return area_ipcc

    @property
    def data(self):
        # Load #
        df = self.area_ipcc
        # Add country long name #
        long_names = country_codes[['iso2_code', 'country']]
        long_names.columns = ['country', 'long_name']
        df = df.left_join(long_names, on=['country'])
        # Adjust to million hectares #
        df['area'] /= 1e6
        # Return #
        return df

    def plot(self, **kwargs):
        # Number of columns #
        col_wrap = math.ceil(len(self.data[self.facet_var].unique()) / 8.0) + 1

        # Colors #
        colors = brewer2mpl.get_map('Set1', 'qualitative', 5).mpl_colors
        name_to_color = {'IPCC':      colors[0],
                         'SOEF':      colors[1],
                         'HPFFRE':    colors[2],
                         'FAOSTAT':   colors[3],
                         'ROBERTO':   colors[4]}

        # Facet grid #
        p = seaborn.FacetGrid(data     = self.data,
                              col      = self.facet_var,
                              sharey   = False,
                              col_wrap = col_wrap,
                              height   = 6.0)

        # Functions #
        def line_plot(x, y, **kwargs):
            df = kwargs.pop("data")
            pyplot.plot(df[x], df[y], marker=".", markersize=10.0, **kwargs)

        # Make the two skinny lines #
        p.map_dataframe(line_plot, 'year', 'area')

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
        p.set_axis_labels("Year", "Area in million hectares")

        # Leave some space for the y axis labels #
        pyplot.subplots_adjust(left=0.03)

        # Save #
        self.save_plot(**kwargs)

        # Convenience: return for display in notebooks for instance #
        return p