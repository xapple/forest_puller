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
from forest_puller.reports.template      import Header, Footer

# First party modules #
from plumbing.cache    import property_cached
from pymarktex         import Document
from pymarktex.figures import ScaledFigure, BareFigure
from pymarktex.tables  import LatexTable

# Third party modules #

###############################################################################
class ComparisonReport(Document):
    """
    A report generated in PDF describing several countries and
    several data sources.
    """

    header_template = Header
    footer_template = Footer

    def __init__(self, parent):
        # Attributes #
        self.parent    = parent
        self.continent = parent
        # Paths #
        self.output_path = cache_dir + 'reports/comparison.pdf'

    @property_cached
    def template(self): return ComparisonTemplate(self)

    def load_markdown(self): self.markdown = str(self.template)

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
        result += str(ScaledFigure(graph   = legend,
                                   caption = caption,
                                   label   = 'comp_increments',
                                   width   = '9em'))
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
        result += str(ScaledFigure(graph   = legend,
                                   caption = caption,
                                   label   = 'comp_conv_to_tons',
                                   width   = '9em'))
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
        result += str(ScaledFigure(graph   = genus_legend,
                                   caption = caption,
                                   label   = 'genus_comp'))
        # Return #
        return result

    #-------------------------- Compare SOEF vs CBM --------------------------#
    def genus_soef_vs_cbm(self):
        # Caption #
        caption = "Comparison of genus composition between the SOEF and CBM-EU" \
                  " datasets at 3 different time points."
        # Import #
        from forest_puller.viz.genus_soef_vs_cbm import all_graphs, genus_legend
        # Initialize #
        result = ""
        # Loop every country #
        for graph in all_graphs: result += str(BareFigure(graph=graph)) + '\n\n'
        # Add the legend #
        result += str(ScaledFigure(graph   = genus_legend,
                                   caption = caption,
                                   label   = 'genus_soef_vs_cbm'))
        # Return #
        return result

    #--------------------------- Total over Europe ---------------------------#
    def eu_tot_area(self):
        # Caption #
        caption = "Sum of total forest area for 27 different countries" \
                  " in four data sources."
        # Import #
        from forest_puller.viz.area_aggregate import area_agg
        # Return #
        return str(ScaledFigure(graph=area_agg, caption=caption))

    def inc_agg_ipcc(self):
        # Caption #
        caption = "Average of net change per hectare for 27 different countries" \
                  " together from the IPCC data source."
        # Import #
        from forest_puller.viz.inc_aggregate import inc_agg_ipcc
        # Return #
        return str(ScaledFigure(graph=inc_agg_ipcc, caption=caption))

    def inc_agg_soef(self):
        # Caption #
        caption = "Average of increments per hectare for 11 different countries" \
                  " from the SOEF data source."
        # Import #
        from forest_puller.viz.inc_aggregate import inc_agg_soef
        # Return #
        return str(ScaledFigure(graph=inc_agg_soef, caption=caption))

    def inc_agg_faostat(self):
        # Caption #
        caption = "Average of losses per hectare for 27 different countries" \
                  " from the FAOSTAT data source."
        # Import #
        from forest_puller.viz.inc_aggregate import inc_agg_faostat
        # Return #
        return str(ScaledFigure(graph=inc_agg_faostat, caption=caption))

    def inc_agg_cbm(self):
        # Caption #
        caption = "Average of increments per hectare for 26 different countries" \
                  " from the EU-CBM data source."
        # Import #
        from forest_puller.viz.inc_aggregate import inc_agg_cbm
        # Return #
        return str(ScaledFigure(graph=inc_agg_cbm, caption=caption))

    def eu_tot_genus(self):
        # Caption #
        caption = "Sum of the growing stock genus breakdown for 24 different" \
                  " countries for the year 2010 in the SOEF data source."
        # Import #
        from forest_puller.viz.genus_aggregate import genus_agg
        # Return #
        return str(ScaledFigure(graph=genus_agg, caption=caption))

    #--------------------------------- Tables --------------------------------#
    def max_area(self):
        # Caption #
        caption = "Maximum forest area over time for 27 different" \
                  " countries in five data sources."
        # Import #
        from forest_puller.tables.max_area_over_time import max_area
        # Return #
        return str(LatexTable(table=max_area, caption=caption))

    def area_ipcc_vs_soef(self):
        # Caption #
        caption = "Comparison of maximum areas between IPCC and SOEF " \
                  " for 27 different countries."
        # Import #
        from forest_puller.tables.area_ipcc_vs_soef import soef_vs_ipcc
        # Return #
        return str(LatexTable(table=soef_vs_ipcc, caption=caption))

    def avail_for_supply(self):
        # Caption #
        caption = "Comparison of area available for wood supply between" \
                  " two data sources for 27 different countries."
        # Import #
        from forest_puller.tables.available_for_supply import afws_comp
        # Return #
        return str(LatexTable(table=afws_comp, caption=caption))

    def avg_increments(self):
        # Caption #
        caption = "Comparison of heterogeneous gains and losses for" \
                  " five data sources and for 27 different countries."
        # Import #
        from forest_puller.tables.average_growth import avg_inc
        # Return #
        return str(LatexTable(table=avg_inc, caption=caption))

    def avg_inc_to_tons(self):
        # Caption #
        caption = "Comparison of converted gains and losses for" \
                  " five data sources and for 27 different countries."
        # Import #
        from forest_puller.tables.average_growth import avg_tons
        # Return #
        return str(LatexTable(table=avg_tons, caption=caption))

    def avg_density(self):
        # Caption #
        caption = "Weighted average wood density" \
                  " for 27 different countries."
        # Import #
        from forest_puller.tables.density_table import wood_density
        # Return #
        return str(LatexTable(table=wood_density, caption=caption))
