import matplotlib.pyplot as plt
import pandas as pd
import os
from argparse import Namespace

FIG_SIZE = (10, 7.5)
SAVE_PATH = "plot.png"


def load_data(file_path: str):
    try:
        return pd.read_csv(os.path.join(file_path))
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except pd.errors.ParserError:
        print(f"Error parsing the file {file_path}. Please check the file format.")
        return None


def plot_data(ax, data, x, y, title, ylabel):
    ax.plot(data[x], data[y], linewidth=2)
    ax.set_xlabel(x)
    ax.set_ylabel(ylabel, rotation=0)
    ax.set_title(title)
    ax.grid(True)


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


def plot(args: Namespace):
    data = load_data(args.file)
    if data is None:
        return

    fig, (ax_theta, ax_omega) = plt.subplots(nrows=2, ncols=1, figsize=FIG_SIZE)

    fig.suptitle(r"Pendulum $\theta$ and $\omega$ plots", fontsize="xx-large")
    fig.subplots_adjust(hspace=.3)
    show_args(fig, args)

    plots = {
        "theta": (ax_theta, r"Angle of pendulum with time", r"$\theta$"),
        "omega": (ax_omega, r"Angular velocity of pendulum with time", r"$\omega$")
    }

    for key, (ax, title, ylabel) in plots.items():
        plot_data(ax, data, "t", key, title, ylabel)

    if args.save:
        save_plot(fig)

    plt.show()
