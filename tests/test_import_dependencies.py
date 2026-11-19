import pytest

# List of runtime dependencies declared in pyproject.toml
dependencies = [
    "AquaSEBS",
    "BESS_JPL",
    "check_distribution",
    "colored_logging",
    "ECOv002_calval_tables",
    "ECOv002_CMR",
    "ECOv002_granules",
    "ECOv003_exit_codes",
    "ECOv003_granules",
    "FLiESANN",
    "GEOS5FP",
    "JET3",
    "koppengeiger",
    "monte_carlo_sensitivity",
    "numpy",
    "onnx",
    "onnxruntime",
    "pandas",
    "PMJPL",
    "PTJPLSM",
    "dateutil",
    "pytictoc",
    "rasterio",
    "rasters",
    "sklearn",
    "skl2onnx",
    "solar_apparent_time",
    "STIC_JPL",
    "sun_angles",
    "untangle",
    "verma_net_radiation",
]


@pytest.mark.parametrize("dependency", dependencies)
def test_dependency_import(dependency):
    __import__(dependency)
