#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule like this:

    >>> from forest_puller.viz.area_comp import area_comp_data
    >>> print(area_comp_data.df)

Or if you want to look at the legend:

    >>> from forest_puller.viz.area_comp import legend
    >>> print(legend)

To re-plot the graphs do the following:

    >>> from forest_puller.viz.area_comp import all_graphs
    >>> for g in all_graphs: g.plot(rerun=True)
    >>> from forest_puller.viz.area_comp import legend
    >>> legend.plot(rerun=True)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.helper.multiplot   import Multiplot
from forest_puller                        import cache_dir
from forest_puller.viz.helper.solo_legend import SoloLegend
from forest_puller.common                 import country_codes

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas, brewer2mpl
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
    def fra(self):
        # Import #
        import forest_puller.fra.concat
        # Load #
        df = forest_puller.fra.concat.df.copy()
        # Filter #
        df = df.query('category == "Forest"')
        # The value now is the area #
        df = df.rename(columns={'value': 'area'})
        # Take only these columns #
        df = df[['country', 'year', 'area']]
        # Add source #
        df.insert(0, 'source', 'fra')
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
        # Add source #
        df.insert(0, 'source', 'eu_cbm')
        # Return #
        return df

    #------------------------------- Combine ---------------------------------#
    @property_cached
    def df(self):
        # Load all data sources #
        sources = [self.ipcc, self.soef, self.faostat, self.hpffre,
                   self.fra, self.eu_cbm]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Adjust to million hectares #
        df['area'] /= 1e6
        # Make the countries categorical #
        df['country'] = df['country'].astype("category")
        # Set a fixed order for the countries #
        order = [iso2 for iso2 in country_codes['iso2_code']]
        df['country'].cat.set_categories(order, inplace=True)
        # Sort the dataframe #
        df = df.sort_values(['country', 'source', 'year'])
        # Return #
        return df

###############################################################################
class AreaComparison(Multiplot):

    # Basic params #
    formats    = ('pdf',)
    share_y    = False
    share_x    = False
    height     = 7
    width      = 30

    # Labels for axes #
    x_label = 'Year'
    label_y = 'Area in million hectares'

    # Size of grid #
    n_rows = 1
    n_cols = 4

    # Sources to include #
    sources = ('ipcc', 'soef', 'hpffre', 'faostat', 'fra', 'eu_cbm')

    # The ISO2 codes of the countries in the current batch #
    @property
    def short_name(self): return '_'.join(c for c in self.parent)

    def line_plot(self, country, source, color, **kw):
        # Load #
        df = area_comp_data.df
        # Filter for the country and source #
        df = df.query("country == '%s'" % country)
        df = df.query("source == '%s'"  % source)
        # Plot #
        pyplot.plot(df['year'], df['area'],
                    marker     = ".",
                    markersize = 10.0,
                    color      = color,
                    **kw)

    def plot(self, **kwargs):
        # Load colors #
        colors = legend.label_to_color.values()

        # Plot every country #
        for country, axes in zip(self.parent, self.axes):
            pyplot.sca(axes)
            for source, color in zip(self.sources, colors):
                self.line_plot(country, source, color)

        # Change the X labels #
        self.set_x_labels(self.x_label)

        # Change the Y labels only for the rightmost graph #
        self.axes[0].set_ylabel(self.label_y, fontsize=12)

        # Remove ugly box around figures #
        self.remove_frame()

        # Adjust details on the subplots #
        self.y_grid_on()

        # Add the country name as a title  #
        for country, axes in zip(self.parent, self.axes):
            row = country_codes.loc[country_codes['iso2_code'] == country]
            row = row.iloc[0]['country']
            axes.text(0.05, 1.05, row, transform=axes.transAxes, ha="left", size=22)

        # Prune graphs if we are shorter than n_cols #
        if len(self.parent) < self.n_cols:
            for axes in self.axes[len(self.parent):]:
                self.hide_full_axes(axes)

        # Leave some space around the graph #
        pyplot.subplots_adjust(wspace=0.2, top=0.9, left=0.04, right=0.95, bottom=0.1)
        # Save #
        self.save_plot(**kwargs)
        # Convenience: return for display in notebooks for instance #
        return self.fig

###############################################################################
class AreaLegend(SoloLegend):
    # Params #
    capitalize = False

    # Colors #
    colors = brewer2mpl.get_map('Set1', 'qualitative', 7).mpl_colors

    # Name mapping #
    label_to_color = {'IPCC':    colors[0],
                      'SOEF':    colors[1],
                      'HPFFRE':  colors[2],
                      'FAOSTAT': colors[3],
                      'FRA':     colors[4],
                      'EU-CBM':  colors[6]}

###############################################################################
# The object that holds the data #
area_comp_data = AreaCompData()

# List of all countries #
codes = [iso2 for iso2 in country_codes['iso2_code']]

# Sort countries into batches of a given size #
batch_size = AreaComparison.n_cols
batches    = [codes[i:i + batch_size] for i in range(0, len(codes), batch_size)]

# Where to save the graphs #
export_dir = cache_dir + 'graphs/area/'

# Create a multiplot for each batch of countries #
all_graphs = [AreaComparison(batch, export_dir) for batch in batches]

# Create a separate standalone legend #
legend = AreaLegend(base_dir = export_dir)
