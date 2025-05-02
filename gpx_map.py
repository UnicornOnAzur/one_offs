"""
@author: UnicornOnAzur

This module provides functionality to generate a folium map with GPX tracks.
It allows users to upload GPX files, extract their coordinates, and visualize
the tracks on an interactive map.
"""

#  Standard library
import typing
# Third party
import folium
import geopandas as gpd
import matplotlib as mpl
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
#
UPLOADED_FILE: typing.TypeAlias =\
    typing.Optional[typing.List[st.runtime.uploaded_file_manager.UploadedFile]]


def make_map(
    file_list: UPLOADED_FILE
        ) -> str:
    """
    Generates a folium map with GPX tracks.

    This function reads GPX files, extracts their coordinates, and creates a
    map with polylines representing the tracks.

    Parameters:
        file_list : A single GPX file or a list of GPX files to be plotted on
        the map.

    Returns:
        The rendered HTML representation of the folium map.
    """
    def _read_gpx(file_name):
        """Reads a GPX file and returns its contents as a GeoDataFrame.

        Parameters:
            file_name : The GPX file to read.

        Returns:
            The GeoDataFrame containing the GPX data.
        """
        return gpd.read_file(file_name, layer="tracks")

    def get_coordinates(
        file: str
            ) -> gpd.GeoDataFrame:
        """
        Extracts coordinates from a GPX file and reverses the order of 'x' and
        'y'.

        Parameters:
            file : The GPX file from which to extract coordinates.

        Returns:
            A DataFrame containing the coordinates with 'y' and 'x' columns.
        """
        return _read_gpx(file).geometry.get_coordinates()[["y", "x"]]

    def make_polyline(
        gpx_file: UPLOADED_FILE,
        color: str
            ) -> folium.FeatureGroup:
        """
        Creates a polyline feature for a GPX file.

        Parameters:
            gpx_file : The GPX file to create a polyline for.
            color : The color of the polyline.

        Returns:
            The feature group containing the polyline.
        """
        lines_layer: folium.FeatureGroup = folium.FeatureGroup(name=gpx_file)
        coords: gpd.GeoDataFrame = get_coordinates(gpx_file)
        folium.PolyLine(locations=coords,
                        color=color).add_to(lines_layer)
        return lines_layer

    def update_bounds(
        file_list: UPLOADED_FILE
            ) -> tuple[float]:
        """
        Updates the bounds of the map based on the GPX files.

        Parameters:
            file_list : A list of GPX files to calculate bounds from.

        Returns:
            A tuple containing the minimum and maximum bounds.
        """
        gdf: gpd.GeoDataFrame = pd.concat(map(_read_gpx, file_list))
        bounds: tuple[float] = gdf.geometry.total_bounds
        return bounds

    colormap: typing.List[str] = list(map(mpl.colors.rgb2hex,
                                          mpl.colormaps["Set1"].colors))
    map_: folium.Map = folium.Map()
    for file_name, color in zip(file_list or [], colormap):
        make_polyline(file_name, color).add_to(map_)

    # Fit the extent of the map to the tracks
    if file_list:
        xmin, ymin, xmax, ymax = update_bounds(file_list)
        map_.fit_bounds([[ymin, xmin], [ymax, xmax]])
    return folium.Figure().add_child(map_).render()


def main() -> None:
    """
    Initializes the Streamlit application to display GPX tracks on a map.

    This function sets up the page configuration, allows users to upload GPX
    files, generates an HTML map from the uploaded files, and provides a
    download button for the generated map.

    Parameters:
    None

    Returns:
        None
    """
    st.set_page_config(page_title="Display GPX on map",
                       page_icon=":world_map:",
                       layout="wide")
    st.title("Display GPX on a Map")
    left, right = st.columns([.2, .8], gap="small",
                             vertical_alignment="center")
    files: UPLOADED_FILE = left.file_uploader(
        label="Upload your GPX tracks", type="gpx",
        accept_multiple_files=True)
    html_map: str = make_map(files)
    left.download_button(label="Download your map", data=html_map,
                         file_name="your_map.html")
    with right:
        components.html(html_map, height=500)


if __name__ == "__main__":
    main()
