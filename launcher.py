#!/usr/bin/env python3
"""
Launcher script for Text Merge Application.
Automatically detects command-line arguments and launches either CLI or GUI.

Usage:
    python launcher.py                      # Launch GUI
    python launcher.py --cli <input> <output> ...  # Launch CLI
    python launcher.py -h                   # Show help
"""

import sys
import argparse
from pathlib import Path


def launch_gui() -> None:
    """Launch the GUI application."""
    try:
        from src.gui import run_gui
        run_gui()
    except ImportError as e:
        print(f"Error: Required packages not installed for GUI mode")
        print(f"Install with: pip install -r requirements.txt")
        print(f"\nDetails: {str(e)}")
        sys.exit(1)


def launch_cli(args: argparse.Namespace) -> None:
    """Launch the CLI application."""
    import main
    
    # Convert args to match expected format
    sys.argv = [
        "main.py",
        str(args.input_folder),
        args.output_name,
    ]
    
    if hasattr(args, "format") and args.format:
        sys.argv.extend(["--format", args.format])
    
    if hasattr(args, "sort_order") and args.sort_order:
        sys.argv.extend(["--sort-order", args.sort_order])
    
    if hasattr(args, "log_level") and args.log_level:
        sys.argv.extend(["--log-level", args.log_level])
    
    # Run main.py
    main.main()


def main() -> None:
    """Main entry point - decide between GUI and CLI."""
    # Check if any arguments provided
    if len(sys.argv) == 1:
        # No arguments - launch GUI
        print("Launching GUI...")
        launch_gui()
        return

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Text Merge Application - GUI or CLI",
        add_help=False
    )

    # Check if --cli flag is present
    if "--cli" in sys.argv:
        # CLI mode
        sys.argv.remove("--cli")
        
        cli_parser = argparse.ArgumentParser(
            description="Text Merge Application - CLI Mode"
        )
        cli_parser.add_argument(
            "input_folder",
            type=str,
            help="Path to folder containing .txt files"
        )
        cli_parser.add_argument(
            "output_name",
            type=str,
            help="Output file name (without extension)"
        )
        cli_parser.add_argument(
            "--format",
            type=str,
            default="both",
            choices=["docx", "pdf", "both"],
            help="Export format (default: both)"
        )
        cli_parser.add_argument(
            "--sort-order",
            type=str,
            default="name",
            choices=["name", "date"],
            help="File sorting order (default: name)"
        )
        cli_parser.add_argument(
            "--log-level",
            type=str,
            default="INFO",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Logging level (default: INFO)"
        )

        args = cli_parser.parse_args()
        launch_cli(args)
    else:
        # Assume CLI mode with positional arguments
        if len(sys.argv) < 3:
            # Not enough arguments - launch GUI
            print("Launching GUI...")
            launch_gui()
        else:
            # Try CLI mode
            import main
            main.main()


if __name__ == "__main__":
    main()
