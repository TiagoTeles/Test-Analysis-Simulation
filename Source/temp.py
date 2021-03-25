import csv
import cartopy as cp
import matplotlib.pyplot as plt

# ---------- Setup ---------- #
# General settings
GIT_DIR = __file__[0:-14]
print(GIT_DIR)
ASSET_DIR = GIT_DIR + "Assets/"
DIR_2019 = GIT_DIR + "2019_Filtered/"
DIR_2020  = GIT_DIR + "2020_Filtered/"
FLIGHT_DIR = "EU_flights_2020_01.csv"
AIRPORT_DIR = "Airports.csv"

# Caropy settings
COLOUR_OCEAN = (1, 1, 1)
COLOUR_LAND = (0.9, 0.9, 0.9)
MAP_BOUNDS = (-30, 60, 25, 70)
PROJECTION = cp.crs.PlateCarree()
TRANSFORM = cp.crs.Geodetic()


# Open the file
airport_file = open(ASSET_DIR+AIRPORT_DIR, encoding="utf8")

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
for coordinate in coordinates:
    # Coordinates
    origin = (coordinate[1], coordinate[2])
    destination = origin

    # Convert to x and y datasets
    latitudes = (origin[0], destination[0])
    longitudes = (origin[1], destination[1])

    # Plot
    plt.plot(longitudes, latitudes, c = "Red", lw = 0,
             ms = 2, ls = "-", marker = "o", transform = TRANSFORM)

# Display map
plt.show()
