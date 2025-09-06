"""
author: UnicornOnAzur

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
# Constants
UPLOADED_FILE: typing.TypeAlias =\
    typing.Optional[typing.List[st.runtime.uploaded_file_manager.UploadedFile]]


def make_map(
    file_list: UPLOADED_FILE
        ) -> str:
    """
    Generates a folium map with GPX tracks.

    This function reads GPX files, extracts their coordinates, and creates a
    map with polylines representing the tracks that is fitted to the extent of
    the tracks.

    Parameters:
        file_list : An optional list of GPX files to be plotted on the map.

    Returns:
        The rendered HTML representation of the folium map.
    """
    colormap: typing.List[str] = list(map(mpl.colors.to_hex,
                                          mpl.colormaps["Set1"].colors))
    map_: folium.Map = folium.Map()
    gdfs: typing.List[gpd.GeoDataFrame] = []
    for file_name, color in zip(file_list, colormap):
        # Read the GPX file into a GeoDataFrame from the "tracks" layer and add
        # it to the list.
        gdf: gpd.GeoDataFrame = gpd.read_file(file_name, layer="tracks")
        gdfs.append(gdf)
        #  Create a FeatureGroup for the current file to hold its polyline and
        # add that to the map
        lines_layer: folium.FeatureGroup = folium.FeatureGroup(name=file_name)
        folium.PolyLine(locations=gdf.geometry.get_coordinates()[["y", "x"]],
                        color=color).add_to(lines_layer)
        lines_layer.add_to(map_)
    # Fit the extent of the map to the tracks
    xmin, ymin, xmax, ymax = pd.concat(gdfs).total_bounds if gdfs\
        else [-50, -50, 50, 50]
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
