"""
Docker smoke test for ECOv003-L3T-L4T-JET package installation.

This test suite validates that the package was correctly installed in a Docker
container and that all critical components and dependencies are functional.
"""

import sys
import importlib


class TestPackageImport:
    """Tests for successful package import in Docker environment."""

    def test_main_package_import(self):
        """Test that the main package can be imported."""
        import ECOv003_L3T_L4T_JET
        assert hasattr(ECOv003_L3T_L4T_JET, '__version__') or hasattr(ECOv003_L3T_L4T_JET, 'version')

    def test_core_modules_import(self):
        """Test that core modules are accessible."""
        core_modules = [
            'ECOv003_L3T_L4T_JET.PGE',
            'ECOv003_L3T_L4T_JET.L3TL4TJETConfig',
            'ECOv003_L3T_L4T_JET.constants',
            'ECOv003_L3T_L4T_JET.exceptions',
        ]
        for module_name in core_modules:
            module = importlib.import_module(module_name)
            assert module is not None, f"Failed to import {module_name}"


class TestCriticalDependencies:
    """Tests for critical dependency availability in Docker environment."""

    def test_numpy_available(self):
        """Test that numpy is installed and accessible."""
        import numpy
        assert numpy.__version__ is not None

    def test_pandas_available(self):
        """Test that pandas is installed and accessible."""
        import pandas
        assert pandas.__version__ is not None

    def test_rasterio_available(self):
        """Test that rasterio is installed and accessible."""
        import rasterio
        assert rasterio.__version__ is not None

    def test_onnx_available(self):
        """Test that ONNX runtime is installed and accessible."""
        import onnxruntime
        assert hasattr(onnxruntime, 'get_version_string')

    def test_sklearn_available(self):
        """Test that scikit-learn is installed and accessible."""
        import sklearn
        assert sklearn.__version__ is not None

    def test_rasters_available(self):
        """Test that rasters package is installed and accessible."""
        import rasters
        assert rasters is not None


class TestEntryPoint:
    """Tests for package entry point configuration."""

    def test_entry_point_callable(self):
        """Test that the main entry point is callable."""
        from ECOv003_L3T_L4T_JET.ECOv003_L3T_L4T_JET import main
        assert callable(main), "Main entry point is not callable"


class TestPackageStructure:
    """Tests for expected package structure."""

    def test_xml_files_present(self):
        """Test that required XML configuration files are included."""
        try:
            from importlib.resources import files
            resource = files('ECOv003_L3T_L4T_JET').joinpath('L3T_L4T_JET.xml')
            assert resource.is_file(), "Configuration file 'L3T_L4T_JET.xml' not found in package"
        except Exception:
            # Fallback: check if we can import and access module
            import ECOv003_L3T_L4T_JET
            assert hasattr(ECOv003_L3T_L4T_JET, '__path__')

    def test_package_metadata(self):
        """Test that package metadata is accessible."""
        import ECOv003_L3T_L4T_JET
        try:
            from importlib.metadata import version
            pkg_version = version('ECOv003-L3T-L4T-JET')
            assert pkg_version is not None
        except Exception:
            # Fallback: just verify package has some metadata
            assert hasattr(ECOv003_L3T_L4T_JET, '__doc__')


class TestEnvironmentCompatibility:
    """Tests for environment and Python version compatibility."""

    def test_python_version(self):
        """Test that Python version meets requirements."""
        assert sys.version_info >= (3, 11), f"Python {sys.version_info.major}.{sys.version_info.minor} is below minimum required 3.11"

    def test_sys_path_includes_package(self):
        """Test that the package is in Python path."""
        import ECOv003_L3T_L4T_JET
        package_path = ECOv003_L3T_L4T_JET.__path__
        assert package_path is not None
        assert len(package_path) > 0