#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
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
    width  = 30

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
                                     left   = 0.05,
                                     right  = 0.95)

    @property_cached
    def countries(self):
        """One object per country."""
        klass = CountryGenusComparison
        return [klass(self, i, c) for i, c in enumerate(self.parent)]

    def plot(self, **kwargs):
        # Call each country #
        for country in self.countries: country.plot()
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
        # Shortcuts #
        self.fig        = self.parent.fig
        self.outer_grid = self.parent.gridspec

    @property_cached
    def country_name(self):
        """The long name of this country."""
        row = country_codes.query('iso2_code == @self.iso2_code')
        return row.iloc[0]['country']

    @property_cached
    def gridspec(self):
        """Return the inner `GridSpec` object."""
        # This is a `SubplotSpec` object #
        sub_spec = self.outer_grid[self.num]
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
            sub_axes = self.fig.add_subplot(sub_spec)
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
            # Fill empty cells #
            df = df.fillna(0.0)
            # Set index #
            df = df.set_index('genus')
            # Convert to fractions #
            df = df.div(df.sum(axis=0), axis=1)
            # Return #
            return df
        # Make a dictionary #
        return {year: compute(year) for year in self.years}

    @property_cached
    def genera_used(self):
        """Return a set of all the genera seen in this comparison."""
        return {genus for df in self.year_to_df.values() for genus in df.index}

    def plot(self, **kwargs):
        """Takes care of plotting all years of a given country."""
        for axes, year in zip(self.axes, self.years):
            self.plot_one_year(axes, year, **kwargs)

    def plot_one_year(self, axes, year, **kwargs):
        """Takes care of plotting a single year and two bars."""
        # Get the stock data #
        df = self.year_to_df[year]
        # Reorder the rows #
        pass #TODO
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
            pyplot.bar([0,1],
                       values,
                       bottom = cum_size,
                       color  = color)
            # Increase #
            cum_size += values

###############################################################################
class GenusPairedLegend(SoloLegend):

    n_col = 5

    @property_cached
    def label_to_color(self):
        """Mapping of genera to colors."""
        # Each country's genus comparison #
        comps = [c for graph in all_graphs for c in graph.countries]
        # Find all genera used #
        genera = list(set.union(*(comp.genera_used for comp in comps)))
        # Sort the genera #
        genera.sort(key=self.genus_to_placement)
        # Import #
        from forest_puller.other.tree_species_info import df as species_info
        # Uniquify on genera #
        df = species_info.groupby('genus').first()
        # Filter for the genera we have #
        df = df.loc[genera, 'plot_color']
        # Return #
        return df.to_dict()

    def genus_to_placement(self, genus):
        """
        Sort the genera according to the following rules.
        The first level of organization is always:

            <all conifers, missing, all broadleaved>

        Then, within each category, we want to sort by the average
        growing stock across all years with highest first.
        """
        # Import #
        from forest_puller.other.tree_species_info import conifers, broads
        # Function to sort the columns #
        if genus == 'missing': return 0
        if genus in conifers:  return  self.tot_stock[genus].mean()
        if genus in broads:    return -self.tot_stock[genus].mean()

    @property_cached
    def tot_stock(self):
        """xxxx"""
        # Each country's genus comparison #


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
1/0