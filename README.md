# Text Merge Application

A production-ready Python application for merging multiple text files and exporting to DOCX and PDF formats with full UTF-8 support, including Thai language.

## Features

✅ **Clean Architecture** - Modular, maintainable code structure  
✅ **UTF-8 Support** - Full support for Thai and other multi-byte languages  
✅ **Multiple Formats** - Export to DOCX and/or PDF  
✅ **Modern GUI** - CustomTkinter desktop interface with drag & drop  
✅ **Comprehensive Logging** - File and console logging with configurable levels  
✅ **Exception Handling** - Robust error handling throughout the application  
✅ **Pathlib** - Modern path operations (not os.path)  
✅ **Clear Comments** - Well-documented code with type hints  
✅ **VS Code Compatible** - Works seamlessly with Visual Studio Code

## Quick Start

### Launch GUI (Easiest)

```bash
python gui_launcher.py
```

### CLI Mode

```bash
python main.py ./sample_input merged_document
```

## Project Structure

```
TextMergeProject/
├── main.py                    # CLI entry point
├── gui_launcher.py            # GUI launcher
├── launcher.py                # Universal launcher (CLI or GUI)
├── requirements.txt           # Python dependencies
├── src/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration management
│   ├── file_merger.py        # File merging logic
│   ├── docx_exporter.py      # DOCX export functionality
│   ├── pdf_exporter.py       # PDF export functionality
│   ├── font_manager.py       # Font management for PDF
│   ├── gui.py                # Modern CustomTkinter GUI
│   └── utils.py              # Utility functions
├── sample_input/             # Sample .txt files
├── output/                   # Output directory for generated files
├── fonts/                    # Thai fonts (optional)
└── logs/                     # Application logs
```

## GUI Features

The application includes a **modern desktop GUI** with:

- 🎨 **Dark mode interface** - Professional appearance
- 📁 **Drag & drop** - Drop .txt files directly into the app
- 📊 **Progress bar** - Real-time operation progress
- 📋 **Live logs** - View detailed logs as operation proceeds
- 🔤 **Font selection** - Choose Thai fonts for PDF output
- 📤 **Output folder** - Select where to save files
- 🎯 **Format selection** - Choose DOCX, PDF, or both
- ⚡ **Non-blocking** - Responsive UI during merge operations

See [GUI_GUIDE.md](GUI_GUIDE.md) for detailed GUI documentation.

## Installation

### 1. Clone/Download the project

```bash
cd TextMergeProject
```

### 2. Create a Python virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode (Recommended for most users)

Launch the modern desktop interface:

```bash
python gui_launcher.py
```

**GUI Features:**

- Browse or drag & drop input folder
- Select output folder
- Choose export format (DOCX/PDF/Both)
- Select Thai font for PDF
- View real-time progress and logs
- Non-blocking UI with threading

For detailed GUI instructions, see [GUI_GUIDE.md](GUI_GUIDE.md).

### CLI Mode (For automation and scripts)

Merge files from a folder and export to both DOCX and PDF:

```bash
python main.py ./sample_input merged_document
```

### Advanced Options

Export to DOCX only:

```bash
python main.py ./sample_input merged_document --format docx
```

Export to PDF only:

```bash
python main.py ./sample_input merged_document --format pdf
```

Sort files by modification date instead of name:

```bash
python main.py ./sample_input merged_document --sort-order date
```

Set logging level to DEBUG:

```bash
python main.py ./sample_input merged_document --log-level DEBUG
```

### Command-line Arguments

- `input_folder` (required): Path to folder containing .txt files
- `output_name` (required): Output file name without extension
- `--format`: Export format - `docx`, `pdf`, or `both` (default: `both`)
- `--sort-order`: File sorting - `name` or `date` (default: `name`)
- `--log-level`: Logging level - `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` (default: `INFO`)

## Output

The application generates:

- **Merged files** in the `output/` directory
- **Logs** in the `logs/` directory (text_merger.log)

### Output Files

- `merged_document.docx` - Word document with formatted content
- `merged_document.pdf` - PDF with proper pagination
- `logs/text_merger.log` - Application logs

## Examples

### Example 1: Basic Merge (Both Formats)

```bash
python main.py ./sample_input my_merged_files
```

Creates:

- `output/my_merged_files.docx`
- `output/my_merged_files.pdf`

### Example 2: DOCX Only with Thai Support

```bash
python main.py ./sample_input thai_document --format docx
```

### Example 3: Debug Mode

```bash
python main.py ./sample_input test_output --log-level DEBUG
```

## Configuration

Edit `src/config.py` to customize:

- File encoding (default: UTF-8)
- Output directory path
- File extensions to process
- Logging format and level

## Thai Language Support

The application fully supports Thai and other UTF-8 text with optimized font rendering:

### Features

- All text files must be UTF-8 encoded
- Automatic detection of multi-byte characters
- **Proper rendering in DOCX and PDF output**
- **Custom TTF font support for PDF generation**
- See `sample_input/02_thai_content.txt` for examples

### PDF Thai Font Setup

For optimal Thai text rendering in PDF output, install a Thai-compatible TTF font:

#### Option 1: Using TH Sarabun New (Recommended)

1. Download TH Sarabun New font:
   - Windows: Download from [Google Fonts](https://fonts.google.com/specimen/Sarabun)
   - Or download directly: https://github.com/notofonts/noto-cjk/releases

2. Extract and place in `./fonts` directory:

   ```
   TextMergeProject/
   └── fonts/
       └── THSarabunNew.ttf
   ```

3. The application will automatically detect and use it

#### Option 2: Using Noto Sans Thai

1. Download Noto Sans Thai:
   - Download: https://fonts.google.com/specimen/Noto+Sans+Thai
   - File: `NotoSansThai-Regular.ttf`

2. Place in `./fonts` directory:
   ```
   TextMergeProject/
   └── fonts/
       └── NotoSansThai-Regular.ttf
   ```

#### Option 3: Using Noto Serif Thai

For serif text, use Noto Serif Thai:

```
TextMergeProject/
└── fonts/
    └── NotoSerifThai-Regular.ttf
```

### Automatic Font Detection

The application automatically:

1. Discovers all TTF files in the `./fonts` directory
2. Registers them with ReportLab
3. Uses the best available Thai font (priority order):
   - THSarabunNew
   - NotoSansThai
   - NotoSerifThai
4. Falls back to Helvetica if no Thai fonts are found

### Font Directory Structure

Create a `fonts` directory in the project root:

```
TextMergeProject/
├── main.py
├── fonts/                    # Create this directory
│   ├── THSarabunNew.ttf     # Optional Thai fonts
│   ├── NotoSansThai-Regular.ttf
│   └── NotoSerifThai-Regular.ttf
├── sample_input/
└── output/
```

### Verifying Thai Font Installation

Check if fonts are detected:

```bash
python -c "from pathlib import Path; print(list(Path('fonts').glob('*.ttf')))"
```

View debug output with font information:

```bash
python main.py ./sample_input test_output --log-level DEBUG
```

Look for messages like:

```
DEBUG - Found 1 TTF file(s) in ./fonts
DEBUG - Available font: THSarabunNew (THSarabunNew.ttf)
DEBUG - Font registered successfully: THSarabunNew
DEBUG - Using Thai font: THSarabunNew
```

### Troubleshooting Thai Fonts

**Issue: Thai text appears as boxes in PDF**

- Cause: Font not installed or not registered
- Solution:
  1. Download Thai font (TH Sarabun New recommended)
  2. Place in `./fonts` directory
  3. Re-run application
  4. Check debug logs: `--log-level DEBUG`

**Issue: Font file not found error**

- Cause: TTF file not in correct location or wrong filename
- Solution:
  1. Verify file is in `./fonts` directory
  2. Ensure filename ends with `.ttf`
  3. Run `ls fonts/` (macOS/Linux) or `dir fonts` (Windows)

**Issue: ReportLab cannot read TTF file**

- Cause: Font file corrupted or incompatible format
- Solution:
  1. Download font again from official source
  2. Verify it opens in your OS font viewer
  3. Try a different Thai font (Noto Sans Thai, Noto Serif Thai)

### PDF vs DOCX Thai Support

| Feature        | DOCX              | PDF                    |
| -------------- | ----------------- | ---------------------- |
| Thai Text      | ✅ Native support | ✅ With TTF font       |
| Font Embedding | ✅ Automatic      | ✅ Via fonttools       |
| Custom Fonts   | ⚠️ Limited        | ✅ Full TTF support    |
| File Size      | Smaller           | Larger (font embedded) |

## Requirements

- Python 3.9 or higher
- Dependencies listed in `requirements.txt`
- **Optional:** Thai TTF fonts for PDF output (in `./fonts` directory)

## VS Code Integration

### Recommended Extensions

- Python (Microsoft)
- Pylance (Microsoft)
- Python Docstring Generator (Nils Werner)

### Debug Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Text Merge Application",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "args": ["./sample_input", "output/test_merge"]
    }
  ]
}
```

## Error Handling

The application handles:

- Missing or invalid input folders
- File encoding issues
- Missing dependencies
- File I/O errors
- Unicode errors

All errors are logged with full stack traces in `logs/text_merger.log`.

## Logging

### Log Files

- Console output: Real-time application status
- File log (`logs/text_merger.log`): Detailed logs including debug information

### Log Levels

- `DEBUG` - Detailed information for debugging
- `INFO` - General informational messages
- `WARNING` - Warning messages for issues
- `ERROR` - Error messages for problems
- `CRITICAL` - Critical errors

## Development Notes

### Code Style

- Follows PEP 8 style guide
- Type hints included throughout
- Comprehensive docstrings
- Clear variable naming

### Modules

- **config.py** - Configuration dataclasses
- **file_merger.py** - Core file merging with UTF-8 support
- **docx_exporter.py** - python-docx based Word export
- **pdf_exporter.py** - ReportLab based PDF export
- **utils.py** - Helper functions and logging setup

## Troubleshooting

### Issue: Thai text appears as boxes in output

- **Solution**: Ensure input files are UTF-8 encoded
- Use Notepad++ or VS Code to verify encoding

### Issue: "Module not found" error

- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: Permission denied error

- **Solution**: Check folder permissions and ensure output directory is writable

### Issue: PDF output is empty

- **Solution**: Check log file for errors, ensure content is not corrupted

## Future Enhancements

- Batch processing support
- Custom styling templates
- Password protection for output files
- Progress bar for large file operations
- Support for additional formats (XLSX, RTF)

## License

This is a sample production-ready application demonstrating best practices in Python development.

## Support

Check `logs/text_merger.log` for detailed error messages and debugging information.

---

**Author**: Senior Python Developer  
**Version**: 1.0.0  
**Last Updated**: 2026-05-25
#   T e x t M e r g e P r o j e c t  
 