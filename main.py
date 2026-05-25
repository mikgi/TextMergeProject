#!/usr/bin/env python3
"""
Text File Merger Application
Production-ready application to merge multiple text files and export to DOCX/PDF.
Supports UTF-8 Thai language and other multi-byte character encodings.

Usage:
    python main.py <input_folder> <output_name> [--format docx|pdf|both] [--sort-order]
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Import local modules
from src.config import Config, LogConfig
from src.file_merger import FileMerger
from src.docx_exporter import DocxExporter
from src.pdf_exporter import PdfExporter
from src.utils import validate_folder_exists, setup_logging


class TextMergeApplication:
    """Main application class orchestrating file merging and export operations."""

    def __init__(self, config: Config):
        """
        Initialize the application with configuration.

        Args:
            config (Config): Application configuration object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.file_merger = FileMerger(config)

    def merge_and_export(
        self,
        input_folder: Path,
        output_name: str,
        export_formats: list[str],
        sort_order: str = "name",
    ) -> bool:
        """
        Merge text files and export to specified formats.

        Args:
            input_folder (Path): Path to folder containing .txt files
            output_name (str): Output file name (without extension)
            export_formats (list[str]): Export formats ['docx', 'pdf', or both]
            sort_order (str): File sorting order ('name' or 'date')

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.info(f"Starting merge operation for folder: {input_folder}")
            self.logger.info(f"Export formats: {', '.join(export_formats)}")

            # Validate input folder
            if not validate_folder_exists(input_folder):
                self.logger.error(f"Input folder does not exist: {input_folder}")
                return False

            # Merge files
            self.logger.info("Merging text files...")
            merged_content = self.file_merger.merge_files(
                input_folder, sort_order=sort_order
            )

            if not merged_content:
                self.logger.warning("No text files found to merge")
                return False

            self.logger.info(
                f"Successfully merged files. Total content length: {len(merged_content)} characters"
            )

            # Export to specified formats
            success = True
            output_path = self.config.output_directory

            for export_format in export_formats:
                try:
                    if export_format.lower() == "docx":
                        self.logger.info(f"Exporting to DOCX format...")
                        exporter = DocxExporter(self.config)
                        output_file = output_path / f"{output_name}.docx"
                        exporter.export(merged_content, output_file)
                        self.logger.info(f"DOCX export successful: {output_file}")

                    elif export_format.lower() == "pdf":
                        self.logger.info(f"Exporting to PDF format...")
                        exporter = PdfExporter(self.config)
                        output_file = output_path / f"{output_name}.pdf"
                        exporter.export(merged_content, output_file)
                        self.logger.info(f"PDF export successful: {output_file}")

                except Exception as e:
                    self.logger.error(
                        f"Failed to export to {export_format.upper()}: {str(e)}"
                    )
                    success = False

            if success:
                self.logger.info("All export operations completed successfully")
            else:
                self.logger.warning("Some export operations failed")

            return success

        except Exception as e:
            self.logger.error(f"Unexpected error during merge operation: {str(e)}", exc_info=True)
            return False


def main():
    """Main entry point for the application."""

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Merge text files and export to DOCX/PDF with Thai language support"
    )
    parser.add_argument(
        "input_folder", type=str, help="Path to folder containing .txt files"
    )
    parser.add_argument(
        "output_name", type=str, help="Output file name (without extension)"
    )
    parser.add_argument(
        "--format",
        type=str,
        default="both",
        choices=["docx", "pdf", "both"],
        help="Export format (default: both)",
    )
    parser.add_argument(
        "--sort-order",
        type=str,
        default="name",
        choices=["name", "date"],
        help="File sorting order (default: name)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: INFO)",
    )

    args = parser.parse_args()

    # Initialize configuration
    config = Config()
    
    # Setup logging
    log_config = LogConfig(level=args.log_level)
    setup_logging(log_config)
    
    logger = logging.getLogger(__name__)

    try:
        # Determine export formats
        export_formats = (
            ["docx", "pdf"]
            if args.format == "both"
            else [args.format]
        )

        # Initialize and run application
        app = TextMergeApplication(config)
        input_path = Path(args.input_folder)
        
        success = app.merge_and_export(
            input_folder=input_path,
            output_name=args.output_name,
            export_formats=export_formats,
            sort_order=args.sort_order,
        )

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"Critical error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()