"""
Example script for downloading ECOSTRESS granules and running the L3T/L4T JET Product Generating Executable (PGE).

This script demonstrates how to:
1. Download ECOSTRESS L2T_LSTE and L2T_STARS granules using the Common Metadata Repository (CMR) API via the ECOv002-CMR package.
2. Generate a run configuration XML file for the L3T/L4T JET PGE using the ECOv003-L3T-L4T-JET package.
3. Execute the PGE and print the results.

Requirements:
- ECOv002-CMR package
- ECOv003-L3T-L4T-JET package

Update the working and static directory paths as needed for your environment.
"""

import logging
import os
from ECOv002_CMR import download_ECOSTRESS_granule
from ECOv003_L3T_L4T_JET import generate_L3T_L4T_JET_runconfig, L3T_L4T_JET

# Disable all logger output for a cleaner script output
logging.getLogger().handlers = []

# Set the working and static directories
working_directory = os.path.join("~", "data", "ECOv003_example")  # Directory for downloaded granules and outputs
static_directory = os.path.join("~", "data", "L3T_L4T_static")      # Directory for static input files

# Download the L2T_LSTE granule for a specific orbit, scene, tile, and date
L2T_LSTE_granule = download_ECOSTRESS_granule(
    product="L2T_LSTE",
    orbit=35698,
    scene=14,
    tile="11SPS",
    aquisition_date="2024-10-22",
    parent_directory=working_directory
)

# Download the L2T_STARS granule for the same tile and date (used as prior)
L2T_STARS_granule = download_ECOSTRESS_granule(
    product="L2T_STARS",
    tile="11SPS",
    aquisition_date="2024-10-22",
    parent_directory=working_directory
)

# Generate the XML run configuration file for the L3T/L4T JET PGE
runconfig_filename = generate_L3T_L4T_JET_runconfig(
    L2T_LSTE_filename=L2T_LSTE_granule.product_filename,
    L2T_STARS_filename=L2T_STARS_granule.product_filename,
    working_directory=working_directory,
    static_directory=static_directory
)
print(f"Run configuration file generated: {runconfig_filename}")

# Print the contents of the generated run configuration file
with open(runconfig_filename, "r") as f:
    print(f.read())

# Run the L3T/L4T JET PGE using the generated configuration file
# By default, processing will be skipped if output files already exist
exit_code = L3T_L4T_JET(runconfig_filename=runconfig_filename, overwrite=True, save_diagnostics=False)
print(f"L3T/L4T JET PGE exited with code: {exit_code}")

# To force regeneration of output files even if they exist, use overwrite=True:
# exit_code = L3T_L4T_JET(runconfig_filename=runconfig_filename, overwrite=True)
# print(f"L3T/L4T JET PGE exited with code: {exit_code}")



