#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.ipcc.zip_files import zip_files
    >>> print(zip_files)

To re-download the files you can do:

    >>> from forest_puller.ipcc.zip_files import zip_files
    >>> zip_files.refresh_cache()
"""

# Built-in modules #
import time

# Internal modules #
import forest_puller.ipcc.links
from forest_puller import cache_dir

# First party modules #
from plumbing.cache import property_cached
from plumbing.scraping.browser import download_via_browser
from plumbing.scraping.blockers import check_blocked_request

# Third party modules #
from tqdm import tqdm
import pandas

###############################################################################
class ZipFiles:
    """
    For every country: download the Common Reporting Format (CRF) zip file from the
    IPCC website.
    See the `DownloadsLinks` class for more information on the provenance of the
    data.
    """

    def __init__(self, crf_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = crf_cache_dir

    # ---------------------------- Properties --------------------------------#
    @property
    def cache_is_valid(self):
        """Checks if every file needed has been correctly downloaded."""
        return True

    # ------------------------------ Methods ---------------------------------#
    def refresh_cache(self):
        """Will download all the required zip files to the cache directory."""
        # Add method .progress_apply() in addition to .apply() #
        tqdm.pandas()
        # Get each zip file #
        forest_puller.ipcc.links.links.df.T.progress_apply(self.get_one_zip)

    def get_one_zip(self, row):
        """Download one zip file and put it in the cache directory."""
        # We don't want to flood the server #
        time.sleep(0.5)
        print(row)
        print('------')
        # Save to disk #
        #destination = download_via_browser(url, self.cache_dir, uncompress=False)
        # Check if we were blocked #
        #check_blocked_request(destination)

###############################################################################
# Create a singleton #
zip_files = ZipFiles(cache_dir + 'ipcc/zip/')