"""
PDF exporter module for exporting merged text to PDF format.
Supports UTF-8 Thai language using ReportLab for PDF generation.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

from src.config import Config
from src.font_manager import create_thai_font_manager
from src.text_cleaner import clean_text_line


class PdfExporter:
    """Handles exporting content to PDF format with Thai language support."""

    PAGE_SIZE = A4
    TOP_MARGIN = 0.5 * inch
    BOTTOM_MARGIN = 0.5 * inch
    LEFT_MARGIN = 0.75 * inch
    RIGHT_MARGIN = 0.75 * inch

    def __init__(self, config: Config, fonts_directory: Path = None):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.font_manager = create_thai_font_manager(
            fonts_dir=fonts_directory or Path("fonts"),
            register_all=True,
        )
        self.thai_font = self.font_manager.get_thai_font()
        self.logger.debug(f"Using Thai font: {self.thai_font}")

    def _resolve_font(self, font_name: Optional[str]) -> str:
        if font_name and self.font_manager.register_font(font_name):
            return font_name
        if font_name in {"Helvetica", "Times", "Courier"}:
            return font_name
        return self.thai_font

    @staticmethod
    def _normalize_pdf_symbols(text: str) -> str:
        # Some Thai fonts used in PDF exports do not contain CJK corner brackets.
        return (
            text.replace("『", "[")
            .replace("』", "]")
            .replace("「", "[")
            .replace("」", "]")
        )

    @staticmethod
    def _is_same_heading(a: str, b: str) -> bool:
        left = a.strip()
        right = b.strip()
        return left == right or left.startswith(right) or right.startswith(left)

    def export(
        self,
        content: str,
        output_path: Path,
        font_name: Optional[str] = None,
    ) -> Tuple[bool, Optional[Path]]:
        """
        Export content to PDF file.
        """
        try:
            self.logger.debug("Creating PDF document...")
            output_path.parent.mkdir(parents=True, exist_ok=True)

            class OutlineDocTemplate(SimpleDocTemplate):
                def afterFlowable(self, flowable):
                    title = getattr(flowable, "_outline_title", None)
                    key = getattr(flowable, "_outline_key", None)
                    if title and key:
                        self.canv.bookmarkPage(key)
                        self.canv.addOutlineEntry(title, key, level=0, closed=False)

            doc = OutlineDocTemplate(
                str(output_path),
                pagesize=self.PAGE_SIZE,
                topMargin=self.TOP_MARGIN,
                bottomMargin=self.BOTTOM_MARGIN,
                leftMargin=self.LEFT_MARGIN,
                rightMargin=self.RIGHT_MARGIN,
            )

            styles = getSampleStyleSheet()
            body_font = self._resolve_font(font_name)

            heading_style = ParagraphStyle(
                "ChapterHeading",
                parent=styles["Heading1"],
                fontName=body_font,
                fontSize=22,
                leading=28,
                alignment=TA_LEFT,
                spaceBefore=18,
                spaceAfter=10,
            )
            body_style = ParagraphStyle(
                "BodyTextThai",
                parent=styles["BodyText"],
                fontName=body_font,
                fontSize=20,
                leading=30,
                alignment=TA_LEFT,
                firstLineIndent=20,
                spaceAfter=6,
            )

            story = []
            lines = content.split("\n")
            current_file_title = None
            heading_counter = 1

            current_file_title = None
            heading_counter = 1
            for raw in lines:
                text = self._normalize_pdf_symbols(clean_text_line(raw))
                if not text:
                    continue

                if text.startswith("#FILE:"):
                    current_file_title = text.replace("#FILE:", "").strip()
                    continue

                if text.startswith("---"):
                    continue

                # Same intent as DOCX export: chapter-like heading triggers page break + heading style.
                if text.startswith("บทที่") or text.casefold().startswith("chapter"):
                    if current_file_title and self._is_same_heading(text, current_file_title):
                        current_file_title = None
                    if story:
                        story.append(PageBreak())
                    anchor = f"ch_{heading_counter}"
                    heading_counter += 1
                    p = Paragraph(text, heading_style)
                    p._outline_title = text
                    p._outline_key = anchor
                    story.append(p)
                    continue

                if current_file_title:
                    if story:
                        story.append(PageBreak())
                    anchor = f"ch_{heading_counter}"
                    heading_counter += 1
                    p = Paragraph(current_file_title, heading_style)
                    p._outline_title = current_file_title
                    p._outline_key = anchor
                    story.append(p)
                    current_file_title = None

                story.append(Paragraph(text, body_style))
                story.append(Spacer(1, 2))

            doc.build(story)
            self.logger.info(f"PDF file saved successfully: {output_path}")
            return True, output_path

        except IOError as e:
            self.logger.error(f"IO error writing PDF file: {str(e)}", exc_info=True)
            return False, None
        except Exception as e:
            self.logger.error(f"Unexpected error exporting to PDF: {str(e)}", exc_info=True)
            return False, None
