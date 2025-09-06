# -*- coding: utf-8 -*-
"""
author: UnicornOnAzur

This module obtains, processes, and illustrates data concerning the French
departments. It collects geographical, demographic, and historical information,
constructs a GeoDataFrame, and produces an infographic representation of the
departments.

The process involves the following steps:
1. Retrieve data from online sources or cached files;
2. Construct a GeoDataFrame using the retrieved data;
3. Ensure the data is consistent and accurate;
4. Create a figure with multiple axes for data visualization;
5. Store the infographic.
"""
# Standard library
import datetime
import io
import typing
# Third-party
import PIL.Image
import geopandas as gpd
import matplotlib as mpl
import matplotlib.gridspec as gs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PIL
import requests
# File paths
DATA_FOLDER: str = "data/"
GEOJSON_FILENAME: str = f"{DATA_FOLDER}france.geojson"
WIKI_FILE: str = f"{DATA_FOLDER}html.txt"
XLS_FILENAME: str = f"{DATA_FOLDER}evolution-population-dep-2010-2023.xls"
LOGO_FILENAME: str = f"{DATA_FOLDER}logo.png"
# URLS
GEOJSON_URL: str =\
    "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
WIKIPEDIA_URL: str = "https://en.wikipedia.org/wiki/Departments_of_France"
XLS_URL: str = ("https://www.insee.fr/fr/statistiques/fichier/1893198/"
                "evolution-population-dep-2010-2023.xls")
# Text
MAIN_TITLE: str = ("Exploring the Departments of France: A Look at Their "
                   "History and Present")
EXPLANATION: str = (
    "With the onset of the French Revolution, departments were formed to "
    "dismantle the $l'Ancien$ $Regime$'s power over the regions. They arranged"
    " the boundaries so that every settlement was within a day's travel to the"
    " department's capital, promoting a more cohesive nation and improved "
    "oversight. All departments were named after rivers, mountains, or coastal"
    " areas and they were numbered according to their alphabetical order. As "
    "of now, there are 96 departments in metropolitan France.")
SUB_TITLE_1: str =\
    "The current department INSEE codes colored in numerical order"
SUB_TITLE_2: str = "Departments colored by area size"
SUB_TITLE_3: str = "Departments colored by population size"
SUB_TITLE_4: str =\
    "Establishment dates of the current departments: numbers per year"
# Column names
XLS_POPULATION_COLUMN: str = "Estimations de population au 1er janvier 2023"
COLUMN_POPULATION: str = "population"
COLUMN_AREA: str = "area"
COLUMN_CODE: str = "code"
COLUMN_CODE_NEW: str = "INSEE code"
COLUMN_DATE: str = "establisment date"
COLUMN_NAME: str = "nom"
# Set matplotlib parameters
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.size"] = 7
mpl.rcParams["mathtext.fontset"] = "dejavuserif"


def _fetch_data(
    filename: str,
    url: str
        ) -> bytes:
    """
    Fetches data from a local file or a remote URL.

    This function attempts to read data from a specified local file. If the
    file does not exist, it retrieves the data from a remote URL and saves it
    locally for future use.

    Parameters:
        filename : The name of the local file to read from.
        url : The URL to fetch data from if the local file is not found.

    Returns:
        The data in bytes format.
    """
    try:
        with open(filename, "rb") as file:
            data_bytes: bytes = file.read()
            print(f"{filename} retrieved from local file.")
    except FileNotFoundError:
        print(f"Retrieving data from {url}...")
        response: requests.Response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data_bytes: bytes = response.content
        with open(filename, "wb") as file:
            file.write(data_bytes)
        print(f"{filename} saved to local file.")
    return data_bytes


def fetch_files() -> tuple[bytes, bytes, io.BytesIO]:
    """
    Fetches GeoJSON data, Wikipedia page content, and population statistics
    from local files or remote URLs.

    This function attempts to read GeoJSON data, Wikipedia page content, and
    population statistics from specified local files. If the files do not
    exist, it retrieves the data from remote URLs and saves them locally for
    future use.

    Parameters:
        None

    Returns:
        A tuple containing GeoJSON data, Wikipedia page content, and population
        statistics in bytes format.
    """

    geojson_bytes: bytes = _fetch_data(GEOJSON_FILENAME, GEOJSON_URL)
    page_content: bytes = _fetch_data(WIKI_FILE, WIKIPEDIA_URL)
    population: bytes = _fetch_data(XLS_FILENAME, XLS_URL)
    return geojson_bytes, page_content, io.BytesIO(population)


def _validate_data(
    gdf: gpd.GeoDataFrame
        ) -> None:
    """
    Validate the loaded GeoDataFrame to ensure that specific conditions are
    met.

    This function checks that:
    - The region with the lowest code is 'Ain'.
    - The region with the highest code is 'Val-d'Oise'.
    - The region with the smallest area is 'Paris'.
    - The region with the largest area is 'Gironde'.
    - The region with the lowest population is 'Lozère'.
    - The population of 'Lozère' is exactly 76648.
    - The region with the highest population is 'Nord'.
    - The population of 'Nord' is exactly 2,606,646.
    - The minimum date in the dataset is '1790-02-26'.
    - The maximum date in the dataset is '1979-01-01'.

    Parameters:
        gdf : The GeoDataFrame containing geographical data to validate.

    Raises:
        AssertionError: If any of the validation checks fail.

    Returns:
        None
    """
    assert gdf.loc[gdf[COLUMN_CODE_NEW].idxmin(), COLUMN_NAME] == "Ain"
    assert gdf.loc[gdf[COLUMN_CODE_NEW].idxmax(), COLUMN_NAME] == "Val-d'Oise"
    assert gdf.loc[gdf[COLUMN_AREA].idxmin(), COLUMN_NAME] == "Paris"
    assert gdf.loc[gdf[COLUMN_AREA].idxmax(), COLUMN_NAME] == "Gironde"
    assert gdf.loc[gdf[COLUMN_POPULATION].idxmin(), COLUMN_NAME] == "Lozère"
    assert gdf.loc[gdf[COLUMN_POPULATION].idxmin(),
                   COLUMN_POPULATION] == 76648
    assert gdf.loc[gdf[COLUMN_POPULATION].idxmax(), COLUMN_NAME] == "Nord"
    assert gdf.loc[gdf[COLUMN_POPULATION].idxmax(),
                   COLUMN_POPULATION] == 2606646
    assert gdf[COLUMN_DATE].min() == pd.Timestamp("1790-02-26 00:00:00")
    assert gdf[COLUMN_DATE].max() == pd.Timestamp("1979-01-01 00:00:00")


def create_gdf(
    geojson_file: bytes,
    page_content: bytes,
    population_bytes: bytes
        ) -> gpd.GeoDataFrame:
    """
    Creates a GeoDataFrame by reading geographical data from a GeoJSON file,
    transforming the coordinate reference system, and merging additional data
    being establisment dates from Wikipedia and demographics from an Excel
    file. Before returning the GeoDataFrame, the date is validated.

    Parameters:
        geojson_file : The GeoJSON file containing geographical data.
        page_content : The HTML content from Wikipedia containing
            establishment dates.
        population_bytes : The Excel file containing population data.

    Returns:
        A GeoDataFrame containing geographical and demographic data, and dates.
    """
    gdf: gpd.GeoDataFrame = gpd.read_file(geojson_file)
    # Transform the coordinate reference system to the best fitting for France:
    # RGF93 v1 / Lambert-93 -- France
    gdf.to_crs(2154, inplace=True)
    gdf[COLUMN_AREA] = gdf["geometry"].area
    # Get a central point within the departments to use for labeling
    gdf["coords"] = [coords[0] for coords in gdf["geometry"].apply(
        lambda x: x.representative_point().coords[:])]
    # Clean the INSEE codes form the table with the establisment dates from the
    # Wikipedia page, and load it into a column
    html: pd.DataFrame =\
        pd.read_html(page_content)[3].iloc[2:, [0, 2]].astype({0: str})\
        .set_index(0).drop(["69M"], axis="index").rename(index={"69D": "69"})
    gdf[COLUMN_DATE] = pd.merge(left=gdf, right=html, left_on=COLUMN_CODE,
                                right_on=html.index, how="left")[2].apply(
                                lambda d:
                                datetime.datetime.strptime(d, "%d %B %Y"))
    # Merge Corsica's two department numbers into one
    gdf[COLUMN_CODE_NEW] = gdf[COLUMN_CODE].replace({"2A": "20", "2B": "20"})
    # Load the population number in to a column
    population: pd.DataFrame = pd.read_excel(population_bytes, sheet_name=2,
                                             header=2, usecols=[0, 1])
    gdf[COLUMN_POPULATION] = pd.merge(
        left=gdf, right=population,
        left_on=COLUMN_NAME, right_on="Département")[XLS_POPULATION_COLUMN]
    # Convert columns to appropriate data types
    gdf: gpd.GeoDataFrame = gdf.astype({COLUMN_CODE_NEW: int,
                                        COLUMN_POPULATION: int})

    _validate_data(gdf)
    return gdf


def make_figure(
        ) -> tuple[plt.Figure, typing.Dict[str, mpl.axes.Axes]]:
    """
    Creates a figure with multiple subplots and inset axes.

    This function generates a matplotlib figure with a specified layout,
    including a main plot, minimap, and various inset axes. It configures
    the appearance of the axes and returns the figure and axes for further
    customization.

    Parameters:
        None

    Returns:
        A tuple containing the created figure and a dictionary of axes.
    """
    axes: typing.Dict[str, mpl.axes.Axes] = {}
    # Create a figure with the specified size and set the title and header. The
    # basic figure is scaled from a 700 pixel width.
    scale: float = 1.25
    figure: plt.Figure = plt.figure(figsize=(7*scale, 5.85*scale))
    # Create a grid layout for the subplots with specified height and width
    # ratios, define the position of the insets and add all the axes to the
    # dictionary.
    gridspec: gs.GridSpec = gs.GridSpec(nrows=4, ncols=2, left=0, bottom=0,
                                        right=1, top=1, wspace=0, hspace=0,
                                        height_ratios=[.08, .4, .4, .12],
                                        width_ratios=[2/3, 1/3],
                                        )
    inset_colorbar_position: typing.List[float] = [.025, .005, .85, .075]
    axes["left"] = (axis1 := figure.add_subplot(gridspec[1:3, 0]))

    axes["minimap"] = axis1.inset_axes([.79, .8, .2, .2])
    axes["top_right"] = (axis2 := figure.add_subplot(gridspec[1, 1]))
    axes["inset_tr"] = axis2.inset_axes(inset_colorbar_position)
    axes["bottom_right"] = (axis3 := figure.add_subplot(gridspec[2, 1]))
    axes["inset_br"] = axis3.inset_axes(inset_colorbar_position)
    axes["timeline"] = (axis4 := figure.add_subplot(gridspec[3, 0:]))
    axes["logo"] = axis4.inset_axes([.72, .09, .5, .5])
    # Style all axes
    for name, ax in axes.items():
        ax.set_xticks([])
        ax.set_yticks([])
        if name != "minimap":  # Remove all spines except for the minimap
            ax.axis("off")
    return figure, axes


def _draw_choropleth(
    ax: mpl.axes.Axes,
    gdf: gpd.GeoDataFrame,
    column: str,
    title: str,
    cmap_name: str,
    dy: typing.Optional[int] = 0
        ) -> None:
    """
    Draws a choropleth map on the provided axes.

    Parameters:
        ax : The axes on which to draw the choropleth.
        gdf : The GeoDataFrame containing the geographical data.
        column : The column name in the GeoDataFrame to be visualized.
        title : The title of the choropleth map.
        cmap_name : The name of the colormap to be used for the choropleth.
        dy : Vertical adjustment for the title position, optional.

    Returns:
        None
    """
    gdf.plot(column=column,
             cmap=mpl.colormaps.get_cmap(cmap_name),
             ax=ax,
             aspect=None,
             edgecolor="black",
             linewidth=.25)
    ax.set_title(title, loc="left", y=.935+dy, fontweight="bold")


def _create_custom_colormap(
    number_of_points: int
        ) -> mpl.colors.ListedColormap:
    """
    Creates a custom colormap using specified color transitions going from
    blue through white to red to symbolize the colors of the French flag.

    Parameters:
        number_of_points: The total number of color points in the colormap.

    Returns:
        A colormap object that can be used in matplotlib visualizations.
    """
    def _generate_color_values(
        start1: float,
        end1: float,
        start2: float,
        end2: float
            ) -> np.ndarray:
        """
        Generates a concatenated array of color values.

        Parameters:
            start1 : Starting value for the first color range.
            end1 : Ending value for the first color range.
            start2 : Starting value for the second color range.
            end2 : Ending value for the second color range.

        Returns:
            An array of concatenated color values.
        """
        return np.concatenate((np.linspace(start1, end1, number_of_points//2),
                               np.linspace(start2, end2, number_of_points//2 +
                                           number_of_points % 2)
                               ), axis=None)
    # Create an array with RGBA channels
    vals: np.ndarray = np.ones((number_of_points, len("RGBA")))
    vals[:, 0] = _generate_color_values(0, 1, 1, 1)  # Red channel
    vals[:, 1] = _generate_color_values(0, 1, 1, 0)  # Green channel
    vals[:, 2] = _generate_color_values(1, 1, 1, 0)  # Blue channel
    return mpl.colors.ListedColormap(vals)


def _place_colorbar(
    ax: mpl.axes.Axes,
    cmap: mpl.colors.Colormap,
        ) -> None:
    """
    Places a colorbar on the given axes with specified colormap.

    Parameters:
        ax : The axes on which to place the colorbar.
        cmap : The colormap to use for the colorbar.

    Returns:
        None
    """
    cbar: mpl.colorbar.Colorbar = plt.colorbar(
        mpl.cm.ScalarMappable(cmap=cmap),
        cax=ax.inset_axes([.025, .005, .85, .05]),
        orientation="horizontal"
        )
    cbar.set_ticks(ticks=[], labels=[])  # Set empty ticks and labels
    for insee_code in np.linspace(10, 90, 9):
        cbar.ax.text(insee_code/100, .5, int(insee_code),
                     ha="center", va="center")


def _create_kde_colorbar(
    ax: mpl.axes.Axes,
    dataset: pd.Series,
    names: pd.Series,
    cmap_name: str
        ) -> None:
    """
    Creates a Kernel Density Estimate (KDE) colorbar on the provided axes.

    Parameters:
        ax : The axes on which to draw the colorbar.
        dataset : The dataset used for the KDE.
        names: The dataset to reference the department names from.
        cmap_name : The name of the colormap to be used for the colorbar.

    Returns:
        None
    """
    # Calculate the KDE for the dataset
    kde = mpl.mlab.GaussianKDE(dataset=dataset)
    x: np.ndarray = np.linspace(min(dataset), max(dataset), 1000)
    y: np.ndarray = kde(x)
    # Calculate midpoints for x and y
    x_midpts: np.ndarray = np.hstack((x[0], 0.5 * (x[1:] + x[:-1]), x[-1]))
    y_midpts: np.ndarray = np.hstack((y[0], 0.5 * (y[1:] + y[:-1]), y[-1]))
    # Create segments for the colorbar
    coord_start: np.ndarray = np.column_stack(
        (x_midpts[:-1], y_midpts[:-1]))[:, np.newaxis, :]
    coord_mid: np.ndarray = np.column_stack((x, y))[:, np.newaxis, :]
    coord_end: np.ndarray = np.column_stack(
        (x_midpts[1:], y_midpts[1:]))[:, np.newaxis, :]
    segments: np.ndarray = np.concatenate(
        (coord_start, coord_mid, coord_end), axis=1)
    # Generate colors for each segment
    colors: np.ndarray = plt.colormaps[cmap_name](np.linspace(0, 1,
                                                              len(segments)))
    # Create a LineCollection for the segments and add to the axis
    lc: mpl.collections.LineCollection = mpl.collections.LineCollection(
        segments, linewidths=1.5, colors=colors, alpha=1, capstyle="butt")
    ax.add_collection(lc)
    # Fill between segments with corresponding colors
    for idx, segment in enumerate(segments):
        ax.fill_between([segment[0][0], segment[-1][0]],
                        [segment[0][1], segment[-1][1]],
                        color=colors[idx]
                        )
    ax.set_ylim([0, max(y)*1.05])
    # Annotate the minimum and maximum values on the axes
    if min(dataset) > 10**7:
        text_min, text_max = f"{min(dataset)/10**6:.0f} km\u00b2", \
                             f"{max(dataset)/10**6:.0f} km\u00b2"
    else:
        text_min, text_max = map(str, (min(dataset), max(dataset)))
    text_min: str = f"{names.loc[dataset.idxmin()]}\n" + text_min
    text_max: str = f"{names.loc[dataset.idxmax()]}\n" + text_max
    _annotate_min_max(ax, text_min, x, y, min, "left")
    _annotate_min_max(ax, text_max, x, y, max, "right")
    # Mark the median
    median_value: float = np.median(dataset)
    ax.axvline(median_value, c="black")
    ax.text(median_value, 0, "median", rotation=90, fontsize=4.5,
            verticalalignment="bottom", horizontalalignment="right")


def _annotate_min_max(
    ax: mpl.axes.Axes,
    text: str,
    x: typing.List[float],
    y: typing.List[float],
    func: typing.Callable[[typing.Iterable[float]], float],
    align: str
        ) -> None:
    """
    Annotates the minimum or maximum point on a given axis.

    Parameters:
    ax : The axes on which to annotate.
    text : The text to display at the annotation.
    x : The x-coordinates of the axes.
    y : The y-coordinates of the axes.
    func : A function that returns either the minimum or maximum of a list.
    align : The horizontal alignment of the annotation text.
    """
    # Annotate the specified point on the graph
    ax.annotate(text, xy=(func(x), 0),
                xytext=(func(x), max(y)),
                horizontalalignment=align,
                fontsize=5,
                arrowprops={"arrowstyle": "->"})


def _make_timeline(
    ax: mpl.axes.Axes,
    dataset: gpd.GeoSeries
        ) -> None:
    """
    Creates a timeline visualization on the provided axes using the given
    dataset.

    Parameters:
        ax : The axes on which to draw the timeline.
        dataset : A pandas Series containing datetime data for the timeline.

    Returns:
        None
    """
    # Count occurrences of each year in the dataset
    counts: pd.DataFrame = dataset.dt.year.value_counts()\
        .reset_index().sort_values(COLUMN_DATE)
    # Calculate y positions using logarithmic scale
    y_positions: np.ndarray = np.log(counts["count"]) + 1
    ymax: float = max(y_positions)
    time_range: typing.List[int] = [1775, 2025]
    # Add a timeline by adding a horizontal line with major and minor ticks.
    # Furthermore, add the centuries as text above the major ticks.
    timeline_color: str = "#bdbdbd"
    centuries: np.ndarray = np.linspace(1800, 2000, 3)
    ax.axhline(.1, c=timeline_color, linewidth=2, zorder=5)
    ax.vlines(np.linspace(*time_range, 11), .1, .5, colors=timeline_color)
    ax.vlines(centuries, .1, 3, linewidth=5, colors=timeline_color)
    ax.vlines(centuries, 5.5, 6.5, linewidth=5, colors=timeline_color)
    for century in centuries:
        ax.text(century-1, 3.5, int(century), color=timeline_color,
                rotation=90, fontdict={"size": 6})
    # Highlight the French Revolution period
    ax.axvspan(1789, 1799, ymax=.95, color="maroon", alpha=.5)
    ax.annotate(" French revolution:\n 1789-1799", (1789, 7),
                xytext=(1777, .5),  size=5, rotation=90,
                arrowprops={"arrowstyle": "-", "color": "grey"})
    # Plot establishment years with annotations
    for x_pos, y_pos, count, color in zip(
            counts[COLUMN_DATE],
            y_positions,
            counts["count"],
            mpl.colormaps["plasma"](np.linspace(0, 1, counts.shape[0]))):
        ax.vlines(x=x_pos, ymin=0, ymax=y_pos, colors=color, alpha=.7)
        ax.plot(x_pos, y_pos, "ko", mfc=color)
        ax.annotate(f"{x_pos}: {count}", (x_pos+2, y_pos),
                    xytext=(x_pos+10, y_pos if x_pos == 1871 else y_pos+.5),
                    size=7, horizontalalignment="left",
                    arrowprops={"arrowstyle": "-"})
    # Set title and limits for the axes
    ax.set_title(SUB_TITLE_4, loc="center", y=.75)
    ax.set_xlim(time_range)
    ax.set_ylim([0, 1.5*ymax])


def fill_axes(
    dataframe: gpd.GeoDataFrame,
    figure: plt.Figure,
    axes: typing.Dict[str, mpl.axes.Axes]
        ) -> None:
    """
    Fills the provided axes with choropleth maps and annotations based on the
    given dataframe.

    Parameters:
        dataframe : The data source containing department information.
        figure : The figure object to which the axes belong.
        axes : A dictionary containing the axes for plotting.

    Returns:
        None
    """
    # Header
    figure.suptitle(MAIN_TITLE, y=.999, **{"fontsize": 10,
                                           "fontweight": "bold"})
    figure.text(x=0.01, y=.93, s=EXPLANATION, wrap=True)
    # Figure 1: Department colored by number
    cmap1: mpl.colors.ListedColormap =\
        _create_custom_colormap(len(dataframe[COLUMN_CODE_NEW].unique()))
    _draw_choropleth(axes["left"], dataframe, COLUMN_CODE_NEW, SUB_TITLE_1,
                     cmap1, .0255)
    _place_colorbar(axes["left"], cmap1)
    # Create minimap
    _draw_choropleth(axes["minimap"], dataframe, COLUMN_CODE_NEW, "",
                     cmap1)
    axes["minimap"].set_xlim([.635*10**6, .675*10**6])
    axes["minimap"].set_ylim([6.8515*10**6, 6.8915*10**6])
    axes["left"].indicate_inset_zoom(axes["minimap"], edgecolor="black",
                                     alpha=.4)
    # Add department numbers
    numbers: typing.Dict = {}
    for _, row in dataframe.iterrows():
        target_axes: mpl.axes.Axes = axes["left"]\
            if row[COLUMN_AREA] > 1.5 * 10**9 else axes["minimap"]
        numbers[row[COLUMN_CODE_NEW]] = target_axes.annotate(
            row[COLUMN_CODE], xy=row["coords"], horizontalalignment="center",
            size=5)
    axes["left"].annotate(90, xy=dataframe.loc[dataframe["code"] == "90",
                                               "coords"].values[0],
                          xytext=(1_100_000, 6_700_000),
                          arrowprops={"arrowstyle": "->",
                                      "connectionstyle": "angle3"},
                          size=5)
    # Adjust some department numbers
    numbers[22].set_y(6_820_000)
    numbers[31].set_y(6_240_000)
    numbers[54].set_y(6_850_000)
    # Figure 2: Department colored by area
    cmap2: str = "Blues"
    _draw_choropleth(axes["top_right"], dataframe, COLUMN_AREA,
                     SUB_TITLE_2, cmap2)
    _create_kde_colorbar(axes["inset_tr"], dataframe[COLUMN_AREA],
                         dataframe[COLUMN_NAME], cmap2)

    # # Figure 3: Department colored by population size
    cmap3: str = "Reds"
    _draw_choropleth(axes["bottom_right"], dataframe, COLUMN_POPULATION,
                     SUB_TITLE_3, cmap3)
    _create_kde_colorbar(axes["inset_br"], dataframe[COLUMN_POPULATION],
                         dataframe[COLUMN_NAME], cmap3)
    # Figure 4: A timeline of the establisment dates of departments
    _make_timeline(axes["timeline"], dataframe[COLUMN_DATE])
    # Add logo
    axes["logo"].imshow(PIL.Image.open(LOGO_FILENAME))


def main() -> None:
    gdf: gpd.GeoDataFrame = create_gdf(*fetch_files())
    fig, axes = make_figure()
    fill_axes(gdf, fig, axes)
    plt.show()


if __name__ == "__main__":
    main()
