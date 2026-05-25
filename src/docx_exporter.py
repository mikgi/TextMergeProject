"""
DOCX exporter module for exporting merged text to Word format.
Supports UTF-8 Thai language and styled document formatting.
"""

import logging
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

from src.config import Config


# =====================================
# DOCUMENT SETTINGS
# =====================================

DOCUMENT_TITLE = ""

DOCUMENT_FONT = "TH Sarabun New"

BODY_FONT_SIZE = 20

HEADING_FONT_SIZE = 22

TITLE_FONT_SIZE = 26


class DocxExporter:
    """Handles exporting content to DOCX format."""

    def __init__(self, config: Config):

        self.config = config
        self.logger = logging.getLogger(__name__)

    def export(
        self,
        content: str,
        output_path: Path
    ) -> bool:
        """
        Export content to DOCX file.
        """

        try:

            self.logger.debug(
                "Creating DOCX document..."
            )

            # =====================================
            # AUTO FILE NAME
            # =====================================

            chapter_numbers = re.findall(
                r"บทที่\s*(\d+)",
                content
            )

            if chapter_numbers:

                first_chapter = chapter_numbers[0]
                last_chapter = chapter_numbers[-1]

                new_filename = (
                    f"บทที่ {first_chapter} - "
                    f"บทที่ {last_chapter}.docx"
                )

                output_path = (
                    output_path.parent / new_filename
                )

            # =====================================
            # CREATE DOCUMENT
            # =====================================

            doc = Document()

            # =====================================
            # DEFAULT FONT
            # =====================================

            style = doc.styles["Normal"]

            font = style.font

            font.name = DOCUMENT_FONT
            font.size = Pt(BODY_FONT_SIZE)

            # Thai font rendering
            style._element.rPr.rFonts.set(
                qn("w:eastAsia"),
                DOCUMENT_FONT
            )

            # =====================================
            # DOCUMENT TITLE
            # =====================================

            if DOCUMENT_TITLE:

                title = doc.add_heading(
                    DOCUMENT_TITLE,
                    level=0
                )

                title.alignment = (
                    WD_PARAGRAPH_ALIGNMENT.CENTER
                )

                title_run = title.runs[0]

                title_run.font.name = DOCUMENT_FONT
                title_run.font.size = Pt(TITLE_FONT_SIZE)
                title_run.bold = True

                title_run._element.rPr.rFonts.set(
                    qn("w:eastAsia"),
                    DOCUMENT_FONT
                )

            # =====================================
            # CONTENT
            # =====================================

            lines = content.split("\n")

            current_file_title = None

            for line in lines:

                cleaned_text = line.strip()

                # Skip empty lines
                if not cleaned_text:
                    continue

                # =====================================
                # REMOVE SPAM TEXT
                # =====================================

                spam_keywords = [
                    "( yaaaaacha )",
                    "มังฮวาชื่อเดียวกัน",
                    "เพื่อเข้าลิงค์อ่านได้เลย หรือกดอ่านในหน้าโปรไฟล์ก็ได้",
                    "yakksha.com",
                    
                    "✦ สตรีมเมอร์หวนคืน55ชาติ ✦",
                    "<<< แปลชนต้นฉบับ 20 ตอนแล้ว มังฮวา 20 = นิยาย 21 เสิช",

                    "✦ จักรพรรดิทรายในโลกาวินาศ ✦",
                    "<<< แปลชนต้นฉบับ 20 ตอนแล้ว มังฮวา 20 = นิยาย 13 เสิช",
                    
                ]

                for keyword in spam_keywords:

                    cleaned_text = cleaned_text.replace(
                        keyword,
                        ""
                    )

                cleaned_text = cleaned_text.strip()

                # Skip if empty after cleaning
                if not cleaned_text:
                    continue

                # =====================================
                # FILE TITLE
                # =====================================

                if cleaned_text.startswith("#FILE:"):

                    file_title = cleaned_text.replace(
                        "#FILE:",
                        ""
                    ).strip()

                    current_file_title = file_title

                    continue

                # =====================================
                # IGNORE SEPARATOR
                # =====================================

                if cleaned_text.startswith("---"):
                    continue

                # =====================================
                # CHAPTER DETECTION
                # =====================================

                if cleaned_text.startswith("บทที่"):

                    # Add page break before new chapter
                    if doc.paragraphs:
                        doc.add_page_break()

                    # Prevent duplicate from filename
                    if current_file_title:

                        if cleaned_text.startswith(
                            current_file_title
                        ):

                            current_file_title = None

                    chapter = doc.add_heading(
                        cleaned_text,
                        level=1
                    )

                    run = chapter.runs[0]

                    run.font.name = DOCUMENT_FONT

                    run.font.size = Pt(
                        HEADING_FONT_SIZE
                    )

                    run.bold = True

                    # Thai rendering
                    run._element.rPr.rFonts.set(
                        qn("w:eastAsia"),
                        DOCUMENT_FONT
                    )

                    chapter.paragraph_format.space_before = Pt(24)
                    chapter.paragraph_format.space_after = Pt(12)

                    continue

                # =====================================
                # FALLBACK FILE TITLE
                # =====================================

                if current_file_title:

                    # Add page break before new file
                    if doc.paragraphs:
                        doc.add_page_break()

                    heading = doc.add_heading(
                        current_file_title,
                        level=1
                    )

                    run = heading.runs[0]

                    run.font.name = DOCUMENT_FONT

                    run.font.size = Pt(
                        HEADING_FONT_SIZE
                    )

                    run.bold = True

                    # Thai rendering
                    run._element.rPr.rFonts.set(
                        qn("w:eastAsia"),
                        DOCUMENT_FONT
                    )

                    heading.paragraph_format.space_before = Pt(24)
                    heading.paragraph_format.space_after = Pt(12)

                    current_file_title = None

                # =====================================
                # NORMAL PARAGRAPH
                # =====================================

                p = doc.add_paragraph()

                run = p.add_run(
                    cleaned_text
                )

                run.font.name = DOCUMENT_FONT

                run.font.size = Pt(
                    BODY_FONT_SIZE
                )

                # Thai rendering
                run._element.rPr.rFonts.set(
                    qn("w:eastAsia"),
                    DOCUMENT_FONT
                )

                # Paragraph spacing
                p.paragraph_format.space_after = Pt(6)

                # First line indent
                p.paragraph_format.first_line_indent = Pt(24)

            # =====================================
            # SAVE DOCUMENT
            # =====================================

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            doc.save(str(output_path))

            self.logger.info(
                f"DOCX file saved successfully: {output_path}"
            )

            return True

        except IOError as e:

            self.logger.error(
                f"IO error writing DOCX file: {str(e)}",
                exc_info=True
            )

            raise

        except Exception as e:

            self.logger.error(
                f"Unexpected error exporting DOCX: {str(e)}",
                exc_info=True
            )

            raise