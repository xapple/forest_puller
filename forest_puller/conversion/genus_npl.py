#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class like this:

    >>> from forest_puller.conversion.genus_npl import genus_parser
    >>> print(genus_parser.known_species)
    >>> genus_parser.test()
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

     "Subtype 5 Carpinus (over bark)"    -->      ('carpinus', 'missing')

    Note: non-recognized words are obviously ignored.
    """

    #----------------------------- Data sources ------------------------------#
    @property_cached
    def known_species(self):
        """
        Load our reference species and genera list.
        For now we will just pick those from the density CSV.
        """
        # Import #
        from forest_puller.conversion.tree_species_info import df as species_info
        # Filter #
        df = species_info[['genus', 'species']]
        # Return #
        return df

    #------------------------------ Processing -------------------------------#
    def latin_to_genus_species(self, latin_name):
        """
        Function used to compute each row (used below).
        Takes a latin_name and returns genus_name, species_name.
        This function should account for several special cases:

           * The species name is the same as another possible genus
             name (e.g. "picea abies" in finland),
           * The genus name is a substring of an other possible genus
             name (e.g. "pinus" and "carpinus")

                   | carpinus | abies | tree  ||             | carpinus | abies | tree
        abies      |          |   X   |       ||  pinaster   |          |       |
        acer       |          |       |       ||  radiata    |          |       |
        alnus      |          |       |       ||  strobus    |          |       |
        betula     |          |       |       ||  sylvestris |          |       |
        carpinus   |    X     |       |       ||  silvestris |          |       |
        castanea   |          |       |       ||  contorta   |          |       |
        fagus      |          |       |       ||  nigra      |          |       |
        fraxinus   |          |       |       ||
        larix      |          |       |       ||
        picea      |          |       |       ||
        pinus      |    -     |       |       ||
        populus    |          |       |       ||
        prunus     |          |       |       ||
        pseudotsuga|          |       |       ||
        quercus    |          |       |       ||
        robinia    |          |       |       ||
        salix      |          |       |       ||
        tilia      |          |       |       ||
        """
        # Default #
        genus_name   = 'missing'
        species_name = 'missing'
        # Lower case the input #
        latin_name  = latin_name.lower()
        # Split into words #
        words = latin_name.split()
        # Get all possible genera #
        genera = self.known_species['genus'].unique().tolist()
        # Compare against all possible genera, take first match #
        for word in words:
            if genus_name != 'missing': break
            for genus in genera:
                if genus_name != 'missing': break
                if word == genus: genus_name = genus
        # Get all possible species #
        all_species = self.known_species.query("genus==@genus_name")
        all_species = all_species['species'].unique().tolist()
        # Compare against all possible species, take first match #
        for word in words:
            if species_name != 'missing': break
            for species in all_species:
                if species_name != 'missing': break
                if word == species: species_name = species
        # Return #
        return genus_name, species_name

    #------------------------------ Testing ----------------------------------#
    test_cases = [
        'Pinus silvestris',
        'Pinus lorem ipsum',
        'Fagus sylvatica',
        'Abies alba (xyz)',
        'Picea abies',
        'Pseudotsuga nigra',
        'Carpinus betulus',
        'Peugot 305'
    ]

    def test(self):
        for case in self.test_cases:
            print(case, '---', self.latin_to_genus_species(case))

    #------------------------------ Convenience ------------------------------#
    def __call__(self, x): return self.latin_to_genus_species(x)

###############################################################################
# Create a singleton #
genus_parser = GenusParser()