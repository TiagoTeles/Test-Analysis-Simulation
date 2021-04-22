""" This scipt provides tools to plot timeseries """


# ---------- Imports ---------- #
import matplotlib.pyplot as plt
import numpy as np
from centrality import get_betweenness, get_closeness, get_clustering, get_degree, get_giant
from data_visualization import create_graph

# ---------- Setup ---------- #
GIT_DIR = __file__[0:-28]
TOP_AIRPORTS = ["EGLL", "LFPG", "EDDF", "EHAM", "LEMD"]
MONTHS = ["January", "February", "March", "April",  "May", "June", "July",
          "August", "September", "October", "November", "December"]

# ---------- Function Definitions ---------- #
def get_filename(git_dir, year, month, european = True):
    """
    Determines the filename based on the parameters given.

    Arguments:
        git_dir (String): Base directory
        year (int): Year the data was collected
        month (int): Month the data was collected
        european (Boolean): Whether the data is from europe or intercontinential

    Returns:
        filename (String): Name of the file
    """

    month_str = str(month).zfill(2)
    year_str = str(year)

    if european:
        filename = "{0}{1}_Filtered//EU_flights_{1}_{2}.csv".format(git_dir, year_str, month_str)
    else:
        filename = "{0}{1}_Filtered//Inter_flights_{1}_{2}.csv".format(git_dir, year_str, month_str)

    return filename


def timeseries_average(func, index, **args):
    """
    Plots a timeseries using the function and parameters provided.

    Arguments:
        func (Function): Function used to determine the Y values
        index (int): Index of the values in the return tuple
        **args (Dict): Optional arguments
    """

    # Decode arguments
    title = args.get("title", "")
    x_label = args.get("x_label", "")
    y_label = args.get("y_label", "")

    # Determine values
    values_2019 = []
    values_2020 = []
    for month in range(1, 13):

        # Get filename
        filename_2019 = get_filename(GIT_DIR, 2019, month)
        filename_2020 = get_filename(GIT_DIR, 2020, month)

        # Get graphs
        graph_2019 = create_graph(filename_2019)
        graph_2020 = create_graph(filename_2020)

        # Determine value
        values_2019.append(func(graph_2019, [], **args)[index])
        values_2020.append(func(graph_2020, [], **args)[index])

    # Plot values
    x_values = list(range(1, 13))
    plt.plot(x_values, values_2019, color = "darkorange", label = "2019", linewidth = 3,  marker = "o")
    plt.plot(x_values, values_2020, color = "dodgerblue", label = "2020", linewidth = 3,  marker = "o")

    # Configure plot
    plt.xlim(1, 12)
    plt.grid(axis = "x", linestyle = "--")
    plt.xticks(x_values, MONTHS, rotation = 45)

    # Configure labels
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()

    # Display plot
    plt.show()


def timeseries_airports(func, index, airports, **args):
    """
    Plots a timeseries of the top airports using the function and parameters provided.

    Arguments:
        func (Function): Function used to determine the Y values
        index (int): Index of the values in the return tuple
        airports (List): List of airports to be displayed
        **args (Dict): Optional arguments
    """

    # Decode arguments
    title = args.get("title", "")
    x_label = args.get("x_label", "")
    y_label = args.get("y_label", "")

    # Determine values
    values_2019 = []
    values_2020 = []
    for month in range(1, 13):

        # Get filename
        filename_2019 = get_filename(GIT_DIR, 2019, month)
        filename_2020 = get_filename(GIT_DIR, 2020, month)

        # Get graphs
        graph_2019 = create_graph(filename_2019)
        graph_2020 = create_graph(filename_2020)

        # Determine value
        values_2019.append(func(graph_2019, airports, **args)[index])
        values_2020.append(func(graph_2020, airports, **args)[index])

    x_values = list(range(1, 13))

    # Plot for 2019
    axis_2019 = plt.subplot(1, 2, 1)
    for i, icao in enumerate(airports):
        y_values = np.array(values_2019).transpose()[i]
        axis_2019.plot(x_values, y_values, label = icao, linewidth = 3, marker = "o")

    # Configure plot
    plt.xlim(1, 12)
    plt.grid(axis = "x", linestyle = "--")
    plt.xticks(x_values, MONTHS, rotation = 45)

    # Configure labels
    plt.title(title  + str(": 2019"))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()

    # Plot for 2020
    axis_2020 = plt.subplot(1, 2, 2, sharey = axis_2019)
    for i, icao in enumerate(airports):
        y_values = np.array(values_2020).transpose()[i]
        axis_2020.plot(x_values, y_values, label = icao, linewidth = 3, marker = "o")

    # Configure plot
    plt.xlim(1, 12)
    plt.grid(axis = "x", linestyle = "--")
    plt.xticks(x_values, MONTHS, rotation = 45)

    # Configure labels
    plt.title(title  + str(": 2020"))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()

    # Display plot
    plt.show()


# ---------- Main Program ---------- #
if __name__ == "__main__":
    TITLE = "Average closeness centrality in Europe"
    X_LABEL = "Month"
    Y_LABEL = "Closeness centrality"
    timeseries_average(get_closeness, 0, title = TITLE, x_label = X_LABEL, y_label = Y_LABEL)

    # TITLE = "Closeness centrality of the top five airports in Europe"
    # X_LABEL = "Month"
    # Y_LABEL = "Closeness centrality"
    # timeseries_airports(get_closeness, 1, TOP_AIRPORTS, title = TITLE, x_label = X_LABEL, y_label = Y_LABEL)
