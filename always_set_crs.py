"""
author: UnicornOnAzur

This module provides a custom GeoDataFrame class that extends GeoPandas'
GeoDataFrame to include additional methods as well as function for
transforming coordinate reference systems (CRS) using different strategies.
"""
# Standard library
import typing
# Third party
import geopandas as gpd
# Constant
DEFAULT_CRS: str = "EPSG:4087"


class MyGeoDataFrame(gpd.GeoDataFrame):
    """
    Custom GeoDataFrame class that extends GeoPandas' GeoDataFrame
    to include additional CRS transformation methods.
    """
    def __init__(
        self,
        *args: typing.Any,
        **kwargs: typing.Any
            ) -> None:
        super().__init__(*args, **kwargs)

    def always_to_crs(
        self,
        crs: typing.Union[int, str],
        method: str,
        inplace: bool = True,
            ) -> typing.Optional[gpd.GeoDataFrame]:
        """
        Transforms the GeoDataFrame to a specified coordinate reference system
        (CRS).

        Parameters:
            crs : The target CRS.
            method : The method to use for transformation ('lbyl' or 'eafp').
            inplace : If True, modifies the GeoDataFrame in place.

        Returns:
            The transformed GeoDataFrame if inplace is False.
        """
        match method:
            case "lbyl":
                return self._to_crs_lbyl(crs, inplace)
            case "eafp":
                return self._to_crs_eafp(crs, inplace)
            case _:
                raise ValueError("Method must be either 'lbyl' or 'eafp'.")

    def _to_crs_lbyl(
        self,
        crs: typing.Union[int, str],
        inplace: bool
            ) -> typing.Optional[gpd.GeoDataFrame]:
        """
        Transform CRS using the 'Look Before You Leap' method.

        Parameters:
            crs : The target CRS.
            inplace : If True, modifies the GeoDataFrame in place.

        Returns:
            The transformed GeoDataFrame if inplace is False.
        """
        if self.crs is None:
            self.set_crs(DEFAULT_CRS, inplace=True)
        return self.to_crs(crs, inplace=inplace)

    def _to_crs_eafp(
        self,
        crs: typing.Union[int, str],
        inplace: bool
            ) -> typing.Optional[gpd.GeoDataFrame]:
        try:
            return self.to_crs(crs, inplace=inplace)
        except ValueError:
            self.set_crs(DEFAULT_CRS, inplace=True)
            return self.to_crs(crs, inplace=inplace)


def to_crs_lbyl(
    gdf: gpd.GeoDataFrame,
    crs: typing.Union[int, str]
        ) -> gpd.GeoDataFrame:
    """
    Transform a GeoDataFrame to a specified CRS using the 'Look Before You
    Leap' method.

    Parameters:
        gdf : The GeoDataFrame to transform.
        crs : The target CRS.

    Returns:
        The transformed GeoDataFrame.
    """
    if gdf.crs is None:
        gdf.set_crs(DEFAULT_CRS, inplace=True)
    return gdf.to_crs(crs)


def to_crs_eafp(
    gdf: gpd.GeoDataFrame,
    crs: typing.Union[int, str]
        ) -> gpd.GeoDataFrame:
    """
    Transform a GeoDataFrame to a specified CRS using the 'Easier to Ask for
    Forgiveness than Permission' method.

    Parameters:
        gdf : The GeoDataFrame to transform.
        crs : The target CRS.

    Returns:
        The transformed GeoDataFrame.
    """
    try:
        return gdf.to_crs(crs)
    except ValueError:
        return gdf.set_crs(DEFAULT_CRS).to_crs(crs)


def demo():
    """
    Demonstrates the functionality of the MyGeoDataFrame class and the CRS
    transformation functions.
    """
    import itertools

    def _create_geodataframe() -> gpd.GeoDataFrame:
        return gpd.GeoDataFrame(geometry=gpd.points_from_xy([10], [10]))

    WGS_84_int: int = 4326
    WGS_84_str: str = "4326"
    demo_gdf: gpd.GeoDataFrame = _create_geodataframe()
    print(f"{demo_gdf.crs=}")
    for func, crs in itertools.product([to_crs_lbyl, to_crs_eafp],
                                       [WGS_84_int, WGS_84_str]):
        if func(demo_gdf, crs).crs == crs:
            print(f"{func.__name__} worked with {crs=}")

    for method, crs, in_place in itertools.product(["lbyl", "eafp"],
                                                   [WGS_84_int, WGS_84_str],
                                                   [True, False]):
        new_gdf: gpd.GeoDataFrame = MyGeoDataFrame(
            geometry=gpd.points_from_xy([10], [10]))
        other_gdf: typing.Optional[gpd.GeoDataFrame] =\
            new_gdf.always_to_crs(crs, method, in_place)
        if [gdf for gdf in [other_gdf, new_gdf]
                if isinstance(gdf, gpd.GeoDataFrame)][0].crs == crs:
            print(f"{method} worked with {crs=} and {in_place=}")


if __name__ == "__main__":
    demo()
