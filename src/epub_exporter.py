"""
EPUB exporter module for exporting merged text to EPUB format.
Uses pure-Python stdlib (zip/xml) for broad compatibility.
"""

import html
import logging
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

from src.config import Config
from src.text_cleaner import clean_text_line


class EpubExporter:
    """Handles exporting content to EPUB format."""

    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _is_same_heading(a: str, b: str) -> bool:
        left = a.strip()
        right = b.strip()
        return left == right or left.startswith(right) or right.startswith(left)

    def _content_html(self, content: str, book_title: str) -> tuple[str, list[tuple[str, str]]]:
        chunks: list[str] = []
        toc: list[tuple[str, str]] = []
        current_file_title = None
        heading_index = 1
        for raw in content.split("\n"):
            text = clean_text_line(raw)
            if not text:
                continue
            if text.startswith("#FILE:"):
                current_file_title = text.replace("#FILE:", "").strip()
                continue
            if text.startswith("---"):
                continue
            if text.startswith("บทที่") or text.casefold().startswith("chapter"):
                if current_file_title and self._is_same_heading(text, current_file_title):
                    current_file_title = None
                anchor = f"h{heading_index}"
                heading_index += 1
                toc.append((anchor, text))
                chunks.append(f"<h2 id=\"{anchor}\">{html.escape(text)}</h2>")
                continue
            if current_file_title:
                anchor = f"h{heading_index}"
                heading_index += 1
                toc.append((anchor, current_file_title))
                chunks.append(f"<h2 id=\"{anchor}\">{html.escape(current_file_title)}</h2>")
                current_file_title = None
            chunks.append(f"<p>{html.escape(text)}</p>")

        body = "\n".join(chunks)
        xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="th">
<head>
  <title>{html.escape(book_title)}</title>
  <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
  {body}
</body>
</html>
"""
        return xhtml, toc

    def export(self, content: str, output_path: Path) -> Tuple[bool, Optional[Path]]:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            book_id = str(uuid.uuid4())
            modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            book_title = output_path.stem

            container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""
            content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{book_id}</dc:identifier>
    <dc:title>{html.escape(book_title)}</dc:title>
    <dc:language>th</dc:language>
    <meta property="dcterms:modified">{modified}</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="text" href="text.xhtml" media-type="application/xhtml+xml"/>
    <item id="css" href="styles.css" media-type="text/css"/>
  </manifest>
  <spine>
    <itemref idref="text"/>
  </spine>
</package>
"""
            text_xhtml, toc_entries = self._content_html(content, book_title)
            if toc_entries:
                toc_items = "\n".join(
                    [f'      <li><a href="text.xhtml#{anchor}">{html.escape(title)}</a></li>' for anchor, title in toc_entries]
                )
            else:
                toc_items = f'      <li><a href="text.xhtml">{html.escape(book_title)}</a></li>'

            nav_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="th">
<head><title>Table of Contents</title></head>
<body>
  <nav epub:type="toc" xmlns:epub="http://www.idpf.org/2007/ops">
    <ol>
{toc_items}
    </ol>
  </nav>
</body>
</html>
"""
            css = """
body { font-family: "TH Sarabun New", "Sarabun", serif; line-height: 1.6; }
h1 { font-size: 1.6em; margin: 0 0 1em 0; }
h2 { font-size: 1.2em; margin: 1.2em 0 .5em 0; }
p { text-indent: 1.4em; margin: .35em 0; }
"""
            with zipfile.ZipFile(output_path, "w") as zf:
                zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
                zf.writestr("META-INF/container.xml", container_xml)
                zf.writestr("OEBPS/content.opf", content_opf)
                zf.writestr("OEBPS/nav.xhtml", nav_xhtml)
                zf.writestr("OEBPS/styles.css", css)
                zf.writestr("OEBPS/text.xhtml", text_xhtml)

            self.logger.info(f"EPUB file saved successfully: {output_path}")
            return True, output_path
        except Exception as e:
            self.logger.error(f"Unexpected error exporting to EPUB: {str(e)}", exc_info=True)
            return False, None
