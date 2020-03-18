# Done for the project:

* Fix detection of last line

* Decide which ISO3 code
    - DK, take "DNK".
    - BG, take "GBR".
    - FR, take "FRA".

* Fix repetition in `land_use` and `subdivision`

* Row headers, make them all readable

* Convert all units

* Specific NaNs with all combination of identifiers.

* Recompute the line 10 (total) as a sanity check

* Check there are only `float64` columns directly in the package

* Rewrite the sanity check

* Pickle the final df in the cache repository

* Update repositories on gitlab (logos, public)

* Publish also on github

* Rewrite the sample test

* Rewrite the indexed dataframe

* Write the documentation

* Debug the problem with the sanity check

* Add README in puller_cache

* Auto-clone the cache repository on install

* Check the tutorial works on a fresh Ubuntu

* Add new data source: Forest Europe

* Rename columns to short name for soef

* Convert units for soef

* Create pickled df for soef

* Created a large concatenated df for soef

* Write doc for the new data source

* Add data source: faostat (the flag file with all products)

* Add data source: diabolo

* Drop a mail for the extra C++ model

* Check that the FRA faostat matches the classical faostat data for area

* Add data source: faostat forest area

* Refactor: Centralize the import of "country_codes" to one file

* Make area compare visualizations

* Reverse the HPFFRE line

* Make PDF with figure legend

* For each source a separate plot of increment and fellings in unit/ha on total forest area if available otherwise on forest area available for wood supply.

* Check conversion factor for hpffre

* Higher font size for y label in increments

* HPFFRE, make a rolling difference window to estimate the increments

* Remove future values from HPFFRE and remove dotted line.

* Place the zero at the same spot on the Y axis for every graph.

* For EU-CBM the red line: plot `provided_volume` and filter NF.

* For EU-CBM the green line: Plot 'gross_growth_ag'. And remain in tons of carbon.

* For the README add a graph of increments and losses but with only one source so it doesn't take too much space. The country 5 biggest surfaces.

* Cache CBM dataframes.

* Add Cyprus to countries available.

* Table in 1.2c in SOEF can enable us to perform an inter-source check of consistency

* Deal with special case genus is 'pinus'.

* Collapse missing species into remaining.

* Possibly convert the m^3 into net CO2 emission in tons for faostat, ipcc, hpffre.  Strategy for converting volume into tons of carbon:

  - See demand_to_dist in dist_maker.

  - To go from over to under: 0.88 conversion factor. See UNEC.

  - See https://www.unece.org/fileadmin/DAM/timber/publications/DP-49.pdf

  - Tons of dry matter are converted to tons of carbon by applying a 0.5 conversion factor.

    - First get the proportion of species from each country from either FAOSTAT or SOEF. Not sure yet.

    - Then get species-specific conversion coefficients from "IPCC basic wood density of selected tree species"

     - Reference: Chapter 4: Forest Land 2006 IPCC Guidelines for National Greenhouse Gas Inventories 4.71 TABLE 4.14 BASIC WOOD DENSITY (D) OF SELECTED TEMPERATE AND BOREAL TREE TAXA

    - Link: https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_04_Ch4_Forest_Land.pdf   PAGE 71

* Graph of species proportion in each country.

* Conifers (have 4 genera) vs broadleaved could have distinguished colors. Use black for missing. Abies (dark green), picea (dark green), pinus (green), pseudotsuga (light green).

* Manage the case when the species name is the same as another possible genus name (e.g. "picea abies" in finland), the string matching algorithm should favor the first word.

* Make a script for the security group.

* Plot the proportion of genera in CBM also and compare side by side.

* Add species breakdown to README showcase.

* Make a total of all EU countries for area.

* Make a total of all EU countries increments (for soef only some countries, for ipcc only net curve, for faostat start in 2000).

* Make a total of all EU also for genus composition.


# TODO

* The area comparison graph has a different country order: fix.

* Write up introduction and methods.

* Reset the history of the puller_cache repository for faster downloads.

* Switch all text that reads "26 countries" to "27 countries".

* Adapt the CBM-EU fluxes used in gains and losses based on expert input.

* Make predictions based on data acquired?


## Analysis tables

Each table should include for 27 european countries.

* Create statistic that shows (e.g. for the last year available) in form of a table,
  the total surface for the given country and the proportion of that
  that is "available for wood supply",
  for each given source that has this information (SOEF, HPFFRE, FAOSTAT?).

* Export SOEF table "Forest area" and "of which available for wood supply" (aws)
  add a column prop_aws = area_aws / forest_area (important for the discussion).
  
* Maximum forest area in million ha, one column per source
  (see picture of hand-written table)
  
* Maximum forest area in million ha for IPCC and SOEF only.
  Add a column diff_percent = (IPCC_area - SOEF_area) / SOEF_area * 100
  sort by the diff_percent column
  
* Average gains / growth per hectare
  (see picture of hand-written table)
  
* Average losses / harvest per hectare


# Ideas

Example variable descriptions:

    no |  variable |    name_in_ipcc | name_in_faostat | si_unit
    --------------------------------------------------------------------
     1 |      area |     forest area |   area_forested | hectare
     2 | emissions | total emissions |             NaN | tons of carbon


# Obtaining the cache

There are several ways the end-users can get a copy of the cached data upon installation or first use:

- Add to the source code repository directly
- Add to source tarball and upload on pypi with python package
- (+) Clone to `tempfile.gettempdir()`
- Clone to `~/.forest_puller`
- Clone to `__module_dir__` but permission problem if not `--user`
- (+) Force or suggest the setting of `$FOREST_PULLER_CACHE_DIR` environment variable
- Have it download every time to RAM on each python process
- Prompt the user with `input()` to specify a dir and save to a dotfile
- Split up sources into different `puller_cache` repositories
