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

# Internal modules #
from forest_puller.ipcc.zip_files import zip_files
from forest_puller import cache_dir, module_dir

# First party modules #

# Third party modules #
from tqdm import tqdm
import pandas

# Load country codes #
country_codes = module_dir + 'extra_data/country_codes.csv'
country_codes = pandas.read_csv(str(country_codes))

###############################################################################
class UncompressFiles:
    """
    For every country: uncompress the zip file(s) that were downloaded from the
    IPCC website and place the result it in a directory.

    The final file structure will look like this:

        /puller_cache/ipcc/xls/AT:
        16M Jan 12 18:15 aut-2019-crf-15apr19.zip

        /puller_cache/ipcc/xls/DK:
        17M Jan 12 18:15 dnm-2019-crf-12apr19.zip
        14M Jan 12 18:15 dke-2019-crf-12apr19.zip
        15M Jan 12 18:15 dnk-2019-crf-12apr19.zip
    """

    def __init__(self, crf_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = crf_cache_dir

    # ------------------------------ Methods ---------------------------------#
    def run(self):
        """
        Will uncompress all the files to the right directory.
        """
        # Add method .progress_apply() in addition to .apply() #
        tqdm.pandas()
        # Get list of countries with zip files #
        df = forest_puller.ipcc.links.links.df
        # Download each zip file #
        df.T.progress_apply(self.get_one_zip)

###############################################################################
# Create a singleton #
uncompress = UncompressFiles(cache_dir + 'ipcc/xls/')