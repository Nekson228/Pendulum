import numpy as np


def angular_acceleration(theta: float, length: float, g: float) -> float:
    # differential equation for the angular acceleration of the pendulum
    return -g / length * np.sin(theta)


def angular_velocity(omega: float) -> float:
    return omega
