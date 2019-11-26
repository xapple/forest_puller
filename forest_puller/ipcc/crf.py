#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import requests, pandas
from lxml import etree

###############################################################################
class IPCC_CRF:
    """
    Download and parse table no. 4 of every year of every country from the IPCC
    website. These excel files are found here: https://tinyurl.com/y474yu9e
    """

    download_url = "https://tinyurl.com/y474yu9e"
    domain = "https://unfccc.int"

    def __init__(self, data_dir):
        # Record where the cache will be located on disk #
        self.data_dir = data_dir

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

        # Return #
        return

    @property
    def cache_is_valid(self):
        """Checks if every file needed has been correctly downloaded."""
        return False

    @property_cached
    def download_page_html(self):
        """Returns the full HTML of the IPCC download page."""
        response = requests.get(self.download_url)
        response.raise_for_status()
        return response.text

    @property_cached
    def all_links(self):
        """
        Parses the HTML of the IPCC download page and returns the CRF download
        links for every country in a data frame.
        Note: unfortunately pandas.read_html(self.download_page) will not
        preserve hyperlinks that we later need.
        """
        # Use lxml #
        tree = etree.HTML(self.download_page_html)
        # Get column names #
        cols = tree.xpath('//table/thead/tr/th')
        cols = [self.get_text_of_elem(th) for th in cols]
        # Parse rows #
        def tr_to_list_with_links(tr):
            name  = tr.xpath('th')[0].text.strip()
            links = [self.extract_links(td) for td in tr.xpath('td')]
            return [name] + links
        rows = tree.xpath('//table/tbody/tr')
        rows = [tr_to_list_with_links(tr) for tr in rows]
        # Make a data frame #
        df = pandas.DataFrame(rows, columns=cols)
        # Drop other columns and rename #
        df = df[['Party', 'Latest submitted CRF 1']]
        df.columns = ['country', 'crf']
        # Repeat columns if a country has several CRF files #
        df = df.explode('crf')
        # Add the english zip download link #
        df['zip'] = df['crf'].apply(self.get_zip_link)
        # Return #
        return df

    # ------------------------------ Methods ---------------------------------#
    def refresh_cache(self):
        """
        Will download all the required zip files to the cache directory.
        """
        pass

    def get_text_of_elem(self, elem):
        """Get all text of one element recursively and clean the text."""
        # Join all bits of text #
        text = ' '.join(list(elem.itertext()))
        # Remove strange characters #
        to_clean = ('\t', '\n', '\xa0')
        for chr in to_clean: text = text.replace(chr, '')
        # Remove double spaces #
        text = text.replace('  ', ' ').strip()
        # Return #
        return text

    def extract_links(self, elem):
        """Get all <a> child elements of input and return all the urls in a list."""
        # Get all <a> child elements #
        links = elem.xpath('.//a')
        # Extract URLs #
        links = [a.get('href') for a in links]
        # Fix relative links that are missing the domain name #
        links = [url if url.startswith('http') else self.domain + url for url in links]
        # Return #
        return links

###############################################################################
# Create a singleton #
dataset = IPCC_CRF(cache_dir + 'ipcc/crf/')