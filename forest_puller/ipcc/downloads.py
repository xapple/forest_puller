#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.ipcc.downloads import downloads
    >>> with pandas.option_context('max_colwidth', 100): print(downloads.df)
"""

# Built-in modules #
import time

# Internal modules #
from forest_puller import cache_dir as cache_dir_package

# First party modules #
from plumbing.cache import property_pickled
from plumbing.scraping import retrieve_from_url

# Third party modules #
import pandas
from tqdm import tqdm
from lxml import etree

###############################################################################
class DownloadsIPCC:
    """
    Parses the HTML of the IPCC download page.
    and returns all the CRF download links for every country in a data frame.
    The link points to "National Inventory Submissions 2019" (c.f. `download_url`)
    """

    download_url = "https://unfccc.int/process-and-meetings/transparency-and-reporting" \
                   "/reporting-and-review-under-the-convention/greenhouse-gas-inventories-annex-i-parties" \
                   "/national-inventory-submissions-2019"
    tiny_url     = "https://tinyurl.com/y474yu9e"
    domain       = "https://unfccc.int"

    def __init__(self, cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = cache_dir

    # ---------------------------- Properties --------------------------------#
    @property_pickled
    def df(self):
        """
        Note: unfortunately `pandas.read_html(self.download_page)` will not
        preserve hyperlinks that we later need so we have to use something
        else.
        """
        # Get the HTML of the download table with all countries #
        html_content = retrieve_from_url(self.download_url)
        # Use the `lxml` package #
        tree = etree.HTML(html_content)
        # Check if they blocked our request #
        self.check_blocked_request(tree)
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
        # Repeat columns if a country has several CRF files available #
        df = df.explode('crf')
        # Add method .progress_apply() in addition to .apply() #
        tqdm.pandas()
        # Add the zip download link as a new column #
        df['zip'] = df['crf'].progress_apply(self.get_zip_url)
        # Return #
        return df

    # ------------------------------ Methods ---------------------------------#
    def get_text_of_elem(self, elem):
        """Get all text of one XML element recursively and clean the text."""
        # Join all bits of text #
        text = ' '.join(list(elem.itertext()))
        # Remove strange characters #
        to_clean = ('\t', '\n', '\xa0')
        for char in to_clean: text = text.replace(char, '')
        # Remove double spaces #
        text = text.replace('  ', ' ').strip()
        # Return #
        return text

    def extract_links(self, elem):
        """Get all <a> child elements of input and return all the URLs in a list."""
        # Get all <a> child elements #
        links = elem.xpath('.//a')
        # Extract URLs #
        links = [a.get('href') for a in links]
        # Fix relative links that are missing the domain name #
        links = [url if url.startswith('http') else self.domain + url for url in links]
        # Return #
        return links

    def get_zip_url(self, crf_url):
        """
        Extract the zip file URL of a specific CRF document page.
        e.g. the 'English' link from https://unfccc.int/documents/194890
        """
        # We don't want to flood the server #
        time.sleep(0.5)
        # Get the HTML of an individual CRF download page #
        html_content = retrieve_from_url(crf_url)
        # Use the `lxml` module #
        tree = etree.HTML(html_content)
        # Check if they blocked our request #
        self.check_blocked_request(tree)
        # Find all <a> with 'English' as the text #
        file_url = tree.xpath("//a[contains(text(),'English')]")
        # There should be only one such <a> #
        assert len(file_url) == 1
        # Return the URL #
        return file_url[0].get('href')

    def check_blocked_request(self, tree):
        """Check if the request was denied by the server."""
        # By default we are good #
        blocked = False
        # Result type 1 from Incapsula #
        meta = tree.xpath("//head/meta[@name='ROBOTS']")
        if meta and 'NOINDEX' in meta[0].get('content'): blocked = True
        # Result type 2 from Incapsula #
        meta = tree.xpath("//head/meta[@name='robots']")
        if meta and 'noindex' in meta[0].get('content'): blocked = True
        # If we were indeed blocked, we can stop here #
        if blocked: raise Exception("The request was flagged and blocked by the server.")

###############################################################################
# Create a singleton #
downloads = DownloadsIPCC(cache_dir_package + 'ipcc/downloads/')