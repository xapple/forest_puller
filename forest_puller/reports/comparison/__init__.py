#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

To regenerate the report, simply do:

    >>> from forest_puller.core.continent import continent
    >>> print(continent.report())

To also regenerate the graphs, simply delete them from puller_cache.
"""

# Built-in modules #

# Internal modules #
from forest_puller.reports.base_template import ReportTemplate
from forest_puller                       import cache_dir
from forest_puller.common                import country_codes

# First party modules #
from plumbing.cache    import property_cached
from pymarktex         import Document
from pymarktex.figures import ScaledFigure, BareFigure

# Third party modules #
from tabulate import tabulate

###############################################################################
class ComparisonReport(Document):
    """
    A report generated in PDF describing several countries and
    several data sources.
    """

    builtin_template = 'sinclair_bio'

    def __init__(self, parent):
        # Attributes #
        self.parent    = parent
        self.continent = parent
        # Paths #
        self.output_path = cache_dir + 'reports/comparison.pdf'

    @property_cached
    def template(self): return ComparisonTemplate(self)

    def load_markdown(self):
        self.params = {'main_title': 'forest\_puller - Comparison report'}
        self.markdown = str(self.template)

###############################################################################
class ComparisonTemplate(ReportTemplate):
    """All the parameters to be rendered in the markdown template."""

    delimiters = (u'{{', u'}}')

    def __repr__(self):
        return '<%s object on %s>' % (self.__class__.__name__, self.parent)

    def __init__(self, parent):
        # Attributes #
        self.parent    = parent
        self.report    = parent
        self.continent = self.report.continent

    #-------------------------------- Area -----------------------------------#
    def comp_total_area(self):
        # Caption #
        caption = "Comparison of total forest area reported in" \
                  " 26 countries and 5 data sources."
        # Import #
        from forest_puller.viz.area import area_comp
        # Return #
        return str(ScaledFigure(graph=area_comp, caption=caption))

    #----------------------------- Increments --------------------------------#
    def comp_increments(self):
        # Caption #
        caption = "Comparison of gains, losses, and totals reported" \
                  " in 26 countries and 5 data sources."
        # Import #
        from forest_puller.viz.increments import countries, legend
        # Initialize #
        result = ""
        # Loop every country #
        for iso2_code in country_codes['iso2_code']:
            graph = countries[iso2_code]
            result += str(BareFigure(graph=graph)) + '\n\n'
        # Add the legend #
        result += str(ScaledFigure(graph=legend, width='9em', caption=caption))
        # Return #
        return result

    #--------------------------- Converted to tons ----------------------------#
    def comp_conv_to_tons(self):
        # Caption #
        caption = "Comparison of gains, losses, and totals converted to tons of" \
                  " carbon reported in 26 countries and 5 data sources."
        # Import #
        from forest_puller.viz.converted_to_tons import countries, legend, all_codes
        # Initialize #
        result = ""
        # Loop every country #
        for iso2_code in all_codes:
            graph = countries[iso2_code]
            result += str(BareFigure(graph=graph)) + '\n\n'
        # Add the legend #
        result += str(ScaledFigure(graph=legend, width='9em', caption=caption))
        # Return #
        return result

    #--------------------------- Genus composition ---------------------------#
    def genus_comp(self):
        # Caption #
        caption = "Comparison of genus composition in the growing stock at" \
                  " 4 different time points in 26 countries."
        # Import #
        from forest_puller.viz.genus_barstack import all_graphs, genus_legend
        # Initialize #
        result = ""
        # Loop every country #
        for graph in all_graphs: result += str(BareFigure(graph=graph)) + '\n\n'
        # Add the legend #
        result += str(ScaledFigure(graph=genus_legend, caption=caption))
        # Return #
        return result

