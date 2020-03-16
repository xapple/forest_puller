#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.genus_soef_vs_cbm import all_graphs
    >>> comps   = [c for graph in all_graphs for c in graph.countries]
    >>> country = [c for c in comps if c.iso2_code == 'CY'][0]
    >>> df      = country.year_to_df[2005]
    >>> print(df)

Or if you want to look at the legend:

    >>> from forest_puller.viz.genus_soef_vs_cbm import genus_legend
    >>> print(genus_legend.label_to_color)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.helper.gridspec_plot import GridspecPlot
from forest_puller                          import cache_dir
from forest_puller.viz.helper.solo_legend   import SoloLegend
from forest_puller.common                   import country_codes
from forest_puller.viz.genus_barstack       import genus_barstack_data

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas, numpy
from matplotlib import pyplot

###############################################################################
class GenusPairedBarstack(GridspecPlot):
    """
    Group several countries together in a 'batch' and plot these countries
    together in a single graph using `gridspec` functionality.
    """

    # Size of outer grid #
    n_cols = 3
    n_rows = 1

    # Size of the final PDF #
    height = 8
    width  = 24

    # Spacing between countries #
    cntry_spacer = 0.2

    # Spacing between years #
    year_spacer = 0.2

    @property
    def short_name(self):
        """All the ISO2 codes of the countries in the current batch."""
        return '_'.join(c for c in self.parent)

    @property_cached
    def fig(self):
        """The matplotlib.Figure object."""
        return pyplot.figure(constrained_layout=False)

    @property_cached
    def gridspec(self):
        """The outer `GridSpec` object."""
        return self.fig.add_gridspec(nrows  = self.n_rows,
                                     ncols  = self.n_cols,
                                     wspace = self.cntry_spacer,
                                     left   = 0.03,
                                     right  = 0.97)

    @property_cached
    def countries(self):
        """One object per country."""
        klass = CountryGenusComparison
        return [klass(self, i, c) for i, c in enumerate(self.parent)]

    def plot(self, **kwargs):
        # Call each country #
        for country in self.countries: country.plot()
        # Change the Y labels only for the rightmost graph #
        axes = self.countries[0].axes[0]
        axes.set_ylabel("Fraction of growing stock volume", fontsize=12)
        # Save #
        self.save_plot(**kwargs)
        # Convenience: return for display in notebooks for instance #
        return self.fig

###############################################################################
class CountryGenusComparison:
    """
    Plotting methods for a single country.
    Produces a paired stacked bar chart of genera comparing several years
    across several data sources.
    """

    # Size of inner grid #
    n_cols = 3
    n_rows = 1

    # Which years are shown in which order #
    years = [2000, 2005, 2010]

    def __init__(self, parent, num, iso2_code):
        # Save params #
        self.parent    = parent
        self.num       = num
        self.iso2_code = iso2_code

    @property_cached
    def country_name(self):
        """The long name of this country."""
        row = country_codes.query('iso2_code == @self.iso2_code')
        return row.iloc[0]['country']

    @property_cached
    def gridspec(self):
        """Return the inner `GridSpec` object."""
        # This is a `SubplotSpec` object #
        sub_spec = self.parent.gridspec[self.num]
        # The inner grid #
        return sub_spec.subgridspec(nrows  = self.n_rows,
                                    ncols  = self.n_cols,
                                    wspace = self.parent.year_spacer)

    @property_cached
    def axes(self):
        """Return a single axes object for each year."""
        # Check #
        assert len(self.years) == self.n_cols
        # Initialize #
        axes = []
        # Loop #
        for i, year in enumerate(self.years):
            sub_spec = self.gridspec[i]
            sub_axes = self.parent.fig.add_subplot(sub_spec)
            axes.append(sub_axes)
        # Return #
        return axes

    @property_cached
    def soef_df(self):
        """Return a dataframe with the data for SOEF."""
        from forest_puller.soef.country import countries
        country = countries[self.iso2_code]
        return country.genus_comp.stock_comp_genus

    @property_cached
    def ecbm_df(self):
        """Return a dataframe with the data for EU-CBM."""
        from forest_puller.cbm.country import countries
        country = countries[self.iso2_code]
        return country.stock_comp_genus

    @property_cached
    def year_to_df(self):
        """
        Return a dataframe for each year that has the stock fraction data
        for both sources together. Looks like:

            Year: 2000
            ----------
            genus          stock_m3_soef  stock_m3_ecbm
            abies          0.043112       0.044986
            carpinus       0.006560       0.000000
            missing        0.065604       0.094553
            quercus        0.023430       0.019502
        """
        def compute(year):
            # Filter year #
            soef_df = self.soef_df.query("year == @year")
            ecbm_df = self.ecbm_df.query("year == @year")
            # Drop columns #
            soef_df = soef_df[['genus', 'stock_m3']]
            ecbm_df = ecbm_df[['genus', 'stock_m3']]
            # Join #
            df = soef_df.outer_join(ecbm_df,
                                    on      = 'genus',
                                    rsuffix = '_ecbm',
                                    lsuffix = '_soef')
            # Set index #
            df = df.set_index('genus')
            # Fill empty cells #
            df = df.fillna(0.0)
            # Convert to fractions #
            df = df.div(df.sum(axis=0), axis=1)
            # Fill empty cells #
            df = df.fillna(0.0)
            # Return #
            return df
        # Make a dictionary #
        return {year: compute(year) for year in self.years}

    def plot(self, **kw):
        """Takes care of plotting all years of a given country."""
        # For every year #
        for axes, year in zip(self.axes, self.years):
            # The main stacked bars #
            self.plot_bars_one_year(axes, year, **kw)
            # The cosmetics #
            self.add_style(axes, year)
        # Only on the first axes #
        axes = self.axes[0]
        # Add the custom title #
        axes.text(0.05, 1.09, self.country_name,
                  transform=axes.transAxes, ha="left", size=30)

    def plot_bars_one_year(self, axes, year, **kw):
        """Takes care of plotting a single year and two bars."""
        # Get the stock data #
        df = self.year_to_df[year]
        # Reorder the rows always in the same order #
        df = df.reindex(genus_legend.label_to_color.keys())
        df = df.dropna()
        # Number of bars and numbers of categories within bars #
        num_cats, num_bars = df.shape
        # Record the bottoms for each successive new bar #
        cum_size = numpy.zeros(num_bars)
        # Loop #
        for i, row in df.iterrows():
            # Unpack #
            genus   = row.name
            sources = row.index
            values  = row.values
            # Pick the right color #
            color = genus_legend.label_to_color[genus]
            # Plot #
            axes.bar([0, 1],
                     values,
                     bottom = cum_size,
                     color  = color)
            # Increase #
            cum_size += values

    def add_style(self, axes, year, **kw):
        """Takes care of styling the plot for a single year."""
        # Hide spines #
        for s in axes.spines.values(): s.set_visible(False)
        axes.spines["bottom"].set_visible(True)
        # Hide Y ticks #
        axes.set_yticks([])
        # Set X ticks #
        axes.set_xticks([0, 1])
        axes.set_xticklabels(['SOEF', 'EU-CBM'])
        # Rotate them a bit #
        pyplot.setp(axes.xaxis.get_majorticklabels(), rotation=70)
        # Add the year title #
        axes.set_title(year, fontsize="14", fontweight="bold")
        # Set the limits on X #
        axes.set_xlim(-0.5, 1.5)
        # Set the limits on Y #
        axes.set_ylim(0, 1)

###############################################################################
class GenusPairedLegend(SoloLegend):

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
        # Each country's genus comparison #
        comps    = [c for graph in all_graphs for c in graph.countries]
        # Each dataframe for each year for each country #
        year_dfs = [y for c in comps for y in c.year_to_df.values()]
        # All the stock fractions data together #
        df = pandas.concat(y.reset_index() for y in year_dfs)
        # Sum all the fractions to determine optimal sorting #
        df['cum_frac'] = df['stock_m3_soef'] + df['stock_m3_ecbm']
        df = df.groupby(['genus']).aggregate({'cum_frac': 'sum'})
        df = df.reset_index()
        # Import #
        from forest_puller.other.tree_species_info import df as species_info
        # Uniquify on genera #
        info = species_info.groupby('genus').first().reset_index()
        # Add the species information #
        df = df.left_join(info, on='genus')
        # Make all broadleaved negative #
        df['cum_frac'] = numpy.where(df['kind'] == 'broad',
                                    -df['cum_frac'], df['cum_frac'])
        # Make all missing null #
        df['cum_frac'] = numpy.where(df['genus'] == 'missing',
                                     0, df['cum_frac'])
        # Sort by cumulative fraction #
        df = df.sort_values(['cum_frac'], ascending=False)
        # Keep only two columns #
        df = df.set_index('genus')['plot_color'].to_dict()
        # Return #
        return df

###############################################################################
# List of all countries #
codes = [c.iso2_code for c in genus_barstack_data.countries.values()]

# Sort countries into batches of a given size #
batch_size = GenusPairedBarstack.n_cols
batches    = [codes[i:i + batch_size] for i in range(0, len(codes), batch_size)]

# Where to save the graphs #
export_dir = cache_dir + 'graphs/genus_soef_vs_cbm/'

# Create a multiplot for each batch of countries #
all_graphs = [GenusPairedBarstack(batch, export_dir) for batch in batches]

# Create a separate standalone legend #
genus_legend = GenusPairedLegend(base_dir = export_dir)
