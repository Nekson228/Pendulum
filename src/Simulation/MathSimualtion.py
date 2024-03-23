import numpy as np
from typing import Iterator


class MathSimulation:
    def __init__(self, omega_0: float, theta_0: float, t_max: float, g: float, l: float, step: float):
        self._omega_0 = omega_0
        self._theta_0 = theta_0
        self._t_max = t_max
        self._g = g
        self._l = l
        self._step = step

    def run(self) -> Iterator[tuple[float, float, float]]:
        nat_freq = np.sqrt(self._g / self._l)

        def theta(t: float, ) -> float:
            return self._theta_0 * np.cos(nat_freq * t) + self._omega_0 / nat_freq * np.sin(nat_freq * t)

        def omega(t: float) -> float:
            return -nat_freq * self._theta_0 * np.sin(nat_freq * t) + self._omega_0 * np.cos(nat_freq * t)

        t = 0
        while t <= self._t_max:
            yield float(t), theta(t), omega(t)
            t += self._step
