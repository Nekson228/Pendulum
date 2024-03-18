import numpy as np
import pytest

from src.RungeKuttaTable.Table import Table


def test_parser():
    n_steps, rk_coefficients, weights = Table._parse_butcher('../data/Methods/Euler.txt')
    assert n_steps == 1
    assert rk_coefficients.size == 0
    assert weights == [1.]


def test_parser2():
    n_steps, rk_coefficients, weights = Table._parse_butcher('../data/Methods/Midpoint.txt')
    assert n_steps == 2
    assert np.all(rk_coefficients == [.5])
    assert np.all(weights == [0., 1.])


def test_table():
    table = Table('../data/Methods/Euler.txt')
    assert table.s == 1
    assert np.all(table.weights == [1.])
    with pytest.raises(ValueError):
        table.get_rk_row(2)
    with pytest.raises(ValueError):
        table.get_rk_row(0)


def test_table2():
    table = Table('../data/Methods/RungeKutta4.txt')
    assert table.s == 4
    assert np.all(table.weights == [0.166666667, 0.333333333, 0.333333333, 0.166666667])
    assert np.all(table.get_rk_row(2) == [1./2])
    assert np.all(table.get_rk_row(3) == [0., 1./2])
    assert np.all(table.get_rk_row(4) == [0., 0., 1.])


