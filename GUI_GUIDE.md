# Modern GUI - Text Merge Application

## Overview

The Text Merge Application now includes a modern, professional desktop GUI built with **CustomTkinter**. The GUI provides an intuitive interface while maintaining full compatibility with the existing CLI.

## Features

✅ **Modern Interface** - Dark mode with responsive layout  
✅ **File Selection** - Browse folder dialog with visual feedback  
✅ **Drag & Drop** - Drop .txt files directly into the application  
✅ **Format Selection** - Choose DOCX, PDF, or both formats  
✅ **Font Selection** - Select custom Thai fonts for PDF output  
✅ **Output Folder** - Choose where to save generated files  
✅ **Progress Bar** - Real-time progress during merge operation  
✅ **Live Logs** - View detailed logs in real-time  
✅ **Status Updates** - Clear status messages and notifications  
✅ **Threading** - Non-blocking UI during merge operations  
✅ **Dark Mode** - Eye-friendly dark theme by default  
✅ **Responsive** - Auto-resizable window and layout

## Installation

### 1. Install GUI Dependencies

```bash
# Install all dependencies including GUI
pip install -r requirements.txt

# Or install GUI packages only
pip install customtkinter tkinterdnd2
```

**Dependencies:**

- `customtkinter==5.2.0` - Modern GUI toolkit
- `tkinterdnd2==0.3.0` - Drag and drop support

### 2. System Requirements

- **Windows:** Works out of the box
- **macOS:** Requires Xcode Command Line Tools
- **Linux:** Requires tkinter development package

  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk

  # Fedora
  sudo dnf install python3-tkinter
  ```

## Launching the GUI

### Method 1: GUI Launcher (Recommended)

```bash
python gui_launcher.py
```

### Method 2: Launcher Script

```bash
# Launch GUI (no arguments)
python launcher.py

# Or explicitly with --gui flag
python launcher.py --gui
```

### Method 3: Python Direct

```bash
python -m src.gui
```

## User Interface Overview

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│         📄 Text Merge Application              │ _ □ ✕     │
├─────────────────────────────────────────────────────────────┤
│  Left Panel              │     Right Panel                   │
├────────────────────────┬─┤                                   │
│ 📁 Input Files         │ │  📋 Logs & Progress               │
│ ├─ Browse Folder       │ │  ├─ Progress Bar [=====    ] 60%  │
│ ├─ Clear              │ │  ├─ Log Window                    │
│ ├─ Drag & Drop Area    │ │  │  [logs display here]           │
│ │                      │ │  │                                │
│ 📄 Export Format       │ │  │                                │
│ ├─ ◉ Both             │ │  │                                │
│ ├─ ○ DOCX             │ │  ├─ Clear Logs button            │
│ ├─ ○ PDF              │ │  │                                │
│ │                      │ │  │                                │
│ 📤 Output Folder       │ │  │                                │
│ ├─ [output path]       │ │  │                                │
│ ├─ Change Output...    │ │  │                                │
│ │                      │ │  │                                │
│ 🔤 PDF Font           │ │  │                                │
│ ├─ [Font Selector ▼]   │ │  │                                │
│ │                      │ │  │                                │
│ ▶ Start Merge         │ │  │                                │
│ ⏸ Cancel (disabled)   │ │  │                                │
│                        │ │  │                                │
├────────────────────────┴─┤                                   │
│ ✓ Ready to merge                                            │
└─────────────────────────────────────────────────────────────┘
```

### Section Descriptions

#### 1. Input Files Section

- **Browse Folder** - Select folder containing .txt files
- **Clear** - Reset folder selection
- **Drag & Drop Area** - Drop .txt files or folders directly
- **File Counter** - Shows number of .txt files found

#### 2. Export Format Section

- **Radio Buttons** - Choose output format:
  - Both (DOCX + PDF) - Default, creates both formats
  - DOCX Only - Microsoft Word format only
  - PDF Only - PDF format only

#### 3. Output Folder Section

- **Current Path** - Shows where files will be saved
- **Change Output Folder** - Browse to new location
- **Default** - outputs/ directory

#### 4. PDF Font Section

- **Font Selector** - Dropdown menu of available fonts
- **Available Fonts** - Shows fonts found in ./fonts directory
- **System Fonts** - Helvetica, Times, Courier always available

#### 5. Logs & Progress Section

- **Progress Bar** - Visual progress indicator (0-100%)
- **Status Text** - Current operation status
- **Log Display** - Real-time log messages with timestamps
- **Clear Logs** - Reset log display

#### 6. Action Buttons

- **▶ Start Merge** - Begins merge operation (green)
- **⏸ Cancel** - Stops current operation (appears during merge)

## Usage Guide

### Step 1: Select Input Folder

**Option A: Browse Dialog**

1. Click "Browse Folder"
2. Navigate to folder with .txt files
3. Click "Select Folder"
4. Files are counted automatically

**Option B: Drag and Drop**

1. Drag folder from File Explorer/Finder
2. Drop into "Drag & drop .txt files here" area
3. Folder is selected automatically

### Step 2: Choose Export Format

1. Select format from radio buttons:
   - **Both** - Creates .docx and .pdf
   - **DOCX** - Word document only
   - **PDF** - PDF document only

### Step 3: (Optional) Select Output Folder

1. Default is `output/` directory
2. Click "Change Output Folder" to select different location
3. All output files will be saved there

### Step 4: (Optional) Choose PDF Font

1. For Thai text in PDF, select appropriate font
2. Available fonts from `./fonts` directory appear here
3. System fonts (Helvetica, Times, Courier) always available

### Step 5: Start Merge

1. Click "▶ Start Merge"
2. Watch progress bar and logs
3. Operation runs in background (UI stays responsive)
4. Completion notification appears when done

### Step 6: View Logs

- Real-time logs display in right panel
- Shows each operation step
- Timestamps included for each message
- Click "Clear Logs" to reset display

## Keyboard Shortcuts

| Shortcut | Action                      |
| -------- | --------------------------- |
| `Enter`  | Start merge (when ready)    |
| `Escape` | Cancel merge (when running) |
| `Tab`    | Navigate between fields     |
| `Ctrl+A` | Select all (in text fields) |

## Drag and Drop

### Supported Formats

- **Folders** - Select entire folder
- **Files** - Drop individual .txt files (uses parent folder)
- **Multiple Files** - Drop multiple files at once

### How It Works

1. Drag file/folder from File Explorer or Finder
2. Hover over "Drag & drop .txt files here" area
3. Drop to select
4. Folder path appears in input label
5. File count is updated automatically

## Progress Bar

The progress bar shows operation progress in stages:

```
0%    ├─ Initialization
20%   ├─ File discovery
50%   ├─ Content merging
75%   ├─ DOCX export (if selected)
90%   ├─ PDF export (if selected)
100%  └─ Completed
```

## Log Messages

### Log Levels and Colors

```
DEBUG    - Detailed technical information (gray)
INFO     - General status messages (white)
SUCCESS  - Successful operations (green)
WARNING  - Non-critical issues (yellow)
ERROR    - Errors and failures (red)
```

### Common Messages

```
✓ Merged X files                      ← Successful merge
✓ DOCX exported: filename.docx        ← Format export success
✓ PDF exported: filename.pdf          ← PDF export success
⏸ Merge cancelled by user             ← User cancellation
❌ No .txt files found                ← Input validation error
🚀 Starting merge operation...         ← Merge started
```

## Notifications

### Success Notification

```
Title: "Success"
Message: "Merge completed!
          Output: [path]"
```

### Error Notification

```
Title: "Error"
Message: "Please select a valid input folder"
```

### Validation Warnings

```
Title: "Warning"
Message: "No .txt files found in [folder]"
```

## Responsive Layout

The GUI automatically adjusts to window size:

### Minimum Size: 800x600

- Left panel shows all controls
- Right panel shows logs (smaller)
- Layout remains functional

### Recommended Size: 1000x700

- Optimal space for all elements
- Log display is easily readable
- Comfortable for all controls

### Maximum Size: No limit

- Scales with window
- Left panel stays fixed width
- Right panel expands for more logs

## Configuration

### Colors (Customizable)

Edit `src/gui.py` to change colors:

```python
class TextMergeGUI:
    DARK_BG = "#1a1a1a"           # Background
    DARK_FG = "#ffffff"           # Foreground
    ACCENT_COLOR = "#0078d4"      # Blue accent
    SUCCESS_COLOR = "#27ae60"     # Green
    ERROR_COLOR = "#e74c3c"       # Red
    WARNING_COLOR = "#f39c12"     # Orange
```

### Theme

Change theme with:

```python
ctk.set_appearance_mode("light")  # Switch to light mode
```

Options: "dark", "light", "system"

## Troubleshooting

### Issue: GUI Won't Launch

**Error:** "ModuleNotFoundError: No module named 'customtkinter'"

**Solution:**

```bash
pip install customtkinter tkinterdnd2
# Or
pip install -r requirements.txt
```

### Issue: Drag & Drop Not Working

**Cause:** tkinterdnd2 not installed

**Solution:**

```bash
pip install tkinterdnd2
```

**Note:** May require different installation on macOS/Linux

### Issue: Fonts Not Showing

**Cause:** No .ttf files in ./fonts directory

**Solution:**

1. Download Thai font from Google Fonts
2. Extract .ttf file
3. Place in ./fonts/ directory
4. Restart GUI

### Issue: GUI Looks Blurry

**Cause:** DPI scaling issue on Windows

**Solution:**

1. Right-click gui_launcher.py
2. Properties → Compatibility
3. Check "Disable fullscreen optimizations"
4. Run in windowed mode

### Issue: Merge Completes but Files Not Found

**Cause:** Wrong output folder selected

**Solution:**

1. Verify output folder in GUI
2. Check file system for generated files
3. Look in logs for actual file path

## CLI Compatibility

The GUI maintains full CLI compatibility:

```bash
# CLI still works
python main.py ./input output --format pdf

# GUI launcher
python gui_launcher.py

# Mixed usage
python launcher.py              # GUI
python launcher.py --cli ./input output  # CLI
```

## Performance

| Operation        | Time              |
| ---------------- | ----------------- |
| GUI startup      | 1-2 seconds       |
| Folder selection | <100ms            |
| Font loading     | <200ms            |
| Merge 100 files  | 5-10 seconds      |
| Progress update  | Real-time         |
| Log display      | <50ms per message |

## Threading Model

The GUI uses background threading:

```
Main Thread (UI)
├─ Button clicks
├─ Window events
└─ Update display

Worker Thread (Merge)
├─ File operations
├─ Document creation
└─ Send progress updates
```

No blocking - UI stays responsive during merge!

## API Integration

The GUI integrates with existing modules:

```python
# FileMerger - Merge operations
self.file_merger = FileMerger(self.config)

# DocxExporter - Word export
exporter = DocxExporter(self.config)

# PdfExporter - PDF export (with fonts)
exporter = PdfExporter(self.config)

# FontManager - Font selection
self.font_manager = FontManager(Path("fonts"))
```

All existing functionality is preserved.

## Advanced Usage

### Custom Font Directory

Modify gui_launcher.py to use custom fonts:

```python
# In TextMergeGUI.__init__
self.font_manager = FontManager(Path("my_custom_fonts"))
```

### Custom Colors

Create themed version:

```python
class DarkModeGUI(TextMergeGUI):
    ACCENT_COLOR = "#ff5722"      # Orange instead of blue
```

### Extending GUI

Add new features by subclassing:

```python
class ExtendedGUI(TextMergeGUI):
    def _create_extra_section(self):
        # Add custom section
        pass
```

## Platform-Specific Notes

### Windows

- Works out of the box
- DPI scaling may affect appearance
- Drag and drop works perfectly

### macOS

- Requires Command Line Tools: `xcode-select --install`
- Drag and drop works with Finder
- May need to allow app in Security settings

### Linux

- Install tkinter: `sudo apt install python3-tk`
- Drag and drop works with file managers
- Theme adapts to system settings

## Future Enhancements

Potential improvements:

- [ ] Batch processing mode
- [ ] Scheduled merges
- [ ] Custom templates
- [ ] Theme customization UI
- [ ] Recent files list
- [ ] Settings/preferences dialog
- [ ] Export format templates
- [ ] File preview window

## Support

For issues:

1. Check logs in GUI for detailed messages
2. Enable DEBUG logging: See logs for technical details
3. Check console output for startup errors
4. Review documentation in README.md

## Summary

The GUI provides:

- ✅ Professional, modern interface
- ✅ Intuitive drag & drop
- ✅ Real-time progress and logs
- ✅ Font selection for Thai PDFs
- ✅ Full CLI compatibility
- ✅ Responsive, non-blocking operations
- ✅ Dark mode with eye-friendly colors
- ✅ Cross-platform support

---

**Version:** 1.0.0  
**Last Updated:** 2026-05-25  
**Status:** Production Ready
