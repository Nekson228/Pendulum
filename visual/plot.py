from visual.load_data import load_data

import matplotlib.pyplot as plt
from argparse import Namespace

FIG_SIZE = (10, 7.5)
SAVE_PATH = "plot.png"
MATH_PENDULUM_COLOR = "gray"
EXP_PENDULUM_COLOR = "blue"
MATH_LABEL = "Mathematical model"
EXP_LABEL = "Experimental data"


def setup_plot(ax, title):
    ax.set_title(title)
    ax.grid(True)


def plot_data(ax, data, x, y, ylabel, color, label=None):
    ax.plot(data[x], data[y], linewidth=2, color=color, label=label)
    ax.set_xlabel(x)
    ax.set_ylabel(ylabel, rotation=0)
    if label:
        ax.legend(loc=2)


def show_args(fig, args: Namespace):
    fig.text(0.08, 0.93,
             f"Method: {args.method}\n"
             f"Step: {args.step}\n"
             f"Length: {args.length}\n"
             f"Gravity: {args.gravity}\n",
             fontsize=12, ha='center', va='center')


def save_plot(fig):
    fig.savefig(SAVE_PATH)
    print(f"Plot saved to {SAVE_PATH}")


def plot(args: Namespace) -> None:
    """
    Function to plot the data from the experiment and the math pendulum (if specified)
    :param args: arguments from the command line
    :return: None
    """
    data_exp = load_data(args.file)
    if data_exp is None:
        return
    data_math = None
    if args.math:
        data_math = load_data(args.mfile)

    fig, (ax_theta, ax_omega) = plt.subplots(nrows=2, ncols=1, figsize=FIG_SIZE)

    fig.suptitle(r"Pendulum $\theta$ and $\omega$ plots", fontsize="xx-large")
    fig.subplots_adjust(hspace=.3)
    show_args(fig, args)

    plots = {
        "theta": (ax_theta, r"Angle of pendulum with time", r"$\theta$"),
        "omega": (ax_omega, r"Angular velocity of pendulum with time", r"$\omega$")
    }

    for key, (ax, title, ylabel) in plots.items():
        setup_plot(ax, title)
        plot_data(ax, data_exp, "t", key, ylabel, EXP_PENDULUM_COLOR, EXP_LABEL)
        if args.math:
            plot_data(ax, data_math, "t", key, ylabel, MATH_PENDULUM_COLOR, MATH_LABEL)

    if args.save:
        save_plot(fig)

    plt.show()
