# -*- coding: utf-8 -*-
"""
author: UnicornOnAzur

Module for creating and managing Plotly subplots.
"""
# Standard library
import typing
# Third party
import plotly.graph_objects as go
import plotly.subplots as psp


def loop_over_grid(
    grid: typing.List[typing.List[typing.Optional[go.Figure]]]
        ) -> typing.Generator[typing.Tuple[go.Figure, int, int], None, None]:
    """
    Iterate over a grid of plots and yield each trace along with its row and
    column indices.

    Parameters:
        grid : A 2D list containing plotly figures.

    Yields:
        A tuple containing a trace and its corresponding row and column
        indices.
    """
    for row_index, column in enumerate(grid, start=1):
        for col_index, plot in enumerate(column, start=1):
            if plot:
                for trace in plot.select_traces():
                    yield trace, row_index, col_index


def make_px_subplots(
    specs: typing.List[typing.List[typing.Optional[dict]]],
    grid: typing.List[typing.List[go.Figure]]
        ) -> go.Figure:
    """
    Create a subplot figure using the provided specifications and grid of
    plots.

    Parameters:
        specs : A 2D list defining the specifications for each subplot.
        grid : A 2D list containing plotly figures to be added to the subplots.

    Returns:
        A plotly figure containing the subplots.
    """
    num_rows: int = len(specs)
    num_cols: int = len(specs[0])
    fig: go.Figure =\
        psp.make_subplots(rows=num_rows, cols=num_cols, specs=specs)
    for trace, row, col in loop_over_grid(grid):
        fig.add_trace(trace, row=row, col=col)
    return fig


if __name__ == "__main__":
    pass
