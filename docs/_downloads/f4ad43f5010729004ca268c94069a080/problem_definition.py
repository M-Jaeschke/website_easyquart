"""
Defining the optimization problem.
==================================

.. sectionauthor: Pauline Werner (HTWK Leipzig)

First, some minimal example usage:
"""

# %%
# Import the Area class and the shapely Polygon function
from shapely.geometry import Polygon

from easyquart.bhe_optimization.core.area import Area
from easyquart.bhe_optimization.core.obstacle import House, Tree

# %%
# Defining the area as a shapely Polygon with a buffer
area_polygon = Polygon([(0, 0), (5, 0), (5, 6), (0, 6)])
d_buffer = 0.5  # Shrinking buffer of 0.5 meters

# %%
# Creating obstacles directly as instances of House, Tree, or Undefined
obstacles = [
    House(Polygon([(3, 4), (5, 4), (5, 6), (3, 6)])),  # A house obstacle
]

# %%
# Create an Area instance with obstacles
area = Area(area_polygon, d_buffer, obstacles)

# %%
# Print the original and buffered polygon
print(f"Original polygon: {area.polygon}")
print(f"Buffered (shrunk) polygon: {area.buffered_polygon()}")

# %%
# Demonstration: Adding an obstacle using append()
new_tree = Tree(Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]))
area.obstacles.append(new_tree)
print(f"After adding an obstacle: {area}")

# %%
# Demonstration: Removing an obstacle using remove()
area.obstacles.remove(new_tree)
print(f"After removing an obstacle: {area}")

# %%
# Export to JSON
area.to_json("data/area.json")

# %%
# Print the Area instance
print(area)

# %%
# Load an Area instance from JSON
loaded_area = Area.from_json("data/area.json")
print(f"Loaded from JSON: {loaded_area}")
print(f"Loaded buffered (shrunk) polygon: {loaded_area.buffered_polygon()}")
