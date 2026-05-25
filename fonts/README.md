# Thai Fonts Setup Guide

This directory is for storing TrueType Font (TTF) files to improve Thai language rendering in PDF output.

## Quick Start

1. Download a Thai-compatible font (see options below)
2. Place the `.ttf` file in this directory
3. Run the application - it will automatically detect and use the font

## Recommended Fonts

### TH Sarabun New (Recommended)

- **Language:** Thai
- **Style:** Serif
- **Download:**
  - Google Fonts: https://fonts.google.com/specimen/Sarabun
  - Download as `THSarabunNew.ttf`

### Noto Sans Thai

- **Language:** Thai
- **Style:** Sans-serif
- **Download:**
  - Google Fonts: https://fonts.google.com/specimen/Noto+Sans+Thai
  - File: `NotoSansThai-Regular.ttf`

### Noto Serif Thai

- **Language:** Thai
- **Style:** Serif
- **Download:**
  - Google Fonts: https://fonts.google.com/specimen/Noto+Serif+Thai
  - File: `NotoSerifThai-Regular.ttf`

## Installation Steps

### Windows

1. Go to https://fonts.google.com/specimen/Sarabun
2. Click "Download family"
3. Extract the zip file
4. Copy `THSarabunNew.ttf` to this directory
5. Done! (No system installation needed)

### macOS/Linux

```bash
# Download Sarabun font
wget https://fonts.google.com/download?family=Sarabun

# Extract
unzip Sarabun.zip

# Copy to project fonts directory
cp THSarabunNew.ttf /path/to/TextMergeProject/fonts/
```

## Font Priority Order

The application uses this priority when multiple fonts are available:

1. **THSarabunNew** - Most complete Thai support
2. **NotoSansThai** - Good Thai support, modern style
3. **NotoSerifThai** - Good Thai support, serif style
4. **Helvetica** - System fallback (basic Thai support)

## Verification

To verify fonts are detected:

```bash
# List all TTF files in this directory
ls -la *.ttf        # macOS/Linux
dir *.ttf           # Windows

# Or use Python
python -c "from pathlib import Path; print([f.name for f in Path('fonts').glob('*.ttf')])"
```

To verify fonts are loaded during application run:

```bash
# Run with debug logging
python main.py ./sample_input test_output --log-level DEBUG

# Look for messages:
# "Found X TTF file(s) in ./fonts"
# "Available font: THSarabunNew"
# "Font registered successfully: THSarabunNew"
# "Using Thai font: THSarabunNew"
```

## File Format Requirements

- **Format:** TrueType Font (TTF)
- **Encoding:** UTF-8 compatible
- **Filename:** Should match pattern `*.ttf` (lowercase extension)
- **Size:** Typically 500KB - 5MB

## Troubleshooting

### Font not detected

- Check file is in this directory (not in subdirectories)
- Ensure filename ends with `.ttf` (lowercase)
- Verify file is valid TTF format

### Thai characters still appear as boxes

- Font might not include Thai Unicode ranges
- Try different font (Noto fonts are more complete)
- Verify font opens in system font viewer

### "Permission denied" error

- On Windows: Ensure file isn't open in font viewer
- On macOS/Linux: Check file permissions (`chmod 644 *.ttf`)

## Font License Information

| Font            | License           | Source       |
| --------------- | ----------------- | ------------ |
| TH Sarabun New  | Open Font License | Google Fonts |
| Noto Sans Thai  | Open Font License | Google Fonts |
| Noto Serif Thai | Open Font License | Google Fonts |

All recommended fonts are open source and free to use.

## Additional Resources

- Google Fonts Thai Selection: https://fonts.google.com/metadata/icons?category=Serif&tag=Thailand
- Unicode Thai Character Set: https://unicode.org/charts/PDF/U0E00.pdf
- ReportLab Documentation: https://www.reportlab.com/docs/reportlab-userguide.pdf

## Support

If Thai fonts don't render correctly:

1. Check `logs/text_merger.log` for font loading messages
2. Verify font file exists and is readable
3. Try a different Thai font
4. Check application is using `--log-level DEBUG` for more details

---

**Note:** This directory should contain only TTF font files. Other file types will be ignored.
