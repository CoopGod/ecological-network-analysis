'''
Purpose: This program consolidates the prior SQL queries and calculations into one script. The
    program generates a dataframe of an pairwise species' spearman's correlations and the pair's network distance,
    separated by year.
Author: Cooper Goddard
Date: April 7, 2026
'''

import pandas as pd
import sqlite3
import os

DB_FILE = 'data_analysis.db'
INTERACTION_FILE = ''
SPECIES_LIST_FILE = ''
ABMI_FILE = ''
INTERACTIONS_SQL = ''
COUNTS_SQL = ''

# create fresh database
if (os.path.exists(DB_FILE)):
    os.remove(DB_FILE)
db = sqlite3.connect(DB_FILE)

# import external data (species list, ABMI data, interactions)
abmi_data = pd.read_csv(ABMI_FILE).to_sql('Abmi', db, if_exists='replace', index=False)
species_list_data = pd.read_csv(SPECIES_LIST_FILE).to_sql('BorealAlberta', db, if_exists='replace', index=False)
interaction_data = pd.read_csv(INTERACTION_FILE).to_sql('Interactions', db, if_exists='replace', index=False)

# generate all possible pairwise interactions
with open(INTERACTIONS_SQL, 'r') as f:
    sql_script = f.read()
db.execute(sql_script)
db.commit()

# generate pairwise counts 
with open(COUNTS_SQL, 'r') as f:
    sql_script = f.read()
db.execute(sql_script)
db.commit()
