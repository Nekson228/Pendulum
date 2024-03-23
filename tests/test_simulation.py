from src.RungeKuttaTable.Table import Table
from src.Simulation.PhysSimulation import Simulation
from src.Simulation.PendulumEquations import angular_velocity, angular_acceleration

from functools import partial

import numpy as np


def test_simulation():
    table = Table('../data/Methods/RungeKutta4.txt')
    step = 0.1
    initial_conditions = np.array([0.1, 0], dtype=Table.float_type)
    t0 = 0
    t_max = 10
    sim = Simulation(table, step, initial_conditions, t0, t_max)
    f_acceleration = partial(angular_acceleration, length=1, g=9.81)
    f_velocity = angular_velocity
    result = list(sim.run(f_acceleration, f_velocity))
    assert len(result) == 101
    assert result[0][0] == 0
    assert np.isclose(result[-1][0], 10)

