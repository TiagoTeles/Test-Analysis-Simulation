import csv
import math
import time
import cartopy.crs as ccrs
import cartopy as cp
import igraph as ig
import matplotlib.pyplot as plt
import pandas as pd

# General settings
GIT_DIR = __file__[0:-28]
ASSET_DIR = GIT_DIR + "Assets/"
DIR_2019 = GIT_DIR + "2019_Filtered/"
DIR_2020 = GIT_DIR + "2020_Filtered/"
FLIGHT_DIR = "EU_flights_2020_01.csv"
AIRPORT_DIR = "Airports.csv"

# Caropy settings
COLOUR_OCEAN = (1, 1, 1)
COLOUR_LAND = (0.9, 0.9, 0.9)
MAP_BOUNDS = (-30, 60, 25, 70)
PROJECTION = cp.crs.PlateCarree()
TRANSFORM = cp.crs.Geodetic()

# IGraph settings
AS = 0.5
RES = (5760, 5760 / 1.8)
FONT_SIZE = 16
LW = 0.5


def commmunities(graph, method):
    """"Presenting a number of community detection algorithms"""

    graph = graph.as_undirected("each")  # Changing the networks from directed to undirected. The infomap algorithm could not create proper communities, therefore it was decided that the multilevel algorithm should be used instead, this however requires the network to be undirected.

    # EDGE_BETWEENNESS most exact but also slowest and most computer heavy
    # time = 946.8 s (edge) + 353.9 s (vertex)
    if method == 'edge_betweenness':
        v = graph.community_edge_betweenness()

    # INFOMAP this one should specifically be for directed graphs but im not sure if we need to detect communities with the graph being directed
    if method == 'infomap':
        v = graph.community_infomap()

    # FAST_GREEDY & MULITLEVEL (very similar) fast and accurate, Multilevel should perform very well
    if method == 'fast_greedy':
        v = graph.community_fastgreedy()
    elif method == 'multilevel':
        v = graph.community_multilevel()

    # WALKTRAP less fast than FAST_GREEDY but slightly more accurate
    if method == 'walktrap':
        v = graph.community_walktrap()

    # LEIDEN algorithm should also be good but only for undirected graphs
    if method == 'leiden':
        v = graph.community_leiden()

    return v


def intersection(lst1, lst2):
    """Find the intersection of two lists"""
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def plot(graph, filename, clusters):
    """"This function gives identical styling to each node within one community and it makes the edges between communities red or green in color"""
    membership = clusters.membership

    if membership is not None:
        gcopy = graph.copy()
        edges = []
        edges_colors = []
        for edge in graph.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                edges_colors.append('Gray')
            else:
                edges_colors.append("Black")
        gcopy.delete_edges(edges)
        graph.es["color"] = edges_colors
    else:
        graph.es["color"] = "gray"

    """"Creating empty lists for the layout of the visualization"""
    airports = []
    coords = []

    """"Reading the coördinates of the airports for the layout"""
    with open(ASSET_DIR + "Airports.csv",
              encoding="mbcs") as file:
        reader = csv.reader(file, delimiter=",")
        i = 0
        for row in reader:
            for name in graph.vs["name"]:
                if row[1] == name:
                    airports.append(row[1])
                    coords.append((float(row[-2]), -float(row[-3])))
                    i += 1
    lout = coords

    """"Determining the visual aspects of the network"""
    visual_style = {}
    visual_style["edge_arrow_size"] = 0.025
    visual_style["vertex_shape"] = "circle"
    visual_style["vertex_size"] = [15 * math.log(graph.degree(i)) for i in graph.vs]
    visual_style['layout'] = lout
    visual_style["edge_width"] = [0.002* int(weight) for weight in graph.es["weight"]]
    visual_style["bbox"] = (5000, 5000)
    visual_style["margin"] = 40
    # visual_style["edge_label"] = graph.es["weight"]
    g.vs["label"] = g.vs["name"]

    """"Creating reference lists to keep track of which community of the new month is most likely equal to another community from a the month before.
        Since March of 2020 has the largest amount of communities, this month was used to create the reference communities shown below."""

    index_0 = ["BIKF", "BIRK", "EBCI", "EGAA", "EGAC", "EGBB", "EGBN", "EGCC", "EGCN", "EGEC", "EGFF", "EGGD",
               "EGGP", "EGGW", "EGHC", "EGHH", "EGHI", "EGHQ", "EGJA", "EGJB", "EGJJ", "EGKK", "EGLC", "EGMC",
               "EGMD", "EGNH", "EGNJ", "EGNM", "EGNR", "EGNS", "EGNT", "EGNV", "EGNX", "EGOV", "EGPA", "EGPB",
               "EGPC", "EGPD", "EGPE", "EGPF", "EGPH", "EGPI", "EGPK", "EGPN", "EGSH", "EGSS", "EGTE", "EGVN",
               "EHAM", "EHEH", "EHRD", "EICK", "EICM", "EIDL", "EIDW", "EIKN", "EIKY", "EINN", "EIWF", "EKKA",
               "LFOH", "LFRD", "LFRH", "LFRK", "LPFR", "LRCL"]
    index_1 = ["BKPR", "EDDC", "EDDE", "EDDG", "EDDH", "EDDK", "EDDL", "EDDM", "EDDN", "EDDR", "EDDS", "EDDV",
               "EDDW", "EDFM", "EDHK", "EDHL", "EDJA", "EDLP", "EDLV", "EDLW", "EDNY", "EDQM", "EDSB", "EDVE",
               "EDVK", "EDXW", "EHGG", "ELLX", "ETNL", "LERS", "LFJL", "LFLB", "LFSL", "LFTH", "LHPP", "LHPR",
               "LOWI", "LOWS", "LRBS", "LRCK", "LRSB", "LSZA", "LSZB", "LSZH", "LSZR", "LWSK", "UMMG"]
    index_2 = ["EBAW", "EBLG", "EBOS", "EDDB", "EDDF", "EDFH", "EHBK", "ENTO", "EVRA", "EYVI", "LBBG", "LBWN",
               "LDSB", "LDZA", "LEJR", "LEZG", "LHBP", "LHDC", "LHSM", "LJLJ", "LJMB", "LKKV", "LKMT", "LKPD",
               "LKPR", "LKTB", "LMML", "LOWG", "LOWK", "LOWL", "LOWW", "LQBK", "LROD", "LROP", "LRTM", "LTBU",
               "LYBE", "LYTV", "LZIB", "LZKZ", "LZTT", "UKBB", "UKKK", "UKLL", "UKLU", "UMMS"]
    index_3 = ["EBBR", "EDDP", "EGLL", "GCFV", "GCLA", "GCLP", "GCRR", "GCTS", "GCXO", "GEML", "LBSF", "LEAS",
               "LEBB", "LEBL", "LECO", "LEGE", "LEGR", "LEIB", "LEMD", "LEMG", "LEMH", "LEPA", "LEPP", "LESA",
               "LEST", "LEVC", "LEVT", "LEVX", "LEZL", "LFBD", "LFBE", "LFBH", "LFBI", "LFBO", "LFBP", "LFBT",
               "LFBU", "LFBZ", "LFCK", "LFCR", "LFJR", "LFKB", "LFKC", "LFKF", "LFKJ", "LFLC", "LFLL", "LFLP",
               "LFLS", "LFLW", "LFMD", "LFMK", "LFML", "LFMN", "LFMP", "LFMT", "LFMV", "LFOB", "LFOP", "LFOT",
               "LFPG", "LFPO", "LFQQ", "LFRB", "LFRC", "LFRN", "LFRQ", "LFRS", "LFSG", "LFST", "LFTW", "LIPR",
               "LPAZ", "LPCS", "LPMA", "LPPD", "LPPM", "LPPR", "LPPT", "LPVZ", "LSGG", "LXGB"]
    index_4 = ["EEKE", "EETN", "EETU", "EFHK", "EFJO", "EFJY", "EFKE", "EFKI", "EFKU", "EFMA", "EFOU", "EFPO",
               "EFRO", "EFSA", "EFTP", "EFTU", "EKAH", "EKBI", "EKCH", "EKEB", "EKOD", "EKRN", "EKSB", "EKSN",
               "EKYT", "ENAL", "ENBO", "ENBR", "ENCN", "ENDU", "ENEV", "ENFL", "ENGM", "ENHD", "ENKB", "ENML",
               "ENNO", "ENOL", "ENRA", "ENRO", "ENSO", "ENVA", "ENZV", "ESDF", "ESGG", "ESGJ", "ESKM", "ESKN",
               "ESMK", "ESMQ", "ESMS", "ESMT", "ESMX", "ESND", "ESNN", "ESNS", "ESNU", "ESNZ", "ESOE", "ESOH",
               "ESOW", "ESPA", "ESSA", "ESSB", "ESSD", "ESSL", "ESSP", "ESSV", "ESTA", "EVLA", "EYKA", "LEAL"]
    index_5 = ["EPBY", "EPGD", "EPKK", "EPKT", "EPLL", "EPMO", "EPPO", "EPRA", "EPRZ", "EPSC", "EPSY", "EPWA",
               "EPWR", "EPZG", "ESOK", "LDRI", "LRTR", "LZZI"]
    index_6 = ["LDPL", "LDSP", "LIBD", "LIBF", "LIBR", "LICA", "LICC", "LICJ", "LICR", "LIEA", "LIEE", "LIEO",
               "LIET", "LIMC", "LIME", "LIMF", "LIMG", "LIMJ", "LIML", "LIMP", "LIMZ", "LIPB", "LIPE", "LIPH",
               "LIPK", "LIPO", "LIPQ", "LIPX", "LIPY", "LIPZ", "LIRA", "LIRF", "LIRJ", "LIRN", "LIRP", "LIRQ",
               "LIRZ"]
    index_7 = ["LGAL", "LGAV", "LGHI", "LGIO", "LGIR", "LGKO", "LGKP", "LGKV", "LGMK", "LGMT", "LGRP", "LGSA",
               "LGSM", "LGSR", "LGST", "LGZA"]
    index_8 = ["UKFF", "ULAA", "ULKK", "ULMM", "ULOO", "UMGG", "UMKK", "URKA", "URML", "URRP", "URWA", "UUBI",
               "UUBW", "UUDD", "UUEE", "UUMO", "UUOB", "UUOO", "UUWW", "UUYS", "UUYY", "UWGG", "UWKD", "UWKE",
               "UWLL", "UWLW", "UWPS", "UWSS", "UWUU", "UWWW"]

    """"Change the clusters from numbers to the ICAO codes of the airports within each cluster, igraph delivers the community clusters as numbers.
        To compare the airports to the reference list, the ICAO codes are used"""
    indices = []
    for cluster_number in range(ig.clustering.VertexClustering.__len__(clusters)):
        index = []
        for node in clusters[cluster_number]:
            index.append(g.vs["name"][node])
        indices.append(index)

    """Determining which community is most likely to belong the of the indexes shwon previously"""
    best_fit_overall = []
    com_indices = []
    for cluster in indices:
        best_fit = []
        best_fit.append(len(intersection(cluster, index_0)))
        best_fit.append(len(intersection(cluster, index_1)))
        best_fit.append(len(intersection(cluster, index_2)))
        best_fit.append(len(intersection(cluster, index_3)))
        best_fit.append(len(intersection(cluster, index_4)))
        best_fit.append(len(intersection(cluster, index_5)))
        best_fit.append(len(intersection(cluster, index_6)))
        best_fit.append(len(intersection(cluster, index_7)))
        best_fit.append(len(intersection(cluster, index_8)))
        best_fit_overall.append(best_fit)
        com_index = best_fit.index(max(best_fit))
        com_indices.append(com_index)

    """Changing the membership index (the cluster to which a node belongs)."""
    pos = 0
    for index in membership:
        if index == 0:
            membership[pos] = com_indices[0]
        elif index == 1:
            membership[pos] = com_indices[1]
        elif index == 2:
            membership[pos] = com_indices[2]
        elif index == 3:
            membership[pos] = com_indices[3]
        elif index == 4:
            membership[pos] = com_indices[4]
        elif index == 5:
            membership[pos] = com_indices[5]
        elif index == 6:
            membership[pos] = com_indices[6]
        elif index == 7:
            membership[pos] = com_indices[7]
        elif index == 8:
            membership[pos] = com_indices[8]
        elif index == 9:
            membership[pos] = com_indices[9]
        elif index == 10:
            membership[pos] = com_indices[10]
        else:
            pass
        pos += 1

    """Coloring the nodes according to their membership index"""
    if membership is not None:
        colors = ['Tomato', 'Orange', 'DodgerBlue', 'MediumSeaGreen', 'SlateBlue', "Violet", "#FF3399", "#9CCC65",
                  "#00838F", "#795548", 'sandybrown', 'skyblue']
        for vertex in graph.vs():
            vertex["color"] = colors[membership[vertex.index]]
        visual_style["vertex_color"] = graph.vs["color"]

    """Ploting the network, either by showing the plot directly (option one), or saving the plot (option two)"""
    # ig.plot(graph, autocurve= False, **visual_style)
    # ig.plot(graph, f'{filename}.png', autocurve= False, **visual_style)
    plt.show()

    return graph, coords, membership


def timeseries(membership):
    """"Returns a list of the amount of nodes within a certain community within a certain timeframe (one month)"""
    n = sum(ig.clustering.VertexClustering.sizes(clusters))
    a = membership.count(0)
    b = membership.count(1)
    c = membership.count(2)
    d = membership.count(3)
    e = membership.count(4)
    f = membership.count(5)
    g = membership.count(6)
    h = membership.count(7)
    i = membership.count(8)

    return [a, b, c, d, e, f, g, h, i]

def plot_time_series(list):
    """"Plotting the time series of the communities"""

    """"Creating empty lists"""
    xx = []
    list_0 = []
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
    list_7 = []
    list_8 = []

    """"Unpacking the data created by the time series function in order to create seperate lists for each community"""
    for i in range(len(list)):
        xx.append(i + 1)
        list_0.append(list[i][0])
        list_1.append(list[i][1])
        list_2.append(list[i][2])
        list_3.append(list[i][3])
        list_4.append(list[i][4])
        try:
            list_5.append(list[i][5])
        except:
            pass
        try:
            list_6.append(list[i][6])
        except:
            pass
        try:
            list_7.append(list[i][7])
        except:
            pass
        try:
            list_8.append(list[i][8])
        except:
            pass

    """"Plotting the time series data, the try statements are use"""
    plt.figure()
    plt.plot(xx, list_0, color="Tomato", marker='o', linewidth='3')
    plt.plot(xx, list_1, color="Orange", marker='D', linestyle='-', linewidth='3')
    plt.plot(xx, list_2, color="DodgerBlue", marker='v', linestyle='-', linewidth='3')
    plt.plot(xx, list_3, color="MediumSeaGreen", marker='^', linestyle='-', linewidth='3')
    plt.plot(xx, list_4, color="SlateBlue", marker='s', linestyle='-', linewidth='3')
    plt.plot(xx, list_5, color="Violet", marker='p', linestyle='-', linewidth='3')
    plt.plot(xx, list_6, color="#FF3399", marker='X', linestyle='-', linewidth='3')
    plt.plot(xx, list_7, color="#9CCC65", marker='p', linestyle='-', linewidth='3')
    plt.plot(xx, list_8, color="#00838F", marker='X', linestyle='-', linewidth='3')

    plt.xlim(1, 24)
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
               ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                "November", "December", "January", "February", "March", "April", "May", "June", "July", "August",
                "September", "October",
                "November", "December"], rotation=45)
    plt.title("Size of communities per month")
    plt.xlabel("Month")
    plt.ylabel("Number of nodes within the community")
    plt.grid(axis="x", linestyle="--")
    plt.tight_layout()

    # show plots
    plt.show()

def histogram_time_series(list, filename):
    print(list)
    fig, ax = plt.subplots(1, 1)
    colors = ['Tomato', 'Orange', 'DodgerBlue', 'MediumSeaGreen', 'SlateBlue', "Violet", "#FF3399", "#9CCC65",
              "#00838F", "#795548", 'sandybrown', 'skyblue']
    xx = [0,1,2,3,4,5,6,7,8]
    labels = ['Red', 'Orange','Blue', 'Green', 'Purple', "Violet", "Pink", "LimeGreen",
              "DarkBlue"]
    plt.rcParams['font.size'] = '11'
    plt.gcf().subplots_adjust(bottom=0.30)
    ax.set(ylim=(0,140))
    # ax.set_xlabel('Communities')
    ax.set_ylabel('Amount of nodes')
    ax.grid(zorder=0)
    ax.bar(xx, list, width=0.8, align='center', color=colors, zorder=3)
    plt.xticks(xx, labels, rotation=45)
    plt.savefig(f'bar chart{filename}')
    return

# def display_map(graph, coords, membership, line_width = 0.01, marker_size = 1, colour = "Black"):
#     """
#     Displays a map with the provided data using
#     matplotlib using the provided settings.
#
#     Arguments:
#         graph (Graph): Graph of the network
#         coordinates (List): List of OD coordinate pairs
#         line_width (float): Line width
#         marker_size (float): Marker size
#         colour (Tuple): Line and marker colour
#     """
#
#     # Determine list of used airports
#     coordinates = []
#     for airport in coords:
#         for name in graph.vs["name"]:
#             if airport[0] == name:
#                 coordinates.append((airport[1], airport[2]))
#
#     # Set projection
#     axes = plt.axes(projection = PROJECTION)
#
#     # Map settings
#     grid = axes.gridlines(draw_labels = True)
#     axes.coastlines(resolution="50m")
#     axes.set_extent(MAP_BOUNDS)
#
#     # Map features
#     axes.add_feature(cp.feature.BORDERS, linestyle='--', alpha=1)
#     axes.add_feature(cp.feature.LAND, facecolor=COLOUR_LAND)
#     axes.add_feature(cp.feature.OCEAN, facecolor=COLOUR_OCEAN)
#     axes.add_feature(cp.feature.LAKES, facecolor=COLOUR_OCEAN)
#
#     # Plot features
#     grid.xlabel_style = {"size": 12}
#     grid.ylabel_style = {"size": 12}
#     grid.xformatter = cp.mpl.gridliner.LONGITUDE_FORMATTER
#     grid.yformatter = cp.mpl.gridliner.LATITUDE_FORMATTER
#     grid.bottom_labels = False
#     grid.left_labels = False
#
#     # Add labels
#     axes.text(-0.01, 0.5, "Latitude, [Deg]", size = 12, va = "bottom", ha = "center",
#               rotation = "vertical", rotation_mode = "anchor", transform = axes.transAxes)
#
#     axes.text(0.5, -0.05, "Longitude, [Deg]", size = 12, va = "bottom", ha = "center",
#               rotation = "horizontal", rotation_mode = "anchor", transform = axes.transAxes)
#
#
#     # Add nodes
#     if membership is not None:
#         # Add flights
#         for vertex in graph.vs():
#             print(membership[vertex.index])
#             for edge in graph.es:
#                 # Coordinates
#                 origin = coordinates[edge.tuple[0]]
#                 destination = coordinates[edge.tuple[1]]
#
#                 # Convert to x and y datasets
#                 latitudes = (origin[0], destination[0])
#                 longitudes = (origin[1], destination[1])
#                 colors = ['Tomato','Orange', 'DodgerBlue', 'MediumSeaGreen', 'SlateBlue', "Violet", "#FF3399", "#9CCC65", "#00838F", "#795548"]
#
#                 # Plot
#                 plt.plot(longitudes, latitudes, c=colors[membership[vertex.index]], lw=line_width,
#                          ms=marker_size, ls="-", marker=".", transform=TRANSFORM)
#
#     # Display map
#     plt.show()


def map_projection(membership, coords, clusters):
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(MAP_BOUNDS, ccrs.PlateCarree())
    ax.coastlines(resolution='50m')

    colors = ['Tomato', 'Orange', 'DodgerBlue', 'MediumSeaGreen', 'SlateBlue', "Violet", "#FF3399", "#9CCC65",
              "#00838F", "#795548", 'sandybrown', 'skyblue']

    for vertex in graph.vs():
        print(vertex.index)
        print(colors[membership[vertex.index]])
        print(coords[vertex.index][0],coords[vertex.index][1])
        plt.plot(coords[vertex.index][0], coords[vertex.index][1], markersize=2, marker='o', color=colors[membership[vertex.index]])

    plt.show()

if __name__ == "__main__":
    """"Runtime"""
    start_time = time.time()

    """"Creating the needed empty lists"""
    time_series = []

    """"Specifying the filename and location"""
    years = ['2019','2020']
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']  # '01','02','03','04','05','06','07','08','09','10','11','12'

    for i in range(len(years)):
        for j in range(len(months)):
            filename = f"Combined_{years[i]}_{months[j]}_b"
            print(filename)
            path = GIT_DIR + 'Combined_' + years[i] + '_new\\' + filename + '.csv'

            """Creating a graph from data"""
            data = pd.read_csv(path, usecols=[1, 2])
            g0 = ig.Graph.DataFrame(edges=data, directed=True)

            """Creating a weighted graph from the adjacency matrix"""
            adj_matrix = g0.get_adjacency()
            adj_matrix = list(adj_matrix)
            g = ig.Graph.Weighted_Adjacency(adj_matrix)
            g.vs["name"] = g0.vs["name"]

            """"Presenting options for which type of community detection algorithm should be used"""
            methods = ["edge_betweenness", "infomap", "fast_greedy", "multilevel", "walktrap", "leiden"]
            clusters = commmunities(g, methods[3])  # According to the research presented in the method section of the paper, we should use the multilevel algorithm

            """"Printing numbers to check the process"""
            print(ig.clustering.VertexClustering.__len__(clusters))
            print(ig.clustering.VertexClustering.sizes(clusters), sum(ig.clustering.VertexClustering.sizes(clusters)))

            """"Appending data to create the time series"""
            graph, coords, membership = plot(g, filename, clusters)
            histogram_time_series(timeseries(membership),filename)
            # time_series.append(timeseries(membership))

            map_projection(membership, coords, clusters)

    """"Plotting the time series"""
    plot_time_series(time_series)

    """"Runtime"""
    print(time.time() - start_time)

# https://www.geeksforgeeks.org/python-intersection-two-lists/

# source of code which helped with visualisation
# https://stackoverflow.com/questions/23184306/draw-network-and-grouped-vertices-of-the-same-community-or-partition
