#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller.reports.base_template import ReportTemplate
from forest_puller import cache_dir

# First party modules #
from plumbing.cache    import property_cached
from pymarktex         import Document
from pymarktex.figures import ScaledFigure

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
        caption = "Comparison of total forest area reported in 26 countries and 5 data sources."
        from forest_puller.viz.area import area_comp
        return str(ScaledFigure(graph=area_comp, caption=caption))

