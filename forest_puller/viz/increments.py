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
from forest_puller.common import country_codes
from forest_puller.viz.facet import FacetPlot

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
        return area_hpff

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
        sources = [self.ipcc, self.soef, self.faostat, self.hpffre, self.eu_cbm]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Add country long name #
        long_names = country_codes[['iso2_code', 'country']]
        long_names.columns = ['country', 'long_name']
        df = df.left_join(long_names, on=['country'])
        # Return #
        return df

###############################################################################
class GainsLossNetGraphPerPage(FacetPlot):

    facet_col  = 'source'
    facet_row  = 'country'

    short_name = 'area_comparison'
    formats    = ('pdf',)

    facet_var  = "country"

    x_label = 'Year'

    @property
    def df(self): return self.parent.df

    def plot(self, **kwargs):
        # Plot every data source #
        self.facet.map_dataframe(line_plot, 'year', 'inc', 'gain')
        self.facet.map_dataframe(line_plot, 'year', 'inc', 'loss')
        self.facet.map_dataframe(line_plot, 'year', 'inc', 'net')

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

# Separate by pages #
#pages = []
#
#country_per_page = 7
#count_pages = math.ceil(len(countries) / country_per_page)
#
#for page_num in range(0, count_pages):
#    klass = type('page_%i' % page_num, {}, {})
#    pages.append()

