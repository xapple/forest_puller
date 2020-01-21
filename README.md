[![PyPI version](https://badge.fury.io/py/forest_puller.svg)](https://badge.fury.io/py/forest_puller)
[![GitHub last commit](https://img.shields.io/github/last-commit/xapple/forest_puller.svg)](https://github.com/xapple/forest_puller/commits/master)
[![GitHub](https://img.shields.io/github/license/xapple/forest_puller.svg)](https://github.com/xapple/forest_puller/blob/master/LICENSE)

# `forest_puller` version 1.1.0

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

# Index(['area', 'area_mineral', 'area_organic', 'biomass_gains_ratio',
#        'biomass_losses_ratio', 'biomass_net_change_ratio', 'net_dead_ratio',
#        'net_litter_ratio', 'net_mineral_soil_ratio', 'net_organic_soil_ratio',
#        'biomass_gains', 'biomass_losses', 'biomass_net_change', 'net_dead',
#        'net_litter', 'net_mineral_soils', 'net_organic_soils', 'net_co2'],
#        dtype='object', name='category')

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

To access the same forest data directly from the IPCC without `forest_puller` you would have to first select your country from the CRF country table in a browser.

![IPCC demo screenshot 1](documentation/ipcc/ipcc_demo_1.png?raw=true "IPCC demo screenshot 1")

Then you would have to manually download the zip file for that specific country through another page.

![IPCC demo screenshot 2](documentation/ipcc/ipcc_demo_2.png?raw=true "IPCC demo screenshot 2")

Next, you would have to uncompress the zip file and locate the xls file that concerns the year you are interested in.

![IPCC demo screenshot 4](documentation/ipcc/ipcc_demo_4.png?raw=true "IPCC demo screenshot 4")

Finally you would have to scroll to the right sheet in your spreadsheet software and find the pertinent cell.

![IPCC demo screenshot 5](documentation/ipcc/ipcc_demo_5.png?raw=true "IPCC demo screenshot 5")


This operation would have to be repeated for every country, and every year you are interested in.

With `forest_puller` you can easily display any information you want for all countries at the same time:

```python
from forest_puller.ipcc.country import countries

category, key = ['total_forest', 'biomass_net_change']
biomass_net_change = {
    k: c.last_year.indexed.loc[category, ''][key]
    for k,c in countries.items()
}

import pprint
pprint.pprint(biomass_net_change)
```

    {'AT': 1367857.0940855271,
     'BE': 374245.08695361385,
     'BG': 2192942.031982918,
     'CZ': 387870.89395249996,
     'DE': 12317598.87352293,
     'DK': -216454.31026543948,
     'EE': 320710.2459538891,
     'ES': 8917649.261547482,
     'FI': 6603815.0,
     'FR': 15051831.9827214,
     'GB': 2892518.0859005335,
     'GR': 583205.0978272819,
     'HR': 1477791.7578513895,
     'HU': 1259385.5890665338,
     'IE': 1069648.7636722159,
     'IT': 5752883.095908434,
     'LT': 2146933.309581986,
     'LU': 101929.37461705346,
     'LV': 1244965.2120000012,
     'NL': 499021.93968,
     'PL': 9353198.2907701,
     'PT': 1536917.4736652463,
     'RO': 5561343.4405591395,
     'SE': 10185839.738999998,
     'SI': 35391.09710503432,
     'SK': 1184611.3471376207}

### More sources to be added in the future

Stay tuned.
