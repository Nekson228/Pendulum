import argparse as ap
from src.Simulation.Simulation import Simulation
from src.RungeKuttaTable.Table import Table
from src.Simulation.PendulumEquations import angular_velocity, angular_acceleration
from visual.plot import plot
from visual.animation import run_animation

from functools import partial
from fractions import Fraction
from typing import Callable

import numpy as np
import json
import csv


def load_json(file_path):
    with open(file_path) as file:
        return json.load(file)


def run_simulation(sim: Simulation, omega_dot: Callable[..., float], theta_dot: Callable[..., float], file_path: str):
    print(f"Running simulation.")
    with open(file_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(['t', 'theta', 'omega'])
        for t, y in sim.run(omega_dot, theta_dot):
            writer.writerow((t, *y))
    print(f"Simulation finished. Data saved to {file_path}")


def main(args: ap.Namespace):
    # creating Runge-Kutta Butcher table
    table = Table(name_to_path[args.method])

    # creating simulation instance
    sim = Simulation(table, args.step, np.array([args.theta, args.omega]), 0, args.time)

    # creating functions to calculate the derivatives of the system
    omega_dot = partial(angular_acceleration, g=args.gravity, length=args.length)
    theta_dot = angular_velocity

    # running the simulation
    run_simulation(sim, omega_dot, theta_dot, args.file)

    # running visualisation
    run_animation(args)
    plot(args)


if __name__ == '__main__':
    name_to_path = load_json('data/name_to_path.json')
    constants = load_json('data/constants.json')

    parser = ap.ArgumentParser(
        description='Pendulum simulation',
        epilog='Nikita Poglazov ETU NMDS 2024',
        formatter_class=ap.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-f', '--file',
                        help="Path for output file (saved in csv format)",
                        type=str,
                        default=constants["data_path"])
    parser.add_argument('-m', '--method',
                        help='Runge-Kutta method name',
                        type=str,
                        metavar="METHOD",
                        choices=name_to_path.keys(),
                        default=constants['method'])
    parser.add_argument('-s', '--step',
                        help='Step size in seconds (as a fraction)',
                        type=Fraction,
                        default=constants['step'])
    parser.add_argument('-t', '--time',
                        help='Simulation time in seconds',
                        type=float,
                        default=constants['time'])
    parser.add_argument('-l', '--length',
                        help='Pendulum length in meters',
                        type=float,
                        default=constants['length'])
    parser.add_argument('-g', '--gravity',
                        help='Gravity acceleration in m/s^2',
                        type=float,
                        default=constants['gravity'])
    parser.add_argument('-a', '--theta',
                        help='Initial angle in radians',
                        type=float,
                        default=constants['theta'])
    parser.add_argument('-v', '--omega',
                        help='Initial angular velocity in rad/s',
                        type=float,
                        default=constants['omega'])
    parser.add_argument('--save',
                        help='Save plot to file',
                        action='store_true')
    # TODO: add save path argument
    main(parser.parse_args())
