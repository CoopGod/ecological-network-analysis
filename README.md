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
To be successful in this walkthrough **Python (ver. >= 3.12)** must be installed on your machine. Also, ensure that all of the files in the zipped `init_data` folder are extracted and placed, unzipped, in a `init_data` folder.
To prepare the data for analysis, the following commands must be run a terminal whose current working directory is the base folder of this repository:

1. Simply type `pip install requirements.txt` (this need only be done once per installation of this package)
2. Then type `python generate_data.py` to run the program...

This  ouputs a file located in the generated_data folder called ***out.csv*** which contains all species pairs in the boreal region of Alberta, their Spearman's correlations, and ecological interaction network distance.

Coming soon: 
- options to change the filtering and such!
- terminal colours!
- optimizations for the final SQL script to speed that up (indexing to avoid O(n^2))

# FUTURE RESEARCH
## CORRELATIONS OVER TIME
An interesting application of this reserach would be to recompute the Spearman's correlations over time. This might help to account for some of the noise seen in my research.
I was not able to do this because ABMI did not have the data of repeat visits at particular sites, though I have been told this ABMI is working to collect this data.

In preparation for this data, I have included some queries that would help a future researcher quickly get calculations:
- `sql_queries/future_queries/species_pair_counts_over_time.sql` would replace `sql_queries/species_pair_counts` in the walk through to group the data by sites instead of years
- in `spearmans.py`, swapping the filtering and grouping variable would allow of Spearman's to be calculated over time.
- `sql_queries/future_queries/species_network_over_time.sql` would replace `sql_queries/species_network.sql` in the walk through to combine this new data we have just calculated
