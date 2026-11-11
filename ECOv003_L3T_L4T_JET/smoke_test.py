"""
Smoke test module for ECOv003-L3T-L4T-JET package.

Provides a top-level test() function to validate package installation
and environment compatibility.

Usage:
    import ECOv003_L3T_L4T_JET
    ECOv003_L3T_L4T_JET.test()
"""

import sys
import importlib
from typing import List, Tuple


def test() -> bool:
    """
    Run smoke tests to validate package installation and environment compatibility.

    This function tests:
    - Package imports
    - Core module availability
    - Critical dependency availability
    - Entry point functionality
    - Python version requirements
    - Package structure and metadata

    Returns:
        bool: True if all tests pass, False otherwise

    Raises:
        SystemExit: Exits with code 0 on success, 1 on failure
    """
    print("=" * 70)
    print("ECOv003-L3T-L4T-JET Package Smoke Test")
    print("=" * 70)
    print()

    # Track results
    all_passed = True

    # Test 1: Python version
    print("[TEST] Python Version Compatibility")
    if sys.version_info < (3, 11):
        print(f"  ✗ FAIL: Python {sys.version_info.major}.{sys.version_info.minor} is below minimum required 3.11")
        all_passed = False
    else:
        print(f"  ✓ PASS: Python {sys.version_info.major}.{sys.version_info.minor}")
    print()

    # Test 2: Package import
    print("[TEST] Main Package Import")
    try:
        import ECOv003_L3T_L4T_JET
        print("  ✓ PASS: ECOv003_L3T_L4T_JET imported successfully")
    except ImportError as e:
        print(f"  ✗ FAIL: Failed to import ECOv003_L3T_L4T_JET: {e}")
        all_passed = False
    print()

    # Test 3: Core modules
    print("[TEST] Core Modules Import")
    core_modules = [
        'ECOv003_L3T_L4T_JET.PGE',
        'ECOv003_L3T_L4T_JET.L3TL4TJETConfig',
        'ECOv003_L3T_L4T_JET.constants',
        'ECOv003_L3T_L4T_JET.exceptions',
    ]
    core_ok = True
    for module_name in core_modules:
        try:
            importlib.import_module(module_name)
            print(f"  ✓ {module_name}")
        except ImportError as e:
            print(f"  ✗ {module_name}: {e}")
            core_ok = False
            all_passed = False
    if core_ok:
        print("  ✓ PASS: All core modules imported")
    else:
        print("  ✗ FAIL: Some core modules failed to import")
    print()

    # Test 4: Critical dependencies
    print("[TEST] Critical Dependencies")
    dependencies = {
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'rasterio': 'Rasterio',
        'onnxruntime': 'ONNX Runtime',
        'sklearn': 'scikit-learn',
        'rasters': 'Rasters',
    }
    deps_ok = True
    for module_name, display_name in dependencies.items():
        try:
            mod = importlib.import_module(module_name)
            version_str = getattr(mod, '__version__', 'unknown')
            print(f"  ✓ {display_name} ({version_str})")
        except ImportError as e:
            print(f"  ✗ {display_name}: {e}")
            deps_ok = False
            all_passed = False
    if deps_ok:
        print("  ✓ PASS: All critical dependencies available")
    else:
        print("  ✗ FAIL: Some dependencies are missing")
    print()

    # Test 5: Entry point
    print("[TEST] Entry Point")
    try:
        from ECOv003_L3T_L4T_JET.ECOv003_L3T_L4T_JET import main
        if callable(main):
            print("  ✓ PASS: Main entry point is callable")
        else:
            print("  ✗ FAIL: Main entry point is not callable")
            all_passed = False
    except ImportError as e:
        print(f"  ✗ FAIL: Could not import main entry point: {e}")
        all_passed = False
    print()

    # Test 6: Package metadata
    print("[TEST] Package Metadata")
    try:
        from importlib.metadata import version
        pkg_version = version('ECOv003-L3T-L4T-JET')
        print(f"  ✓ PASS: Package version: {pkg_version}")
    except Exception as e:
        print(f"  ✗ FAIL: Could not access package metadata: {e}")
        all_passed = False
    print()

    # Final report
    print("=" * 70)
    if all_passed:
        print("✓ ALL SMOKE TESTS PASSED")
        print("=" * 70)
        return True
    else:
        print("✗ SOME SMOKE TESTS FAILED")
        print("=" * 70)
        return False


if __name__ == '__main__':
    """Allow direct execution: python -m ECOv003_L3T_L4T_JET.smoke_test"""
    success = test()
    sys.exit(0 if success else 1)
