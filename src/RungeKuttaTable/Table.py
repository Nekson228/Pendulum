import numpy as np


class Table:
    float_type = np.float64

    def __init__(self, method_path: str):
        self._s, self._a, self._b = self._parse_butcher(method_path)

    @staticmethod
    def _parse_butcher(method_path: str) -> (int, np.ndarray, np.ndarray):
        with open(method_path, 'r') as file:
            # number s of steps
            n_steps = int(file.readline())
            # preallocating runge-kutta matrix
            # (s - 1) + (s - 2) + ... + 2 + 1 = s * (s - 1) / 2 of coefficients
            rk_coefficients_size = n_steps * (n_steps - 1) // 2
            rk_coefficients = np.zeros((rk_coefficients_size,), dtype=Table.float_type)

            for i in range(n_steps - 1):
                start = i * (i + 1) // 2  # starting at sum of naturals before i
                end = start + i + 1  # exactly i + 1 numbers at each row
                rk_coefficients[start:end] = np.fromiter(file.readline().split(), dtype=Table.float_type, count=i + 1)
            weights = np.fromiter(file.readline().split(), dtype=Table.float_type, count=n_steps)

        return n_steps, rk_coefficients, weights

    def get_rk_row(self, i: int) -> np.ndarray:
        if i > self._s:
            raise ValueError(f"Row {i} is out of bounds for this table")
        elif i < 2:
            raise ValueError(f"Row {i} is not defined for this table")
        # start and end are calculated similarly to _parse_butcher but 2nd coefficient is at 0
        start = (i - 1) * (i - 2) // 2
        end = start + i - 1
        return self._a[start:end]

    @property
    def weights(self):
        return self._b

    @property
    def s(self):
        return self._s
