# -*- coding: utf-8 -*-
"""
author: UnicornOnAzur

This module provides functionality to draw a calendar for a specific month,
including the ability to highlight certain days and display icons. It utilizes
matplotlib for rendering the calendar and allows customization of the
appearance of the calendar elements.
"""
# Standard library
import calendar
import typing
# Third party
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pytablericons
# Constants
COLOR: str = "#FC5200"
OFFSET: float = .5


def prepare_axes(
    ax: plt.Axes
        ) -> plt.Axes:
    """
    Prepare the axes for drawing the calendar by setting the aspect ratio to
    1:1, the axis limits both to a range from 0 to 7, and hide all axis
    decorations.

    Parameters:
        ax : The axes to be prepared.

    Returns:
        The prepared axes.
    """
    ax.set(aspect=1, xlim=(0, 7), ylim=(0, 7))
    ax.axis("off")
    return ax


def place_text(
    ax: plt.Axes, x: int, y: int, text: str, highlighted: bool = False
        ) -> None:
    """
    Place text on the given axes at specified coordinates.

    Parameters:
        ax: The axes on which to place the text.
        x: The x-coordinate, without offset, for the text placement.
        y: The y-coordinate, without offset, for the text placement.
        text: The text to be displayed.
        highlighted: When True use the background color of the axis, otherwise
        use the standard color (default is False).

    Returns:
        None
    """
    ax.text(x+OFFSET, y+OFFSET,
            s=text,
            ha="center", va="center",
            color=COLOR if not highlighted else ax.get_facecolor())


def label_weekday(
    ax: plt.Axes
        ) -> None:
    """
    Label the weekdays, with the first letter, on the top row of given axes.

    Parameters:
        ax : The axes on which to label the weekdays.

    Returns:
        None
    """
    top_row_position: int = 6
    for day_number, weekday in enumerate(calendar.day_abbr):
        place_text(ax=ax, x=day_number, y=top_row_position, text=weekday[0])


def draw_circle(
    ax: plt.Axes,
    x_pos: int,
    y_pos: int,
    highlight: bool = False
        ) -> None:
    """
    Draw a circle on the given axes at specified coordinates with a radius
    that fits within one grid cell.

    Parameters:
        ax : The axes on which to draw the circle.
        x_pos : The x-coordinate, without offset, for the circle's center.
        y : The y-coordinate, without offset, for the circle's center.
        highlight : Whether to fill the circle (default is False meaning the
                    circle facecolor is not set).

    Returns:
        None
    """
    ax.add_artist(
        mpatches.Circle(
            (x_pos+OFFSET, y_pos+OFFSET), radius=.45,
            edgecolor=COLOR, facecolor=COLOR if highlight else "None")
                  )


def place_icon(
    ax,
    activity,
    x_pos,
    y
        ) -> None:
    icons: typing.Dict[str, pytablericons.OutlineIcon] = {
        "bike": pytablericons.OutlineIcon.BIKE,
        "run": pytablericons.OutlineIcon.RUN,
        "swim": pytablericons.OutlineIcon.SWIMMING,
        "weight": pytablericons.OutlineIcon.BARBELL
    }
    padding: float = .02
    newax: plt.Axes = ax.inset_axes([x_pos/7+padding, y/7+padding, .1, .1])
    icon: pytablericons.OutlineIcon =\
        icons.get(activity) or pytablericons.OutlineIcon.BOLT
    newax.imshow(pytablericons.TablerIcons.load(icon))
    newax.axis('off')


def draw_calendar_of_a_month(
    ax: plt.Axes,
    first: int,
    num_days: int,
    highlights: typing.List[int] = None,
    activities: typing.List[str] = None,
    show_icon: bool = False
        ) -> None:
    """
    Draw the calendar of a month on the given axes.

    Parameters:
        ax: The axes on which to draw the calendar.
        first : The first day of the month (0=Monday, 6=Sunday).
        num_days : The total number of days in the month.
        highlights : A list of days to highlight (default is None).
        activities : A list of the activities done (default is None).
        show_icon : Whether to show an icon for highlighted days (default is
                    False).

    Returns:
        None
    """
    ax: plt.Axes = prepare_axes(ax)
    label_weekday(ax)
    x_pos: int = first
    y: int = 5

    for day in range(1, num_days+1):
        highlight: bool = day in highlights if highlights else False
        draw_circle(ax, x_pos, y, highlight)
        if show_icon and day in highlights:
            place_icon(ax, activities.pop(0) if activities else None, x_pos, y)
        else:
            place_text(ax, x_pos, y, day, highlighted=highlight)
        x_pos: int = (x_pos+1) % 7
        if x_pos == 0:
            y -= 1


def main() -> None:
    """
    Main function to execute the calendar drawing.

    Parameters:
        None

    Returns:
        None
    """
    active_days: typing.List[int] = [5, 6, 7, 10, 27]
    activities: typing.List[str] = ["bike", "run", "swim", "weight"]

    # Plot June 2025 the month that spans six calendar weeks
    fig: plt.Figure = plt.figure()
    ax: plt.Axes = fig.add_subplot()
    first_day, number_of_days = calendar.monthrange(2025, 6)
    draw_calendar_of_a_month(
        ax, first_day, number_of_days)

    # Plot June 2025 the month that spans six calendar weeks
    fig: plt.Figure = plt.figure()
    ax: plt.Axes = fig.add_subplot()
    first_day, number_of_days = calendar.monthrange(2025, 6)
    draw_calendar_of_a_month(
        ax, first_day, number_of_days, active_days, activities, True)

    # Plot the whole year on one figure
    fig, axes = plt.subplots(3, 4, figsize=(14, 8))
    fig.subplots_adjust(left=.01, right=.99, bottom=.01, top=.99,
                        wspace=.1, hspace=.1)
    for ax, month in zip(axes.flatten(), range(1, 13)):
        first_day, number_of_days = calendar.monthrange(2025, month)
        draw_calendar_of_a_month(
            ax, first_day, number_of_days, active_days, show_icon=True)

    plt.show()


if __name__ == "__main__":
    main()
