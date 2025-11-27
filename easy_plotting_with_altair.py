"""
This module demonstrates many uses of Vega-Altair through making five
visualizations using well-known datasets.
"""

# Standard library
import io
import typing
# Third party
import altair as alt
import pandas as pd
import plotly
import requests
import vega_datasets
# Enable browser rendering for Altair
alt.renderers.enable("browser")
# Constants for chart dimensions and colors
HEIGHT: int = 600
WIDTH: int = 1000
SUBTITLE_SIZE: int = 13
TITLE_SIZE: int = 16
ROUND_TO_NEXT_INTEGER: str = ".0f"
SUBDUED_COLOR: str = "lightgrey"
SUBTITLE_COLOR: str = "grey"
TITLE_COLOR: str = "darkgrey"
DISCRETE_COLOR_SCHEME: str = "dark2"
CONTINUOUS_COLOR_SCHEME: str = "spectral"
COLOR: str = "rebeccapurple"


def format_label(label_text: str) -> str:
    """
    Formats the label by replacing underscores with spaces and capitalizing.
    """
    return " ".join(label_text.split("_")).capitalize()


def part1(
    dataset: pd.DataFrame
        ) -> alt.LayerChart:
    """
    Creates a layered chart visualizing life expectancy over the years for
    selected countries.

    Parameters:
        dataset : The dataset containing life expectancy data.

    Returns:
        A layered chart visualizing life expectancy.
    """
    # Define properties for the chart
    feature_property: str = "year"
    target_property: str = "lifeExp"
    encoding_x: str = "T"
    encoding_y: str = "Q"
    x_value: str = f"{feature_property}:{encoding_x}"
    y_value: str = f"{target_property}:{encoding_y}"
    line_color: str = "darkslategray"
    # Determine the range of years
    first_year: int = dataset["year"].dt.year.min()
    last_year: int = dataset["year"].dt.year.max()
    # Create line charts for all and the average life expectancy
    base_chart: alt.Chart = alt.Chart(dataset).mark_line(
        color=SUBDUED_COLOR, strokeWidth=1).encode(
        x=alt.X(x_value,
                # Enforce the use of explicit labels
                axis=alt.Axis(
                    grid=False,
                    labelColor=SUBTITLE_COLOR,  # Color the axis label
                    titleColor=TITLE_COLOR,  # Color the axis title
                    values=sorted(dataset["year"].unique())),
                # Extend beyond the years in the dataset
                scale=alt.Scale(
                    domain=(pd.to_datetime([first_year-2], format="%Y")[0],
                            pd.to_datetime([last_year+2], format="%Y")[0])),
                title="Year"),
        y=alt.Y(y_value,
                axis=alt.Axis(grid=False, labelColor=SUBTITLE_COLOR,
                              titleColor=TITLE_COLOR),
                title="Life expectancy (in years)"),
        detail="country:N")
    avg_line: alt.Chart = alt.Chart(dataset).mark_line(
        color=line_color, strokeDash=(4, 4)  # 4 pixels line, 4 pixels gap
        ).encode(
        x=x_value, y=f"median({target_property}):{encoding_y}")
    # Create subset for highlighted countries
    subset: alt.Chart = alt.Chart(dataset).encode(
        x=x_value, y=y_value,
        color=alt.Color("country:N", legend=None
                        ).scale(scheme=DISCRETE_COLOR_SCHEME)
        ).transform_filter(
        alt.FieldOneOfPredicate(
            field="country", oneOf=["Afghanistan", "Brazil", "Netherlands"]))
    # Create highlight and text annotations
    highlight: alt.Chart = subset.mark_line(point=True).encode()
    avg_text: alt.Chart = avg_line.mark_text(
        angle=347,  # Hardcoded angle to have text perpendicular to line
        baseline="middle", color=line_color, fontWeight="bold"
        ).encode(
        x=f"mean({feature_property}):{encoding_x}",
        y=alt.Y(f"{target_property}").aggregate("mean"),
        text=alt.datum("Median life expactancy")
        )
    country_name: alt.Chart = subset.mark_text(
        align="left", angle=355, baseline="bottom", dy=-7, fontWeight="bold"
        ).encode(
        x=f"min({feature_property})", y=alt.Y(y_value).aggregate("min"),
        text="country:N"
        )
    min_exp: alt.Chart = subset.mark_text(
        align="right", dx=-10, dy=-5, fontWeight="bold"
        ).encode(
        x=f"min({feature_property})", y=f"min({target_property}):{encoding_y}",
        text=alt.Text(f"min({target_property})", format=ROUND_TO_NEXT_INTEGER))
    max_exp: alt.Chart = subset.mark_text(
        align="left",
        dx=10, dy=-5,
        fontWeight="bold"
        ).encode(
        x=f"max({feature_property})", y=f"max({target_property}):{encoding_y}",
        text=alt.Text(f"max({target_property})", format=ROUND_TO_NEXT_INTEGER))
    # Combine all charts into a layered chart
    combined_chart: alt.LayerChart = (
        base_chart+avg_line+highlight+avg_text+country_name+min_exp+max_exp
        ).properties(
        height=HEIGHT, width=WIDTH,
        title=alt.Title(
            f"The life expectancy in three countries between {first_year} and {last_year}.",  # noqa E501
            color=TITLE_COLOR, fontSize=TITLE_SIZE,
            subtitle="Data is taken from the Gapminder dataset.",
            subtitleColor=SUBTITLE_COLOR, subtitleFontSize=SUBTITLE_SIZE
            )
        ).configure_view(
        strokeOpacity=0  # Hide the top and right axis
        )
    return combined_chart


def part2(
    dataset: pd.DataFrame
        ) -> alt.FacetChart:
    """
    Generates a FacetChart visualizing average sale prices and number of sales
    per neighborhood over the years.

    Parameters:
        dataset : The input DataFrame containing sales data, which should
        include columns for 'Yr Sold', 'SalePrice', and 'Neighborhood'.

    Returns:
        A faceted chart visualizing average sale prices and number of sales.
    """
    # Define properties for the chart
    number_of_columns: int = 7
    number_of_rows: int = 4
    x_property: str = "Yr Sold"
    y_property: str = "SalePrice"
    facet_property: str = "Neighborhood"
    # Determine if the average sale price is empty
    empty_value: int = 0
    is_empty = alt.datum.avg_sale_price == empty_value
    # Create the chart
    chart: alt.FacetChart = alt.Chart(
        data=dataset,
        height=HEIGHT//(number_of_rows + 1), width=WIDTH//number_of_columns
        ).transform_impute(
        impute=y_property,  # The property that has a missing value
        value=empty_value,  # The fill value for missing values
        key=facet_property,  # The key to identify unique data
        groupby=[x_property],  # Force imputation on a per-group basis
        method="value"  # The method for imputation
        ).transform_aggregate(
        avg_sale_price=f"mean({y_property})",  # Take the average of SalePrice
        number_of_sales=f"count({y_property})",  # Count the number of sales
        # Force the transformation on a per-group basis
        groupby=[facet_property, x_property]
        ).transform_bin(
        as_="Average Sale Price",
        bin=alt.BinParams(step=100_000),  # Set the bin size
        field="avg_sale_price"
        ).mark_point().encode(
        x=alt.X(f"{x_property}:N").title("Year of sale"),
        y=alt.Y("number_of_sales:Q").title("Number of sales"),
        size="Average Sale Price:O",
        color=alt.when(is_empty).then(
            alt.value("black")).otherwise(
            alt.Color(f"{x_property}:N",
                      legend=None).scale(scheme=DISCRETE_COLOR_SCHEME)),
        shape=alt.when(is_empty).then(
            alt.value("square")).otherwise("Average Sale Price:O")
        ).facet(
        facet=alt.Facet(f"{facet_property}:N", title=None),
        columns=number_of_columns,
        title=alt.Title(text="Average Sales Volume and Total Number of Sales for Each Year per Neighborhood",    # noqa E501
                        subtitle="Missing values are denoted by a black square; circles are sized and shaped by average sale volume in steps of 100,000",    # noqa E501
                        )
        ).configure_axis(
        labelColor=SUBTITLE_COLOR, titleColor=TITLE_COLOR
        ).configure_header(
        labelColor=SUBDUED_COLOR,  # Color the facet headers
        labelAnchor="start",  # Position the facet headers
        titleAnchor="middle"
        ).configure_legend(
        cornerRadius=10,  # Round the corners of the legend
        direction="horizontal",  # Position the legend elements sideways
        fillColor="#EEEEEE",  # Background for the legend
        # If orient is set to none, legendX,legendY can be specified
        orient="none", legendX=200, legendY=15,  # Custom position for x and y
        padding=5,  # Padding between the border and the elements
        offset=0  # No offset for the legend from the data rectangle and axes
        ).configure_title(
        anchor="middle",
        # Title color and size
        color=TITLE_COLOR, fontSize=TITLE_SIZE,
        # Color and size the subtitle
        subtitleColor=SUBTITLE_COLOR, subtitleFontSize=SUBTITLE_SIZE
        ).configure_view(
        strokeOpacity=0  # Hide all axis
        )
    return chart


def part3(
    dataset: pd.DataFrame
        ) -> alt.HConcatChart:
    """
    Generates a horizontal concatenation of scatter plots with regression lines
    for the relationship between 'Miles_per_Gallon' and other vehicle
    attributes.

    Parameters:
        dataset : A DataFrame containing vehicle attributes including
        'Miles_per_Gallon', 'Horsepower', 'Displacement', and 'Weight_in_lbs'.

    Returns:
        A horizontal concatenated chart displaying scatter plots with
        regression lines.
    """
    target_property: str = "Miles_per_Gallon"
    encoding: str = "Q"
    # Create the base chart and apply all the settings as charts with a config
    # cannot be concatenated or layered.
    combined: alt.HConcatChart = alt.hconcat(
        ).properties(
        title=alt.Title(
            "Influence of vehicles attributes on performance",
            anchor="middle", color=TITLE_COLOR, fontSize=TITLE_SIZE,
            subtitle="Comparing the effect of horsepower, displacement and weight on miles per gallon.",  # noqa E501
            subtitleColor=SUBTITLE_COLOR, subtitleFontSize=SUBTITLE_SIZE)
        ).configure_axis(
        labelColor=SUBTITLE_COLOR, titleColor=TITLE_COLOR
        ).configure_view(
        strokeOpacity=0  # Hide all axis
        )
    # Iterate through the specified columns to create scatter plots
    for idx, column in enumerate(
            ["Horsepower", "Displacement", "Weight_in_lbs"]):
        column_base: alt.Chart = alt.Chart(dataset).encode(
            x=alt.X(f"{column}:{encoding}",
                    axis=alt.Axis(grid=False),
                    title=format_label(column)),
            y=alt.Y(f"{target_property}:{encoding}",
                    axis=alt.Axis(grid=False)
                    if idx == 0 else
                    # Hide the axis, label and ticks on all but the left panel
                    alt.Axis(domainOpacity=0, grid=False,
                             labels=False, ticks=False),
                    title=format_label(target_property)
                    if idx == 0 else None))
        row: alt.Chart = column_base.mark_point().encode(
            color=alt.Color(
                f"{target_property}:{encoding}", legend=None,
                scale=alt.Scale(
                    scheme=CONTINUOUS_COLOR_SCHEME,
                    # Invert the color scheme by setting the domain from the
                    # maximum value to the minimum value
                    domain=[dataset[target_property].max(),
                            dataset[target_property].min()]),
                    ))
        # Create regression line
        regression_line: alt.Chart = column_base.transform_regression(
            column, target_property, method="linear").mark_line(
            color=COLOR)
        # Calculate the Pearson correlation coefficient and add the text
        coefficient: alt.Chart = row.transform_filter(
            # Filter out any value is null, undefined, or NaN
            f"isValid(datum.{target_property})"
            ).transform_joinaggregate(
            # Calculate the mean for x and y and join it to the dataset
            mean_x=f"mean({column})", mean_y=f"mean({target_property})"
            ).transform_calculate(
            # Calculate the variance per row
            sub=(f"(datum.{column} - datum.mean_x) *"
                 f" (datum.{target_property} - datum.mean_y)")
            ).transform_aggregate(
            std_x=f"stdev({column})", std_y=f"stdev({target_property})",
            length_x=f"count({column})",
            # Calculate covariance
            cov_sub="sum(sub)"
            ).transform_calculate(
            # Finalize calculating the correlation coefficient
            r_value=("(datum.cov_sub/datum.length_x)/"
                     "(datum.std_x * datum.std_y)"),
            label='"R: "+format(datum.r_value,".2f")'  # Create the label
            ).mark_text(
            fontWeight="bold"
            ).encode(
            x=alt.value(200),  # Position in pixels from left
            y=alt.value(300),  # Position in pixels from top
            text="label:N",
            color=alt.value(COLOR)
            )
        # Combine the row, regression line, and coefficient into the final
        # panel and concatenate it to the chart
        combined |= (row + regression_line + coefficient).properties(
            height=HEIGHT, width=WIDTH//3)
    return combined


def part4(
    dataset: pd.DataFrame
        ) -> alt.VConcatChart:
    """
    Creates a vertical concatenation of scatter plots comparing the lengths
    and widths of iris flower petals and sepals.

    Parameters:
        dataset : The dataset containing iris flower measurements.

    Returns:
        A vertical concatenated chart displaying the comparisons.
    """
    category_name: str = "species"
    base: alt.Chart = alt.Chart(
        dataset, height=HEIGHT//2, width=WIDTH//2
        ).mark_circle()
    # Define a selection parameter for species on the legend
    selection: alt.Parameter =\
        alt.selection_point(fields=[category_name], bind="legend")
    # Generate scatter plots for each pair of measurements
    charts: typing.List[alt.Chart] = [base.encode(
        x=alt.X(f"{x}:Q", title=format_label(x),
                scale=alt.Scale(
                    domain=[0, dataset["sepal_length"].round().max()])),
        y=alt.Y(f"{y}:Q", title=format_label(y),
                scale=alt.Scale(
                    domain=[0, dataset["sepal_width"].round().max()+1])),
        color=alt.Color(f"{category_name}:N",
                        scale=alt.Scale(scheme=DISCRETE_COLOR_SCHEME)),
        tooltip=[alt.Tooltip(f"{category_name}:N",
                             title=format_label(category_name)),
                 alt.Tooltip(f"{x}:Q", title=format_label(x)),
                 alt.Tooltip(f"{y}:Q", title=format_label(y))],
        opacity=(alt.when(selection)
                 .then(alt.value(.8)).otherwise(alt.value(.2)))
        ) for x, y in zip(["sepal_length", "petal_length"],
                          ["sepal_width", "petal_width"])]
    # Combine the charts into a vertical concatenated chart with properties
    combined: alt.VConcatChart = alt.vconcat(*charts).properties(
        title=alt.Title(
            "Iris flower properties compared",
            anchor="middle", color=TITLE_COLOR, fontSize=TITLE_SIZE,
            subtitle="Comparing the length and width for pedals and sepals",
            subtitleColor=SUBTITLE_COLOR, subtitleFontSize=SUBTITLE_SIZE)
            ).configure_axis(
            labelColor=SUBTITLE_COLOR, titleColor=TITLE_COLOR
            ).add_params(selection)
    return combined


def part5(
    dataset: pd.DataFrame
        ) -> alt.VConcatChart:
    """
    Generates a visual representation of the factors affecting housing sale
    prices.

    Parameters:
        dataset : The dataset containing housing sale data with relevant
        features.

    Returns:
        A vertical concatenation of scatter and correlation plots.
    """
    # Standardize column names by replacing spaces with underscores
    dataset.columns = [col.replace(" ", "_") for col in dataset.columns]
    features = ["Year_Built", "Yr_Sold", "Lot_Area", "Overall_Qual"]
    # Set the y-axis
    target_property: str = "SalePrice"
    title_y_axis: str = "Sale price"
    # Create scatter plots for each feature against the target property
    # creating a RepeatChart
    scatter_plots: alt.RepeatChart = alt.Chart(
        dataset, height=HEIGHT//2, width=WIDTH//2
        ).mark_point(
        ).encode(
        x=alt.X(alt.repeat(), bin=alt.Bin(maxbins=10), type="quantitative"),
        y=alt.Y(f"{target_property}:Q", title=title_y_axis),
        color=alt.Color(target_property, legend=None,
                        scale=alt.Scale(scheme=CONTINUOUS_COLOR_SCHEME,
                                        domain=[dataset[target_property].max(),
                                                dataset[target_property].min()]
                                        ))
        ).repeat(
        features, columns=2)
    # Create correlation plots for each feature against the target property
    correlation: alt.VConcatChart = alt.vconcat(
        *[(alt.Chart(dataset).encode(
          x=feature,
          y=alt.Y(target_property,
                  scale=alt.Scale(domain=[0, dataset[target_property].max()]),
                  title=title_y_axis)
          ).transform_regression(
          feature, target_property
          ).mark_line(color=COLOR) +
          alt.Chart(dataset).encode(
          x=feature, y=target_property
          ).transform_joinaggregate(
          # Calculate the mean for x and y and join it to the dataset
          mean_x=f"mean({feature})", mean_y=f"mean({target_property})"
          ).transform_calculate(
          # Calculate the variance per row
          sub=(f"(datum.{feature} - datum.mean_x) *"
               f" (datum.{target_property} - datum.mean_y)")
          ).transform_aggregate(
          std_x=f"stdev({feature})", std_y=f"stdev({target_property})",
          length_x=f"count({feature})",
          # Calculate covariance
          cov_sub="sum(sub)"
          ).transform_calculate(
          # Finalize calculating the correlation coefficient
          r_value=("(datum.cov_sub/datum.length_x)/"
                   "(datum.std_x * datum.std_y)"),
          label='"R: "+format(datum.r_value,".2f")'  # Create the label
          ).mark_text(
          fontWeight="bold"
          ).encode(
          x=alt.value(150),  # Position in pixels from left
          y=alt.value(100),  # Position in pixels from top
          text="label:N",
          color=alt.value(COLOR)
          )).properties(height=HEIGHT//5, width=WIDTH//5)
          for feature in features])
    # Combine scatter plots and correlation plots with titles and styling
    combined = (scatter_plots | correlation).configure_axis(
        labelColor=SUBTITLE_COLOR, titleColor=TITLE_COLOR
        ).properties(
        title=alt.Title(
            "What affects the sale price of housing the most?",
            anchor="middle", color=TITLE_COLOR, fontSize=TITLE_SIZE,
            subtitle=("Comparing the influence of the year it was built, the"
                      " year it was sold, the size of the lot or the overall "
                      "quality on the Sale price."),
            subtitleColor=SUBTITLE_COLOR, subtitleFontSize=SUBTITLE_SIZE))
    return combined


def main() -> None:
    """
    Main function to load datasets and create plots.
    """
    # Load the gapminder dataset and convert years to datetime object
    gapminder: pd.DataFrame = plotly.data.gapminder()
    gapminder["year"] = pd.to_datetime(gapminder["year"], format="%Y")
    # Load the housing dataset by reading the retreived csv into a Pandas
    # DataFrame
    url: str = (
        r"https://raw.githubusercontent.com/wblakecannon/ames/refs/"
        r"heads/master/data/housing.csv")
    housing: pd.DataFrame = pd.read_csv(
        io.BytesIO(requests.get(url).content), sep=",")
    # Load the cars and iris datasets
    mt_cars: pd.DataFrame = vega_datasets.data.cars()
    iris: pd.DataFrame = plotly.data.iris()
    # Create and show plots
    part1(gapminder).show()
    part2(housing).show()
    part3(mt_cars).show()
    part4(iris).show()
    part5(housing).show()


if __name__ == "__main__":
    main()
