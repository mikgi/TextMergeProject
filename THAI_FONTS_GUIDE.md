# Thai Font Setup & PDF Rendering Guide

## Overview

The Text Merge Application now includes advanced Thai language font support for PDF generation using ReportLab with TTF font embedding.

## Architecture

### Font Management System

```
FontManager (src/font_manager.py)
├── Font Discovery (./fonts directory)
├── Font Registration (ReportLab)
├── Priority Selection (Thai fonts)
└── Fallback Handling (System fonts)

↓

PdfExporter (src/pdf_exporter.py)
├── Initializes FontManager
├── Gets best Thai font
├── Creates styled paragraphs
└── Generates PDF with embedded fonts
```

## Quick Setup

### 1. Download Thai Font

**Option A: TH Sarabun New (Recommended)**

```bash
# Visit: https://fonts.google.com/specimen/Sarabun
# Download and extract "THSarabunNew.ttf"
```

**Option B: Noto Sans Thai**

```bash
# Visit: https://fonts.google.com/specimen/Noto+Sans+Thai
# Download "NotoSansThai-Regular.ttf"
```

### 2. Place in Fonts Directory

```bash
# Windows
copy THSarabunNew.ttf D:\Works\TextMergeProject\fonts\

# macOS/Linux
cp THSarabunNew.ttf /path/to/TextMergeProject/fonts/
```

### 3. Verify Installation

```bash
# Check fonts are detected
python -c "from pathlib import Path; print(list(Path('fonts').glob('*.ttf')))"
```

### 4. Run Application

```bash
python main.py ./sample_input thai_output --format pdf --log-level INFO
```

## Font Priority System

The application uses this selection logic:

```python
1. Check if THSarabunNew.ttf exists in ./fonts/
   └─ YES: Register and use THSarabunNew
   └─ NO:  Continue to step 2

2. Check if NotoSansThai-Regular.ttf exists in ./fonts/
   └─ YES: Register and use NotoSansThai
   └─ NO:  Continue to step 3

3. Check if NotoSerifThai-Regular.ttf exists in ./fonts/
   └─ YES: Register and use NotoSerifThai
   └─ NO:  Continue to step 4

4. Use Helvetica (System font - fallback)
   └─ Note: Helvetica has limited Thai support
```

## Font Details

| Font            | Format | License     | Notes                                   |
| --------------- | ------ | ----------- | --------------------------------------- |
| TH Sarabun New  | TTF    | OFL         | Best Thai support, serif style          |
| Noto Sans Thai  | TTF    | OFL         | Modern, sans-serif, excellent coverage  |
| Noto Serif Thai | TTF    | OFL         | Serif alternative, full Unicode support |
| Helvetica       | System | Proprietary | Fallback only, limited Thai support     |

## Implementation Details

### FontManager Class

Located in `src/font_manager.py`:

```python
class FontManager:
    """Manages font registration and loading for ReportLab PDFs."""

    Methods:
    - __init__()              # Initialize and discover fonts
    - register_font()         # Register TTF with ReportLab
    - get_thai_font()         # Get best Thai font with fallback
    - register_all_available_fonts()  # Register all discovered fonts
    - list_registered_fonts()  # Get registered fonts
    - list_available_fonts()   # Get available fonts in ./fonts
```

### PdfExporter Integration

Updated `PdfExporter.__init__()`:

```python
def __init__(self, config: Config, fonts_directory: Path = None):
    # Initialize font manager
    self.font_manager = create_thai_font_manager(
        fonts_dir=fonts_directory or Path("fonts"),
        register_all=True
    )

    # Get best available Thai font
    self.thai_font = self.font_manager.get_thai_font()
```

### PDF Generation Process

```
1. Initialize PdfExporter
   ├─ Create FontManager
   ├─ Discover fonts in ./fonts
   ├─ Register all TTF files
   └─ Select best Thai font

2. Create ParagraphStyles
   ├─ Title: Helvetica-Bold (ASCII)
   ├─ Body: Thai Font (Thai + English)
   └─ Separator: Helvetica-Oblique (ASCII)

3. Process Content
   ├─ Read merged text
   ├─ Create paragraphs
   ├─ Use Thai font for body text
   └─ Include fallback logic

4. Generate PDF
   ├─ Build story with styled paragraphs
   ├─ Embed selected Thai font
   ├─ Auto-paginate at 50 lines
   └─ Save to output file
```

## Debugging Thai Fonts

### Enable Debug Logging

```bash
python main.py ./sample_input test_output --log-level DEBUG
```

### Sample Debug Output

```
DEBUG - Found 1 TTF file(s) in ./fonts
DEBUG - Available font: THSarabunNew (THSarabunNew.ttf)
DEBUG - Registering font: THSarabunNew from fonts/THSarabunNew.ttf
INFO - Font registered successfully: THSarabunNew
DEBUG - Using Thai font: THSarabunNew
DEBUG - Creating PDF document...
DEBUG - Added line with THSarabunNew font
```

### Verify Font Registration

```python
# In Python REPL
from src.font_manager import create_thai_font_manager
from pathlib import Path

fm = create_thai_font_manager(fonts_dir=Path("fonts"), register_all=True)
print("Registered fonts:", fm.list_registered_fonts())
print("Available fonts:", fm.list_available_fonts())
print("Selected Thai font:", fm.get_thai_font())
```

## Troubleshooting

### Problem: "Font not found"

**Symptoms:**

```
WARNING - No Thai fonts found in fonts directory. Using Helvetica fallback.
```

**Solutions:**

1. Download Thai font from Google Fonts
2. Place `.ttf` file in `./fonts` directory
3. Ensure filename ends with `.ttf` (lowercase)
4. Run with `--log-level DEBUG` to verify detection

### Problem: Thai text appears as boxes/rectangles

**Cause:** Font file doesn't include Thai Unicode ranges

**Solutions:**

1. Try different font (Noto fonts have better coverage)
2. Verify font opens in system font viewer
3. Download from official source (not corrupted file)
4. Check font file size (typically > 500KB for Thai fonts)

### Problem: "ReportLab cannot read TTF file"

**Cause:** Font file format incompatible or corrupted

**Solutions:**

```bash
# Verify font format
file fonts/THSarabunNew.ttf  # Should show "TrueType font"

# Check file integrity
python -c "from reportlab.pdfbase.ttfonts import TTFont; TTFont('test', 'fonts/THSarabunNew.ttf')"

# Re-download font if corrupted
```

### Problem: PDF too large (font embedding)

**Note:** Embedded fonts increase PDF size

**Solutions:**

1. This is expected behavior (5-10MB PDF is normal with embedded fonts)
2. Use PDF compression (post-processing tool)
3. Split large documents into multiple PDFs

## Performance Impact

| Operation              | Time      | Size               |
| ---------------------- | --------- | ------------------ |
| Font discovery         | <100ms    | -                  |
| Font registration      | <200ms    | -                  |
| PDF generation (small) | 200-500ms | 2-5MB (with font)  |
| PDF generation (large) | 1-5s      | 5-20MB (with font) |

Font embedding adds ~3-8MB to PDF file size.

## Advanced Usage

### Custom Fonts Directory

```python
from src.pdf_exporter import PdfExporter
from pathlib import Path

# Use custom fonts location
exporter = PdfExporter(config, fonts_directory=Path("custom_fonts"))
exporter.export(content, output_path)
```

### Programmatic Font Management

```python
from src.font_manager import FontManager
from pathlib import Path

fm = FontManager(fonts_directory=Path("fonts"))

# Register specific font
fm.register_font("THSarabunNew", Path("fonts/THSarabunNew.ttf"))

# Get available fonts
available = fm.list_available_fonts()
print(f"Available fonts: {available}")

# Get registered fonts
registered = fm.list_registered_fonts()
print(f"Registered fonts: {registered}")

# Get best Thai font
thai_font = fm.get_thai_font()
print(f"Using font: {thai_font}")
```

### Adding New Fonts

To add support for additional languages:

1. Place TTF files in `./fonts` directory
2. They'll be automatically discovered
3. Reference in application code:

```python
# Get specific font
font = font_manager.get_font("NotoSansThai")

# List all available
all_fonts = font_manager.list_available_fonts()
```

## Dependencies

New dependency added to `requirements.txt`:

```
fonttools==4.46.0  # TTF font handling for ReportLab
```

This enables:

- TTF font loading
- Font metrics extraction
- Character mapping
- Unicode support

## References

### Font Resources

- Google Fonts Thai: https://fonts.google.com/?query=thai
- Noto Fonts Project: https://github.com/notofonts/noto-cjk
- Adobe Open Source Fonts: https://github.com/adobe-fonts

### Documentation

- ReportLab Docs: https://www.reportlab.com/docs/reportlab-userguide.pdf
- fonttools Docs: https://fonttools.readthedocs.io/
- Unicode Thai Block: https://unicode.org/charts/PDF/U0E00.pdf

## Best Practices

✅ **DO**

- Use Noto or Google Fonts (well-maintained)
- Place fonts in `./fonts` directory
- Check debug logs when troubleshooting
- Test with sample Thai text first
- Keep fonts organized by name

❌ **DON'T**

- Use fonts from untrusted sources
- Mix different encoding fonts
- Modify TTF files manually
- Assume system fonts are available
- Place fonts in random directories

## Conclusion

The improved Thai font system provides:

- ✅ Automatic font discovery and registration
- ✅ Smart fallback handling
- ✅ Seamless integration with PDF generation
- ✅ Support for multiple Thai fonts
- ✅ Full UTF-8 character support
- ✅ Debug logging for troubleshooting

---

**Last Updated:** 2026-05-25  
**Version:** 1.0.0
