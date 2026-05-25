"""
Headless smoke test for TextMergeProject.
Performs merging of sample_input and exports to DOCX and PDF.
Does not launch GUI.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import Config
from src.file_merger import FileMerger
from src.docx_exporter import DocxExporter
from src.pdf_exporter import PdfExporter
from src.font_manager import create_thai_font_manager


def run():
    base = Path(__file__).resolve().parents[1]
    sample = base / "sample_input"
    out = base / "output"
    out.mkdir(parents=True, exist_ok=True)

    config = Config()
    fm = create_thai_font_manager(fonts_dir=base / "fonts", register_all=True)
    print("Available fonts:", fm.list_available_fonts())
    print("Registered fonts:", fm.list_registered_fonts())
    thai_font = fm.get_thai_font()
    print("Selected Thai font:", thai_font)

    merger = FileMerger(config)
    content = merger.merge_files(sample)
    if not content:
        print("No content to merge")
        return 2

    docx_path = out / "smoke_test_merged.docx"
    pdf_path = out / "smoke_test_merged.pdf"

    docx_exporter = DocxExporter(config)
    docx_exporter.export(content, docx_path)
    print("DOCX exported:", docx_path)

    pdf_exporter = PdfExporter(config)
    pdf_exporter.export(content, pdf_path)
    print("PDF exported:", pdf_path)

    # verify files exist
    assert docx_path.exists(), "DOCX output missing"
    assert pdf_path.exists(), "PDF output missing"

    print("Smoke test passed")
    return 0


if __name__ == '__main__':
    sys.exit(run())
