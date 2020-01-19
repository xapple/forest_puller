[![PyPI version](https://badge.fury.io/py/forest_puller.svg)](https://badge.fury.io/py/forest_puller)
[![GitHub last commit](https://img.shields.io/github/last-commit/xapple/forest_puller.svg)](https://github.com/xapple/forest_puller/commits/master)
[![GitHub](https://img.shields.io/github/license/xapple/forest_puller.svg)](https://github.com/xapple/forest_puller/blob/master/LICENSE)

# `forest_puller` version 1.0.2

`forest_puller` is a package for retrieving data concerning forests on the European continent. This includes forest growth rates, amount of forested areas and forest inventory (standing stock).

There are several public data sources that are accessible online to retrive this type of information. This package will automate the process of scrapping these website and parsing the resulting excel files.

Once `forest_puller` is installed you can easily access forest data through standard pandas data frames.

## Installing

`forest_puller` is a python package and hence is compatible with all operating systems: Linux, macOS and Windows. Once python 3 is installed on your computer, if it is not already, simply type the following on your terminal:

    $ pip3 install --user forest_puller

Or if you want to install it for all users of the system:

    $ sudo pip3 install forest_puller

## Usage

For instance to retrieve the net carbon dioxide emission of Austria in 2017 that were due to *coniferous* forest land from the IPCC official data source, you can do the following:

```python
# Import #
from forest_puller.ipcc.country import countries

# Get the country #
austria = countries['AT']

# Get the 2017 indexed dataframe #
at_2017 = austria.years[2017].indexed

# Print some data #
print(at_2017.loc['remaining_forest', 'Coniferous']['net_co2'])
```

     904282.4970403439

To see what information is available you can of course display the column titles and row indexes of that data frame:

```python
print(at_2017.columns)

#Index(['area', 'area_mineral', 'area_organic', 'biomass_gains_ratio',
#       'biomass_losses_ratio', 'biomass_net_change_ratio', 'net_dead_ratio',
#       'net_litter_ratio', 'net_mineral_soil_ratio', 'net_organic_soil_ratio',
#       'biomass_gains', 'biomass_losses', 'biomass_net_change', 'net_dead',
#       'net_litter', 'net_mineral_soils', 'net_organic_soils', 'net_co2'],
#      dtype='object', name='category')

print(at_2017.index)

# MultiIndex(levels=[['cropland_to_forest', 'grassland_to_forest',
# 'land_to_forest', 'other_land_to_forest', 'remaining_forest',
# 'settlements_to_forest', 'total_forest', 'wetlands_to_forest'],
# ['', 'Coniferous', 'Deciduous', 'Forest not in yield', 'Total']])
```

To examine what countries and what years are available:

```python
print(list(c.iso2_code for c in countries.values()))

# ['AT', 'BE', 'BG', 'HR', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR',
# 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI',
# 'ES', 'SE', 'GB', 'ZZ']

print(list(y for y in austria.years))
# [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000,
# 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
# 2013, 2014, 2015, 2016, 2017]
```

## Data sources

### IPCC

To download the forest data from the IPCC you would have to ...

### More sources to be added in the future

Stay tuned.
