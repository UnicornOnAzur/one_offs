# -*- coding: utf-8 -*-
"""
@author: UnicornOnAzur

"""
# Standard library
import sys
# Third party
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
# Local import
sys.path.append(".")
from sna_toolbox.src import similarities  # noqa E402
# Constants
BARHEIGHT: float = .9
COLORS: list = ["#e5c185", "#96e585", "#9b85e5"]
LINE_COLORS: list = ["#003f5c", "#58508d", "#bc5090", "#ff6361", "#ffa600"]
LABELS: list = ["set A", "overlap", "set B"]
TICK_ROTATION: int = 20
TITLES: list[str] = ["Overlap", "Jaccard", "Dice-Sørensen", "Cosine", "SMC"]


def overlap_plot():
    def create_circle(xy: tuple[float],
                      color: str = "blue") -> plt.Circle:
        """
        """
        return plt.Circle(xy,
                          radius=1,
                          alpha=.5,
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
        #
        ax.set_axis_off()

    fig: plt.Figure = plt.figure(figsize=(10, 3))
    axes = fig.subplots(nrows=2, ncols=5, squeeze=True)
    for row in range(2):
        for col, title in enumerate(TITLES):
            draw_overlapping_circles(axes[row][col], bool(row))
            if row == 0:
                axes[row][col].set_title(title)
    fig.subplots_adjust(hspace=0, wspace=0)
    plt.axhline(y=1.3, color='blue', linewidth=2)
    # Title
    fig.suptitle("Visualisation of similarity measures", y=1)
    # Subtitle
    plt.show(block=True)
    return fig


def bar_plot():
    #
    widths, starts_left, starts_right, table_data = create_data()
    #
    fig: plt.Figure = plt.figure(figsize=(10, 5),
                                 linewidth=1,
                                 edgecolor="grey")
    axes = fig.subplots(nrows=2, ncols=2,
                        squeeze=True,
                        gridspec_kw={"width_ratios": [4, 3]}
                        )
    # for row in axes:
    #     for ax in row:
    #         ax.set_ylim([0, 7])
    tuple(map(format_axis, [ax for ax_ in axes for ax in ax_]))
    # top row
    create_bar(axes[0][0], widths, starts_left, [-.5, 200.5])
    create_bar(axes[0][1], widths, starts_right, [-.5, 150.5])
    # bottom row
    create_table(table_data, axes[1][0])
    create_lineplot(table_data, axes[1][1])
    #
    fig.suptitle(t="Change of similarity measures",
                 verticalalignment="top",
                 fontsize=18)
    fig.text(0.5, 0.9,
             "Constant size of overlap and changing size of sets",
             ha='center',
             fontsize=12)
    plt.subplots_adjust(left=.02, right=.98,
                        top=.92, bottom=.08,
                        hspace=.14, wspace=0.01)
    plt.show(block=True)

    return fig


def format_axis(ax):
    # Removing the spines
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)

    # Turn off labels and ticks
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylim([0, 7])


def create_lineplot(table_data, ax):
    offset = dict(zip(TITLES, [0, -15, -15, -5, -15]))
    rotation = dict(zip(TITLES, [330, 270, 270, 290, 330]))
    for idx, color, label in zip(range(2, 7), LINE_COLORS, TITLES):
        x = [c[idx] for c in table_data]
        y = list(map(lambda x: x, range(6, 0, -1)))
        ax.plot(x, y,
                linewidth=5,
                color=color,
                alpha=.5)
        ax.plot(x, y,
                color=color)
        ax.annotate(label,
                    xy=(x[-1], 1),
                    textcoords="offset points",
                    xytext=(offset.get(label), 0),
                    color=color,
                    rotation=rotation.get(label))
    #
    ticks = [i/4 for i in range(5) if i != 0]
    ax.set_xticks(ticks=ticks,
                  labels=ticks,
                  rotation=TICK_ROTATION)
    ax.tick_params(axis='x', which='major', pad=-1)
    ax.set_xlim([-.05, 1.05])


def create_table(table_data, ax):
    table = ax.table(cellText=table_data,
                     # The alignment of the text within the cells.
                     cellLoc="center",
                     # The text alignment of the row header cells.
                     rowLoc="center",
                     # The text of the column header cells.
                     colLabels=["Set A", "Set B", *TITLES],
                     # A bounding box to draw the table into.
                     bbox=[0, 0, 1, 1],
                     # The cell edges to be drawn with a line.
                     edges="closed")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    ax.set_xlim([0, 7])
    ax.set_xticks([])


def create_data():
    widths = [[] for _ in range(6)]
    starts_left = [[] for _ in range(6)]
    starts_right = [[] for _ in range(6)]
    table_data = [[] for _ in range(6)]
    #
    for i, (a, b) in enumerate(zip(range(100, 151, 10), range(0, 51, 10))):
        #
        seta = set(range(a))
        setb = set(range(50+b, 150))
        #
        widths[i].extend([a, 50, len(setb)-50])
        starts_left[i].extend([(offset := (5-i)*10), 100, a+offset])
        starts_right[i].extend([0, a-50, a])
        #
        table_data[i] = [
            a,
            100 - b,
            round(similarities.overlap_coefficient(seta, setb), 3),
            round(similarities.jaccard_similarity(seta, setb), 3),
            round(similarities.dice_sørensen_coefficient(seta, setb), 3),
            round(similarities.cosine_similarity(seta, setb), 3),
            round(similarities.simple_matching_coefficient(seta, setb), 3),
        ]
    return widths, starts_left, starts_right, table_data


def create_bar(ax, widths: list[int], starts: list[int], xrange: list[int]
               ) -> None:
    for row in range(6):
        for width, start, color, label in zip(widths[row],
                                              starts[row],
                                              COLORS,
                                              LABELS):
            row_height: float = (6-row)-.05
            ax.barh(y=row_height,
                    width=width,
                    height=BARHEIGHT,
                    left=start,
                    align="center",
                    color=color,
                    alpha=.8,
                    label=label)
            if row == 0:
                ax.text(x=start+15,
                        y=row_height-0.2,
                        s=label,
                        color=color,
                        fontweight="semibold",
                        path_effects=[pe.withStroke(linewidth=3,
                                                    foreground="lightgrey"),
                                      pe.withStroke(linewidth=1,
                                                    foreground="black")])
    new_patches = []
    for patch in ax.patches:
        bb = patch.get_bbox()
        color = patch.get_facecolor()
        p_bbox: mpatches.FancyBboxPatch = mpatches.FancyBboxPatch(
            xy=(bb.xmin,
                bb.ymin),
            width=abs(bb.width),
            height=BARHEIGHT,
            boxstyle=mpatches.BoxStyle("Round",
                                       pad=0,
                                       rounding_size=None
                                       ),
            ec="none",
            fc=color,
            mutation_aspect=1
            )
        patch.remove()
        new_patches.append(p_bbox)
    # add the patches
    for patch in new_patches:
        ax.add_patch(patch)
    #
    ax.set_xlim(xrange)
    ax.set_xticks(ticks=[0, 50, 100, 150],
                  labels=[0, 50, 100, 150],
                  rotation=TICK_ROTATION)
    ax.tick_params(axis='x', which='major', pad=-1)


def scatter_plot():
    fig, ax = plt.subplots()
    #
    jacc = []
    dice = []
    m = 20
    jacc, dice = list(zip(*[[similarities.jaccard_similarity(
                                    set(range(i)),
                                    set(range(j, m))),
                             similarities.dice_sørensen_coefficient(
                                    set(range(i)),
                                    set(range(j, m)))]
                            for i in range(m) for j in range(i)]))
    ax.scatter(jacc, dice, alpha=1)
    #
    j_, d_ = list(zip(*[[(ji := x/100), 2 * ji / (1 + ji)] for x in range(100)]))
    ax.plot(j_, d_, color="red", alpha=.5)
    #
    ax.set_xlim([0, 1])
    ax.set_xlabel(TITLES[1])
    ax.set_ylim([0, 1])
    ax.set_ylabel(TITLES[2])
    #
    plt.show(block=True)
    return fig


def pair_plot():
    def format_axis(ax):
        # Removing the spines
        ax.spines[["top", "right"]].set_visible(False)

        # Turn off labels and ticks
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel('')
        ax.set_ylabel('')

    def draw_diagonal(ax):
        format_axis(ax)

    def draw_bottom(ax):
        format_axis(ax)

    def draw_top(ax):
        format_axis(ax)

    fig: plt.Figure = plt.figure(figsize=(10, 5))
    axes = fig.subplots(nrows=5, ncols=5, squeeze=True)
    for row in range(5):
        for col in range(5):
            # Add the plots
            if row == col:
                draw_diagonal(axes[row][col])
            elif row > col:
                draw_bottom(axes[row][col])
            elif col > row:
                draw_top(axes[row][col])
            # Add labels
            if col == 0:
                axes[row][col].set_ylabel(TITLES[row])
            if row == 4:
                axes[row][col].set_xlabel(TITLES[col])
    # Title
    fig.suptitle("Pairplot of similarity measures")
    # Subtitle
    plt.show(block=True)
    return fig


def main():
    """
    """
    # overlap_plot()
    # bar_plot()
    scatter_plot()
    # pair_plot()


if __name__ == "__main__":
    main()
