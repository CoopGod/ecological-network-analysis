# Ecological Network Testing: Data & Tools
---
# PURPOSE
This purpose of the data and tools provided in this repository is to provide insight into the dyanmic coupling between species pairs on the basis of ecological network distance.

It has been designed in a way that it can be modified and run to further analyze the data in ways which I have not, or to gain further insight into my findings.

# DATA
There are 3 sets of inital data that are important to understand regarding this project:
### ABMI Data
This data is from [ABMI](https://abmi.ca/abmi-home/data-resources/data-portal-main.html), compiled by ABMI's Information Coordinator, Brett Bodeux.
It is a set of data from ABMI's Autonomous Recording Units's located in the boreal region of Alberta, and other accessory data.
### Interaction Data
This data is from [A Trophic and Non-Trophic Seasonal Interaction Network Reveals Potential Management Units and Functionally Important Species](https://doi.org/10.1111/geb.13940). It is a collection of all noted interactions between species across the boreal region of North America.

### Boreal Alberta Species Data
This data is compiled by myself. It is a list of all species in the boreal region of Alberta. The species are separated into multiple groups:
- 0: Not present in the boreal region of Alberta in the summer.
- 1: present in the boreal region of Alberta in the summer.
- 2: migratory over boreal region of Alberta, so not necessarily present within sampling months or for extended time.
- 3: grouped species for use with the Interaction data previously mentioned.

# WALKTHROUGH
To be successful in this walkthrough, **SQLite3 (ver. >= 3.49)** and **Python (ver. >= 3.12)** must be installed on your machine. Also, ensure that all of the files in the zipped `init_data` folder are extracted and placed in unzipped `init_data` folder.
To prepare the data for analysis, the following commands must be run a terminal whose current working directory is this folder:

Firstly, create a database and upload the inital information:
- `sqlite3 data_analysis.db` to enter SQLite3's command interface
- `.import 'init_data/abmi.csv' Abmi --csv`
- `.import 'init_data/boreal_alberta.csv' BorealAlberta --csv`
- `.import 'init_data/interaction_data.csv' Interactions --csv`

Next, we need to use the given data to create species pairs found in the boreal region of Alberta and prepare to assign Spearman's correlations to them:
- `.read 'sql_queries/species_pair_interactions.sql'`
  - Note: remove the last query in this script to calculate a trophic network, as opposed to a combined network
- `.read 'sql_queries/species_pair_counts.sql'`
  - Note: the final query in this script can be altered to change the variable by which the species pairs are filtered (i.e. location, year, etc.) and the magnitude of the filtering. In this case, the data only includes where (species_pair, location) is found more than 3 times in a given *year* (year being the filtering variable).
- `.quit` to exit SQLite3's command interface
- `sqlite3 -header -csv data_analysis.db 'SELECT * FROM FilteredSpeciesPairs;' > 'generated_data/pair_counts.csv'`

Now, we will assign Spearman's correlations to the species counts we have generated and add it to the database:
- `python spearmans.py`
  - **Note: this process takes time. Allow the program multiple minutes to run**.
  - Note: the global variable GROUPING_VARIABLE in this script can be altered to change the varible by which the species pairs are grouped in the Spearman's correlations. This must be combined with the changes to species_pair_counts.sql to work as intended.
  - Note: the global variable FILTERING_VARIABLE can be changed as well, in accordance with the above note.
- `sqlite3 data_analysis.db` to enter SQLite3's command interface
- `.import 'generated_data/pair_spearmans.csv' PairSpearmans --csv`

Finally, we will assign the uncalculated network distances to this data:
- `.read 'sql_queries/species_network.sql'`
- `.quit` to exit SQLite3's command interface
- `sqlite3 -header -csv data_analysis.db 'SELECT * FROM SpearmansDistancePairs;' > 'generated_data/interaction_and_spearmans.csv'`
- `python network.py`

Which ouputs a file located in the generated_data folder called ***completed_network_data.csv*** which contains all species pairs in the boreal region of Alberta, their Spearman's correlations, and ecological interaction network distance.
