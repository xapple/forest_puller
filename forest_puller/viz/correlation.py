#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.x import x
    >>> print(x)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.helper.multiplot   import Multiplot
from forest_puller                        import cache_dir
from forest_puller.common                 import country_codes
from forest_puller.viz.increments         import gain_loss_net_data

# First party modules #
from plumbing.cache  import property_cached

# Third party modules #
from matplotlib import pyplot

###############################################################################
class CorrelationData:
    """
    Aggregate and prepare all the data frames that will be used in the
    correlation plot.
    """

    #----------------------------- Data sources ------------------------------#
    @property_cached
    def ipcc_faos(self):
        # Load #
        ipcc = gain_loss_net_data.ipcc
        faos = gain_loss_net_data.faostat
        # Remove source columns #
        ipcc = ipcc.drop(columns=['source'])
        faos = faos.drop(columns=['source'])
        # Remove unused columns #
        ipcc = ipcc.drop(columns=['gain_per_ha', 'net_per_ha'])
        # Join #
        df = ipcc.left_join(faos, ['country', 'year'], lsuffix='_ipcc', rsuffix='_faos')
        # Drop missing values #
        df = df.dropna()
        # Drop countries with less than 5 values #
        df = df.groupby(['country']).filter(lambda x: len(x) > 4)
        # Return #
        return df

    @property_cached
    def ipcc_faos_corr(self):
        # Load #
        df = self.ipcc_faos
        # Correlate #
        groups = (df.groupby(['country'])[['loss_per_ha_ipcc', 'loss_per_ha_faos']])
        corr   = groups.corr()
        corr   = corr.unstack().iloc[:, 1].reset_index()
        # Rename columns #
        corr.columns = ['country', 'corr_losses']
        # Make into dictionary #
        df = corr.set_index('country')['corr_losses'].to_dict()
        # Return #
        return df

###############################################################################
class CorrelationPlot(Multiplot):

    # Basic params #
    formats    = ('pdf',)
    share_y    = False
    share_x    = False
    height     = 7
    width      = 30

    # Labels for axes #
    label_x = 'Losses FAOSTAT in m^3 per hectare (under bark)'
    label_y = 'Losses IPCC in m^3 per hectare (over bark)'

    # Size of grid #
    n_rows = 1
    n_cols = 4

    # The ISO2 codes of the countries in the current batch #
    @property
    def short_name(self): return '_'.join(c for c in self.parent)

    def line_plot(self, country, axes, **kw):
        # Load #
        df = correlation_data.ipcc_faos
        # Filter for the country #
        df = df.query("country == '%s'" % country)
        # Plot #
        axes.scatter(df['loss_per_ha_faos'],
                     df['loss_per_ha_ipcc'],
                     color = 'k',
                     **kw)

    def plot(self, **kwargs):
        # Plot every country #
        for country, axes in zip(self.parent, self.axes):
            self.line_plot(country, axes)

        # Change the X labels #
        self.set_x_labels(self.label_x)

        # Change the Y labels only for the rightmost graph #
        self.axes[0].set_ylabel(self.label_y, fontsize=12)

        # Remove ugly box around figures #
        self.remove_frame()

        # Adjust details on the subplots #
        self.y_grid_on()

        # Add the country name as a title #
        for country, axes in zip(self.parent, self.axes):
            row   = country_codes.loc[country_codes['iso2_code'] == country]
            text  = row.iloc[0]['country']
            axes.text(0.05, 1.05, text, transform=axes.transAxes, ha="left", size=22)

        # Add the country correlation #
        for country, axes in zip(self.parent, self.axes):
            corr = correlation_data.ipcc_faos_corr[country]
            text = "(correlation %.2f)" % corr
            axes.text(0.05, 1.0, text, transform=axes.transAxes, ha="left", size=14)

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
# Create the large df #
correlation_data = CorrelationData()

# Load countries that can be correlated #
codes = correlation_data.ipcc_faos['country'].unique().tolist()

# Sort countries based on their correlation #
codes.sort(key=lambda c: correlation_data.ipcc_faos_corr.get(c), reverse=True)

# Sort countries into batches of a given size #
batch_size = CorrelationPlot.n_cols
batches    = [codes[i:i + batch_size] for i in range(0, len(codes), batch_size)]

# Where to save the graphs #
export_dir = cache_dir + 'graphs/correlation/'

# Create a multiplot for each batch of countries #
all_graphs = [CorrelationPlot(batch, export_dir) for batch in batches]