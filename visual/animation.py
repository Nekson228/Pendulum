import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
from argparse import Namespace
from visual.load_data import load_data

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
INTERVAL_MS = 10


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


def animate_pendulum(ax, data, length, color, markersize):
    pendulum_line, = ax.plot([0, data['theta'][0]], [0, length], color=color, linewidth=5)
    pendulum_head, = ax.plot(data['theta'][0], length, 'o', color='red', markersize=markersize)
    pendulum_origin, = ax.plot(0, 0, 'o', color='red', markersize=markersize)

    def update(frame):
        pendulum_line.set_xdata([0, data['theta'][frame]])
        pendulum_head.set_xdata([data['theta'][frame]])
        return pendulum_line, pendulum_head, pendulum_origin

    return pendulum_line, pendulum_head, pendulum_origin, update


def run_animation(args: Namespace):
    data_exp = load_data(args.file)
    if data_exp is None:
        return
    data_math = None
    if args.math:
        data_math = load_data(args.mfile)

    fig, ax = setup_plot()

    pendulum_line_exp, pendulum_head_exp, pendulum_origin_exp, update_exp = (
        animate_pendulum(ax, data_exp, args.length, 'blue', 10)
    )
    pendulum_line_math, pendulum_head_math, pendulum_origin_math, update_math = None, None, None, None
    if args.math:
        pendulum_line_math, pendulum_head_math, pendulum_origin_math, update_math = (
            animate_pendulum(ax, data_math, args.length, 'gray', 10)
        )

    time_text = ax.text(*TIME_TEXT_POSITION, '', transform=ax.transAxes, fontsize=TIME_TEXT_FONT_SIZE)

    def update(frame):
        update_exp(frame)
        time_text.set_text(TIME_TEMPLATE % data_exp['t'][frame])
        if args.math:
            update_math(frame)
            return (pendulum_line_exp, pendulum_head_exp, pendulum_origin_exp, pendulum_line_math, pendulum_head_math,
                    pendulum_origin_math, time_text)
        return pendulum_line_exp, pendulum_head_exp, pendulum_origin_exp, time_text

    def init():
        return update(0)

    animation_step = int(1 / args.step * INTERVAL_MS / 1000)
    animation_frames = np.arange(0, len(data_exp), animation_step)
    ani = anim.FuncAnimation(fig, update,
                             frames=animation_frames,
                             init_func=init, blit=True, interval=INTERVAL_MS)
    if args.save:
        save_animation(ani)

    plt.show()
