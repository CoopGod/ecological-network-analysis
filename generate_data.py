"""
Purpose: This program consolidates the prior SQL queries and calculations into one script. The
    program generates a dataframe of an pairwise species' spearman's correlations and the pair's network distance,
    separated by year.
Author: Cooper Goddard
Date: April 7, 2026
"""

# external imports
import pandas as pd
import sqlite3
import os
import time

# internal imports
import spearmans
import network

# Global File Names
DB_FILE = "./data_analysis.db"
INTERACTION_FILE = "./init_data/interaction_data.csv"
SPECIES_LIST_FILE = "./init_data/boreal_alberta.csv"
ABMI_FILE = "./init_data/abmi.csv"
INTERACTIONS_SQL = "./sql_queries/species_pair_interactions.sql"
COUNTS_SQL = "./sql_queries/species_pair_counts.sql"
NETWORK_SQL = "./sql_queries/species_network.sql"
NETWORK_FILE_OUT = ""
DATA_FILE_OUT = "./completed_data/out.csv"
# Global Column Names (should remain constant unless changing the operation of the script)
BASE_VARIABLE = (
    "species_pair"  # Expected to be a pair structured: 'Obj1-Obj2' where Obj1 < Obj2
)
BV_COUNT_1 = "first_count"
BV_COUNT_2 = "second_count"
DISTANCE_NAME = "distance"
SPECIES_PAIR_NAME = "species_pair_nn"
# Testing Globals
COLLAPSING_VARIABLE = "lid"
GROUPING_VARIABLE = "year"
DO_NETWORK_VISUALIZATION = False


def main():
    print("Creating DB and uploading initial data...")
    start = time.time()
    # create fresh database
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    db = sqlite3.connect(DB_FILE)

    # import external data (species list, ABMI data, interactions)
    pd.read_csv(ABMI_FILE).to_sql(
        "Abmi", db, if_exists="replace", index=False
    )
    pd.read_csv(SPECIES_LIST_FILE).to_sql(
        "BorealAlberta", db, if_exists="replace", index=False
    )
    pd.read_csv(INTERACTION_FILE).to_sql(
        "Interactions", db, if_exists="replace", index=False
    )
    print(f"Finished creating DB and uploading initial data in {time.time() - start}.")

    print("Generating pairwise interactions and counts...")
    start = time.time()
    # generate all possible pairwise interactions
    with open(INTERACTIONS_SQL, "r") as f:
        sql_script = f.read()
    db.executescript(sql_script)
    db.commit()

    # generate pairwise counts
    with open(COUNTS_SQL, "r") as f:
        sql_script = f.read()
    db.executescript(sql_script)
    db.commit()
    print(f"Finished generating pairwise interactions and counts in {time.time() - start}.")


    # calculate spearmans values
    print("Calculating Spearman's values...")
    start = time.time()
    df = pd.read_sql_query("SELECT * FROM FilteredSpeciesPairs", db)
    new_df = (
        df.groupby([BASE_VARIABLE, GROUPING_VARIABLE])
            .apply(
                spearmans.calculateSpearmans,
                col1=BV_COUNT_1,
                col2=BV_COUNT_2,
                col_name=COLLAPSING_VARIABLE,
                include_groups=False
                )
            .reset_index()
    )
    new_df.to_sql("PairSpearmans", db, if_exists="replace", index=False)
    print(f"Finished calculating Spearman's values in {time.time() - start}.")


    # combine spearmans data with interaction data
    print("Combining Spearman's and interaction data...")
    start = time.time()
    with open(NETWORK_SQL, "r") as f:
        sql_script = f.read()
    db.executescript(sql_script)
    db.commit()
    print(f"Finished combining Spearman's and interaction data in {time.time() - start}")
    
    print("Generating network distances...")
    start = time.time()
    # use network to generate network distances
    df = pd.read_sql_query("SELECT * FROM SpearmansDistancePairs", db)
    nodes = network.initalizeZeroDistanceNodes(
        df, DISTANCE_NAME, SPECIES_PAIR_NAME
    )  # init 0 distance nodes
    if (
        DO_NETWORK_VISUALIZATION
    ):  # if flag is active, then output the network visualization, otherwise skip.
        network.createNetworkVisualizer(nodes)
    new_df = network.calculateNetworkDistances(
        df, nodes, DISTANCE_NAME, SPECIES_PAIR_NAME
    )  # find distances for others
    print(f"Finished generating network distances in {time.time() - start}.")

    # output network to file
    new_df.to_csv(DATA_FILE_OUT)

if __name__ == "__main__":
    main()
