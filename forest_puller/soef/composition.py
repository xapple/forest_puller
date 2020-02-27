#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.soef.composition import composition_data
    >>> print(composition_data.avg_densities)
"""

# Built-in modules #

# Internal modules #
from forest_puller import module_dir, cache_dir

# First party modules #
from plumbing.cache import property_cached, property_pickled

# Third party modules #
import pandas, numpy

###############################################################################
class CompositionData:
    """
    Post-processing of the soef "growing_stock" table to compute, for instance,
    the relative proportion of genera, in each country, where available,
    as well as their corresponding wood densities for later conversion between
    volume and mass.
    """

    def __init__(self, cache):
        # Where we will pickle all the dataframes #
        self.cache_dir = cache

    #----------------------------- Data sources ------------------------------#
    @property_cached
    def species_to_density(self):
        """
        Parse the hard-coded table genus+species to density.
        These values come from a publication:

            Chapter 4: Forest Land 2006 IPCC Guidelines for National Greenhouse Gas Inventories
            Table 4.14 Basic Wood Density (d) Of Selected Temperate And Boreal Tree Taxa
            https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_04_Ch4_Forest_Land.pdf
            See page 71.

        The density in [tons / m³] more precisely [oven-dry tonnes of C per moist m³].
        We convert it to [kg / m³] here.
        We do not know if they measure the volume over or under bark.
        """
        # Constants #
        result = module_dir + 'extra_data/species_to_wood_density.csv'
        result = pandas.read_csv(str(result))
        # Strip white space #
        for col in ['species', 'genus']:
            result[col] = result[col].str.strip()
        # Fill missing values #
        for col in ['species', 'genus']:
            result[col] = result[col].fillna('missing')
        # We want kilograms, not tons #
        result['density'] *= 1000
        # Return #
        return result

    @property_cached
    def stock_comp(self):
        """Load the table with the species breakdown per year per country."""
        # Import #
        import forest_puller.soef.concat
        # Load #
        result = forest_puller.soef.concat.tables['stock_comp']
        # Germany does not provide totals -- cannot be used for this analysis #
        result = result.query("country != 'DE'").copy()
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
        selector = self.species_to_density['genus'].apply(is_in_fn)
        # Case no matches #
        if not any(selector): return genus_name, species_name
        # Case one or several matches, sort by length #
        matched_rows = self.species_to_density[selector]
        genera_found = list(matched_rows['genus'].unique())
        genera_found = sorted(genera_found, key=len, reverse=True)
        genus_name   = genera_found[0]
        # Check for the species now #
        selector   = self.species_to_density['genus'] == genus_name
        genus_rows = self.species_to_density[selector]
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

    @property_cached
    def latin_mapping(self):
        """Assign a species and genus to each latin name."""
        # Load #
        all_latin_names = pandas.Series(self.stock_comp['latin_name'].unique())
        # Mapping table #
        result = all_latin_names.map(self.latin_to_genus_species)
        # Unzip #
        genus, species = list(zip(*result))
        # Make data frame #
        result = pandas.DataFrame({'latin_name': all_latin_names,
                                   'genus':      genus,
                                   'species':    species})
        # Return #
        return result

    @property_cached
    def stock_density(self):
        """Join stock_comp with latin_mapping and density."""
        # Join 1 #
        result = self.stock_comp.left_join(self.latin_mapping, on='latin_name')
        # Join 2 #
        result = result.left_join(self.species_to_density, on=['genus', 'species'])
        # Reorder columns #
        cols = ['country', 'year', 'rank', 'genus', 'species',
                'latin_name', 'growing_stock', 'density']
        result = result[cols]
        # Sort the dataframe #
        result = result.sort_values(by=['country', 'year', 'rank'])
        # Return #
        return result

    def collapse(self, subdf):
        """
        Function used to compute each extra row (used below).
        Takes a dataframe and returns dataframe.
        """
        # Reset the index #
        subdf = subdf.reset_index(drop=True)
        # Parse the country and year #
        country = subdf.loc[0, 'country']
        year    = subdf.loc[0, 'year']
        # Select all unassigned except total #
        selector    = (subdf['density'] != subdf['density']) & \
                      (subdf['rank']    != 'total')
        # Save the unassigned elsewhere #
        unassigned  = subdf[selector].copy()
        # Drop the unassigned in the main dataframe #
        subdf       = subdf[~selector].copy()
        # Sum the unassigned #
        unass_stock = unassigned['growing_stock'].sum()
        # Add a 'remaining' row with the unassigned stock #
        row = pandas.Series({'country':      country,
                             'year':         year,
                             'rank':         'remaining',
                             'latin_name':   'remaining',
                             'species':      'missing',
                             'genus':        'missing',
                             'growing_stock': unass_stock,
                             'density':       numpy.NaN})
        # Can only append a Series if ignore_index=True #
        subdf = subdf.append(row, ignore_index=True)
        # Return #
        return subdf

    @property_cached
    def stock_collapsed(self):
        """Collapse the unmatched into remaining."""
        # Group #
        groups = self.stock_density.groupby(['country', 'year'])
        # Apply #
        result = groups.apply(self.collapse)
        # Drop index #
        result = result.reset_index(drop=True)
        # Return #
        return result

    def sanity_check(self):
        """
        Recompute the total from the composition and see if
        it matches with the original total.
        """
        # Totals by country and year -- from their calculation #
        theirs = self.stock_collapsed.query('rank=="total"')
        theirs = theirs[['country', 'year', 'rank', 'growing_stock']]
        theirs = theirs.reset_index(drop=True)
        # Totals by country and year -- from our calculation #
        groups = self.stock_collapsed.groupby(['country', 'year'])
        # Dataframe to dataframe function #
        def sanity_check_total(subdf):
            # Reset the index #
            subdf = subdf.reset_index(drop=True)
            # Parse the country and year #
            country = subdf.loc[0, 'country']
            year    = subdf.loc[0, 'year']
            # Select all except total #
            selector  = (subdf['rank']    != 'total')
            # Save the unassigned elsewhere #
            all_stock = subdf[selector].copy()
            # Sum the unassigned #
            total     = all_stock['growing_stock'].sum()
            # Add a 'remaining' row with the unassigned stock #
            return pandas.Series({'country':      country,
                                  'year':         year,
                                  'rank':         'total',
                                  'growing_stock': total})
        # Apply #
        ours = groups.apply(sanity_check_total)
        # Drop index #
        ours = ours.reset_index(drop=True)
        # Compare #
        their_years = theirs[['country', 'year']]
        our_years   = ours[['country',   'year']]
        their_years = set(map(tuple, their_years.values.tolist()))
        our_years   = set(map(tuple, our_years.values.tolist()))
        print(their_years ^ our_years)
        # Check #
        their_rows = theirs.iterrows()
        our_rows   = ours.iterrows()
        # Loop #
        for x, y in zip(their_rows, our_rows):
            i = x[0]
            j = y[0]
            row_theirs = x[1]
            row_ours   = y[1]
            assert row_ours['country'] == row_theirs['country']
            assert row_ours['year']    == row_theirs['year']
            country     = row_ours['country']
            year        = row_ours['year']
            our_stock   = row_ours['growing_stock']
            their_stock = row_theirs['growing_stock']
            #if our_stock == 0.0: continue
            if not numpy.allclose(our_stock, their_stock, rtol=0.01):
                print(country, year)
                print(our_stock, their_stock)

    def compute_avg_density(self, subdf):
        """
        Function used to compute each row (used below).
        Takes a dataframe and returns a row.
        """
        # Reset the index #
        subdf = subdf.reset_index(drop=True)
        # Parse the country and year #
        country = subdf.loc[0, 'country']
        year    = subdf.loc[0, 'year']
        # Parse the remaining and total #
        remaining = subdf.query("rank=='remaining'")['growing_stock'].iloc[0]
        total     = subdf.query("rank=='total'")['growing_stock'].iloc[0]
        # Discard those with no remaining #
        if remaining == 0.0: return None
        # Select all assigned #
        selector     = (subdf['density'] == subdf['density'])
        all_assigned = subdf[selector].copy()
        # Discard those with no assigned #
        if len(all_assigned) == 0: return None
        # Average with weights #
        weights     = all_assigned["growing_stock"]
        avg_density = numpy.average(all_assigned["density"], weights=weights)
        # Fraction #
        total_assigned = all_assigned['growing_stock'].sum()
        frac_missing   = 1.0 - (total_assigned / total)
        # Add a 'remaining' row with the unassigned stock #
        row = pandas.Series({'country':      country,
                             'year':         year,
                             'avg_density':  avg_density,
                             'frac_missing': frac_missing})
        # Return #
        return row

    @property_cached
    def avg_densities(self):
        """Add the average density and fraction missing columns."""
        # Groups #
        groups = self.stock_collapsed.groupby(['country', 'year'])
        # Apply #
        result = groups.apply(self.compute_avg_density)
        # Drop NaN #
        result = result.dropna()
        # Drop index #
        result = result.reset_index(drop=True)
        # Return #
        return result

    #----------------------------- Interpolation -----------------------------#
    def resample_year(self, subdf, lower=None, upper=None):
        """Resample a sub-dataframe on the year column."""
        # Computer lower bound #
        if lower is None: lower = int(subdf['year'].min())
        # Compute upper bound #
        if upper is None: upper = int(subdf['year'].max())
        # Add rows with NaNs #
        indexed = subdf.set_index(['year'])
        reindex = indexed.reindex(range(lower, upper + 1))
        ixreset = reindex.reset_index()
        # Return #
        return ixreset

    def interpolate_density(self, subdf):
        """Interpolate the values of a sub-dataframe on the density column."""
        # Process #
        subdf['avg_density'] = subdf['avg_density'].interpolate(method='linear')
        # Return #
        return subdf

    def pad_density(self, subdf):
        """Pad the values of a sub-dataframe on the density column."""
        # Process #
        subdf['avg_density'] = subdf['avg_density'].fillna(method='ffill')
        subdf['avg_density'] = subdf['avg_density'].fillna(method='bfill')
        # Return #
        return subdf

    @property_pickled
    def avg_dnsty_intrpld(self):
        """
        Take the average densities and calculate missing years
        by interpolation strategy.

        Years available are:   1990, 2000, 2005, 2010.
        We will extend to the: 1980 - 2020 range.

        Years that are found within the known interval, will be interpolated
        with the linear method.

        The edges, or years that are outside the interval for which we have
        data will be interpolated using the pad method (i.e. edges will be
        assumed constant).
        """
        # Load #
        result = self.avg_densities
        # Apply first resample #
        groups = result.groupby(['country'])
        result = groups.apply(self.resample_year)
        result = result.drop(columns=['country'])
        result = result.reset_index()
        result = result.drop(columns=['level_1'])
        # Apply first interpolation #
        groups = result.groupby(['country'])
        result = groups.apply(self.interpolate_density)
        # Apply second resample #
        groups = result.groupby(['country'])
        result = groups.apply(self.resample_year, lower=1980, upper=2021)
        result = result.drop(columns=['country'])
        result = result.reset_index()
        result = result.drop(columns=['level_1'])
        # Apply second interpolation #
        groups = result.groupby(['country'])
        result = groups.apply(self.pad_density)
        # Return #
        return result

###############################################################################
# Create a singleton #
cache_path       = cache_dir + 'soef/composition/'
composition_data = CompositionData(cache_path)