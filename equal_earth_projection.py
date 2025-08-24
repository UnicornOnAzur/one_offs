"""

"""
# Standard library

# Third party
import cartopy
import geopandas as gpd
import matplotlib.pyplot as plt
#
WATER_COLOR: str = "lightskyblue"
EARTH_COLOR: str = "tan"
BORDER_COLOR: str = "darkgrey"
HEIGHT: int = 5
WIDTH: int = 14


def equal_earth_geopandas() -> None:
    world: gpd.GeoDataFrame = gpd.read_file("data/naturalearth_lowres.shp")
    #
    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(WIDTH, HEIGHT))
    fig.subplots_adjust(left=.05, right=.95, bottom=0, top=.9, wspace=.1)
    fig.suptitle("Projections in GeoPandas")
    for idx, (ax, crs) in enumerate(
                            zip(axes.flatten(),
                                (4326, "+proj=eqearth", 8857, 8858, 8859, None)
                                )):
        if idx == 5:  # remove the last, unused axis
            ax.remove()
            break
        ax.set_facecolor(WATER_COLOR)
        world.to_crs(crs).plot(ax=ax,
                               edgecolor=BORDER_COLOR,
                               facecolor=EARTH_COLOR,
                               aspect="auto"
                               )
        ax.set_title(crs)
    fig.savefig("output/equal_earth_geopandas.png")


def equal_earth_cartopy() -> None:
    fig: plt.Figure = plt.figure(figsize=(WIDTH, HEIGHT))
    for rect, crs in zip((121, 122),
                         (cartopy.crs.Mercator(), cartopy.crs.EqualEarth())):
        ax: cartopy.mpl.geoaxes.GeoAxes = fig.add_subplot(rect, projection=crs)
        ax.add_feature(cartopy.feature.LAND, color=EARTH_COLOR)
        ax.add_feature(cartopy.feature.BORDERS, color=BORDER_COLOR)
        ax.coastlines(color=BORDER_COLOR)
        ax.set_facecolor(WATER_COLOR)
        ax.set_title(crs.proj4_params["proj"])
    fig.savefig("output/equal_earth_cartopy.png")


def main():
    equal_earth_geopandas()
    equal_earth_cartopy()


if __name__ == "__main__":
    main()
