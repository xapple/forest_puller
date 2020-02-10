#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.soef.links import links
    >>> with pandas.option_context('max_colwidth', 100): print(links.df)
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir

# First party modules #
from plumbing.cache import property_pickled
from plumbing.scraping import retrieve_from_url

# Third party modules #
import pandas
from lxml import etree

###############################################################################
class DownloadsLinks:
    """
    Parses the HTML of the "State of Europe's Forests" quantitative excel file
    download page.  The resulting data frame looks like:

        country    xls
        -------    ---
        Albania    https://dbsoef.foresteurope.org/docs/quantitative/Albania.xls
        Andorra    https://dbsoef.foresteurope.org/docs/quantitative/Andorra.xls
        Austria    https://dbsoef.foresteurope.org/docs/quantitative/Austria.xls
        Belarus    https://dbsoef.foresteurope.org/docs/quantitative/Belarus.xls
        ...

    and will be stored at:

        /puller_cache/soef/downloads/df.pickle
    """

    form_url = "https://dbsoef.foresteurope.org/downloadStatistics.jsp"
    base_url = "https://dbsoef.foresteurope.org/docs/quantitative/"

    def __init__(self, links_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = links_cache_dir

    # ---------------------------- Properties --------------------------------#
    @property_pickled
    def df(self):
        # Get the HTML of the download table with all countries #
        html_content = retrieve_from_url(self.form_url, user_agent=None)
        # Use the `lxml` package #
        tree = etree.HTML(html_content)
        # Get file names #
        options       = tree.xpath('//select/option')
        file_names    = [x.values()[0] for x in options]
        file_names    = [f.split('#')[0] for f in file_names]
        file_names    = [self.base_url + f for f in file_names]
        # Get country names #
        country_names = [x.text for x in options]
        # Make a data frame #
        df = pandas.DataFrame({'country': country_names, 'xls': file_names})
        # Return #
        return df

###############################################################################
# Create a singleton #
links = DownloadsLinks(cache_dir + 'soef/downloads/')