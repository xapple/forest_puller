#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.ipcc.country import all_countries
    >>> for country in tqdm(all_countries): country.uncompress()
"""

# Built-in modules #

# Internal modules #
from forest_puller.ipcc.year import Year
from forest_puller.ipcc.zip_files import all_zip_files
from forest_puller import cache_dir, module_dir

# First party modules #
from autopaths import Path
from plumbing.cache import property_cached

# Third party modules #
from tqdm import tqdm
import pandas

# Load country codes #
country_codes = module_dir + 'extra_data/country_codes.csv'
country_codes = pandas.read_csv(str(country_codes))

###############################################################################
class Country:
    """
    Represents one country's dataset.
    """

    def __init__(self, zip_dir, xls_cache_dir):
        # Main directory #
        self.zip_dir = Path(zip_dir)
        # Record where the cache will be located on disk #
        self.cache_dir = xls_cache_dir
        # The reference ISO2 code #
        self.iso2_code = self.zip_dir.name

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

    # ---------------------------- Properties --------------------------------#
    @property_cached
    def zip_files(self):
        """Return a list of all zip files present for this country."""
        return self.zip_dir.flat_files

    @property_cached
    def zip_file(self):
        """Return only the zip that we are interested in for this country."""
        return self.zip_files[0]

    @property_cached
    def xls_dir(self):
        """Determine where to store all the xls files for this country."""
        return self.cache_dir + self.iso2_code + '/'

    @property_cached
    def all_xls_files(self):
        """For each country we have N excel files, one for each year."""
        return [f for f in self.xls_dir.flat_files if f.extension == '.xlsx']

    @property_cached
    def all_years(self):
        """Every file holds that for a specific year."""
        return [Year(self, xls) for xls in self.all_xls_files]

    @property_cached
    def years(self):
        """Every year for which we have data."""
        return {y.year: y for y in self.all_years}

    @property
    def first_year(self):
        """The earliest year for which we have data."""
        return self.all_years[0]

    @property
    def last_year(self):
        """The latest year for which we have data."""
        return self.all_years[-1]

    # ------------------------------ Methods ---------------------------------#
    def uncompress(self):
        """Uncompress the zip file contents to its own directory."""
        # Remove and regenerate #
        self.xls_dir.remove()
        self.zip_file.unzip_to(self.xls_dir, single=False)
        # Sometimes the zip contains a directory so we have to unnest #
        all_dirs  = self.xls_dir.flat_directories
        all_files = self.xls_dir.flat_files
        if len(all_dirs) == 1 and len(all_files) == 0:
            nested_dir = all_dirs[0]
            nested_dir.unnest()

###############################################################################
# Create every country object #
path          = cache_dir + 'ipcc/xls/'
all_countries = [Country(d, path) for d in all_zip_files.cache_dir.flat_directories]
countries     = {c.iso2_code: c for c in all_countries}

# Sanity check #
assert len(all_countries) > 1