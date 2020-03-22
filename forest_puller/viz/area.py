#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.viz.area import area_comp
    >>> area_comp.plot()
    >>> print(area_comp.path)

Or to dig out the individual data sources:

    >>> from forest_puller.viz.area import area_data
    >>> print(area_data.ipcc)
    >>> print(area_data.soef)
"""

# Built-in modules #

# Internal modules #
from forest_puller                  import cache_dir
from forest_puller.common           import country_codes
from forest_puller.viz.helper.facet import FacetPlot

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas
from matplotlib import pyplot

###############################################################################
class AreaCompData:

    #----------------------------- Data sources ------------------------------#
    @property_cached
    def ipcc(self):
        # Import #
        import forest_puller.ipcc.concat
        # Load #
        df = forest_puller.ipcc.concat.df.copy()
        # Index #
        df = df.reset_index(drop=True)
        df.columns.name = None
        # Filter #
        df = df.query("land_use == 'total_forest'")
        # Columns #
        df = df[['country', 'year', 'area']]
        # Add source #
        df.insert(0, 'source', "ipcc")
        # Return #
        return df

    @property_cached
    def soef(self):
        # Import #
        import forest_puller.soef.concat
        # Load #
        df = forest_puller.soef.concat.tables['forest_area'].copy()
        # Filter #
        df = df.query("category == 'forest'")
        # Columns #
        df = df[['country', 'year', 'area']]
        # Add source #
        df.insert(0, 'source', "soef")
        # Return #
        return df

    @property_cached
    def faostat(self):
        # Import #
        import forest_puller.faostat.land.concat
        # Load #
        df = forest_puller.faostat.land.concat.df.copy()
        # Filter #
        df = df.query('element == "Area"')
        df = df.query('item    == "Forest land"')
        df = df.query('flag    == "A"')
        # Columns #
        df = df[['country', 'year', 'value']]
        df.columns   = ['country', 'year', 'area']
        # Add source #
        df.insert(0, 'source', 'faostat')
        # Return #
        return df

    @property_cached
    def hpffre(self):
        """
        We are not going to plot the future projections,
        Instead we are just gonna take one point and extend it
        to the present year.
        """
        # Import #
        import forest_puller.hpffre.concat
        # Load #
        df = forest_puller.hpffre.concat.df.copy()
        # Filter #
        df = df.query("scenario == 1")
        # Sum all the different categories (FAWS, FNAWS, FRAWS) #
        df = (df.groupby(['country', 'year'])
                .agg({'area': 'sum'})
                .reset_index())
        # Columns #
        df = df[['country', 'year', 'area']]
        # Take only the minimum year for each country #
        selector  = df.groupby('country')['year'].idxmin()
        df = df.loc[selector]
        # Extend the line to the end year #
        other     = pandas.concat([self.ipcc, self.soef], ignore_index=True)
        selector  = other.groupby('country')['year'].idxmax()
        other     = other.loc[selector][['country', 'year']]
        other     = other.left_join(df[['area', 'country']], on='country')
        other     = other.dropna()
        # Add them together #
        df = pandas.concat((df, other), ignore_index=True)
        # Add source #
        df.insert(0, 'source', "hpffre")
        # Return #
        return df

    @property_cached
    def eu_cbm(self):
        # Import #
        import forest_puller.cbm.concat
        # Load #
        df = forest_puller.cbm.concat.area.copy()
        # Add source #
        df.insert(0, 'source', 'eu-cbm')
        # Return #
        return df

    #------------------------------- Combine ---------------------------------#
    @property_cached
    def df(self):
        # Load all data sources #
        sources = [self.ipcc, self.soef, self.faostat, self.hpffre, self.eu_cbm]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Adjust to million hectares #
        df['area'] /= 1e6
        # Load the iso2 code to country long name mapping #
        long_names_map = country_codes[['iso2_code', 'country']]
        long_names_map.columns = ['country', 'long_name']
        # Add country long name #
        df = df.left_join(long_names_map, on=['country'])
        # Make the countries categorical #
        df['country'] = df['country'].astype("category")
        order = [iso2 for iso2 in country_codes['iso2_code']]
        df['country'].cat.set_categories(order, inplace=True)
        # Sort the dataframe #
        df = df.sort_values(['country', 'source', 'year'])
        # Return #
        return df

###############################################################################
class AreaComparison(FacetPlot):
    """
    This graph will show the total forested area in all sources by making one
    sub-plot for each country on a facet plot.
    """

    short_name = 'area_comparison'
    formats    = ('pdf',)

    facet_var  = "country"

    x_label = 'Year'
    y_label = 'Area in million hectares'

    share_y = False
    share_x = True

    @property
    def df(self): return self.parent.df

    def plot(self, **kwargs):
        # Plot every data source #
        self.facet.map_dataframe(self.line_plot, 'year', 'area', 'ipcc')
        self.facet.map_dataframe(self.line_plot, 'year', 'area', 'soef')
        self.facet.map_dataframe(self.line_plot, 'year', 'area', 'hpffre')
        self.facet.map_dataframe(self.line_plot, 'year', 'area', 'faostat')
        self.facet.map_dataframe(self.line_plot, 'year', 'area', 'eu-cbm')
        # Adjust subplots #
        self.facet.map(self.y_grid_on)
        self.facet.map(self.hide_titles)
        self.facet.map(self.y_max_two_decimals)
        # Add a legend #
        self.add_main_legend()
        # Put the title inside the graph and large #
        self.facet.map_dataframe(self.large_title, 'long_name')
        # Change the labels #
        self.facet.set_axis_labels(self.x_label, self.y_label)
        # Leave some space for the y axis labels #
        pyplot.subplots_adjust(left=0.025)
        # Save #
        self.save_plot(**kwargs)
        # Convenience: return for display in notebooks for instance #
        return self.facet

###############################################################################
# Create the large df with all sources #
area_data = AreaCompData()

# Create the graph #
export_dir = cache_dir + 'graphs/area/'
area_comp  = AreaComparison(area_data, export_dir)
