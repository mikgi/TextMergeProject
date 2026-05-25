"""
Utility functions for the Text Merge Application.
Includes logging setup, path validation, and common helpers.
"""

import logging
import sys
from pathlib import Path

from src.config import LogConfig


def setup_logging(log_config: LogConfig) -> logging.Logger:
    """
    Configure application-wide logging.

    Args:
        log_config (LogConfig): Logging configuration object

    Returns:
        logging.Logger: Configured root logger

    Raises:
        ValueError: If log level is invalid
    """
    try:
        # Validate log level
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if log_config.level not in valid_levels:
            raise ValueError(
                f"Invalid log level: {log_config.level}. Valid levels: {valid_levels}"
            )

        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_config.level))

        # Console handler (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_config.level))

        # File handler
        log_file_path = (
            log_config.log_file_dir / log_config.log_file_name
        )
        file_handler = logging.FileHandler(
            log_file_path, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)  # Always log debug to file

        # Formatter
        formatter = logging.Formatter(
            log_config.format_string,
            datefmt=log_config.date_format,
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to root logger
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

        root_logger.info(f"Logging initialized - Level: {log_config.level}")
        root_logger.info(f"Log file: {log_file_path}")

        return root_logger

    except Exception as e:
        print(f"Error setting up logging: {str(e)}", file=sys.stderr)
        raise


def validate_folder_exists(folder_path: Path) -> bool:
    """
    Validate that a folder exists and is accessible.

    Args:
        folder_path (Path): Path to validate

    Returns:
        bool: True if folder exists and is readable, False otherwise
    """
    try:
        if not folder_path.exists():
            return False

        if not folder_path.is_dir():
            return False

        # Check if readable
        if not folder_path.iterdir():
            # Folder is empty but accessible
            pass

        return True

    except PermissionError:
        return False
    except Exception:
        return False


def get_file_size_mb(file_path: Path) -> float:
    """
    Get file size in megabytes.

    Args:
        file_path (Path): Path to file

    Returns:
        float: File size in MB
    """
    if not file_path.exists():
        return 0.0

    return file_path.stat().st_size / (1024 * 1024)


def ensure_output_directory(output_dir: Path) -> bool:
    """
    Ensure output directory exists and is writable.

    Args:
        output_dir (Path): Path to output directory

    Returns:
        bool: True if directory exists/created and is writable, False otherwise
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Test write access
        test_file = output_dir / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        
        return True

    except Exception:
        return False
