#!/usr/bin/env python3
"""
Simple GUI Launcher for Text Merge Application.
Run this to launch the modern CustomTkinter desktop interface.

Usage:
    python gui_launcher.py
"""

import sys
from pathlib import Path


def main():
    """Launch GUI application."""
    try:
        import customtkinter
        from src.gui import run_gui
        
        print("🚀 Launching Text Merge GUI...")
        run_gui()
        
    except ImportError as e:
        if "customtkinter" in str(e):
            print("❌ Error: CustomTkinter not installed")
            print("\nInstall GUI dependencies with:")
            print("  pip install customtkinter")
        else:
            print("❌ Error: Required packages not installed")
            print("\nInstall all dependencies with:")
            print("  pip install -r requirements.txt")
        print(f"\nDebug info: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching GUI: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
