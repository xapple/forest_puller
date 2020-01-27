#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.faostat.zip_file import zip_file
    >>> print(zip_file.cache_is_valid)

To re-download the files you can do:

    >>> from forest_puller.faostat.zip_file import zip_file
    >>> zip_file.refresh_cache()

To see the large data frame you can do:

    >>> from forest_puller.faostat.zip_file import zip_file
    >>> print(zip_file.df)
"""

# Built-in modules #
import zipfile, io

# Internal modules #
from forest_puller import cache_dir

# First party modules #
from plumbing.cache import property_cached
from plumbing.scraping import download_from_url

# Third party modules #
import pandas

###############################################################################
class ZipFile:
    """
    Download the zipped CSV file containing all countries and all products from
    the FAOSTAT webserver (for the forestry category).

    This data is acquired by picking the "All Data Normalized" option from the
    "Bulk download" sidebar at this address:

    * http://www.fao.org/faostat/en/#data/FO

    The final file structure will look like this:

        /puller_cache/faostat/zip/:
        16M Jan 12 18:15 aut-2019-crf-15apr19.zip
    """

    url = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Forestry_E_All_Data_(Normalized).zip"
    csv_name = "Forestry_E_All_Data_(Normalized).csv"

    def __init__(self, zip_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = zip_cache_dir
        # Where the file should be downloaded to #
        self.zip_path = self.cache_dir + 'forestry_all_data_norm.zip'

    @property
    def cache_is_valid(self):
        """Checks if the file needed has been correctly downloaded."""
        return True

    def refresh_cache(self):
        """Will download the required zip files to the cache directory."""
        download_from_url(self.url,
                          self.zip_path,
                          stream     = True,
                          progress   = True,
                          uncompress = False)

    # ---------------------------- Properties --------------------------------#
    @property_cached
    def df(self):
        """Loads the big CSV that's inside the ZIP into memory."""
        # Load the archive #
        zip_archive = zipfile.ZipFile(self.zip_path)
        # Load the CSV #
        with zip_archive.open(self.csv_name) as csv_handle:
            text_mode = io.TextIOWrapper(csv_handle, encoding = "ISO-8859-1")
            df = pandas.read_csv(text_mode)
        #df = pandas.read_csv(self.zip_path)
        # Return #
        return df

    # -------------------------------- Other ---------------------------------#
    def uncompress(self):
        """Uncompress the csv from the zip archive to disk."""
        # Destination #
        dest = self.zip_path.replace_extension('csv')
        # Load the archive #
        zip_archive = zipfile.ZipFile(self.zip_path)
        # Write #
        with zip_archive.open(self.csv_name) as orig:
            with open(dest, 'w') as csv:
                csv.write(orig.read())

    def use_stringio(self):
        """Uncompress the csv from the zip archive and put it in memory."""
        # Import #
        from six import StringIO
        # Destination #
        dest = self.zip_path.replace_extension('csv')
        # Load the archive #
        zip_archive = zipfile.ZipFile(self.zip_path)
        # Create an empty StringIO #
        result = StringIO()
        # Write #
        with zip_archive.open(self.csv_name) as csv:
            result.write(io.TextIOWrapper(csv).read())
        # Go back #
        result.seek(0)
        # Return #
        return result

###############################################################################
# Create a singleton #
zip_file = ZipFile(cache_dir + 'faostat/zip/')