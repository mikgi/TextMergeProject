"""
Font management module for PDF export.
Handles TTF font registration and loading for proper Thai language support.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Tuple

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors


class FontManager:
    """Manages font registration and loading for ReportLab PDFs."""

    # Common font names for different languages
    THAI_FONTS = {
        "THSarabunNew": ["THSarabunNew.ttf", "THSarabun New.ttf"],
        "NotoSansThai": ["NotoSansThai-Regular.ttf", "NotoSansThai_Regular.ttf"],
        "NotoSerifThai": ["NotoSerifThai-Regular.ttf", "NotoSerifThai_Regular.ttf"],
    }

    FALLBACK_FONTS = {
        "Helvetica": None,  # System font, no TTF needed
        "Times": None,  # System font
        "Courier": None,  # System font
    }

    def __init__(self, fonts_directory: Path = None):
        """
        Initialize font manager.

        Args:
            fonts_directory (Path): Path to directory containing TTF font files.
                                   Defaults to ./fonts in project root.
        """
        self.logger = logging.getLogger(__name__)
        self.fonts_directory = fonts_directory or Path("fonts")
        self.registered_fonts: Dict[str, str] = {}
        self.available_fonts: Dict[str, Tuple[str, Path]] = {}

        # Discover available fonts on initialization
        self._discover_fonts()

    def _discover_fonts(self) -> None:
        """
        Discover all available TTF fonts in the fonts directory.

        Updates self.available_fonts with discovered fonts.
        """
        if not self.fonts_directory.exists():
            self.logger.debug(f"Fonts directory not found: {self.fonts_directory}")
            return

        try:
            ttf_files = list(self.fonts_directory.glob("*.ttf"))
            self.logger.debug(f"Found {len(ttf_files)} TTF files in {self.fonts_directory}")

            for font_file in ttf_files:
                # Extract font name from filename (without extension)
                font_name = font_file.stem
                self.available_fonts[font_name] = ("ttf", font_file)
                self.logger.debug(f"Available font: {font_name} ({font_file.name})")

        except Exception as e:
            self.logger.warning(f"Error discovering fonts: {str(e)}")

    def register_font(
        self, font_name: str, font_file: Optional[Path] = None
    ) -> bool:
        """
        Register a TTF font with ReportLab.

        Args:
            font_name (str): Name to register the font as
            font_file (Path): Optional explicit path to TTF file.
                            If not provided, searches available fonts.

        Returns:
            bool: True if font registered successfully, False otherwise
        """
        try:
            # Check if already registered
            if font_name in self.registered_fonts:
                self.logger.debug(f"Font already registered: {font_name}")
                return True

            # If no explicit file, search available fonts
            if font_file is None:
                if font_name not in self.available_fonts:
                    self.logger.warning(f"Font not found: {font_name}")
                    return False
                _, font_file = self.available_fonts[font_name]

            # Verify file exists
            if not font_file.exists():
                self.logger.error(f"Font file not found: {font_file}")
                return False

            # Register with ReportLab
            self.logger.debug(f"Registering font: {font_name} from {font_file}")
            ttfont = TTFont(font_name, str(font_file))
            pdfmetrics.registerFont(ttfont)

            self.registered_fonts[font_name] = str(font_file)
            self.logger.info(f"Font registered successfully: {font_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error registering font {font_name}: {str(e)}")
            return False

    def get_thai_font(self) -> str:
        """
        Get best available Thai font, with fallback logic.

        Returns:
            str: Registered font name for Thai text, or fallback font

        Priority order:
            1. THSarabunNew (if available)
            2. NotoSansThai (if available)
            3. NotoSerifThai (if available)
            4. Helvetica (fallback)
        """
        # Try to register Thai fonts in priority order
        for font_name, filename_variants in self.THAI_FONTS.items():
            # Check if already registered
            if font_name in self.registered_fonts:
                return font_name

            # Try to find and register the font
            for variant in filename_variants:
                font_path = self.fonts_directory / variant
                if font_path.exists():
                    if self.register_font(font_name, font_path):
                        return font_name

        # Fallback to system font
        self.logger.warning(
            "No Thai fonts found in fonts directory. Using Helvetica fallback."
        )
        return "Helvetica"

    def get_font(self, font_preference: str = "thai") -> str:
        """
        Get a registered or system font by preference.

        Args:
            font_preference (str): 'thai' for Thai fonts, 'serif', 'mono', or specific name

        Returns:
            str: Available font name, with fallback to Helvetica
        """
        if font_preference.lower() == "thai":
            return self.get_thai_font()
        elif font_preference.lower() == "serif":
            return "Times" if "NotoSerifThai" not in self.registered_fonts else "NotoSerifThai"
        elif font_preference.lower() == "mono":
            return "Courier"
        else:
            # Try to use specific font preference
            if font_preference in self.registered_fonts:
                return font_preference
            return "Helvetica"

    def register_all_available_fonts(self) -> int:
        """
        Register all discovered fonts.

        Returns:
            int: Number of fonts successfully registered
        """
        count = 0
        for font_name in self.available_fonts.keys():
            if self.register_font(font_name):
                count += 1

        self.logger.info(f"Registered {count} fonts")
        return count

    def list_registered_fonts(self) -> Dict[str, str]:
        """
        Get list of registered fonts.

        Returns:
            Dict[str, str]: Dictionary of font name -> file path
        """
        return self.registered_fonts.copy()

    def list_available_fonts(self) -> Dict[str, str]:
        """
        Get list of available fonts in fonts directory.

        Returns:
            Dict[str, str]: Dictionary of font name -> file path
        """
        return {
            name: str(path) for name, (_, path) in self.available_fonts.items()
        }


def create_thai_font_manager(
    fonts_dir: Path = None,
    register_all: bool = True
) -> FontManager:
    """
    Factory function to create and initialize a font manager.

    Args:
        fonts_dir (Path): Custom fonts directory path
        register_all (bool): Whether to register all available fonts

    Returns:
        FontManager: Initialized font manager instance
    """
    manager = FontManager(fonts_directory=fonts_dir)

    if register_all:
        manager.register_all_available_fonts()

    return manager
