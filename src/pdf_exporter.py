"""
PDF exporter module for exporting merged text to PDF format.
Supports UTF-8 Thai language using ReportLab for PDF generation.
Includes TTF font registration for proper Thai character rendering.
"""

import logging
from pathlib import Path

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER

from src.config import Config
from src.font_manager import FontManager, create_thai_font_manager


class PdfExporter:
    """Handles exporting content to PDF format with Thai language support."""

    # Default page size and margins
    PAGE_SIZE = A4
    TOP_MARGIN = 0.5 * inch
    BOTTOM_MARGIN = 0.5 * inch
    LEFT_MARGIN = 0.75 * inch
    RIGHT_MARGIN = 0.75 * inch

    def __init__(self, config: Config, fonts_directory: Path = None):
        """
        Initialize the PDF exporter with font management.

        Args:
            config (Config): Application configuration
            fonts_directory (Path): Optional path to custom fonts directory.
                                   Defaults to ./fonts
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize font manager for Thai font support
        self.font_manager = create_thai_font_manager(
            fonts_dir=fonts_directory or Path("fonts"),
            register_all=True
        )

        # Get best available Thai font
        self.thai_font = self.font_manager.get_thai_font()
        self.logger.debug(f"Using Thai font: {self.thai_font}")

    def export(self, content: str, output_path: Path) -> bool:
        """
        Export content to PDF file.

        Args:
            content (str): Text content to export
            output_path (Path): Path where PDF file will be saved

        Returns:
            bool: True if export successful, False otherwise

        Raises:
            IOError: If unable to write file
        """
        try:
            self.logger.debug(f"Creating PDF document...")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=self.PAGE_SIZE,
                topMargin=self.TOP_MARGIN,
                bottomMargin=self.BOTTOM_MARGIN,
                leftMargin=self.LEFT_MARGIN,
                rightMargin=self.RIGHT_MARGIN,
            )

            # Create styles with Thai font support
            styles = getSampleStyleSheet()

            # Determine font names - use Thai font for body, keep Helvetica for title
            title_font = "Helvetica-Bold"
            body_font = self.thai_font
            separator_font = "Helvetica-Oblique"

            # Title style
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading1"],
                fontSize=24,
                textColor="#000000",
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName=title_font,
            )

            # Body text style with Thai font support
            body_style = ParagraphStyle(
                "CustomBody",
                parent=styles["BodyText"],
                fontSize=11,
                leading=16,
                spaceAfter=8,
                alignment=TA_LEFT,
                fontName=body_font,
            )

            # Separator style
            separator_style = ParagraphStyle(
                "Separator",
                parent=styles["Normal"],
                fontSize=9,
                textColor="#666666",
                spaceAfter=6,
                alignment=TA_LEFT,
                fontName=separator_font,
            )

            # Build story (PDF content elements) with Thai text support
            story = []

            # Add title
            story.append(Paragraph("Merged Text Document", title_style))
            story.append(Spacer(1, 0.2 * inch))

            # Parse content into paragraphs and add to story
            lines = content.split("\n")
            line_count = 0

            for idx, line in enumerate(lines):
                # Skip very long separator lines but keep as visual breaks
                if line.startswith("=") and len(line) > 50:
                    story.append(Spacer(1, 0.1 * inch))

                    # Extract source file name if present
                    if idx + 1 < len(lines) and lines[idx + 1].startswith("Source:"):
                        source_text = lines[idx + 1]
                        story.append(Paragraph(f"<i>{source_text}</i>", separator_style))
                else:
                    # Add regular text paragraphs with Thai support
                    if line.strip():  # Skip empty lines
                        try:
                            # Use Thai font style for better character rendering
                            story.append(Paragraph(line, body_style))
                            self.logger.debug(f"Added line with {body_font} font")

                        except Exception as e:
                            self.logger.warning(
                                f"Error formatting line with Thai font, retrying: {str(e)}"
                            )
                            # Fallback: try with Helvetica if Thai font fails
                            try:
                                fallback_style = ParagraphStyle(
                                    "FallbackBody",
                                    parent=body_style,
                                    fontName="Helvetica",
                                )
                                story.append(Paragraph(line, fallback_style))
                                self.logger.debug("Fallback to Helvetica successful")
                            except Exception as fallback_e:
                                self.logger.error(
                                    f"Failed to render line even with fallback: {str(fallback_e)}"
                                )
                                # Last resort: add as plain text
                                story.append(Spacer(1, 6))

                line_count += 1

                # Add page break every 50 lines to prevent overly long pages
                if line_count > 0 and line_count % 50 == 0:
                    story.append(PageBreak())

            # Build PDF
            doc.build(story)

            self.logger.info(f"PDF file saved successfully: {output_path}")
            return True

        except IOError as e:
            self.logger.error(f"IO error writing PDF file: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error exporting to PDF: {str(e)}", exc_info=True
            )
            raise
