#!/usr/bin/env python3
"""
Performance Analysis Script for JET Table Processing

This script runs an input CSV file through the process_JET_table function,
displays all console log output in real time, and reports performance metrics.

Usage:
    python analyze_table_processing.py [CSV_FILE_PATH]

    If no CSV file is provided, loads the default ECOv002 cal-val input table via JET3.

Example:
    python analyze_table_processing.py path/to/ECOv002-cal-val-JET-inputs.csv
"""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd
from JET3 import load_ECOv002_calval_JET_inputs, process_JET_table
from pytictoc import TicToc


def setup_logging(level=logging.INFO):
    """Configure logging to display all output in real time."""
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)

    return root_logger


def print_separator(char="=", length=80):
    """Print a separator line."""
    print(char * length)


def print_header(text):
    """Print a formatted header."""
    print_separator()
    print(f"  {text}")
    print_separator()


def analyze_performance(csv_path: str = None, offline_mode: bool = True):
    """
    Run performance analysis on JET table processing.

    Args:
        csv_path: Optional path to input CSV file. If None, uses JET3's default cal-val inputs.
        offline_mode: Whether to run in offline mode (default: True).

    Returns:
        tuple: (output_df, elapsed_time, rows_per_second)
    """
    logger = logging.getLogger(__name__)

    print_header("Loading Input Data")
    load_timer = TicToc()
    load_timer.tic()

    if csv_path:
        logger.info(f"Reading CSV file: {csv_path}")
        input_df = pd.read_csv(csv_path)
    else:
        logger.info("Loading default ECOv002 cal-val JET inputs from JET3")
        input_df = load_ECOv002_calval_JET_inputs()

    load_time = load_timer.tocvalue()

    logger.info(f"Loaded {len(input_df)} rows in {load_time:.3f} seconds")
    logger.info(f"Input columns: {len(input_df.columns)}")
    logger.info(f"Memory usage: {input_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    print("\n")
    print_header("Processing JET Table")

    process_timer = TicToc()
    process_timer.tic()

    try:
        output_df = process_JET_table(
            input_df,
            offline_mode=offline_mode
        )

        process_time = process_timer.tocvalue()

        print("\n")
        print_header("Processing Complete")
        logger.info(f"Output has {len(output_df)} rows and {len(output_df.columns)} columns")
        logger.info(f"New columns added: {len(output_df.columns) - len(input_df.columns)}")
        logger.info(f"Output memory usage: {output_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

        rows_per_second = len(output_df) / process_time if process_time > 0 else 0

        return output_df, process_time, rows_per_second

    except Exception as e:
        logger.error(f"Error during processing: {e}", exc_info=True)
        raise


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Analyze performance of JET table processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        default=None,
        help="Optional path to input CSV file (defaults to JET3 cal-val inputs)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging (DEBUG level)"
    )
    parser.add_argument(
        "--online",
        action="store_true",
        help="Run in online mode (allows data downloads, slower)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Path to save output CSV (optional)"
    )

    args = parser.parse_args()

    csv_path = None
    if args.csv_file:
        path_obj = Path(args.csv_file)
        if not path_obj.is_absolute():
            path_obj = Path(__file__).parent / path_obj
        if not path_obj.exists():
            print(f"Error: CSV file not found: {path_obj}", file=sys.stderr)
            sys.exit(1)
        csv_path = str(path_obj)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)

    logger = logging.getLogger(__name__)

    print_header("JET Table Processing Performance Analysis")
    print(f"Input file: {csv_path or 'JET3 default cal-val dataset'}")
    print(f"Offline mode: {not args.online}")
    print(f"Log level: {logging.getLevelName(log_level)}")
    print()

    overall_timer = TicToc()
    overall_timer.tic()

    try:
        output_df, process_time, throughput = analyze_performance(
            csv_path=csv_path,
            offline_mode=not args.online
        )

        total_time = overall_timer.tocvalue()

        print("\n")
        print_separator("=")
        print("  PERFORMANCE SUMMARY")
        print_separator("=")
        print(f"  Total execution time:    {total_time:.3f} seconds")
        print(f"  JET processing time:     {process_time:.3f} seconds")
        print(f"  Throughput:              {throughput:.2f} rows/second")
        print(f"  Time per row:            {1000 * process_time / len(output_df):.2f} ms")
        print_separator("=")

        if args.output:
            output_path = Path(args.output)
            logger.info(f"Saving output to: {output_path}")
            output_df.to_csv(output_path, index=False)
            logger.info("Output saved successfully")

        return 0

    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
