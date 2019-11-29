#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.ipcc.crf import dataset as crf
    >>> print(crf.df)
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir as cache_dir_package
from forest_puller.ipcc.downloads import downloads

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
from tqdm import tqdm

###############################################################################
class IPCC_CRF:
    """
    Download and parse table no. 4 of every year of every country from the IPCC
    website. These excel files are found here: https://tinyurl.com/y474yu9e
    """

    def __init__(self, cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = cache_dir

    # ---------------------------- Properties --------------------------------#
    @property_cached
    def df(self):
        """
        The data frame containing all the parsed data.
        Columns are: [...]
        """
        # Check if files downloaded #
        if not self.cache_is_valid: self.refresh_cache()
        # Parse #
        pass
        # Return #
        return

    @property
    def cache_is_valid(self):
        """Checks if every file needed has been correctly downloaded."""
        return False

    # ------------------------------ Methods ---------------------------------#
    def refresh_cache(self):
        """
        Will download all the required zip files to the cache directory.
        """
        for i, row in tqdm(downloads.df.iterrows()):
            print(row['zip'])

###############################################################################
# Create a singleton #
dataset = IPCC_CRF(cache_dir_package + 'ipcc/crf/')