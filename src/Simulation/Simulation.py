from src.RungeKuttaTable.Table import Table
from typing import Iterator, Callable
from fractions import Fraction

import numpy as np


class Simulation:
    # class to simulate system behaviour using Runge-Kutta method
    def __init__(self, table: Table, step: Fraction, initial_conditions: np.ndarray, t0: float, t_max: float):
        """
        :param table: instance of Runge-Kutta Butcher table
        :param step: step size
        :param initial_conditions: initial conditions of the system
        :param t0: initial time
        :param t_max: final time
        """
        self._table = table
        self._h = step
        self._initial_conditions = initial_conditions
        self._t0 = t0
        self._t_max = t_max

    # method to calculate the next step using Runge-Kutta method
    def _step_rk(self, t: float, y: np.ndarray, f: tuple[Callable[..., float], ...]) -> (float, np.ndarray):
        s = self._table.s
        # preallocating k array
        n_conditions = len(y)
        k = np.zeros((s, *y.shape), dtype=Table.float_type)
        # calculating k1, k2, ..., ks
        for i in range(s):
            for j in range(len(f)):
                k_i = n_conditions - j - 1
                k[i, k_i] = f[j](y[j] + float(self._h) * (self._table.get_rk_row(i + 1) @ k[:i, k_i]))
        # calculating next step
        y = y + float(self._h) * (self._table.weights @ k)
        return t + self._h, y

    # generator to simulate the system
    def run(self, *f: Callable[..., float]) -> Iterator[tuple[float, np.ndarray]]:
        """
        :param f: functions to calculate the derivatives of the system in the order of the initial conditions
        :return: generator of the system state at each time step
        """
        t = self._t0
        y = self._initial_conditions
        while t < self._t_max:
            yield float(t), y
            t, y = self._step_rk(t, y, f)
        yield float(t), y
