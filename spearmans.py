"""
Purpose: This program calculates Spearman's correlations on a base varible over a restricting variable
Author: Cooper Goddard
Date: April 21, 2025
"""

import pandas
from scipy.stats import spearmanr
import os


DATA_FILE = "generated_data/pair_counts.csv"
OUTPUT_FILE = "generated_data/pair_spearmans.csv"
BASE_VARIABLE = "species_pair"  # Expected to be a pair structured: 'Obj1-Obj2'
BV_COUNT_1 = "first_count"
BV_COUNT_2 = "second_count"
GROUPING_VARIABLE = "lid"
FILTERING_VARIABLE = "year"


def calculateSpearmans(
    df: pandas.DataFrame,
    base_variable: str,
    base_count_1: str,
    base_count_2: str,
    grouping_variable: str,
    filtering_variable: str,
) -> dict:
    """
    This function calculates spearmans correlations on the base_variable counts over the grouping_variable.

    :param base_variable: the variable in the df on which the Spearman's correlations will be calculated. This variable should be a pair of some sort
    :param base_count_1: the count of the first part of the pair base_variable
    :param base_count_2: the count of the second part of the pair base_variable
    :param grouping_variable: the variable in the df on which the base_variable is split into groups (i.e. by year, location, etc.)
    :param filtering_variable: the variable by which the grouping variable is constrained. (i.e. grouping=location, filtering=year yields spearmans over all locations at given year)
    :returns: a dictionary containing the base_variable Spearman's correlations and other important data
    """
    completed_pairs = (
        {}
    )  # use dictionary as hash map, using 'base_variable-grouping_variable' as candidate key
    for index, row in df.iterrows():
        # calculate spearman correaltions by species pairs in given group of grouping_variable
        if (
            completed_pairs.get(f"{row[base_variable]}-{row[filtering_variable]}", None)
            == None
        ):
            current_pair = df[
                (df[base_variable] == row[base_variable])
                & (df[filtering_variable] == row[filtering_variable])
            ]
            rho, p = spearmanr(current_pair[base_count_1], current_pair[base_count_2])
            # save resulting correlation for later
            completed_pairs[f"{row[base_variable]}-{row[filtering_variable]}"] = {
                base_variable: row[base_variable],
                filtering_variable: row[filtering_variable],
                "spearmans": rho,
                f"{grouping_variable}_count": current_pair.shape[0],
                "p_value": p,
            }
    return completed_pairs


def main() -> None:
    cwd = os.getcwd()
    df = pandas.read_csv(os.path.join(cwd, DATA_FILE), encoding="UTF-16")

    completed_pairs = calculateSpearmans(
        df, BASE_VARIABLE, BV_COUNT_1, BV_COUNT_2, GROUPING_VARIABLE, FILTERING_VARIABLE
    )

    # transform collected spearman correlations into table with species pairs, lid, sample size
    completed_df = pandas.DataFrame(completed_pairs.values())
    completed_df.to_csv(os.path.join(cwd, OUTPUT_FILE))


if __name__ == "__main__":
    main()
