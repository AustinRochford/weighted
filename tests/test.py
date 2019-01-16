from hypothesis import example, given
from hypothesis.extra.numpy import arrays, array_shapes
from hypothesis.strategies import composite, floats, integers, sampled_from
import unittest

import numpy as np
import pandas as pd

from weighted import weighted_mean


shape_st = array_shapes(max_dims=1)
float_st = floats()


def val_st(shape=shape_st, elements=float_st):
    return arrays(np.float64, shape, elements=elements)


@composite
def dup_val_st(draw, shape_st=shape_st, n_uniq_val=None):
    shape = draw(shape_st)

    if n_uniq_val is None:
        n_uniq_val = draw(integers(1, max_value=shape[0]))

    # groupby doesn't play nicely with nan and inf
    finite_float_st = floats(allow_nan=False, allow_infinity=False)
    uniq_val = draw(val_st(shape=n_uniq_val, elements=finite_float_st))
    val = draw(val_st(shape=shape, elements=sampled_from(uniq_val)))

    return val


def allclose_with_nan(x, y):
    return (np.isnan(x) & np.isnan(y)) | np.allclose(x, y)


class TestWeightedMean(unittest.TestCase):
    @given(val_st())
    @example(np.array([np.nan]))
    @example(np.arange(10))
    @example(np.array([1, 1, 2, 2]))
    def test_single_element_groups(self, val):
        df = pd.DataFrame({'val': val, 'weight': 1})
        
        mean = df['val'].mean()
        weighted_mean_ = df.pipe(weighted_mean('val', 'weight'))

        assert allclose_with_nan(mean, weighted_mean_)

    @given(dup_val_st())
    @example(np.arange(10))
    @example(np.array([1, 1, 2, 2]))
    def test_groups(self, val):
        df = pd.DataFrame({'val': val})
        weighted_df = (df.groupby('val')
                         .size()
                         .rename('weight')
                         .reset_index())
        
        mean = df['val'].mean()
        weighted_mean_ = weighted_df.pipe(weighted_mean('val', 'weight'))
        
        assert allclose_with_nan(mean, weighted_mean_)
