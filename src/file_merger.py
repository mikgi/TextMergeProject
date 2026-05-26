"""
File merger module for combining multiple text files.
Supports UTF-8 encoding including Thai language and other multi-byte characters.
"""

import logging
import re
from pathlib import Path
from typing import Optional

from src.config import Config


class FileMerger:
    """Handles merging of multiple text files with proper encoding support."""

    def __init__(self, config: Config):
        """
        Initialize the file merger.

        Args:
            config (Config): Application configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _natural_sort_key(file_path: Path) -> tuple:
        """
        Build a natural sort key that keeps numeric segments numeric.
        Works for English and Thai file names (e.g. บทที่ 2 < บทที่ 10).
        """
        name = file_path.stem.casefold()
        parts = re.split(r"(\d+)", name)
        key = []
        for part in parts:
            if part.isdigit():
                key.append((0, int(part), len(part)))
            else:
                key.append((1, part))
        return tuple(key)

    def merge_files(
        self,
        folder_path: Path,
        sort_order: str = "name"
    ) -> Optional[str]:
        """
        Merge all text files from a folder into a single string.

        Args:
            folder_path (Path): Path to folder containing .txt files
            sort_order (str): Sorting order - 'name' or 'date'

        Returns:
            Optional[str]: Merged content or None if no files found
        """

        if sort_order not in ["name", "date"]:
            raise ValueError(
                f"Invalid sort_order: {sort_order}"
            )

        try:

            text_files = self._get_text_files(
                folder_path,
                sort_order
            )

            if not text_files:

                self.logger.warning(
                    f"No text files found in {folder_path}"
                )

                return None

            self.logger.info(
                f"Found {len(text_files)} text file(s)"
            )

            merged_content = self._merge_file_contents(
                text_files
            )

            return merged_content

        except Exception as e:

            self.logger.error(
                f"Error merging files: {str(e)}",
                exc_info=True
            )

            raise

    def _get_text_files(
        self,
        folder_path: Path,
        sort_order: str
    ) -> list[Path]:
        """
        Get all text files from folder.
        """

        text_files = []

        for extension in self.config.file_extensions:

            text_files.extend(
                folder_path.glob(f"*{extension}")
            )

        # Remove duplicates
        text_files = list(set(text_files))

        # Sort files
        if sort_order == "name":

            text_files.sort(
                key=self._natural_sort_key
            )

        elif sort_order == "date":

            text_files.sort(
                key=lambda x: x.stat().st_mtime
            )

        return text_files

    def _merge_file_contents(
        self,
        file_paths: list[Path]
    ) -> str:
        """
        Merge multiple text files into one string.
        """

        merged_parts = []

        for file_path in file_paths:

            try:

                self.logger.debug(
                    f"Reading file: {file_path}"
                )

                # Read UTF-8 text
                content = file_path.read_text(
                    encoding=self.config.file_encoding
                )

                # =====================================
                # FILE HEADER
                # =====================================

                merged_parts.append("\n\n")

                merged_parts.append(
                    f"#FILE: {file_path.stem}\n"
                )

                merged_parts.append(
                    "-" * 60 + "\n\n"
                )

                # =====================================
                # FILE CONTENT
                # =====================================

                merged_parts.append(
                    content.strip()
                )

                # =====================================
                # SPACING BETWEEN FILES
                # =====================================

                merged_parts.append(
                    "\n\n\n"
                )

            except UnicodeDecodeError as e:

                self.logger.error(
                    f"Unicode decode error reading {file_path}: {str(e)}"
                )

                raise

            except IOError as e:

                self.logger.error(
                    f"IO error reading {file_path}: {str(e)}"
                )

                raise

            except Exception as e:

                self.logger.error(
                    f"Unexpected error reading {file_path}: {str(e)}"
                )

                raise

        return "\n".join(merged_parts)
