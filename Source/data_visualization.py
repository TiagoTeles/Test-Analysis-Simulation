"""
This script provides different ways to
visualize an airport network on a map.
"""


# ---------- Imports ---------- #
import math
import csv
import cartopy as cp
import matplotlib.pyplot as plt
import igraph as ig
import pandas as pd

# ---------- Setup ---------- #
# General settings
GIT_DIR = __file__[0:-28]
ASSET_DIR = GIT_DIR + "Assets/"
DIR_2019 = GIT_DIR + "2019_Filtered/"
DIR_2020  = GIT_DIR + "2020_Filtered/"
FLIGHT_DIR = "EU_flights_2019_04.csv"
AIRPORT_DIR = "Airports.csv"

# Caropy settings
COLOUR_OCEAN = (1, 1, 1)
COLOUR_LAND = (0.9, 0.9, 0.9)
MAP_BOUNDS = (-30, 60, 25, 70)
PROJECTION = cp.crs.PlateCarree()
TRANSFORM = cp.crs.Geodetic()

# IGraph settings
AS = 0.5
RES = (5760, 5760/1.8)


# ---------- Function Definitions ---------- #
def create_graph(dir):
    """
    Generates an IGraph graph
    from the data provided.

    Arguments:
        dir (String): Directory of the data file

    Returns:
        g_weighted (Graph): Weighted graph
    """

    # Retrieve data
    data = pd.read_csv(dir, usecols=[1,2])

    # Create unweighted graph
    g_unweighted = ig.Graph.DataFrame(data, directed = True)

    # Create weighted graph
    adjacency = list(g_unweighted.get_adjacency())
    g_weighted = ig.Graph.Weighted_Adjacency(adjacency)

    # Copy attributes
    g_weighted.vs["name"] = g_unweighted.vs["name"]

    return g_weighted


def get_coordinates(dir):
    """
    Gets the airport coordinates.

    Arguments:
        dir (String): Directory of the data file

    Returns:
        coordinates (List): List of airport coordinates (ICAO, Lat, Lon)
    """

    # Open the file
    airport_file = open(dir, encoding="utf8")

    # Read the file
    airport_csv = csv.reader(airport_file)

    # Convert from .CSV to List
    coordinates = []
    for airport in airport_csv:
        try:
            coordinates.append([airport[1], float(airport[4]), float(airport[5])])
        except ValueError:
            pass

    del coordinates[0]     # Remove legend

    return coordinates


def display_map(graph, coords, line_width = 0.01, marker_size = 1, colour = "Black"):
    """
    Displays a map with the provided data using
    matplotlib using the provided settings.

    Arguments:
        graph (Graph): Graph of the network
        coordinates (List): List of OD coordinate pairs
        line_width (float): Line width
        marker_size (float): Marker size
        colour (Tuple): Line and marker colour
    """

    # Determine list of used airports
    coordinates = []
    for airport in coords:
        for name in graph.vs["name"]:
            if airport[0] == name:
                coordinates.append((airport[1], airport[2]))

    # Set projection
    axes = plt.axes(projection = PROJECTION)

    # Map settings
    grid = axes.gridlines(draw_labels = True)
    axes.coastlines(resolution="50m")
    axes.set_extent(MAP_BOUNDS)

    # Map features
    axes.add_feature(cp.feature.BORDERS, linestyle='--', alpha=1)
    axes.add_feature(cp.feature.LAND, facecolor=COLOUR_LAND)
    axes.add_feature(cp.feature.OCEAN, facecolor=COLOUR_OCEAN)
    axes.add_feature(cp.feature.LAKES, facecolor=COLOUR_OCEAN)

    # Plot features
    grid.xlabel_style = {"size": 12}
    grid.ylabel_style = {"size": 12}
    grid.xformatter = cp.mpl.gridliner.LONGITUDE_FORMATTER
    grid.yformatter = cp.mpl.gridliner.LATITUDE_FORMATTER
    grid.bottom_labels = False
    grid.left_labels = False

    # Add labels
    axes.text(-0.01, 0.5, "Latitude, [Deg]", size = 12, va = "bottom", ha = "center",
              rotation = "vertical", rotation_mode = "anchor", transform = axes.transAxes)

    axes.text(0.5, -0.05, "Longitude, [Deg]", size = 12, va = "bottom", ha = "center",
              rotation = "horizontal", rotation_mode = "anchor", transform = axes.transAxes)

    # Add flights
    for edge in graph.es:
        # Coordinates
        origin = coordinates[edge.tuple[0]]
        destination = coordinates[edge.tuple[1]]

        # Convert to x and y datasets
        latitudes = (origin[0], destination[0])
        longitudes = (origin[1], destination[1])

        # Plot
        plt.plot(longitudes, latitudes, c = colour, lw = line_width,
                 ms = marker_size, ls = "-", marker = ".", transform = TRANSFORM)

    # Display map
    plt.show()


def display_network(graph, coords):
    """
    This function imports a graph and
    displays the network in an image viewer.

    Arguments:
        graph (Graph): Graph of the network
        coords (List): List containing the cordinates of airports
    """

    # Determine required coordinates
    coordinates = []
    for vertex in graph.vs()["name"]:
        for row in coords:
            if vertex == row[0]:
                coordinates.append([row[2], -row[1]])

    # Determine vertex size
    v_size = []
    for vertex in graph.vs()["name"]:
        size = 10*math.log(graph.degree(vertex))
        v_size.append(size)

    # Determine edge width
    e_width = []
    for e_weight in graph.es()["weight"]:
        e_width.append(int(e_weight)//100)

    # Display node name
    graph.vs["label"] = graph.vs["name"]

    # Plot graph
    ig.plot(graph, layout = coordinates, vertex_size = v_size,
            edge_width = e_width, edge_arrow_size = AS, bbox = RES)


# ---------- Main Program ---------- #
if __name__ == "__main__":
    graph = create_graph(DIR_2019 + FLIGHT_DIR)
    coordinates = get_coordinates(ASSET_DIR + AIRPORT_DIR)

    display_map(graph, coordinates, colour = "red")
    #display_network(graph, coordinates)
