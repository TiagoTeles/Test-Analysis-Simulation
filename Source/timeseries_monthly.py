"""
This scipt provides tools to plot timeseries.
"""


# ---------- Imports ---------- #
import matplotlib.pyplot as plt
from centrality import get_closeness
from data_visualization import create_graph

# ---------- Setup ---------- #
GIT_DIR = __file__[0:-28]


# ---------- Function Definitions ---------- #
def get_filename(git_dir, year, month, inter = False):
    """
    Determines the filename based
    on the parameters given.

    Arguments:
        git_dir (String): Base directory
        year (int): Year teh data was collected
        month (int): Month the data was collected
        eu (Boolean): Whether the data is from europe or intercontinantal

    Returns:
        filename (String): Name of the file
    """

    month_str = str(month).zfill(2)
    year_str = str(year)

    if not inter:
        filename = "{0}{1}_Filtered//EU_flights_{1}_{2}.csv".format(git_dir, year_str, month_str)
    else:
        filename = "{0}{1}_Filtered//Inter_flights_{1}_{2}.csv".format(git_dir, year_str, month_str)

    return filename


def timeseries_monthly(func, text, index = 0):
    """
    Plots a timeseries for 2019 and 2020
    using the function and parameters provided.

    Arguments:
        f (Function): Function used to determine the Y values
        text (List): Visual settings of the graph
        index (int): Index of the values in the return tuple
    """

    # Determine values
    values_2019 = []
    values_2020 = []
    for month in range(1, 12 + 1):

        # Get filename
        filename_2019 = get_filename(GIT_DIR, 2019, month)
        filename_2020 = get_filename(GIT_DIR, 2020, month)

        # Get graphs
        graph_2019 = create_graph(filename_2019)
        graph_2020 = create_graph(filename_2020)

        # Determine value
        values_2019.append(func(graph_2019)[index])
        values_2020.append(func(graph_2020)[index])

    # Plot values
    x_values = list(range(1, 12 +1))
    plt.plot(x_values, values_2019, color = "darkorange", label = "2019: " + text[3], linewidth = 3)
    plt.plot(x_values, values_2020, color = "dodgerblue", label = "2020: " + text[3], linewidth = 3)

    # Configure settings
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ["January","February", "March",
                "April",  "May","June","July","August", "September", "October", "November",
                "December"], rotation = 45)

    plt.title(text[0])
    plt.xlabel(text[1])
    plt.ylabel(text[2])
    plt.xlim(1, 12)
    plt.legend()
    plt.grid(axis = "x", linestyle = "--")

    # Display plot
    plt.show()


# ---------- Main Program ---------- #
if __name__ == "__main__":
    configs = ["Average closeness centrality per month in EU", "Month",
    "Closeness centrality", "Closeness centrality"]

    timeseries_monthly(get_closeness, configs)
