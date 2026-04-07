"""
Purpose: This program calculates Spearman's correlations on a base varible over a restricting variable
Author: Cooper Goddard
Date: April 21, 2025
"""

import pandas
import numpy as np
from scipy.stats import spearmanr


def calculateSpearmans(
    group: pandas.DataFrame,
    col1: str,
    col2: str,
    col_name: str
) -> pandas.Series:
    """
    This function calculates spearmans correlations on the base_variable counts over the groups of grouping_variable.

    :param group: a mini-dataframe based on the grouping of the base variable and grouping variable
    :param col1: the first column on which the spearmans are calculated
    :param col2: the second column on which the spearmans are calculated
    :param col_name: the name of the collapsing variable
    """
    v1 = group[col1].values
    v2 = group[col2].values

    if np.ptp(v1) > 0 and np.ptp(v2) > 0:
        rho, p = spearmanr(v1, v2)
    else:
        rho, p, = 0, 0

    return pandas.Series({
        'spearmans': rho,
        'p_value': p,
        f"{col_name}_count": len(group)
    })
