# Third party
import pandas as pd
import plotly.express as px
import plotly.subplots as psp
# Local imports
import px_subplots

TEMPLATE = "plotly_dark"


def faux_facet() -> None:
    # Get data for the demonstration
    stocks = px.data.stocks().set_index("date")
    # Create the figure with subplots
    fig = psp.make_subplots(rows=2, cols=1)
    # Create the individual Plotly Express figures
    fig1 = px.line(stocks[["GOOG", "AAPL"]])
    fig2 = px.line(stocks[["AMZN", "MSFT"]])
    # Add each trace to the corresponding subplot
    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.data:
        fig.add_trace(trace, row=2, col=1)
    # Change the colors
    for idx, data in enumerate(fig.data):
        data["line"]["color"] = px.colors.qualitative.D3[idx]
    # <>
    fig.update_layout(width=700, template=TEMPLATE)
    with open("px_facet.png", "wb") as file:
        file.write(fig.to_image("png"))


def many_subplots() -> None:
    # Create the figure with subplots
    fig = psp.make_subplots(rows=2, cols=2,
                            specs=[[{"type": "xy"}, {"type": "polar"}],
                                   [{"type": "domain"}, {"type": "scene"}]])
    # Create the individual Plotly Express figures
    fig1 = px.bar(y=[2, 3, 1])
    fig2 = px.bar_polar(theta=[0, 45, 90], r=[2, 3, 1])
    fig3 = px.pie(values=[2, 3, 1])
    fig4 = px.line_3d(x=[2, 3, 1],
                      y=[0, 0, 0],
                      z=[0.5, 1, 2])
    # Add each trace to the corresponding subplot
    for trace in fig1.select_traces():
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.select_traces():
        fig.add_trace(trace, row=1, col=2)
    for trace in fig3.select_traces():
        fig.add_trace(trace, row=2, col=1)
    for trace in fig4.select_traces():
        fig.add_trace(trace, row=2, col=2)
    # <>
    fig.update_layout(height=700, width=700,
                      showlegend=False,
                      template=TEMPLATE)
    with open("px_many.png", "wb") as file:
        file.write(fig.to_image("png"))


def multiple_sizes() -> None:
    # Create the figure with subplots
    fig = psp.make_subplots(rows=5, cols=2,
                            specs=[[{}, {"rowspan": 2}],
                                   [{}, None],
                                   [{"rowspan": 2, "colspan": 2}, None],
                                   [None, None],
                                   [{}, {}]],
                            )
    # Create the Plotly Express figure
    line_plot = px.line(x=[1, 2], y=[1, 2], markers=True)
    subplots = [[line_plot, line_plot],
                [line_plot, None],
                [line_plot, None],
                [None, None],
                [line_plot, line_plot]]
    color_scale = px.colors.qualitative.Plotly
    for row, c in enumerate(subplots, start=1):
        for col, plot in enumerate(c, start=1):
            if plot:
                for trace in plot.select_traces():
                    # Give each trace a name, a unique color and turn
                    # showlegend on
                    trace.name = f"({row},{col})"
                    trace.line.color = color_scale.pop(0)
                    trace.showlegend = True
                    fig.add_trace(trace, row=row, col=col)
    fig.update_layout(height=700, width=700,
                      template=TEMPLATE)
    with open("px_multiple.png", "wb") as file:
        file.write(fig.to_image("png"))


def shared_colorscale() -> None:
    fig = psp.make_subplots(rows=1, cols=2, shared_yaxes=True)
    fig1 = px.bar(x=[1, 2, 3], y=[4, 5, 6], color=[4, 5, 6])
    fig2 = px.bar(x=[1, 2, 3], y=[2, 3, 5], color=[2, 3, 5])
    for trace in fig1.select_traces():
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.select_traces():
        fig.add_trace(trace, row=1, col=2)
    fig.update_layout(coloraxis={"colorscale": "Bluered_r"}, showlegend=False,
                      width=700,
                      template=TEMPLATE)
    with open("px_colorscale.png", "wb") as file:
        file.write(fig.to_image("png"))


def suboptimal() -> None:
    tasks = pd.DataFrame([dict(Task="Job A", Start='2009-01-01',
                               Finish='2009-02-28', Resource="Alex"),
                          dict(Task="Job B", Start='2009-03-05',
                               Finish='2009-04-15', Resource="Alex"),
                          dict(Task="Job C", Start='2009-02-20',
                               Finish='2009-05-30', Resource="Max")
                          ])
    tips = px.data.tips()
    elections = px.data.election()
    geojson = px.data.election_geojson()
    #
    timeline = px.timeline(tasks, x_start="Start", x_end="Finish", y="Task", 
                           color="Resource")
    density_contour = px.density_contour(tips, x="total_bill", y="tip",
                                         marginal_x="histogram",
                                         marginal_y="histogram")
    choropleth = px.choropleth(elections, geojson=geojson,
                               color="Bergeron", locations="district",
                               featureidkey="properties.district",
                               projection="mercator",
                               fitbounds="locations", basemap_visible=False
                               )
    #
    fig = px_subplots.make_px_subplots(
        specs=[[{"type": "xy"}, {"type": "heatmap", "rowspan": 2}],
               [{"type": "choropleth"}, None]],
        grid=[[timeline, density_contour], [choropleth, None]])
    fig.update_layout(width=700, template=TEMPLATE)
    with open("px_suboptimal.png", "wb") as file:
        file.write(fig.to_image("png"))
    # Correct the layout
    fig.update_layout(xaxis={"type": "date"}, yaxis={"autorange": "reversed"},
                      geo={"fitbounds": "locations"})
    with open("px_suboptimal1.png", "wb") as file:
        file.write(fig.to_image("png"))


if __name__ == "__main__":
    faux_facet()
    many_subplots()
    multiple_sizes()
    shared_colorscale()
    suboptimal()
