import numpy as np


def is_not_null(s):
    return s.isnull().apply(np.logical_not)


def weighted_mean(col, weight_col):
    """
    Return a function to calculate the weighted mean of a column in a DataFrame
    based on weights from another column.
    """
    def _weighted_mean(df):
        weighted_sum =  (df[col]
                           .mul(df[weight_col])
                           .sum())

        total_weight = (df[col]
                          .pipe(is_not_null)
                          .mul(df[weight_col])
                          .sum())

        return weighted_sum / total_weight

    return _weighted_mean
