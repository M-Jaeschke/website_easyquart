"""
Discretization of the defined area.
===================================

.. sectionauthor: Pauline Werner (HTWK Leipzig)

First, some minimal example usage:
"""

# %%
# Import necessary python packages and functions

import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Polygon

from easyquart.bhe_optimization.core.area import Area
from easyquart.bhe_optimization.core.obstacle import House

# %%
# Defining the area as a shapely Polygon with a buffer
area_polygon = Polygon([(0, 0), (5, 0), (5, 6), (0, 6)])
d_buffer = 1.0  # Shrinking buffer of 0.5 m

# %%
# Creating obstacles as instances of House, Tree or Undefined
obstacles = [
    House(Polygon([(3, 4), (5, 4), (5, 6), (3, 6)])),  # House obstacle
]

# %%
# Create an Area instance with obstacles
area = Area(area_polygon, d_buffer, obstacles)

# %%
# Generate valid points
resolution_meter = 1.0
valid_points = area.generate_valid_points(resolution_meter)

# %%
# Convert valid points to Pandas DataFrame for better visualization
df_valid_points = pd.DataFrame(
    [(i, j, p.x, p.y) for i, j, p in valid_points],
    columns=["x_index", "y_index", "x_coord", "y_coord"],
)
print(df_valid_points.to_string(index=False))

# %%
# Demonstration: Plotting the area, obstacles and valid points
fig, ax = plt.subplots()

# Plot original area
x, y = area.polygon.exterior.xy
ax.plot(x, y, label="Original Area", color="black", linestyle="dashed")

# Plot buffered area
x, y = area.buffered_polygon().exterior.xy
ax.plot(x, y, label="Buffered Area", color="blue")

# Plot obstacles
for obs in obstacles:
    x, y = obs.polygon.exterior.xy
    ax.fill(x, y, color="red", alpha=0.5, label="Obstacle")

# Extract x and y coordinates from indexed valid points and plot them
x_valid = [p.x for _, _, p in valid_points]
y_valid = [p.y for _, _, p in valid_points]
ax.scatter(x_valid, y_valid, color="green", s=10, label="Valid Points")

ax.set_aspect("equal")
plt.show()
