# -*- coding: utf-8 -*-
"""
@author: UnicornOnAzur

"""
# Standard library

# Third party
import matplotlib.pyplot as plt

# Local import
from sna_toolbox import similarities


def create_circle(xy: tuple[float],
                  color: str = "blue") -> plt.Circle:
    """
    """
    return plt.Circle(xy,
                      radius=1,
                      alpha=.6,
                      color=color)


def draw_overlapping_circles(ax, spine_on):
    """
    """
    # Add circles to the plot
    ax.add_artist(create_circle((-0.4, 0)))
    ax.add_artist(create_circle((0.4, 0), "red"))

    # Set limits and aspect
    g, h = 1.5, 1.1
    ax.set_xlim(-g, g)
    ax.set_ylim(-h, h)
    ax.set_aspect("equal", adjustable="box")

    # Removing the spines
    ax.spines[["left", "right", "bottom"]].set_visible(False)
    if not spine_on:
        ax.spines[["top"]].set_visible(False)

    # Turn off labels and ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')


def diagrams():
    titles = ["Overlap", "Jaccard", "Dice-Sørensen", "Cosine", ""]
    fig: plt.Figure = plt.figure(figsize=(10, 3))
    axes = fig.subplots(nrows=2, ncols=5, squeeze=True)
    for col in range(2):
        for row, title in enumerate(titles):
            draw_overlapping_circles(axes[col][row], bool(col))
            if col == 0:
                axes[col][row].set_title(title)
    fig.subplots_adjust(hspace=0, wspace=0)
    plt.axhline(y=1.3, color='blue', linewidth=2)
    # Title
    fig.suptitle("Visualisation of similarity measures", y=1)
    # Subtitle
    fig.show()


def pairplot():
    # fig: plt.Figure = plt.figure(figsize=(10,5))
    # axes = fig.subplots(nrows=5, ncols=5, squeeze=True)
    # fig.suptitle("Pairplot of similarity measures")
    # fig.show()
    pass


def main():
    """
    """
    diagrams()
    pairplot()


if __name__ == "__main__":
    main()
