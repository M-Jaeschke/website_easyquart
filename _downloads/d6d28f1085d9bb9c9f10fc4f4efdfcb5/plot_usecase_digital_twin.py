"""
Example usage of the DigitalTwin Class
==================================

.. sectionauthor: Max Jäschke (HTWK Leipzig)

"""

# %%
# Import the needed packages and the digital twin class

from pathlib import Path
from tempfile import mkdtemp

import matplotlib.pyplot as plt
import numpy as np

from easyquart.digital_twin import DigitalTwinEasyQuart

# %%
# Define simple data arrays to demonstrate the showcase

timevalues = np.linspace(start=0, stop=10, num=11)
network_flow_rate = np.full(11, 0.002)
building_power = np.full(11, 1000)
bhe_to_network_temperatures = np.tile(np.array([273.15, 280.15]), 11)
bhe_to_network_avg_temperature = np.full(11, 273.15)
network_to_bhe_temperatures = np.tile(np.array([273.15, 280.15]), 11)
network_to_bhe_avg_temperature = np.full(11, 273.15)
network_to_building_temperature = np.full(11, 273.15)
building_to_network_temperature = np.full(11, 273.15)

# %%
# Create class object with known values from the building and HVAC simulation and write to file

tmp_dir = Path(mkdtemp())
h5_file = tmp_dir / "iter_0.h5"

building_digital_twin = DigitalTwinEasyQuart(
    rho_refrigerant=1000,
    cp_refrigerant=4000.0,
    timevalues=timevalues,
    network_flow_rate=network_flow_rate,
    networkToBuilding_temperature=network_to_building_temperature,
    buildingToNetwork_temperature=building_to_network_temperature,
    building_power=building_power,
)

building_digital_twin.save_h5(h5_file)

# %%
# Load the data from file and use it e.g. for the network or subsurface simulation

digital_twin_iter0 = DigitalTwinEasyQuart.load_h5(h5_file)

modelica_txt_file = tmp_dir / "input_modelica.txt"
digital_twin_iter0.write_dataclass_to_txt(
    columns_to_write=[
        "timevalues",
        "network_flow_rate",
        "buildingToNetwork_temperature",
    ],
    path_for_txt=modelica_txt_file,
    table_name="network_input_from_building",
)

# %%
# Perform the network or subsurface simulation and store all results by overwriting file

digital_twin_iter0.networkToBHE_avg_temperature = network_to_bhe_avg_temperature
digital_twin_iter0.networkToBHE_temperatures = network_to_bhe_temperatures

digital_twin_iter0.bheToNetwork_avg_temperature = bhe_to_network_avg_temperature

digital_twin_iter0.bheToNetwork_temperatures = bhe_to_network_temperatures

digital_twin_iter0.save_h5(h5_file)

# %%
# Use the results for plotting and further analysis

plt.plot(
    digital_twin_iter0.timevalues,
    digital_twin_iter0.bheToNetwork_avg_temperature - 273.15,
    label="BHEtoNetwork",
)
plt.plot(
    digital_twin_iter0.timevalues,
    digital_twin_iter0.bheToNetwork_avg_temperature - 273.15,
    label="NetworkToBHE",
)
plt.ylabel(r"$\vartheta$ in °C")
plt.xlabel("t in s")
plt.show()
