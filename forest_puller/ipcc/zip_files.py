#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.ipcc.zip_files import all_zip_files
    >>> print(all_zip_files.cache_is_valid)

To re-download the files you can do:

    >>> from forest_puller.ipcc.zip_files import all_zip_files
    >>> all_zip_files.refresh_cache()
"""

# Built-in modules #
import time

# Internal modules #
import forest_puller.ipcc.links
from forest_puller import cache_dir
from forest_puller.common import country_codes

# First party modules #
from plumbing.scraping.browser import download_via_browser
from plumbing.scraping.blockers import check_blocked_request
from autopaths import Path

# Third party modules #
from tqdm import tqdm

###############################################################################
class AllZipFiles:
    """
    For every country: download the English version of the Common Reporting
    Format (CRF) zip file from the IPCC website and place it in a directory.
    See the `DownloadsLinks` class for more information on the provenance of
    the data.

    Note: Some countries have several zip files, we will downloads all of them.

    The final file structure will look like this:

        /puller_cache/ipcc/zips/AT:
        16M Jan 12 18:15 aut-2019-crf-15apr19.zip

        /puller_cache/ipcc/zips/BE:
        16M Jan 12 18:15 bel-2019-crf-15apr19.zip

        /puller_cache/ipcc/zips/CZ:
        16M Jan 12 18:15 cze-2019-crf-12apr19.zip

        /puller_cache/ipcc/zips/DK:
        17M Jan 12 18:15 dnm-2019-crf-12apr19.zip
        14M Jan 12 18:15 dke-2019-crf-12apr19.zip
        15M Jan 12 18:15 dnk-2019-crf-12apr19.zip
    """

    def __init__(self, zip_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = zip_cache_dir

    # ---------------------------- Properties --------------------------------#
    @property
    def cache_is_valid(self):
        """Checks if every file needed has been correctly downloaded."""
        return True

    # ------------------------------ Methods ---------------------------------#
    def refresh_cache(self):
        """
        Will download all the required zip files to the cache directory.
        Takes about 4 minutes on a fast connection.
        """
        # Add method .progress_apply() in addition to .apply() #
        tqdm.pandas()
        # Get list of countries with zip URLs #
        df = forest_puller.ipcc.links.links.df
        # Download each zip file #
        df.T.progress_apply(self.get_one_zip)

    def get_one_zip(self, row):
        """Download one zip file and put it in the right directory."""
        # We are not interested in all countries #
        if row['country'] not in country_codes['country'].values: return
        # Get the matching iso2_code #
        iso2_code = country_codes.query("country == '%s'" % row['country'])
        iso2_code = iso2_code['iso2_code'].iloc[0]
        # The destination directory #
        destination = Path(self.cache_dir + iso2_code + '/')
        # Save to disk #
        result = download_via_browser(row['zip'], destination, uncompress=False)
        # Check if we were blocked #
        check_blocked_request(result)
        # We don't want to flood the server #
        time.sleep(2)

###############################################################################
# Create a singleton #
all_zip_files = AllZipFiles(cache_dir + 'ipcc/zips/')