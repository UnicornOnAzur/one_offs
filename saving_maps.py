# -*- coding: utf-8 -*-
"""
author: UnicornOnAzur

This module provides functions to export geospatial figures in various formats,
namely PNG, HTML, GeoJSON, Shapefiles, and binary files. It utilizes libraries
such as GeoPandas, Matplotlib, Plotly, and Folium for creating and exporting
the visualizations.
"""
# Standard library
import base64
import io
import pathlib
import PIL
import tempfile
import typing
import zipfile
# Third party
import PIL.Image
import folium
import geodatasets
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import shapely
# Global variables
BOUNDS: typing.List[int] = [-123, 25, -68, 50]


def _create_geodataframe() -> gpd.GeoDataFrame:
    """
    Create a GeoDataFrame with a single point location.

    Returns:
        A GeoDataFrame containing the point location.
    """
    data: typing.Dict[str, typing.List[typing.Union[float, str]]] = {
        "latitude": [38.0000],
        "longitude": [-97.0000],
        "name": ["Location A"]
        }
    data["geometry"] = shapely.Point(data["longitude"], data["latitude"])
    # Create the GeoDataFrame and set the coordinate reference system to WGS84
    gdf: gpd.GeoDataFrame = gpd.GeoDataFrame(data=data).set_crs("EPSG:4326")
    return gdf


def _create_figure_from_geopandas(
    gdf: gpd.GeoDataFrame
        ) -> plt.Figure:
    """
    Create a Matplotlib figure from a GeoDataFrame.

    Parameters:
        gdf : The GeoDataFrame to plot.

    Returns:
        A Matplotlib figure containing the plotted GeoDataFrame.
    """
    figure, ax = plt.subplots(figsize=(7, 7))
    world: gpd.GeoDataFrame =\
        gpd.read_file(geodatasets.get_path("naturalearth.land"))
    world.plot(color="lightgrey", ax=ax)
    gdf.plot(color="blue", ax=ax)
    xmin, ymin, xmax, ymax = BOUNDS
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    return figure


def _create_plotly_figure(
    gdf: gpd.GeoDataFrame
        ) -> go.Figure:
    """
    Creates a Plotly scatter map figure from a GeoDataFrame.

    Parameters:
    gdf: A GeoDataFrame containing latitude and longitude columns.

    Returns:
        A Plotly Figure object representing the scatter map.
    """
    figure: go.Figure = px.scatter_map(data_frame=gdf,
                                       lat="latitude",
                                       lon="longitude",
                                       width=700,
                                       height=700)
    return figure


def _create_folium_map(
    gdf: gpd.GeoDataFrame
        ) -> folium.Map:
    """
    Creates a Folium map centered on the first location in the GeoDataFrame.

    Parameters:
    gdf: A GeoDataFrame containing latitude and longitude columns.

    Returns:
    A Folium Map object centered on the specified coordinates.
    """
    # Extracting the location's latitude and longitude
    location: typing.List[float] = gdf[["latitude", "longitude"]].values[0]
    map_: folium.Map = folium.Map(
        location=location,
        width=700,
        height=700)
    folium.Marker(location).add_to(map_)
    xmin, ymin, xmax, ymax = BOUNDS
    map_.fit_bounds([[ymin, xmin], [ymax, xmax]])
    return map_


def geopandas_to_picture(
    gdf: gpd.GeoDataFrame
        ) -> None:
    """
    Converts a GeoDataFrame to a picture and saves it as a PNG file.

    Parameters:
    gdf: A GeoDataFrame containing geographical data.

    Returns:
    None
    """
    figure: plt.Figure = _create_figure_from_geopandas(gdf)
    figure.savefig("geopandas.png")


def geopandas_to_html(
    figure: plt.Figure
        ) -> None:
    """
    Converts a matplotlib figure to an HTML image tag and saves it to a file.

    Parameters:
    figure: The matplotlib figure to be converted.

    Returns:
    None
    """
    with io.BytesIO() as buffer:
        figure.savefig(buffer, format="png")
        buffer.seek(0)  # Move to the beginning of the buffer
        img_base64: str = base64.b64encode(buffer.read()).decode("utf-8")
        html: str = f'<img src="data:image/png;base64,{img_base64}" />'
        with open("geopandas.html", "w") as file:
            file.write(html)


def geopandas_to_geojson(
    gdf: gpd.GeoDataFrame
        ) -> None:
    """
    Converts a GeoDataFrame to a GeoJSON file.

    Parameters:
    gdf: A GeoDataFrame containing geometrical data.

    Returns:
    None
    """
    gdf.to_file("geopandas.geojson", driver="GeoJSON")


def geopandas_to_shapefile(
    gdf: gpd.GeoDataFrame
        ) -> None:
    """
    Converts a GeoDataFrame to a shapefile.

    Parameters:
    gdf: A GeoDataFrame containing geometrical data.

    Returns:
    None: This function does not return any value.
    """
    gdf.to_file("geopandas.shp", driver="ESRI Shapefile")


def geopandas_to_zipped_shapefile(
    gdf: gpd.GeoDataFrame
        ) -> None:
    """
    Converts a GeoDataFrame to a zipped shapefile.

    Parameters:
    gdf: A GeoDataFrame containing the geographical data to be converted.

    Returns:
    None: This function does not return any value.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path: pathlib.Path = pathlib.Path(temp_dir)
        gdf.to_file(f"{temp_dir_path}/geopandas.shp", driver="ESRI Shapefile")
        with zipfile.ZipFile("geopandas.zip", "w") as zip_file:
            for file in temp_dir_path.glob("*"):
                zip_file.write(file, arcname=file.name)


def geopandas_to_binary1(
    figure: plt.Figure
        ) -> None:
    """
    Converts a Matplotlib figure to binary format and saves it to a text file.

    Parameters:
    figure: The Matplotlib figure to be converted.

    Returns:
    None
    """
    with io.BytesIO() as buffer:
        figure.savefig(buffer, format="png")
        buffer.seek(0)  # Move to the beginning of the buffer
        with open("geopandas_binary1.txt", "wb") as file:
            file.write(buffer.getvalue())


def geopandas_to_binary2(
    gdf: gpd.GeoDataFrame
        ) -> None:
    """
    Converts a GeoDataFrame to a binary format and saves it to a file.

    Parameters:
    gdf: A GeoDataFrame containing geospatial data.

    Returns:
    None
    """
    with io.BytesIO() as buffer:
        gdf.to_file(buffer, driver="GeoJSON")
        buffer.seek(0)  # Move to the beginning of the buffer
        with open("geopandas_binary2.txt", "wb") as file:
            file.write(buffer.getvalue())


def plotly_to_picture1(
    fig: go.Figure
        ) -> None:
    """
    Save a Plotly figure as an image file.

    Parameters:
    fig: A Plotly figure object that needs to be saved as an image.

    Returns:
    None
    """
    fig.write_image("plotly1.png")


def plotly_to_picture2(
    fig: go.Figure
        ) -> None:
    """
    Converts a Plotly figure to a PNG image and saves it to a file.

    Parameters:
    fig: A Plotly figure object that needs to be converted to an image.

    Returns:
    None: This function does not return any value.
    """
    with open("plotly2.png", "wb") as file:
        file.write(fig.to_image("png"))


def plotly_to_html(
    fig: go.Figure
        ) -> None:
    """
    Converts a Plotly figure to an HTML file.

    Parameters:
    fig: The Plotly figure object to be converted.

    Returns:
    None
    """
    fig.write_html("plotly.html")


def plotly_to_binary(
    fig: go.Figure
        ) -> None:
    """
    Converts a Plotly figure to binary format and saves it to a file.

    Parameters:
    fig: A Plotly figure object that needs to be converted to binary.

    Returns:
    None
    """
    img_bytes: bytes = fig.to_image(format="png")
    with io.BytesIO(img_bytes) as buffer, open("plotly.txt", "wb") as file:
        file.write(buffer.getvalue())


def folium_to_picture(
    map_: folium.Map
        ) -> None:
    """
    Converts a Folium map to a PNG image and saves it as 'folium.png'.

    Parameters:
    map_: A Folium map object that needs to be converted to an image.

    Returns:
    None
    """
    img_data: bytes = map_._to_png()
    img: PIL.PngImagePlugin.PngImageFile =\
        PIL.Image.open(io.BytesIO(img_data))
    img.save("folium.png")


def folium_to_html(
    map_: folium.Map
        ) -> None:
    """
    Save a Folium map to an HTML file.

    Parameters:
    map_: A Folium Map object that needs to be saved.

    Returns:
    None
    """
    map_.save("folium.html")


def folium_to_binary(
    map_: folium.Map
        ) -> None:
    """
    Converts a Folium map object to a binary file.

    Parameters:
    map_: A Folium map object that needs to be saved as a binary file.

    Returns:
    None
    """
    with open("folium.txt", "wb") as file:
        file.write(map_._to_png())


def main() -> None:
    """
    Main function to create and export various geospatial visualizations.

    Parameters:
    None

    Returns:
    None
    """
    gdf: gpd.GeoDataFrame = _create_geodataframe()
    figure: plt.Figure = _create_figure_from_geopandas(gdf)
    plotly_figure: go.Figure = _create_plotly_figure(gdf)
    map_: folium.Map = _create_folium_map(gdf)
    # GeoPandas examples
    geopandas_to_picture(gdf)
    geopandas_to_html(figure)
    geopandas_to_geojson(gdf)
    geopandas_to_shapefile(gdf)
    geopandas_to_zipped_shapefile(gdf)
    geopandas_to_binary1(figure)
    geopandas_to_binary2(gdf)
    # Plotly examples
    plotly_to_picture1(plotly_figure)
    plotly_to_picture2(plotly_figure)
    plotly_to_html(plotly_figure)
    plotly_to_binary(plotly_figure)
    # Folium examples
    folium_to_picture(map_)
    folium_to_html(map_)
    folium_to_binary(map_)


if __name__ == "__main__":
    main()
