#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.soef.xls_files import all_xls_files
    >>> print(all_xls_files.cache_is_valid)

To re-download the files you can do:

    >>> from forest_puller.soef.xls_files import all_xls_files
    >>> all_xls_files.refresh_cache()
"""

# Built-in modules #
import time

# Internal modules #
import forest_puller.soef.links
from forest_puller import cache_dir
from forest_puller.common import country_codes

# First party modules #
from plumbing.scraping import download_from_url
from autopaths import Path

# Third party modules #
from tqdm import tqdm
import pandas

###############################################################################
class AllXlsFiles:
    """
    For every country: download the excel file containing all tables.
    See the `DownloadsLinks` class for more information on the provenance of
    the data.

    The final file structure will look like this:

        /puller_cache/soef/xls/
    """

    def __init__(self, xls_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = xls_cache_dir

    # ---------------------------- Properties --------------------------------#
    @property
    def cache_is_valid(self):
        """Checks if every file needed has been correctly downloaded."""
        return True

    # ------------------------------ Methods ---------------------------------#
    def refresh_cache(self):
        """
        Will download all the required xls files to the cache directory.
        Takes about 2 minutes on a fast connection.
        """
        # Add method .progress_apply() in addition to .apply() #
        tqdm.pandas()
        # Get list of countries with xls URLs #
        df = forest_puller.soef.links.links.df
        # Download each zip file #
        df.T.progress_apply(self.get_one_xls)

    def get_one_xls(self, row):
        """Download one xls file and put it in the cache directory."""
        # We are not interested in all countries #
        if row['country'] not in country_codes['country'].values: return
        # Get the matching iso2_code #
        iso2_code = country_codes.query("country == '%s'" % row['country'])
        iso2_code = iso2_code['iso2_code'].iloc[0]
        # The destination directory #
        destination = Path(self.cache_dir + iso2_code + '.xls')
        # Save to disk #
        result = download_from_url(row['xls'], destination, user_agent=None)
        # We don't want to flood the server #
        time.sleep(2)

###############################################################################
# Create a singleton #
all_xls_files = AllXlsFiles(cache_dir + 'soef/xls/')