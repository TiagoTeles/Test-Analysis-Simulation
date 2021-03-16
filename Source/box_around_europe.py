min_longitude = -25
max_longitude = 45
min_latitude = 35
max_latitude = 70


def in_europe(flight):
    """
    Checks whether a flight is contained in Europe.

    :param flight: list containing a flight in the format of the csv data files:
    :return: True if both the start- and endpoints of the flight are in Europe, False otherwise
    """

    try:
        long_2, lat_2 = float(flight[-2]), float(flight[-3])
        long_1, lat_1 = float(flight[-5]), float(flight[-6])
    except ValueError:
        return False

    if min_longitude < long_1 < max_longitude and min_longitude < long_2 < max_longitude and min_latitude < lat_1 < max_latitude and min_latitude < lat_2 < max_latitude:
        return True
    else:
        return False


def inter(flight):
    """
        Checks whether a flight is intercontinental.

        :param flight: list containing a flight in the format of the csv data files:
        :return: True if either the start- or endpoints is in Europe and the other is not, False otherwise
    """

    try:
        long_2, lat_2 = float(flight[-2]), float(flight[-3])
        long_1, lat_1 = float(flight[-5]), float(flight[-6])
    except ValueError:
        return False

    if (min_latitude < lat_1 < max_latitude and min_longitude < long_1 < max_latitude) and not (
            min_latitude < lat_2 < max_latitude and min_longitude < long_2 < max_latitude) or (
            min_latitude < lat_2 < max_latitude and min_longitude < long_2 < max_latitude) and not (
            min_latitude < lat_2 < max_latitude and min_longitude < long_2 < max_latitude):
        return True
    else:
        return False