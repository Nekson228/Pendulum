import matplotlib.pyplot as plt
import matplotlib.animation as anim
import pandas as pd
import numpy as np
from argparse import Namespace

FIG_SIZE = (9, 9)
THETA_ZERO_LOCATION = 'S'
RLABEL_POSITION = 180
TICK_LABEL_SIZE = 7
TITLE = "Pendulum animation"
TITLE_FONT_SIZE = "xx-large"
TIME_TEMPLATE = 'time = %.2fs'
TIME_TEXT_POSITION = (.8, 0)
TIME_TEXT_FONT_SIZE = 14
SAVE_PATH = "pendulum.gif"
SAVE_WRITER = "PillowWriter"
INTERVAL_MS = 5


def load_data(file_path: str):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except pd.errors.ParserError:
        print(f"Error parsing the file {file_path}. Please check the file format.")
        return None


def save_animation(ani: anim.FuncAnimation):
    ani.save(SAVE_PATH, writer=SAVE_WRITER, fps=100)
    print(f"Animation saved to {SAVE_PATH}")


def setup_plot():
    fig, ax = plt.subplots(figsize=FIG_SIZE, subplot_kw={"projection": "polar"})
    ax.set_theta_zero_location(THETA_ZERO_LOCATION)
    ax.set_rlabel_position(RLABEL_POSITION)
    ax.tick_params(axis='y', labelsize=TICK_LABEL_SIZE)
    ax.set_title(TITLE, fontsize=TITLE_FONT_SIZE)
    return fig, ax


def run_animation(args: Namespace):
    data = load_data(args.file)
    if data is None:
        return

    fig, ax = setup_plot()

    pendulum_line, = ax.plot([0, data['theta'][0]], [0, args.length], color='blue', linewidth=5)
    pendulum_head, = ax.plot(data['theta'][0], args.length, 'o', color='red', markersize=10)
    pendulum_origin, = ax.plot(0, 0, 'o', color='red', markersize=10)

    time_text = ax.text(*TIME_TEXT_POSITION, '', transform=ax.transAxes, fontsize=TIME_TEXT_FONT_SIZE)

    def update(frame):
        pendulum_line.set_xdata([0, data['theta'][frame]])
        pendulum_head.set_xdata([data['theta'][frame]])
        time_text.set_text(TIME_TEMPLATE % data['t'][frame])
        return pendulum_line, pendulum_head, pendulum_origin, time_text

    def init():
        pendulum_line.set_xdata([0, data['theta'][0]])
        pendulum_head.set_xdata([data['theta'][0]])
        time_text.set_text(TIME_TEMPLATE % data['t'][0])
        return pendulum_line, pendulum_head, pendulum_origin, time_text

    ani = anim.FuncAnimation(fig, update,
                             frames=np.arange(len(data["t"]), step=INTERVAL_MS), interval=INTERVAL_MS,
                             blit=True, init_func=init)
    if args.save:
        save_animation(ani)

    plt.show()
