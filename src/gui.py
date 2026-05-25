"""
Modern, production-ready desktop GUI for Text Merge Application using CustomTkinter.
Provides a polished, VS Code/Notion-inspired interface with dark theme.
"""

import logging
import threading
from pathlib import Path
from typing import Optional, Callable
from datetime import datetime

import customtkinter as ctk
from tkinter import filedialog, messagebox

from src.config import Config
from src.file_merger import FileMerger
from src.docx_exporter import DocxExporter
from src.pdf_exporter import PdfExporter
from src.font_manager import FontManager
from src.utils import validate_folder_exists


class Theme:
    """VS Code-inspired dark theme constants."""
    
    BG_PRIMARY = "#0e1117"
    BG_SECONDARY = "#161b22"
    BG_TERTIARY = "#21262d"
    TEXT_PRIMARY = "#e6edf3"
    TEXT_SECONDARY = "#8b949e"
    ACCENT_BLUE = "#1f6feb"
    ACCENT_BLUE_HOVER = "#388bfd"
    SUCCESS_GREEN = "#238636"
    SUCCESS_GREEN_HOVER = "#2ea043"
    BORDER_COLOR = "#30363d"
    
    FONT_MAIN = ("Segoe UI", 10)
    FONT_TITLE = ("Segoe UI", 16, "bold")
    FONT_SECTION = ("Segoe UI", 12, "bold")
    FONT_SMALL = ("Segoe UI", 9)
    FONT_MONO = ("Consolas", 9)
    
    PADDING_XS = 4
    PADDING_SM = 8
    PADDING_MD = 12
    PADDING_LG = 16
    PADDING_XL = 24


class ModernCard(ctk.CTkFrame):
    """Reusable rounded card component."""
    
    def __init__(self, parent, fg_color=None, border_color=None, **kwargs):
        if fg_color is None:
            fg_color = Theme.BG_TERTIARY
        if border_color is None:
            border_color = Theme.BORDER_COLOR
        
        super().__init__(
            parent,
            fg_color=fg_color,
            corner_radius=8,
            border_width=1,
            border_color=border_color,
            **kwargs
        )


class ModernButton(ctk.CTkButton):
    """Reusable modern button."""
    
    def __init__(self, parent, text: str, is_primary: bool = False, **kwargs):
        bg_color = Theme.ACCENT_BLUE if is_primary else Theme.BG_TERTIARY
        hover_color = Theme.ACCENT_BLUE_HOVER if is_primary else Theme.BORDER_COLOR
        text_color = "#ffffff" if is_primary else Theme.TEXT_PRIMARY
        
        super().__init__(
            parent,
            text=text,
            font=Theme.FONT_MAIN,
            fg_color=bg_color,
            hover_color=hover_color,
            text_color=text_color,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            corner_radius=6,
            height=36,
            **kwargs
        )


class ActionButton(ctk.CTkButton):
    """Large action button for primary operations."""
    
    def __init__(self, parent, text: str, is_success: bool = False, **kwargs):
        bg_color = Theme.SUCCESS_GREEN if is_success else Theme.ACCENT_BLUE
        hover_color = Theme.SUCCESS_GREEN_HOVER if is_success else Theme.ACCENT_BLUE_HOVER
        
        super().__init__(
            parent,
            text=text,
            font=("Segoe UI", 11, "bold"),
            fg_color=bg_color,
            hover_color=hover_color,
            text_color="#ffffff",
            corner_radius=8,
            height=44,
            **kwargs
        )


class LogHandler(logging.Handler):
    """Custom logging handler for GUI."""
    
    def __init__(self, callback: Callable[[str], None]):
        super().__init__()
        self.callback = callback
    
    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.callback(msg)
        except Exception:
            self.handleError(record)


class TextMergeGUI:
    """Modern desktop GUI for Text Merge Application."""
    
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        self.input_folder: Optional[Path] = None
        self.output_folder: Path = self.config.output_directory
        self.is_processing = False
        self.file_merger = FileMerger(self.config)
        self.font_manager = FontManager(Path("fonts"))
        
        self._setup_window()
        self._setup_logging()
        self._create_ui()
    
    def _setup_window(self) -> None:
        self.root.title("Text Merge Application")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root.configure(fg_color=Theme.BG_PRIMARY)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def _setup_logging(self) -> None:
        gui_handler = LogHandler(self._add_log_message)
        gui_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S")
        gui_handler.setFormatter(formatter)
        root_logger = logging.getLogger()
        root_logger.addHandler(gui_handler)
    
    def _create_ui(self) -> None:
        self._create_header()
        self._create_main_content()
        self._create_footer()
    
    def _create_header(self) -> None:
        header = ctk.CTkFrame(self.root, fg_color=Theme.BG_SECONDARY, height=60)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)
        
        header_container = ctk.CTkFrame(header, fg_color="transparent")
        header_container.pack(fill="both", expand=True, padx=Theme.PADDING_LG, pady=Theme.PADDING_MD)
        
        title_frame = ctk.CTkFrame(header_container, fg_color="transparent")
        title_frame.pack(fill="x")
        
        title = ctk.CTkLabel(title_frame, text="📄 Text Merge", font=Theme.FONT_TITLE, text_color=Theme.TEXT_PRIMARY)
        title.pack(side="left")
        
        subtitle = ctk.CTkLabel(title_frame, text="Professional Document Merger", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY)
        subtitle.pack(side="left", padx=(Theme.PADDING_MD, 0))
    
    def _create_main_content(self) -> None:
        main_container = ctk.CTkFrame(self.root, fg_color=Theme.BG_PRIMARY)
        main_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=0)
        main_container.grid_columnconfigure(1, weight=1)
        
        left_panel = ctk.CTkFrame(main_container, fg_color=Theme.BG_PRIMARY)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=Theme.PADDING_LG, pady=Theme.PADDING_LG)
        left_panel.grid_rowconfigure(5, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)
        
        self._create_control_panel(left_panel)
        
        separator = ctk.CTkFrame(main_container, fg_color=Theme.BORDER_COLOR, width=1)
        separator.grid(row=0, column=0, sticky="ns", padx=(0, Theme.PADDING_LG), pady=Theme.PADDING_LG)
        
        right_panel = ctk.CTkFrame(main_container, fg_color=Theme.BG_PRIMARY)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, Theme.PADDING_LG), pady=Theme.PADDING_LG)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        self._create_logs_panel(right_panel)
    
    def _create_control_panel(self, parent: ctk.CTkFrame) -> None:
        self._create_input_section(parent)
        self._create_format_section(parent)
        self._create_output_section(parent)
        self._create_font_section(parent)
        self._create_buttons_section(parent)
    
    def _create_input_section(self, parent: ctk.CTkFrame) -> None:
        card = ModernCard(parent)
        card.grid(row=0, column=0, sticky="ew", pady=(0, Theme.PADDING_LG))
        card.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(card, text="📁 Input Files", font=Theme.FONT_SECTION, text_color=Theme.TEXT_PRIMARY)
        title.grid(row=0, column=0, sticky="w", padx=Theme.PADDING_MD, pady=(Theme.PADDING_MD, Theme.PADDING_SM))
        
        self.input_label = ctk.CTkLabel(card, text="No folder selected", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY)
        self.input_label.grid(row=1, column=0, sticky="ew", padx=Theme.PADDING_MD, pady=(0, Theme.PADDING_MD))
        
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=Theme.PADDING_MD, pady=(0, Theme.PADDING_MD))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        
        browse_btn = ModernButton(button_frame, "📂 Browse Folder", command=self._browse_input_folder)
        browse_btn.grid(row=0, column=0, sticky="ew", padx=(0, Theme.PADDING_SM))
        
        clear_btn = ModernButton(button_frame, "✕", command=self._clear_input_folder)
        clear_btn.grid(row=0, column=1, sticky="ew", padx=0)
        
        dnd_card = ModernCard(card, fg_color=Theme.BG_SECONDARY, border_color=Theme.ACCENT_BLUE)
        dnd_card.grid(row=3, column=0, sticky="ew", padx=Theme.PADDING_MD, pady=(Theme.PADDING_SM, Theme.PADDING_MD))
        dnd_card.grid_columnconfigure(0, weight=1)
        
        self.dnd_label = ctk.CTkLabel(dnd_card, text="📂 Or use Browse button above", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY)
        self.dnd_label.grid(row=0, column=0, sticky="ew", padx=Theme.PADDING_MD, pady=Theme.PADDING_LG)
    
    def _create_format_section(self, parent: ctk.CTkFrame) -> None:
        card = ModernCard(parent)
        card.grid(row=1, column=0, sticky="ew", pady=(0, Theme.PADDING_LG))
        card.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(card, text="📄 Export Format", font=Theme.FONT_SECTION, text_color=Theme.TEXT_PRIMARY)
        title.grid(row=0, column=0, sticky="w", padx=Theme.PADDING_MD, pady=(Theme.PADDING_MD, Theme.PADDING_SM))
        
        self.format_var = ctk.StringVar(value="both")
        formats = [("Both (DOCX + PDF)", "both", "📦"), ("DOCX Only", "docx", "📃"), ("PDF Only", "pdf", "🔴")]
        
        options_frame = ctk.CTkFrame(card, fg_color="transparent")
        options_frame.grid(row=1, column=0, sticky="ew", padx=Theme.PADDING_MD, pady=(0, Theme.PADDING_MD))
        
        for idx, (text, value, icon) in enumerate(formats):
            radio = ctk.CTkRadioButton(options_frame, text=f"{icon} {text}", variable=self.format_var, value=value, font=Theme.FONT_SMALL, text_color=Theme.TEXT_PRIMARY)
            radio.grid(row=idx, column=0, sticky="w", pady=Theme.PADDING_XS)
    
    def _create_output_section(self, parent: ctk.CTkFrame) -> None:
        card = ModernCard(parent)
        card.grid(row=2, column=0, sticky="ew", pady=(0, Theme.PADDING_LG))
        card.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(card, text="📤 Output Folder", font=Theme.FONT_SECTION, text_color=Theme.TEXT_PRIMARY)
        title.grid(row=0, column=0, sticky="w", padx=Theme.PADDING_MD, pady=(Theme.PADDING_MD, Theme.PADDING_SM))
        
        self.output_label = ctk.CTkLabel(card, text=str(self.output_folder), font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY, wraplength=280)
        self.output_label.grid(row=1, column=0, sticky="ew", padx=Theme.PADDING_MD, pady=(0, Theme.PADDING_MD))
        
        output_btn = ModernButton(card, "📂 Change Location", command=self._browse_output_folder)
        output_btn.grid(row=2, column=0, sticky="ew", padx=Theme.PADDING_MD, pady=(0, Theme.PADDING_MD))
    
    def _create_font_section(self, parent: ctk.CTkFrame) -> None:
        card = ModernCard(parent)
        card.grid(row=3, column=0, sticky="ew", pady=(0, Theme.PADDING_LG))
        card.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(card, text="🔤 PDF Font", font=Theme.FONT_SECTION, text_color=Theme.TEXT_PRIMARY)
        title.grid(row=0, column=0, sticky="w", padx=Theme.PADDING_MD, pady=(Theme.PADDING_MD, Theme.PADDING_SM))
        
        registered_fonts = self.font_manager.list_registered_fonts()
        font_options = list(registered_fonts.keys()) if registered_fonts else ["TH Sarabun New", "Helvetica", "Times", "Courier"]
        
        if registered_fonts:
            thai_fonts = [f for f in font_options if "Thai" in f or "Sarabun" in f]
            other_fonts = [f for f in font_options if f not in thai_fonts]
            font_options = thai_fonts + other_fonts
        
        self.font_var = ctk.StringVar(value=font_options[0] if font_options else "Helvetica")
        
        font_menu = ctk.CTkComboBox(card, values=font_options, variable=self.font_var, state="readonly", font=Theme.FONT_SMALL, text_color=Theme.TEXT_PRIMARY, fg_color=Theme.BG_SECONDARY, button_color=Theme.ACCENT_BLUE)
        font_menu.grid(row=1, column=0, sticky="ew", padx=Theme.PADDING_MD, pady=(0, Theme.PADDING_MD))
        
        available_fonts = self.font_manager.list_available_fonts()
        font_info = ctk.CTkLabel(card, text=f"📌 {len(available_fonts)} Thai fonts available in ./fonts", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY)
        font_info.grid(row=2, column=0, sticky="w", padx=Theme.PADDING_MD, pady=(0, Theme.PADDING_MD))
    
    def _create_buttons_section(self, parent: ctk.CTkFrame) -> None:
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.grid(row=4, column=0, sticky="ew", pady=(Theme.PADDING_LG, 0))
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(1, weight=1)
        
        self.merge_btn = ActionButton(buttons_frame, "▶ Start Merge", is_success=True, command=self._start_merge)
        self.merge_btn.grid(row=0, column=0, sticky="ew", pady=(0, Theme.PADDING_SM))
        
        self.cancel_btn = ActionButton(buttons_frame, "⏹ Cancel", is_success=False, command=self._cancel_merge)
        self.cancel_btn.grid(row=1, column=0, sticky="ew")
        self.cancel_btn.configure(state="disabled")
        
        spacer = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        spacer.grid(row=2, column=0, sticky="nsew", pady=Theme.PADDING_LG)
    
    def _create_logs_panel(self, parent: ctk.CTkFrame) -> None:
        title = ctk.CTkLabel(parent, text="📋 Activity & Logs", font=Theme.FONT_SECTION, text_color=Theme.TEXT_PRIMARY)
        title.grid(row=0, column=0, sticky="w", pady=(0, Theme.PADDING_LG))
        
        progress_card = ModernCard(parent)
        progress_card.grid(row=1, column=0, sticky="ew", pady=(0, Theme.PADDING_LG))
        progress_card.grid_columnconfigure(0, weight=1)
        
        self.progress_label = ctk.CTkLabel(progress_card, text="⏳ Ready to merge", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY)
        self.progress_label.grid(row=0, column=0, sticky="w", padx=Theme.PADDING_MD, pady=(Theme.PADDING_SM, Theme.PADDING_XS))
        
        self.progress_var = ctk.DoubleVar(value=0)
        self.progress_bar = ctk.CTkProgressBar(progress_card, variable=self.progress_var, mode="determinate", fg_color=Theme.BG_SECONDARY, progress_color=Theme.ACCENT_BLUE, height=6)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=Theme.PADDING_MD, pady=Theme.PADDING_SM)
        self.progress_bar.set(0)
        
        self.progress_percent = ctk.CTkLabel(progress_card, text="0%", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY)
        self.progress_percent.grid(row=2, column=0, sticky="e", padx=Theme.PADDING_MD, pady=(Theme.PADDING_SM, Theme.PADDING_MD))
        
        logs_card = ModernCard(parent)
        logs_card.grid(row=2, column=0, sticky="nsew", pady=(0, Theme.PADDING_LG))
        logs_card.grid_rowconfigure(0, weight=1)
        logs_card.grid_columnconfigure(0, weight=1)
        
        log_title = ctk.CTkLabel(logs_card, text="📝 Log Output", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY)
        log_title.grid(row=0, column=0, sticky="w", padx=Theme.PADDING_MD, pady=(Theme.PADDING_MD, Theme.PADDING_SM))
        
        self.log_text = ctk.CTkTextbox(logs_card, font=Theme.FONT_MONO, fg_color=Theme.BG_PRIMARY, text_color=Theme.TEXT_SECONDARY, border_width=0, corner_radius=0)
        self.log_text.grid(row=1, column=0, sticky="nsew", padx=Theme.PADDING_MD, pady=(0, Theme.PADDING_MD))
        self.log_text.configure(state="disabled")
        
        clear_btn = ModernButton(logs_card, "🗑 Clear Logs", command=self._clear_logs)
        clear_btn.grid(row=2, column=0, sticky="w", padx=Theme.PADDING_MD, pady=(0, Theme.PADDING_MD))
    
    def _create_footer(self) -> None:
        footer = ctk.CTkFrame(self.root, fg_color=Theme.BG_SECONDARY, height=40)
        footer.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        footer.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(footer, text="✓ Ready to merge | TH Sarabun New font loaded", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY)
        self.status_label.pack(side="left", padx=Theme.PADDING_LG, pady=Theme.PADDING_SM)
    
    def _browse_input_folder(self) -> None:
        folder = filedialog.askdirectory(title="Select folder with .txt files")
        if folder:
            self.input_folder = Path(folder)
            self._update_input_label()
    
    def _clear_input_folder(self) -> None:
        self.input_folder = None
        self._update_input_label()
    
    def _update_input_label(self) -> None:
        if self.input_folder:
            file_count = len(list(self.input_folder.glob("*.txt")))
            self.input_label.configure(text=f"✓ {self.input_folder.name}\n{file_count} .txt files")
        else:
            self.input_label.configure(text="No folder selected")
    
    def _browse_output_folder(self) -> None:
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder = Path(folder)
            self.output_label.configure(text=str(self.output_folder))
            self.status_label.configure(text=f"✓ Output folder: {self.output_folder.name}")
    
    def _start_merge(self) -> None:
        if not self.input_folder or not validate_folder_exists(self.input_folder):
            messagebox.showerror("Invalid Input", "Please select a valid input folder")
            return
        
        file_count = len(list(self.input_folder.glob("*.txt")))
        if file_count == 0:
            messagebox.showwarning("No Files", f"No .txt files found in\n{self.input_folder}")
            return
        
        format_choice = self.format_var.get()
        formats = ["docx", "pdf"] if format_choice == "both" else [format_choice]
        output_name = self.input_folder.name + "_merged_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.is_processing = True
        self.merge_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress_var.set(0)
        self.progress_percent.configure(text="0%")
        self.progress_label.configure(text="⏳ Processing...")
        
        thread = threading.Thread(target=self._merge_thread, args=(self.input_folder, output_name, formats), daemon=True)
        thread.start()
    
    def _merge_thread(self, input_folder: Path, output_name: str, formats: list) -> None:
        try:
            self._add_log_message("=" * 60)
            self._add_log_message("🚀 MERGE OPERATION STARTED")
            self._add_log_message(f"Input:  {input_folder.name}")
            self._add_log_message(f"Output: {self.output_folder.name}")
            self._add_log_message(f"Format: {', '.join(formats).upper()}")
            self._add_log_message("=" * 60)
            
            self.progress_var.set(0.15)
            self.progress_percent.configure(text="15%")
            self.progress_label.configure(text="📚 Merging files...")
            self._add_log_message("📚 Reading and merging files...")
            
            merged_content = self.file_merger.merge_files(input_folder)
            if not merged_content:
                self._add_log_message("✗ No content to merge")
                self.progress_label.configure(text="✗ Failed - no content")
                return
            
            file_count = len(list(input_folder.glob("*.txt")))
            self._add_log_message(f"✓ Merged {file_count} files")
            self.progress_var.set(0.4)
            self.progress_percent.configure(text="40%")
            
            success_count = 0
            for idx, fmt in enumerate(formats):
                try:
                    if fmt == "docx":
                        self.progress_label.configure(text="📃 Exporting to DOCX...")
                        self._add_log_message("📃 Exporting to DOCX...")
                        exporter = DocxExporter(self.config)
                        output_file = self.output_folder / f"{output_name}.docx"
                        exporter.export(merged_content, output_file)
                        file_size_mb = output_file.stat().st_size / (1024 * 1024)
                        self._add_log_message(f"✓ DOCX saved: {output_file.name} ({file_size_mb:.2f} MB)")
                        success_count += 1
                    elif fmt == "pdf":
                        self.progress_label.configure(text="🔴 Exporting to PDF...")
                        self._add_log_message("🔴 Exporting to PDF...")
                        exporter = PdfExporter(self.config)
                        output_file = self.output_folder / f"{output_name}.pdf"
                        exporter.export(merged_content, output_file)
                        file_size_mb = output_file.stat().st_size / (1024 * 1024)
                        self._add_log_message(f"✓ PDF saved: {output_file.name} ({file_size_mb:.2f} MB)")
                        success_count += 1
                    
                    progress_pct = 40 + (idx + 1) * (50 // len(formats))
                    self.progress_var.set(progress_pct / 100.0)
                    self.progress_percent.configure(text=f"{progress_pct}%")
                except Exception as e:
                    self._add_log_message(f"✗ Error exporting to {fmt.upper()}: {str(e)}")
            
            if success_count > 0:
                self.progress_var.set(1.0)
                self.progress_percent.configure(text="100%")
                self.progress_label.configure(text="✓ Merge completed successfully!")
                self._add_log_message("=" * 60)
                self._add_log_message(f"🎉 SUCCESS: {success_count}/{len(formats)} formats exported")
                self._add_log_message(f"📂 Output location: {self.output_folder}")
                self._add_log_message("=" * 60)
                self.status_label.configure(text=f"✓ Merge completed | {success_count} format(s)")
                messagebox.showinfo("Success", f"Merge completed!\n{success_count}/{len(formats)} format(s) exported\n\nOutput: {self.output_folder}")
            else:
                self._add_log_message("✗ Merge failed - no formats exported")
                self.progress_label.configure(text="✗ Failed - export error")
        except Exception as e:
            self._add_log_message(f"✗ Critical error: {str(e)}")
            self.progress_label.configure(text="✗ Failed - internal error")
            messagebox.showerror("Error", f"Merge failed:\n{str(e)}")
        finally:
            self.is_processing = False
            self.merge_btn.configure(state="normal")
            self.cancel_btn.configure(state="disabled")
            self.status_label.configure(text="✓ Ready to merge")
    
    def _cancel_merge(self) -> None:
        self.is_processing = False
        self._add_log_message("⏹ Merge cancelled by user")
        self.progress_label.configure(text="⏹ Cancelled")
        self.merge_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        messagebox.showinfo("Cancelled", "Merge operation cancelled")
    
    def _add_log_message(self, message: str) -> None:
        self.log_text.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.root.update_idletasks()
    
    def _clear_logs(self) -> None:
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self._add_log_message("🗑 Logs cleared")


def run_gui() -> None:
    root = ctk.CTk()
    app = TextMergeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
