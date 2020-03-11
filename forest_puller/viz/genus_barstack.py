#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.genus_barstack import genus_barstack_data
    >>> country = genus_barstack_data.countries['FR']
    >>> print(country.genus_comp.stock_comp_genus)
    >>> print(country.genus_comp.sort_cols(country.genus_comp.stock_genus_by_year))
    >>> print(country.genus_comp.stock_genus_by_year)

Or if you want to look at the legend:

    >>> from forest_puller.viz.genus_barstack import genus_legend
    >>> print(genus_legend.label_to_color)
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
import pandas, numpy
from matplotlib import pyplot

###############################################################################
class GenusBarstackData:
    """
    Add a property to every SOEF country object.
    """

    @property_cached
    def countries(self):
        """We have one dataframe for every country."""
        # Load #
        from forest_puller.soef.country import countries
        # Add a property by monkey patching #
        for c in countries.values(): c.genus_comp = GenusComposition(c)
        # Return #
        return countries

###############################################################################
class GenusComposition:
    """
    Every SOEF country object gets one instance of this class as a property.
    This class produces one dataframe (for each country) detailing
    the breakdown of the growing stock (m^3) in terms of genera.
    """

    def __init__(self, soef_country):
        # Parent #
        self.parent = soef_country
        # The reference ISO2 code #
        self.iso2_code = soef_country.iso2_code
        # The long name #
        row = country_codes.loc[country_codes['iso2_code'] == self.iso2_code]
        self.country_name = row.iloc[0]['country']

    @property_cached
    def stock_comp_genus(self):
        """
        Looks like:

            year     genus       stock_m3
            1990  carpinus      5000000.0
            1990      acer      9000000.0
            1990     pinus      9000000.0
            1990     abies     43000000.0
            1990   missing     61000000.0
            1990     abies    550000000.0
        """
        # Import #
        from forest_puller.soef.composition import composition_data as comp_data
        # Load #
        df = comp_data.stock_comp.query("country==@self.iso2_code")
        # The stock is in cubic meters #
        df = df.rename(columns={'growing_stock': 'stock_m3'})
        # Drop totals #
        df = df.query('rank!="total"')
        # Join #
        df = df.left_join(comp_data.latin_mapping, on='latin_name')
        # Sum rows that are the same genus #
        df = df.groupby(['genus', 'year']).aggregate({'stock_m3': 'sum'})
        # Reset index #
        df = df.reset_index()
        # Sort the dataframe #
        df = df.sort_values(by=['year', 'stock_m3'])
        # Return #
        return df

    @property_cached
    def stock_genus_by_year(self):
        """
        Looks like:

            genus        abies        fagus       pinus     missing
            year
            1990   593000000.0   82000000.0  82000000.0  61000000.0
            2000   686000000.0   96000000.0  83000000.0  70000000.0
            2005   707000000.0  102000000.0  82000000.0  72000000.0
            2010   721000000.0  106000000.0  81000000.0  76000000.0
        """
        # Load #
        df = self.stock_comp_genus
        # Join and sum #
        df = df.pipe(pandas.pivot_table,
                     index   = ['year'],
                     columns = ['genus'],
                     values  = 'stock_m3',
                     aggfunc = numpy.sum)
        # Some countries like italy have NaNs in some cells #
        df = df.fillna(0.0)
        # Reorder the rows always in the same order #
        df = df.reindex(columns=genus_legend.label_to_color.keys())
        df = df.dropna(axis=1)
        # Return #
        return df

###############################################################################
class GenusBarstack(Multiplot):

    # Basic params #
    x_label    = 'Year'
    formats    = ('pdf',)
    share_y    = True
    share_x    = False
    height     = 8
    width      = 30

    # Size of grid #
    n_rows = 1
    n_cols = 5

    # The ISO2 codes of the countries in the current batch #
    @property
    def short_name(self): return '_'.join(c.iso2_code for c in self.parent)

    # Where the years are shown on the X axis coordinates #
    year_to_index = {1990: 1,
                     2000: 2,
                     2005: 3,
                     2010: 4}

    def stacked_barplot(self, country):
        """Plotting function for one single country."""
        # Load #
        df = country.genus_comp.stock_genus_by_year
        # Convert to fractions #
        df = df.div(df.sum(axis=1), axis=0)
        # Transpose, each row is a genus now #
        df = df.T
        # Number of bars and numbers of categories within bars #
        num_cats, num_bars = df.shape
        # Record the bottoms for each successive new bar #
        cum_size = numpy.zeros(num_bars)
        # Loop #
        for i, row in df.iterrows():
            # Unpack #
            genus  = row.name
            years  = row.index
            values = row.values
            # Space each bar one unit apart from the next #
            x_locations = [self.year_to_index[y] for y in years]
            # Pick the right color #
            color = genus_legend.label_to_color[genus]
            # Plot #
            pyplot.bar(x_locations,
                       values,
                       bottom = cum_size,
                       color  = color)
            # Increase #
            cum_size += values

    def plot(self, **kwargs):
        # Plot every country #
        for country, axes in zip(self.parent, self.axes):
            pyplot.sca(axes)
            self.stacked_barplot(country)

        # Remove ugly box around figures #
        self.remove_frame()

        # Also remove the Y axis on the left #
        fn = lambda a: a.spines["left"].set_visible(False)
        self.iterate_all_axes(fn)
        self.set_y_ticks([])

        # Change the Y labels only for the rightmost graph #
        self.axes[0].set_ylabel("Fraction of growing stock volume",
                                fontsize=12)

        # Change the X labels #
        self.set_x_labels(self.x_label)

        # Set the X axis limits #
        a = min(self.year_to_index.values()) - 1
        b = max(self.year_to_index.values()) + 1
        self.set_x_lim(a, b)

        # Change the X ticks #
        ticks = list(self.year_to_index.values())
        self.set_x_ticks(ticks)

        # Change the X ticks labels #
        labels = list(map(str, self.year_to_index.keys()))
        self.set_x_tick_labels(labels)

        # Add the custom title  #
        for country, axes in zip(self.parent, self.axes):
            title = country.genus_comp.country_name
            axes.text(0.05, 1.05, title, transform=axes.transAxes, ha="left", size=22)

        # Prune graphs if we are shorter than n_cols #
        if len(self.parent) < self.n_cols:
            for axes in self.axes[len(self.parent):]:
                self.hide_full_axes(axes)

        # Leave some space around the graph #
        pyplot.subplots_adjust(wspace=0.3, top=0.9, left=0.04, right=0.91, bottom=0.1)
        # Save #
        self.save_plot(**kwargs)
        # Convenience: return for display in notebooks for instance #
        return self.fig

###############################################################################
class GenusBarstackLegend(SoloLegend):

    n_col = 5

    @property_cached
    def label_to_color(self):
        """
        Mapping of genera to colors.
        Sort the genera according to the following rules.
        The first level of organization is always:

            <all conifers, missing, all broadleaved>

        Then, within each category, we want to sort by the average
        growing stock across all years with highest first.
        """
        # Each country's genus breakdown #
        cntrys = [c.genus_comp.stock_comp_genus for c in c_vals]
        # All the stock fractions data together #
        df = pandas.concat(cntrys)
        # Sum all the growing stock in all countries #
        df = df.groupby(['genus']).aggregate({'stock_m3': 'sum'})
        df = df.reset_index()
        # Import #
        from forest_puller.other.tree_species_info import df as species_info
        # Uniquify on genera #
        info = species_info.groupby('genus').first().reset_index()
        # Add the species information #
        df = df.left_join(info, on='genus')
        # Make all broadleaved negative #
        df['stock_m3'] = numpy.where(df['kind'] == 'broad',
                                     -df['stock_m3'], df['stock_m3'])
        # Make all missing null #
        df['stock_m3'] = numpy.where(df['genus'] == 'missing',
                                     0, df['stock_m3'])
        # Sort by total stock #
        df = df.sort_values(['stock_m3'], ascending=False)
        # Keep only two columns #
        df = df.set_index('genus')['plot_color'].to_dict()
        # Return #
        return df

###############################################################################
# Add the required properties #
genus_barstack_data = GenusBarstackData()
c_vals = list(genus_barstack_data.countries.values())

# Remove countries that don't have data #
missing_countries = ['GR', 'LU']
c_vals = [c for c in c_vals if c.iso2_code not in missing_countries]

# Sort countries into batches of a given size #
batch_size = GenusBarstack.n_cols
batches    = [c_vals[i:i + batch_size] for i in range(0, len(c_vals), batch_size)]

# Where to save the graphs #
export_dir = cache_dir + 'graphs/genus_barstack/'

# Create a multiplot for each batch of countries #
all_graphs = [GenusBarstack(batch, export_dir) for batch in batches]

# Create a separate standalone legend #
genus_legend = GenusBarstackLegend(base_dir = export_dir)

# To re-plot the graphs do the following #
# for g in all_graphs: g.plot(rerun=True)
# genus_legend.plot(rerun=True)