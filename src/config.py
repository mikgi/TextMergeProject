"""
Configuration module for the Text Merge Application.
Handles all application settings and logging configuration.
"""

import logging
from pathlib import Path
from dataclasses import dataclass


@dataclass
class LogConfig:
    """Logging configuration settings."""

    level: str = "INFO"
    format_string: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    log_file_dir: Path = Path("logs")
    log_file_name: str = "text_merger.log"

    def __post_init__(self):
        """Ensure log directory exists."""
        self.log_file_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class Config:
    """Main application configuration."""

    # File encoding (UTF-8 for Thai language support)
    file_encoding: str = "utf-8"

    # Output directory
    output_directory: Path = Path("output")

    # Sample input directory
    sample_input_directory: Path = Path("sample_input")

    # File extensions to process
    file_extensions: list[str] = None
    
    # Logging configuration
    logging: LogConfig = None

    def __post_init__(self):
        """Initialize defaults and validate configuration."""
        if self.file_extensions is None:
            self.file_extensions = [".txt"]
        
        if self.logging is None:
            self.logging = LogConfig()

        # Create output directory if it doesn't exist
        self.output_directory.mkdir(parents=True, exist_ok=True)

    def get_log_file_path(self) -> Path:
        """
        Get the full path to the log file.

        Returns:
            Path: Full path to log file
        """
        return self.logging.log_file_dir / self.logging.log_file_name


# Create default config instance
DEFAULT_CONFIG = Config()
