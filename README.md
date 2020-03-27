[![PyPI version](https://badge.fury.io/py/forest-puller.svg)](https://badge.fury.io/py/forest-puller)
[![GitHub last commit](https://img.shields.io/github/last-commit/xapple/forest_puller.svg)](https://github.com/xapple/forest_puller/commits/master)
[![GitHub](https://img.shields.io/github/license/xapple/forest_puller.svg)](https://github.com/xapple/forest_puller/blob/master/LICENSE)

# `forest_puller` version 1.2.0

`forest_puller` is a python package for retrieving data concerning forests of European countries. This includes the amount of forested areas, the forest inventory (standing stock), the forest growth rates as well as the forest loss dynamics (disturbances).
 
There are several public data sources accessible online that provide these types of information in various forms and granularity. This package automates the process of scrapping these websites and parsing the resulting csv tables or excel files.

Once `forest_puller` is installed you can easily access forest data through standard python pandas data frames.

## Scope and sources

Currently `forest_puller` provides data for the following 27 EU member states (past and present):

* Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden, United Kingdom

Currently `forest_puller` caches and provides programmatic access to the forest-relevant data from these data sources:

* IPCC (https://tinyurl.com/y474yu9e)
* SOEF (https://dbsoef.foresteurope.org/)
* FAOSTAT (http://www.fao.org/faostat/en/)
* HPFFRE (https://doi.org/10.5061/dryad.4t880qh)

What other data source you would like to see added here? Contact the authors by opening an issue in the issue tracker.

## Installing

`forest_puller` is a python package and hence is compatible with all operating systems: Linux, macOS and Windows. The only prerequisite is python3 which is often installed by default. Simply type the following on your terminal:

    $ pip3 install --user forest_puller

Or if you want to install it for all users of the system:

    $ sudo pip3 install forest_puller

If you do not have `pip` on your system you can usually get it with these commands (fresh Ubuntu 18LTS):

    sudo apt-get update
    sudo apt-get install python3-distutils
    curl -O https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py --user

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

To get a large data frame with all years and all countries inside:

```python
from forest_puller.ipcc.concat import df
print(df)
```

## Cache

When you import `forest_puller`, we will check the `$FOREST_PULLER_CACHE` environment variable to see where to download and store the cached data. If this variable is not set, we will default to the platform's temporary directory and clone a repository there. This could result in re-downloading the cache after every reboot.

## Data sources

### IPCC

To access the same forest data directly from the IPCC website without the use of `forest_puller`, you would have to first select your country of interest from the CRF country table in a browser at [this address](https://tinyurl.com/y474yu9e).

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

### Forest Europe (SOEF)

This data is provided by the "Ministerial Conference on the Protection of Forests in Europe" and is accessible at: https://dbsoef.foresteurope.org/

Three tables are provided for every country:

* Table 1.1a: Forest area
* Table 1.3a1: Age class distribution (area of even-aged stands)
* Table 3.1: Increment and fellings

It is accessed in a similar way to other data sources:

```python
from forest_puller.soef.country import countries

country = countries['AT']
print(country.forest_area.indexed)
print(country.age_dist.indexed)
print(country.fellings.indexed)
```

There is also a large data frame containing all countries concatenated together:

```python
from forest_puller.soef.concat import tables
print(tables['forest_area'])
print(tables['age_dist'])
print(tables['fellings'])
```

### Faostat (forestry)

This data is acquired by picking the "All Data Normalized" option from the "Bulk download" sidebar at this address: http://www.fao.org/faostat/en/#data/FO

It is accessed in a similar way to other data sources:

```python
from forest_puller.faostat.forestry.country import countries

country = countries['AT']
print(country.df)
```

There is also a large data frame containing all countries concatenated together:

```python
from forest_puller.faostat.forestry.concat import df
print(df)
```

### Faostat (land)

This data is acquired by picking the "All Data Normalized" option from the "Bulk download" sidebar at this address: http://www.fao.org/faostat/en/#data/GF

It is accessed in a similar way to other data sources:

```python
from forest_puller.faostat.land.country import countries

country = countries['AT']
print(country.df)
```

There is also a large data frame containing all countries concatenated together:

```python
from forest_puller.faostat.land.concat import df
print(df)
```

### Diabolo (hpffre)

Was a project run by a consortium of 33 partners from 25 countries. Experts in the fields of policy analysis, forest inventory, forest modelling. 7 work packages.

 Link: http://diabolo-project.eu/

One of the outcomes of the Diabolo project is the following publication:

Vauhkonen et al. 2019 - [Harmonised projections of future forest resources in Europe](https://doi.org/10.1007/s13595-019-0863-6)

Abbreviated "hpffre". The authors used EFDM (mainly) to project forest area, growing stock, fellings and above ground carbon for European countries. There are several scenario outcomes.

The dataset is available at: https://doi.org/10.5061/dryad.4t880qh

It is accessed in a similar way to other data sources:

```python
from forest_puller.hpffre.country import countries

country = countries['AT']
print(country.df)
```

There is also a large data frame containing all countries concatenate together:

```python
from forest_puller.hpffre.concat import df
print(df)
```

## Visualizations

The `forest_puller` package can also generate several plots that enable the user to compare and visualize the data.

For instance here is are a series of graphs comparing the total reported forest area between data sources as seen in the `forest_puller.viz.area` submodule:

![Comparison of total forest area](documentation/viz/area/area.svg?sanitize=true "Comparison of total forest area")

Another type of graph that can be produced is the comparison of gains and losses across several data-sources and across countries. This code is found in the `forest_puller.viz.increments` submodule and shows the five largest countries in terms of forest area.

![Comparison of increments for SE](documentation/viz/increments/SE.svg?sanitize=true "Comparison of increments for SE")
![Comparison of increments for FR](documentation/viz/increments/FR.svg?sanitize=true "Comparison of increments for FR")
![Comparison of increments for FI](documentation/viz/increments/FI.svg?sanitize=true "Comparison of increments for FI")
![Comparison of increments for ES](documentation/viz/increments/ES.svg?sanitize=true "Comparison of increments for ES")
![Comparison of increments for DE](documentation/viz/increments/DE.svg?sanitize=true "Comparison of increments for DE")

With data from the SOEF source, we can also plot a breakdown of the growing stock volume genus composition of many countries across time. This code is found in the `forest_puller.viz.increments` submodule.

![Comparison of genus breakdown](documentation/viz/genus/AT_BE_BG_HR_CY.svg?sanitize=true "Comparison of genus breakdown")
![Comparison of genus breakdown](documentation/viz/genus/CZ_DK_EE_FI_FR.svg?sanitize=true "Comparison of genus breakdown")
![Comparison of genus breakdown](documentation/viz/genus/DE_HU_IE_IT_LV.svg?sanitize=true "Comparison of genus breakdown")
![Comparison of genus breakdown](documentation/viz/genus/LT_NL_PL_PT_RO.svg?sanitize=true "Comparison of genus breakdown")
![Comparison of genus breakdown](documentation/viz/genus/SK_SI_ES_SE_GB.svg?sanitize=true "Comparison of genus breakdown")
![Genera legend](documentation/viz/genus/legend.svg?sanitize=true "Genera legend")