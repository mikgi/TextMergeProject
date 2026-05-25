#!/usr/bin/env python3
"""
GUI Verification Test - Validates the modern CustomTkinter GUI functionality.
Tests the GUI components without launching the full window.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gui import Theme, ModernCard, ModernButton, ActionButton, TextMergeGUI, LogHandler
from src.config import Config
from src.font_manager import FontManager
import customtkinter as ctk


def test_theme_constants():
    """Verify theme constants are properly defined."""
    print("Testing Theme constants...")
    assert Theme.BG_PRIMARY == "#0e1117", "Primary bg color incorrect"
    assert Theme.TEXT_PRIMARY == "#e6edf3", "Primary text color incorrect"
    assert Theme.ACCENT_BLUE == "#1f6feb", "Accent blue incorrect"
    assert Theme.FONT_TITLE == ("Segoe UI", 16, "bold"), "Title font incorrect"
    assert Theme.PADDING_LG == 16, "Large padding incorrect"
    print("✓ Theme constants verified")


def test_components_instantiation():
    """Test that GUI components can be instantiated."""
    print("\nTesting GUI component instantiation...")
    
    root = ctk.CTk()
    root.withdraw()  # Hide window
    
    try:
        # Test ModernCard
        card = ModernCard(root)
        print("✓ ModernCard created")
        
        # Test ModernButton
        btn = ModernButton(root, "Test Button", is_primary=True)
        print("✓ ModernButton created")
        
        # Test ActionButton
        action_btn = ActionButton(root, "Action", is_success=True)
        print("✓ ActionButton created")
        
        # Test LogHandler
        messages = []
        def capture_msg(msg):
            messages.append(msg)
        
        handler = LogHandler(capture_msg)
        print("✓ LogHandler created")
        
    finally:
        root.destroy()


def test_gui_initialization():
    """Test that the TextMergeGUI can be initialized."""
    print("\nTesting TextMergeGUI initialization...")
    
    root = ctk.CTk()
    root.withdraw()  # Hide window
    
    try:
        gui = TextMergeGUI(root)
        
        # Verify key attributes exist
        assert gui.input_folder is None, "Input folder should start as None"
        assert gui.output_folder.exists(), "Output folder should exist"
        assert gui.config is not None, "Config should be initialized"
        assert gui.file_merger is not None, "FileMerger should be initialized"
        assert gui.font_manager is not None, "FontManager should be initialized"
        
        print("✓ TextMergeGUI initialized successfully")
        print(f"  - Input folder: {gui.input_folder}")
        print(f"  - Output folder: {gui.output_folder}")
        print(f"  - Config loaded: {gui.config.output_directory}")
        
    finally:
        root.destroy()


def test_font_manager_integration():
    """Test font manager integration with GUI."""
    print("\nTesting FontManager integration...")
    
    fm = FontManager(Path("fonts"))
    available = fm.list_available_fonts()
    
    print(f"✓ FontManager loaded")
    print(f"  - Available fonts: {len(available)}")
    
    # Verify Thai fonts are available
    thai_font_names = [name for name in available.keys() if "Thai" in name or "Sarabun" in name]
    print(f"  - Thai fonts found: {len(thai_font_names)}")
    
    assert len(available) > 0, "No fonts available"
    assert len(thai_font_names) > 0, "No Thai fonts available"
    print("✓ FontManager integration verified")


def test_config_loading():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    config = Config()
    
    assert config.output_directory.exists(), "Output directory should exist"
    # Log directory lives under config.logging.log_file_dir
    assert config.logging.log_file_dir.exists(), "Log directory should exist"
    assert config.file_encoding == "utf-8", "File encoding should be UTF-8"
    
    print("✓ Configuration verified")
    print(f"  - Output directory: {config.output_directory}")
    print(f"  - Log directory: {config.logging.log_file_dir}")
    print(f"  - File encoding: {config.file_encoding}")


def main():
    """Run all GUI verification tests."""
    print("=" * 70)
    print("TEXT MERGE GUI - VERIFICATION TEST SUITE")
    print("=" * 70)
    
    try:
        test_theme_constants()
        test_components_instantiation()
        test_font_manager_integration()
        test_config_loading()
        test_gui_initialization()
        
        print("\n" + "=" * 70)
        print("✅ ALL GUI VERIFICATION TESTS PASSED")
        print("=" * 70)
        print("\nGUI is ready for use!")
        print("  → Run: python gui_launcher.py")
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
