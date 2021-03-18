"""
This script imports a datasset of flights and
displays them using the specified projection.
"""


# ---------- Imports ---------- #
import cartopy as cp
import matplotlib.pyplot as plt
from networktest import coords_lst

# ---------- Setup ---------- #
# Caropy settings
COLOUR_OCEAN = (0.0,0.42,0.58)
COLOUR_LAND = (0.96,0.96, 0.86)
MAP_BOUNDS = (-35, 60, 25, 75)


# ---------- Main Program ---------- #

# Set projection
ax = plt.axes(projection=cp.crs.Robinson())

# Set resolution
ax.coastlines(resolution="50m")

# Set borders
ax.set_extent (MAP_BOUNDS, cp.crs.PlateCarree())

# Show gridlines
ax.gridlines()

# Map features
ax.add_feature(cp.feature.BORDERS, linestyle='--', alpha=1)
ax.add_feature(cp.feature.LAND, facecolor=COLOUR_LAND)
ax.add_feature(cp.feature.OCEAN, facecolor=COLOUR_OCEAN)
ax.add_feature(cp.feature.LAKES, facecolor=COLOUR_OCEAN)

# Display flights
for edge in coords_lst:
	coords_origin = edge[0] 
	coords_destination = edge[1] 

	plt.plot((coords_origin[0], coords_destination[0]), (coords_origin[1], coords_destination[1])
            , color = "Blue", linestyle='-', linewidth = 0.25, marker = ".", markersize = 5, transform=cp.crs.Geodetic())

# Show map
plt.show()
