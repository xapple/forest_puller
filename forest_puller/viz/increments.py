#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule like this:

    >>> from forest_puller.viz.increments import gain_loss_net_data
    >>> print(gain_loss_net_data.ipcc)
"""

# Built-in modules #

# Internal modules #
from forest_puller.common                import country_codes
from forest_puller                       import cache_dir
from forest_puller.viz.helper.multiplot  import Multiplot
from forest_puller.viz.increments_extras import extra_data

# First party modules #
from plumbing.cache  import property_cached
from plumbing.graphs import Graph

# Third party modules #
import numpy, pandas
from matplotlib import pyplot

###############################################################################
class GainsLossNetGraph(Multiplot):
    """
    This facet plot will produce five graphs, one per data source, for a
    given country.
    """

    # Basic params #
    x_label    = 'Year'
    formats    = ('pdf',)

    # Size of grid #
    n_rows = 1
    n_cols = 5

    # Cosmetic params #
    display_legend = False
    share_y        = False
    share_x        = True
    height         = 5
    width          = 30

    # Mapping of lines to colors #
    name_to_color = {'gain_per_ha': 'green',
                     'loss_per_ha': 'red',
                     'extra':       'black',
                     'net_per_ha':  'black'}

    # Mapping of unit to each source #
    source_to_y_label = {
        'ipcc':    "Tons of carbon per hectare",
        'soef':    "Cubic meters over bark per hectare",
        'faostat': "Cubic meters under bark per hectare",
        'hpffre':  "Cubic meters over bark per hectare",
        'eu-cbm':  "Tons of carbon per hectare",
    }

    # The lines we want on each axes #
    curves = ('gain_per_ha', 'loss_per_ha', 'net_per_ha', 'extra')

    # The ISO2 code of the country #
    @property
    def short_name(self): return self.parent

    @property
    def country_name(self):
        # Load name mappings #
        row = country_codes.loc[country_codes['iso2_code'] == self.parent]
        row = row.iloc[0]
        # Return the long name #
        return row['country']

    @property_cached
    def source_to_axes(self):
        return dict(zip(self.source_to_y_label.keys(), self.axes))

    @property
    def all_data(self):
        """A link to the dataframe containing all countries."""
        from forest_puller.viz.increments_df import increments_data
        return increments_data

    def line_plot(self, axes, source, curve, **kw):
        # Use underscores for property names #
        source = source.replace('-', '_')
        # The default dataframe #
        df = pandas.DataFrame(columns=['year', 'country', curve])
        # Get the current data source #
        if curve == 'extra':  df = getattr(extra_data, source, df)
        else:                 df = getattr(self.all_data, source, df)
        # Filter for this country #
        df = df.query("country == @self.parent").copy()
        # We only want two columns #
        df = df.reindex(columns = ('year', curve))
        # Add arguments #
        if 'marker' not in kw:     kw['marker']     = '.'
        if 'markersize' not in kw: kw['markersize'] = 10
        if 'color' not in kw:      kw['color']      = self.name_to_color[curve]
        # Add arguments #
        if curve == 'extra': kw['linestyle'] = '--'
        # Plot #
        axes.plot(df['year'], df[curve], **kw)

    def plot(self, **kwargs):
        # Plot every curve on every data source #
        for source, axes in self.source_to_axes.items():
            for curve in self.curves:
                self.line_plot(axes, source, curve)

        # Adjust details on the subplots #
        self.y_grid_on()

        # Hide the default titles #
        self.hide_titles()

        # Center the Y axis origin  #
        self.y_center_origin()

        # Change the X labels #
        self.set_x_labels(self.x_label)

        # Remove ugly box around figures #
        self.remove_frame()

        # Add the custom title  #
        for source, axes in self.source_to_axes.items():
            title  = self.country_name + '  (from ' + source.upper() + ')'
            axes.text(0.05, 1.05, title, transform=axes.transAxes, ha="left", size=18)

        # Set the custom Y labels #
        for source, axes in self.source_to_axes.items():
            axes.set_ylabel(self.source_to_y_label[source], fontsize=13)

        # Leave some space for the y axis labels and custom titles #
        pyplot.subplots_adjust(wspace=0.3, top=0.9, left=0.04, right=0.985, bottom=0.1)

        # Save #
        self.save_plot(**kwargs)

        # Convenience: return for display in notebooks for instance #
        return self.fig

###############################################################################
class GainsLossNetLegend(Graph):
    """
    A figure that contains no plot, only a legend, for composition purposes
    with the other graphs.
    """

    # Parameters #
    short_name    = "legend"
    add_soef_line = True

    # Names #
    title_to_color = {'Gains':            'green',
                      'Losses':           'red',
                      'Net (Gain+Loss)':  'black'}

    def plot(self, **kwargs):
        # Plot #
        fig  = pyplot.figure()
        axes = fig.add_subplot(111)
        # Create lines #
        from matplotlib.lines import Line2D
        items = self.title_to_color.items()
        kw    = {'linewidth': 10, 'linestyle': '-'}
        lines = [Line2D([0], [0], color=v, label=k, **kw) for k,v in items]
        # Add a special line #
        if self.add_soef_line:
            kw.update({'color': 'black', 'label': 'Net estimated', 'linestyle': ':'})
            lines += [Line2D([0], [0], **kw)]
        # Suppress a warning #
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            leg = fig.legend(handles   = lines,
                             borderpad = 1,
                             prop      = {'size': 20},
                             frameon   = True,
                             shadow    = True,
                             loc       = 'center')
        # Remove the axes #
        axes.axis('off')
        # Find the bounding box to remove useless white space #
        fig.canvas.draw()
        expand = [-10, -10, 10, 10]
        bbox   = leg.get_window_extent()
        bbox   = bbox.from_extents(*(bbox.extents + numpy.array(expand)))
        bbox   = bbox.transformed(fig.dpi_scale_trans.inverted())
        # Save #
        self.dpi  = 'figure'
        self.bbox = bbox
        self.save_plot(**kwargs)
        # Return for display in notebooks for instance #
        return fig

###############################################################################
# Create a facet for each country #
export_dir = cache_dir + 'graphs/increments/'
all_graphs = [GainsLossNetGraph(iso2, export_dir) for iso2 in country_codes['iso2_code']]
countries  = {c.parent: c for c in all_graphs}

# Create a separate standalone legend #
legend = GainsLossNetLegend(base_dir = export_dir)