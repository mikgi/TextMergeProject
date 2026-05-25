# Usage Guide - Text Merge Application

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2a. GUI Mode (Recommended for most users)

```bash
python gui_launcher.py
```

Then use the visual interface:

1. Click "Browse Folder" to select input folder
2. Select export format (Both/DOCX/PDF)
3. Click "▶ Start Merge"
4. View real-time progress and logs

**See [GUI_GUIDE.md](GUI_GUIDE.md) for detailed GUI instructions.**

### 2b. CLI Mode (For automation and scripts)

```bash
python main.py ./sample_input merged_document
```

This creates:

- `output/merged_document.docx`
- `output/merged_document.pdf`
- `logs/text_merger.log`

## Command Reference

### Syntax

```bash
python main.py <input_folder> <output_name> [options]
```

### Options

| Option         | Values                                          | Default | Description        |
| -------------- | ----------------------------------------------- | ------- | ------------------ |
| `--format`     | `docx`, `pdf`, `both`                           | `both`  | Output format      |
| `--sort-order` | `name`, `date`                                  | `name`  | File sorting order |
| `--log-level`  | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | `INFO`  | Logging verbosity  |

## Usage Examples

### Example 1: Merge to Both Formats (Default)

```bash
python main.py ./sample_input my_merged
```

**Output:**

- `output/my_merged.docx`
- `output/my_merged.pdf`

### Example 2: Export to DOCX Only

```bash
python main.py ./sample_input thai_document --format docx
```

**Output:**

- `output/thai_document.docx`

### Example 3: Export to PDF Only

```bash
python main.py ./sample_input report_pdf --format pdf
```

**Output:**

- `output/report_pdf.pdf`

### Example 4: Sort Files by Date Modified

```bash
python main.py ./my_text_files chronological_merge --sort-order date
```

Merges files in order of modification date instead of filename.

### Example 5: Enable Debug Logging

```bash
python main.py ./sample_input debug_test --log-level DEBUG
```

Creates detailed logs in `logs/text_merger.log` for troubleshooting.

### Example 6: Custom Input and Output Directories

```bash
python main.py D:/Documents/TextFiles merged_report
```

### Example 7: Complete Example with All Options

```bash
python main.py ./input_folder final_document --format both --sort-order name --log-level INFO
```

## Real-World Use Cases

### Use Case 1: Merge Meeting Notes

```bash
# You have individual meeting notes in ./meetings/
python main.py ./meetings team_meeting_summary --format docx
# Outputs single DOCX for easy sharing
```

### Use Case 2: Combine Translation Files

```bash
# Merge translated text files
python main.py ./translations/thai translation_report --format pdf --log-level INFO
# Outputs PDF with complete translation
```

### Use Case 3: Create Book from Chapters

```bash
# Combine chapter files
python main.py ./chapters/book_project complete_book --format docx
# Merges all chapters into single book
```

### Use Case 4: Consolidate Logs/Reports

```bash
python main.py ./daily_reports weekly_summary --sort-order date --format both
# Merges reports by date, creates both formats
```

## Input File Requirements

### File Format

- Files must be plain text (`.txt`)
- UTF-8 encoding required for Thai and other languages
- Any text size (application handles large files)

### Organizing Input Files

```
input_folder/
├── 01_chapter_one.txt
├── 02_chapter_two.txt
├── 03_chapter_three.txt
└── 04_conclusion.txt
```

**Naming Tip:** Prefix with numbers for natural sort order (01*, 02*, etc.)

### Example Thai Text File

```
สวัสดี
นี่คือไฟล์ตัวอย่าง
Application supports mixed Thai and English text perfectly!
```

## Output File Details

### DOCX Output

- **Format:** Microsoft Word (.docx)
- **Font:** Calibri 11pt (supports Thai characters)
- **Layout:** Standard margins with proper spacing
- **Best for:** Sharing, printing, editing

### PDF Output

- **Format:** Portable Document Format (.pdf)
- **Pages:** Auto-paginated (50 lines per page)
- **Font:** Thai-optimized font with Helvetica fallback
- **Thai Support:** Automatic with embedded TTF fonts
- **Best for:** Distribution, archival, viewing

## Thai Font Setup for PDF

For optimal Thai text rendering in PDF output, the application supports custom TTF fonts.

### Quick Setup

1. Download Thai font (TH Sarabun New recommended):
   - Visit: https://fonts.google.com/specimen/Sarabun
   - Download and extract `THSarabunNew.ttf`

2. Place in fonts directory:

   ```
   TextMergeProject/
   └── fonts/
       └── THSarabunNew.ttf
   ```

3. Run application - fonts are automatically detected:
   ```bash
   python main.py ./sample_input thai_output --format pdf --log-level DEBUG
   ```

### Available Thai Fonts

| Font            | Filename                    | Download                                          |
| --------------- | --------------------------- | ------------------------------------------------- |
| TH Sarabun New  | `THSarabunNew.ttf`          | https://fonts.google.com/specimen/Sarabun         |
| Noto Sans Thai  | `NotoSansThai-Regular.ttf`  | https://fonts.google.com/specimen/Noto+Sans+Thai  |
| Noto Serif Thai | `NotoSerifThai-Regular.ttf` | https://fonts.google.com/specimen/Noto+Serif+Thai |

### Verify Font Installation

```bash
# Check if fonts are detected
python main.py ./sample_input test --log-level DEBUG | grep -i "font"

# Expected output should include:
# "Found X TTF file(s) in ./fonts"
# "Font registered successfully: THSarabunNew"
# "Using Thai font: THSarabunNew"
```

### Font Priority

Application uses fonts in this order:

1. THSarabunNew (if found)
2. NotoSansThai (if found)
3. NotoSerifThai (if found)
4. Helvetica (system fallback)

### Troubleshooting Thai Fonts

**Thai text appears as boxes:**

- Download Thai font and place in `./fonts` directory
- Verify font filename ends with `.ttf`
- Check debug logs: `--log-level DEBUG`

**Font not found error:**

- Ensure `./fonts` directory exists
- Place TTF files directly in `./fonts/` (not subdirectories)
- Re-run application with `--log-level DEBUG` to verify

For detailed Thai font setup, see [THAI_FONTS_GUIDE.md](THAI_FONTS_GUIDE.md).

## Logging

### Log File Location

```
logs/text_merger.log
```

### Log Levels Explained

- **DEBUG:** Detailed information for development/troubleshooting
- **INFO:** General operational messages (default)
- **WARNING:** Warning messages about non-critical issues
- **ERROR:** Error messages about failures
- **CRITICAL:** Critical errors that prevent operation

### Viewing Logs

```bash
# Windows - View last 50 lines
type logs\text_merger.log | tail -50

# macOS/Linux
tail -50 logs/text_merger.log

# Real-time monitoring
tail -f logs/text_merger.log
```

## Troubleshooting

### Problem: No files found

```
⚠️ Warning: No text files found in ./input_folder
```

**Solution:** Ensure folder contains `.txt` files

### Problem: Permission denied

```
❌ Error: IO error writing file: Permission denied
```

**Solution:** Check folder write permissions

```bash
# Windows - Reset permissions
# macOS/Linux
chmod 755 output/
```

### Problem: Thai text appears as boxes

```
⚠️ Thai characters not rendering correctly
```

**Solution:** Ensure input files are UTF-8 encoded

- Use VS Code: Select UTF-8 in bottom right
- Use Notepad++: Encoding → UTF-8

### Problem: File encoding error

```
❌ Error: Unicode decode error reading file
```

**Solution:** Convert file to UTF-8

```bash
# Notepad++: Encoding → Encode in UTF-8
# VS Code: Click UTF-8 in bottom right → Save with encoding
```

### Problem: Module not found

```
❌ ModuleNotFoundError: No module named 'docx'
```

**Solution:** Install dependencies

```bash
pip install -r requirements.txt
```

## Advanced Usage

### Processing Large Files

```bash
# For large merges, use DEBUG logging to monitor
python main.py ./large_folder large_output --log-level DEBUG
# Check progress in logs/text_merger.log
```

### Batch Processing

```bash
# Process multiple folders (create batch script)
@echo off
python main.py ./batch1 output1
python main.py ./batch2 output2
python main.py ./batch3 output3
```

### Scheduled Tasks

```bash
# Windows Task Scheduler
# Create task to run: python main.py <input> <output>

# Linux Cron
# 0 9 * * * cd /path/to/project && python main.py ./input merged_daily
```

## VS Code Integration

### Running from Terminal

```bash
# Ctrl+` to open terminal
python main.py ./sample_input test_output
```

### Running with Debugger

1. Set breakpoint (click left of line number)
2. Select configuration from Run menu
3. Press F5 or click Run button

### Available Debug Configurations

- Text Merge - Basic Test
- Text Merge - DOCX Only
- Text Merge - PDF Only
- Text Merge - Debug Mode

## Tips & Best Practices

### ✅ Do

- Use UTF-8 encoding for all input files
- Name files with numbers for consistent ordering (01*, 02*, etc.)
- Check logs for warnings and errors
- Keep input folder organized
- Use `--log-level DEBUG` when troubleshooting

### ❌ Don't

- Mix different encodings in input files
- Use special characters in filenames
- Run without write permissions on output folder
- Assume files will sort alphabetically (use descriptive names)
- Ignore error messages in the log file

## Performance Notes

- **Small files (< 10MB):** < 1 second
- **Medium files (10-100MB):** 1-5 seconds
- **Large files (> 100MB):** 5-30 seconds
- PDF generation typically takes longer than DOCX

## Getting Help

### Check Logs

```bash
type logs\text_merger.log  # Windows
tail logs/text_merger.log   # macOS/Linux
```

### Enable Detailed Logging

```bash
python main.py ./input output --log-level DEBUG
```

### Verify Setup

```bash
python -m pip list  # Check installed packages
python -c "import docx; import reportlab"  # Verify imports
```

---

**Need More Help?** Check the README.md file or examine the application source code with comments.
