"""
This script imports a dataset of OD pairs and
displays them using the specified projection.
"""


# ---------- Imports ---------- #
import cartopy as cp
import matplotlib.pyplot as plt
from networktest import coords_lst


# ---------- Setup ---------- #
# Caropy settings
COLOUR_OCEAN = (0.0, 0.42, 0.58)
COLOUR_LAND = (0.96, 0.96, 0.86)
MAP_BOUNDS = (-35, 60, 25, 65)
PROJECTION = cp.crs.PlateCarree()
#PROJECTION = cp.crs.Mercator()
#PROJECTION = cp.crs.Miller()
TRANSFORM = cp.crs.Geodetic()       # Curved lines on the map


# ---------- Function Definitions ---------- #
def display_map(coords_list, line_width = 0.01, marker_size = 1, colour = "Black"):
    """
    Displays a map with the provided data using
    matplotlib using the provided settings.

    Arguments:
        coords_list (List): List of OD coordinate pairs
        line_width (float): Line width
        marker_size (float): Marker size
        colour (Tuple): Line and marker colour
    """

    # Set projection
    axes = plt.axes(projection = PROJECTION)

    # Map settings
    axes.coastlines(resolution="50m")
    axes.set_extent (MAP_BOUNDS)
    axes.gridlines()

    # Map features
    axes.add_feature(cp.feature.BORDERS, linestyle='--', alpha=1)
    axes.add_feature(cp.feature.LAND, facecolor=COLOUR_LAND)
    axes.add_feature(cp.feature.OCEAN, facecolor=COLOUR_OCEAN)
    axes.add_feature(cp.feature.LAKES, facecolor=COLOUR_OCEAN)

    # Add flights
    for edge in coords_list:
        latitude_list = (edge[0][1], edge[1][1])
        longitude_list = (edge[0][0], edge[1][0])

        plt.plot(longitude_list, latitude_list, c = colour, lw = line_width,
                 ms = marker_size, ls = "-", marker = ".", transform = TRANSFORM)

    # Display map
    plt.show()

def display_network():
    """
    """

# ---------- Main Program --------- #
if __name__ == "__main__":
    #COORDS_LIST = [((52.3676, 4.9041), (38.7223, -9.1393))]
    #display_map(COORDS_LIST, line_width = 1)

    # Display map
    display_map(coords_lst, colour = "red")
