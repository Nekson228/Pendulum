import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_data(ax, data, x, y, title, ylabel):
    ax.plot(data[x], data[y], linewidth=2)
    ax.set_xlabel(x)
    ax.set_ylabel(ylabel, rotation=0)
    ax.set_title(title)
    ax.grid(True)


data = pd.read_csv(os.path.join("..", "example", "data.csv"))
fig, (ax_theta, ax_omega) = plt.subplots(nrows=2, ncols=1, figsize=(9.6, 7.2))

fig.suptitle(r"Pendulum $\theta$ and $\omega$ plots", fontsize="xx-large")
fig.subplots_adjust(hspace=.3)

plots = {
    "theta": (ax_theta, r"Angle of pendulum with time", r"$\theta$"),
    "omega": (ax_omega, r"Angular velocity of pendulum with time", r"$\omega$")
}

for key, (ax, title, ylabel) in plots.items():
    plot_data(ax, data, "t", key, title, ylabel)

plt.savefig(os.path.join("..", "example", "angle_and_velocity.png"))
