#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.other.genus_npl import genus_parser
    >>> print(genus_parser())
"""

# Built-in modules #

# Internal modules #

# First party modules #
from plumbing.cache import property_cached

# Third party modules #

###############################################################################
class GenusParser:
    """
    A class responsible for parsing natural language strings of text.
    It returns a specific pair of genus and species name from a free text
    user input. For instance:

     "lkjhlk" --> ('aaa', 'missing')

    Note: non-recognized words are obviously ignored.
    """

    #----------------------------- Data sources ------------------------------#
    @property_cached
    def known_species(self):
        """
        Load our reference species and genera list.
        For now we will just pick those from the density list.
        """
        # Return #
        return result

    #------------------------------ Processing -------------------------------#
    # Function to compute for each row #
    def latin_to_genus_species(self, latin_name):
        """
        Function used to compute each row (used below).
        Takes a latin_name and returns genus_name, species_name.
        """
        # Default #
        genus_name   = 'missing'
        species_name = 'missing'
        # Lower case the input #
        latin_name  = latin_name.lower()
        # Case remaining #
        if latin_name in ['remaining']: return genus_name, species_name
        # Case total #
        if latin_name in ['total']:     return genus_name, species_name
        # Check every genus in our table against the current latin_name #
        is_in_fn = lambda s: s in latin_name
        selector = self.known_species['genus'].apply(is_in_fn)
        # Case no matches #
        if not any(selector): return genus_name, species_name
        # Case one or several matches, sort by length #
        matched_rows = self.known_species[selector]
        genera_found = list(matched_rows['genus'].unique())
        genera_found = sorted(genera_found, key=len, reverse=True)
        genus_name   = genera_found[0]
        # Check for the species now #
        selector   = self.known_species['genus'] == genus_name
        genus_rows = self.known_species[selector]
        # Case no species specified for this genera #
        if len(genus_rows) == 1: return genus_name, species_name
        # Case several species specified #
        selector = genus_rows['species'].apply(is_in_fn)
        if not any(selector): return genus_name, species_name
        matched_rows = genus_rows[selector]
        species_found = list(matched_rows['species'].unique())
        species_found = sorted(species_found, key=len, reverse=True)
        species_name  = species_found[0]
        # Return #
        return genus_name, species_name

    #------------------------------ Convenience ------------------------------#
    def __call__(self, x): return self.latin_to_genus_species(x)

###############################################################################
# Create a singleton #
genus_parser = GenusParser()