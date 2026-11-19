import pytest

# List of dependencies
dependencies = [
    "AquaSEBS",
    "BESS_JPL",
    "check_distribution",
    "colored_logging",
    "ECOv002_CMR",
    "ECOv002_granules",
    "ECOv003_exit_codes",
    "ECOv003_granules",
    "FLiESANN",
    "GEOS5FP",
    "JET3",
    "koppengeiger",
    "numpy",
    "pandas",
    "PMJPL",
    "PTJPLSM",
    "dateutil",
    "rasters",
    "sklearn",
    "STIC_JPL",
    "sun_angles",
    "untangle",
    "verma_net_radiation",
]


@pytest.mark.parametrize("dependency", dependencies)
def test_dependency_import(dependency):
    __import__(dependency)
