#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.ipcc.links import links
    >>> with pandas.option_context('max_colwidth', 100): print(links.df)
"""

# Built-in modules #
import time

# Internal modules #
from forest_puller import cache_dir

# First party modules #
from plumbing.cache import property_pickled
from plumbing.scraping import retrieve_from_url
from plumbing.scraping.blockers import check_blocked_request

# Third party modules #
import pandas
from tqdm import tqdm
from lxml import etree

###############################################################################
class DownloadsLinks:
    """
    Parses the HTML of the IPCC download page.
    and returns all the CRF download links for every country in a data frame.
    The link points to "National Inventory Submissions 2019" (c.f. `download_url`)
    The data frame looks something like:

        country     crf                                 zip
        -------     ---                                 ---
        Australia  https://unfccc.int/documents/195780  https://unfc[...]y19.zip
        Austria    https://unfccc.int/documents/194890  https://unfc[...]apr19.zip
        Belarus    https://unfccc.int/documents/194782  https://unfc[...]apr19.zip
        Belgium    https://unfccc.int/documents/194878  https://unfc[...]apr19.zip

    and will be stored at:

        /puller_cache/ipcc/downloads/df.pickle
    """

    download_url = "https://unfccc.int/process-and-meetings/transparency-and-reporting" \
                   "/reporting-and-review-under-the-convention/greenhouse-gas-inventories-annex-i-parties" \
                   "/national-inventory-submissions-2019"
    tiny_url     = "https://tinyurl.com/y474yu9e"
    domain       = "https://unfccc.int"

    def __init__(self, links_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = links_cache_dir

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
        check_blocked_request(tree)
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
        all_links = elem.xpath('.//a')
        # Extract URLs #
        all_links = [a.get('href') for a in all_links]
        # Fix relative links that are missing the domain name #
        all_links = [url if url.startswith('http') else self.domain + url for url in all_links]
        # Return #
        return all_links

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
        check_blocked_request(tree)
        # Find all <a> with 'English' as the text #
        file_url = tree.xpath("//a[contains(text(),'English')]")
        # There should be only one such <a> #
        assert len(file_url) == 1
        # Return the URL #
        return file_url[0].get('href')

###############################################################################
# Create a singleton #
links = DownloadsLinks(cache_dir + 'ipcc/downloads/')