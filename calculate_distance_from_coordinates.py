# -*- coding: utf-8 -*-
"""
author: UnicornOnAzur

This module provides functions to calculate distances between geographical
points on Earth using various formulas, including Haversine, Vincenty, and the
Law of Cosines.

It supports distance calculations in kilometers and miles, and includes utility
functions for converting coordinates from degrees to radians.

Functions:
- calculate_haversine_distance: Computes distance using the Haversine formula.
- calculate_vincenty_distance: Computes distance using the Vincenty formula.
- calculate_law_of_cosines_distance: Computes distance using the Law of
Cosines.
"""
# Standard library
import enum
import math
import typing
# Constants
RADIUS_EARTH: float = 6371.0088


class DistanceUnit(str, enum.Enum):
    KM = "km"
    MILES = "mi"


CONVERSIONS: typing.Dict[DistanceUnit, float] = {
    DistanceUnit.KM: RADIUS_EARTH,
    DistanceUnit.MILES: 0.621371192 * RADIUS_EARTH
}


def _get_earth_radius(
    unit: DistanceUnit
            ) -> float:
    """'
    Get the Earth's radius based on the specified distance unit.

    Parameters:
        unit : The distance unit (KM or MILES).

    Returns:
        The radius of the Earth in the specified unit.
    """
    return CONVERSIONS.get(unit)


def _convert_to_radians(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
        ) -> map:
    """
    Convert latitude and longitude from degrees to radians.

    Parameters:
        lat1 : Latitude of the first point.
        lon1 : Longitude of the first point.
        lat2 : Latitude of the second point.
        lon2 : Longitude of the second point.

    Returns:
        Map object with the coordinates in radians.
    """
    return map(math.radians, [lat1, lon1, lat2, lon2])


def _calculate_haversine_component(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
        ) -> float:
    """
    Calculate the Haversine component for distance calculation.
    Formula:
        a = sin²(Δφ/2) + cos φ1 * cos φ2 * sin²(Δλ/2)

    Parameters:
        lat1 : Latitude of the first point.
        lon1 : Longitude of the first point.
        lat2 : Latitude of the second point.
        lon2 : Longitude of the second point.

    Returns:
        The Haversine component.
    """
    lat1_rad, lon1_rad, lat2_rad, lon2_rad =\
        _convert_to_radians(lat1, lon1, lat2, lon2)
    # Calculate the difference between the two coordinates
    delta_lat: float = lat2_rad - lat1_rad
    delta_lon: float = lon2_rad - lon1_rad
    return (math.sin(delta_lat/2)**2 +
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)


def calculate_haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: typing.Union[str, DistanceUnit] = DistanceUnit.KM
        ) -> float:
    """
    Calculate the distance between two points on the Earth using the Haversine
    formula. This formula calculates the distance between two points on the
    surface of a sphere given their latitude and longitude.

    Formula:
        a = sin²(Δφ/2) + cos φ1 * cos φ2 * sin²(Δλ/2)
        d = 2 * R * asin2(√(a))

    Parameters:
        lat1 : Latitude of the first point.
        lon1 : Longitude of the first point.
        lat2 : Latitude of the second point.
        lon2 : Longitude of the second point.
        unit : The unit of distance (default is kilometers).

    Returns:
        The distance between the two points in the specified unit.
    """
    radius: float = _get_earth_radius(unit)
    distance: float = 2 * radius * math.asin(math.sqrt(
        _calculate_haversine_component(lat1, lon1, lat2, lon2)))
    return distance


def calculate_vincenty_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: typing.Union[str, DistanceUnit] = DistanceUnit.KM
        ) -> float:
    """
    Calculate the distance between two points on the Earth using the Vincenty
    formula.  This formula calculates the distance between two points on the
    surface of an ellipsoid.

    Formula:
        a = sin²(Δφ/2) + cos φ1 * cos φ2 * sin²(Δλ/2)
        c = 2 * atan2(√a, √(1−a))
        b = (1 - (1 / 298.257223563)) * R
        d = b * c

    Parameters:
        lat1 : Latitude of the first point.
        lon1 : Longitude of the first point.
        lat2 : Latitude of the second point.
        lon2 : Longitude of the second point.
        unit : The unit of distance (default is kilometers).

    Returns:
        The distance between the two points in the specified unit.
    """
    radius: float = _get_earth_radius(unit)
    a = _calculate_haversine_component(lat1, lon1, lat2, lon2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    # semi-minor axis of the Earth's ellipsoid
    b = (1 - (1 / 298.257223563)) * radius
    return c * b


def calculate_law_of_cosines_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: typing.Union[str, DistanceUnit] = DistanceUnit.KM
        ) -> float:
    """
    Calculate the distance using the Law of Cosines. This formula calculates
    the distance between two points on the surface of a sphere.

    Formula:
        d = R * acos(sin φ1 * sin φ2 + cos φ1 * cos φ2 * cos(Δλ))

    Parameters:
        lat1 : Latitude of the first point.
        lon1 : Longitude of the first point.
        lat2 : Latitude of the second point.
        lon2 : Longitude of the second point.
        unit : The unit of distance (default is kilometers).

    Returns:
        float: The distance between the two points in the specified unit.
    """
    radius: float = _get_earth_radius(unit)
    lat1_rad, lon1_rad, lat2_rad, lon2_rad =\
        _convert_to_radians(lat1, lon1, lat2, lon2)
    return math.acos(math.sin(lat1_rad) * math.sin(lat2_rad) +
                     math.cos(lat1_rad) * math.cos(lat2_rad) *
                     math.cos(lon2_rad - lon1_rad))*radius


def demo() -> None:
    import haversine
    import pandas as pd
    import pygeodesy
    import sklearn

    def unpack_coords(coords_):
        """Unpack coordinates from a list of tuples."""
        return ([c for coord in coords_ for c in coord])

    def heri_haversine(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2  # noqa: E501
        c = 2 * math.asin(math.sqrt(a))
        r = 6371
        return c * r

    def heri_vincenty(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2  # noqa: E501
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        f = 1/298.257223563
        b = (1 - f) * 6371
        return c * b

    # https://en.wikipedia.org/wiki/Haversine_formula
    coords_white_house = [38.898, -77.037]
    coords_eiffel_tower = [48.858, 2.294]
    # https://pypi.org/project/haversine/
    lyon = (45.7597, 4.8422)
    paris = (48.8567, 2.3508)
    # https://www.thoughtco.com/degree-of-latitude-and-longitude-distance-4070616
    equator_lon = [(0, 0), (1, 0)]

    results: typing.Dict[str, typing.Dict[str, float]] = {}
    global RADIUS_EARTH
    for radius in [6371, 6371.008771415, 6371.0088, 6371.2]:
        RADIUS_EARTH = radius
        CONVERSIONS[DistanceUnit.KM] = radius
        for target, coords, benchmark in zip(["White House <->\nEiffel Tower",
                                              "Lyon <->\nParis",
                                              "Longitude at\nthe equator"],
                                             [(coords_white_house,
                                              coords_eiffel_tower),
                                              (lyon, paris),
                                              equator_lon],
                                             [6161.6, 392.217, 110.567]
                                             ):
            results[target] = {
                "haversine*": haversine.haversine(*coords),
                "haversine**": pygeodesy.formy.haversine(
                    *unpack_coords(coords))/1000,
                "haversine***": sklearn.metrics.pairwise.haversine_distances(
                    [[math.radians(x) for x in y] for y in coords]
                    ).max() * 6371,
                "heri_haversine": heri_haversine(*unpack_coords(coords)),
                "haversine": calculate_haversine_distance(
                    *unpack_coords(coords)),
                "vincenty**": pygeodesy.formy.vincentys(
                    *unpack_coords(coords))/1000,
                "heri_vincenty": heri_vincenty(*unpack_coords(coords)),
                "vincenty": calculate_vincenty_distance(
                    *unpack_coords(coords)),
                "law_of_cosines**": pygeodesy.formy.cosineLaw(
                    *unpack_coords(coords))/1000,
                "law_of_cosines": calculate_law_of_cosines_distance(
                    *unpack_coords(coords)),
                "benchmark": benchmark
                            }
        df: pd.DataFrame = pd.DataFrame().from_dict(results)
        print(f"Radius of the earth: {RADIUS_EARTH}",
              df.to_markdown(floatfmt=".3f"),
              sep="\n", end="\n\n")


if __name__ == "__main__":
    demo()
