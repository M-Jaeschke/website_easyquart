"""
Example for uncertain variables collection
==========================================

.. sectionauthor:: Max Jäschke (HTWK Leipzig)

"""

# %%
# Import the needed packages and the distributions from scipy.stats

from pathlib import Path
from tempfile import mkdtemp

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, skewnorm

from easyquart.uncertainty import (
    UncertainVariable,
    UncertainVariableCollection,
)

# %%
# Create a collection of uncertain variables and add variables

collection = UncertainVariableCollection()

collection.add_variable(
    UncertainVariable(
        name="Soil Conductivity",
        distribution=skewnorm(loc=2, scale=1, a=1.5),
        unit=r"$\lambda$ in W/m*K",
        description="skewnorm distribution of the soil conductivity",
    )
)

collection.add_variable(
    UncertainVariable(
        name="Geothermal Heat Flux",
        distribution=norm(loc=0.078, scale=0.014),
        unit=r"$\dot{q}$ in $W/m^2$",
        description="geothermal heat flux from the earth",
    )
)

collection.add_variable(
    UncertainVariable(
        name="Soil Volumetric Heat Capacity",
        distribution=norm(loc=2e6, scale=0.45e6),
        unit=r"$\rho \cdot c_p$ in J/kg*K",
        description="volumetric heat capacity of the soil",
    )
)

collection.add_variable(
    UncertainVariable(
        name="Grout Conductivity",
        distribution=skewnorm(loc=1.5, scale=0.8, a=3),
        unit=r"$\lambda$ in W/m*K",
        description="skewnorm distribution of the grout conductivity",
    )
)

print(collection.list_variables())

# %%
# Save the collection as a json-file

tmp_dir = Path(mkdtemp())
json_file = tmp_dir / "uncertain_variables.json"
collection.to_json(json_file)

# %%
# Load the variables from the json to a new uncertain variable collection
uncertain_variables = UncertainVariableCollection()
uncertain_variables.from_json(json_file)

all_variables = uncertain_variables.list_variables()
print(all_variables)

# %%
# Plot the distributions
fig, ax = plt.subplots(2, 2, figsize=(10, 6), constrained_layout=True)

for i, var in enumerate(all_variables):
    variable = uncertain_variables.get_variable(var)
    x_min, x_max = variable.distribution.ppf([0.00001, 0.99999])
    x = np.linspace(x_min, x_max, 10000)
    ax[i % 2, int(i / 2)].plot(x, variable.distribution.pdf(x))
    ax[i % 2, int(i / 2)].set_title(var)
    ax[i % 2, int(i / 2)].set_xlabel(variable.unit)
    ax[i % 2, int(i / 2)].set_ylabel(r"$f_p (x)$")
    ax[i % 2, int(i / 2)].grid(True, alpha=0.3)

fig.show()

# %%
# Perform the sampling and add the sample points to the distribution plot
uncertain_variables.latin_hypercube_sampling(n_samples=5)

fig, ax = plt.subplots(2, 2, figsize=(10, 6), constrained_layout=True)
for i, var in enumerate(all_variables):
    variable = uncertain_variables.get_variable(var)
    x_min, x_max = variable.distribution.ppf([0.00001, 0.99999])
    x = np.linspace(x_min, x_max, 10000)
    ax[i % 2, int(i / 2)].plot(x, variable.distribution.pdf(x))
    ax[i % 2, int(i / 2)].set_title(var)
    ax[i % 2, int(i / 2)].set_xlabel(variable.unit)
    ax[i % 2, int(i / 2)].set_ylabel(r"$f_p (x)$")
    ax[i % 2, int(i / 2)].grid(True, alpha=0.3)
    variable = uncertain_variables.get_variable(var)
    ax[i % 2, int(i / 2)].scatter(
        variable.samples, variable.distribution.pdf(variable.samples), color="r"
    )
    for j, sample in enumerate(variable.samples):
        shiftx = 0.90 if sample < variable.distribution.mean() else 1.02
        shifty = 1.02
        ax[i % 2, int(i / 2)].annotate(
            f"{j}",
            (sample * shiftx, variable.distribution.pdf(sample) * shifty),
        )

fig.show()
