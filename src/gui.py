import logging
import re
import threading
import traceback
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

import customtkinter as ctk
from tkinter import filedialog, messagebox

from src.config import Config
from src.docx_exporter import DocxExporter
from src.epub_exporter import EpubExporter
from src.file_merger import FileMerger
from src.font_manager import FontManager
from src.pdf_exporter import PdfExporter
from src.text_cleaner import set_extra_spam_keywords
from src.utils import validate_folder_exists


class Theme:
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
    FONT_SECTION = ("Segoe UI", 12, "bold")
    FONT_SMALL = ("Segoe UI", 9)
    FONT_MONO = ("Consolas", 9)


class ModernCard(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=kwargs.pop("fg_color", Theme.BG_TERTIARY),
            corner_radius=8,
            border_width=1,
            border_color=kwargs.pop("border_color", Theme.BORDER_COLOR),
            **kwargs,
        )


class TextMergeGUI:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        self.file_merger = FileMerger(self.config)
        self.font_manager = FontManager(Path("fonts"))
        self.input_folder: Optional[Path] = None
        self.output_folder: Path = self.config.output_directory
        self.settings_path = self._get_settings_path()
        self.is_processing = False
        self._result_dialog_shown = False

        self._setup_window()
        self._setup_logging()
        self._create_ui()
        self._load_settings()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_window(self) -> None:
        self.root.title("Text Merge Application")
        self.root.geometry("1320x900")
        self.root.minsize(980, 680)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root.configure(fg_color=Theme.BG_PRIMARY)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.bind("<Configure>", self._on_window_resize)

    def _setup_logging(self) -> None:
        class _GuiHandler(logging.Handler):
            def __init__(self, callback: Callable[[str], None]):
                super().__init__()
                self.callback = callback

            def emit(self, record: logging.LogRecord) -> None:
                self.callback(self.format(record))

        handler = _GuiHandler(self._add_log_message)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", "%H:%M:%S"))
        logging.getLogger().addHandler(handler)

    def _create_ui(self) -> None:
        main = ctk.CTkFrame(self.root, fg_color=Theme.BG_PRIMARY)
        main.grid(row=1, column=0, sticky="nsew", padx=14, pady=14)
        main.grid_columnconfigure(0, weight=0)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(main, fg_color=Theme.BG_PRIMARY)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        right = ctk.CTkFrame(main, fg_color=Theme.BG_PRIMARY)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self._create_left(left)
        self._create_right(right)
        self._create_footer()

    def _create_left(self, parent: ctk.CTkFrame) -> None:
        scroll = ctk.CTkScrollableFrame(parent, fg_color=Theme.BG_PRIMARY, width=380)
        scroll.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        scroll.grid_columnconfigure(0, weight=1)

        self.input_label = ctk.CTkLabel(scroll, text="No folder selected", font=Theme.FONT_SMALL)
        input_card = ModernCard(scroll)
        input_card.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        input_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(input_card, text="Input Files", font=Theme.FONT_SECTION).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))
        self.input_label.grid(in_=input_card, row=1, column=0, sticky="w", padx=12, pady=(0, 8))
        ctk.CTkButton(input_card, text="Browse Folder", command=self._browse_input_folder).grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))

        format_card = ModernCard(scroll)
        format_card.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        ctk.CTkLabel(format_card, text="Export Format", font=Theme.FONT_SECTION).pack(anchor="w", padx=12, pady=(12, 6))
        self.format_var = ctk.StringVar(value="docx")
        for text, value in [("Both (DOCX + PDF + EPUB)", "both"), ("DOCX Only", "docx"), ("PDF Only", "pdf"), ("EPUB Only", "epub")]:
            ctk.CTkRadioButton(format_card, text=text, variable=self.format_var, value=value).pack(anchor="w", padx=12, pady=2)

        output_card = ModernCard(scroll)
        output_card.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        ctk.CTkLabel(output_card, text="Output Folder", font=Theme.FONT_SECTION).pack(anchor="w", padx=12, pady=(12, 6))
        self.output_label = ctk.CTkLabel(output_card, text=str(self.output_folder), wraplength=320, justify="left", text_color=Theme.TEXT_SECONDARY)
        self.output_label.pack(anchor="w", padx=12, pady=(0, 8))
        ctk.CTkButton(output_card, text="Change Location", command=self._browse_output_folder).pack(fill="x", padx=12, pady=(0, 12))

        font_card = ModernCard(scroll)
        font_card.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        ctk.CTkLabel(font_card, text="Export Font", font=Theme.FONT_SECTION).pack(anchor="w", padx=12, pady=(12, 6))
        available_fonts = list(self.font_manager.list_available_fonts().keys())
        regular_fonts = [
            f for f in available_fonts
            if "bold" not in f.casefold() and "italic" not in f.casefold()
        ]
        preferred_order = ["THSarabunNew", "THSarabun", "Sarabun-Regular", "NotoSansThai-Regular"]
        base_fonts = preferred_order + sorted(regular_fonts, key=str.casefold) + ["Helvetica", "Times", "Courier"]
        fonts = [f for i, f in enumerate(base_fonts) if f and f not in base_fonts[:i]]
        self.font_var = ctk.StringVar(value=(fonts[0] if fonts else "Helvetica"))
        self.font_combo = ctk.CTkComboBox(
            font_card,
            values=fonts,
            variable=self.font_var,
            state="readonly",
            command=self._on_font_change,
        )
        self.font_combo.pack(fill="x", padx=12, pady=(0, 12))

        spam_card = ModernCard(scroll)
        spam_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        ctk.CTkLabel(spam_card, text="Extra Spam Keywords", font=Theme.FONT_SECTION).pack(anchor="w", padx=12, pady=(12, 6))
        ctk.CTkLabel(
            spam_card,
            text="One keyword per line",
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_SECONDARY,
        ).pack(anchor="w", padx=12, pady=(0, 6))
        self.spam_text = ctk.CTkTextbox(spam_card, height=90, font=Theme.FONT_SMALL)
        self.spam_text.pack(fill="x", padx=12, pady=(0, 12))
        self.spam_text.bind("<FocusOut>", lambda _e: self._save_settings())

        actions = ModernCard(parent, fg_color=Theme.BG_SECONDARY)
        actions.grid(row=1, column=0, sticky="ew")
        self.merge_btn = ctk.CTkButton(actions, text="Start Merge", fg_color=Theme.SUCCESS_GREEN, hover_color=Theme.SUCCESS_GREEN_HOVER, command=self._start_merge)
        self.merge_btn.pack(fill="x", padx=12, pady=(12, 8))
        self.cancel_btn = ctk.CTkButton(actions, text="Cancel", command=self._cancel_merge, state="disabled")
        self.cancel_btn.pack(fill="x", padx=12, pady=(0, 12))

    def _create_right(self, parent: ctk.CTkFrame) -> None:
        ctk.CTkLabel(parent, text="Activity & Logs", font=Theme.FONT_SECTION).grid(row=0, column=0, sticky="w")
        pcard = ModernCard(parent)
        pcard.grid(row=1, column=0, sticky="ew", pady=(8, 10))
        pcard.grid_columnconfigure(0, weight=1)
        self.progress_label = ctk.CTkLabel(pcard, text="Ready", text_color=Theme.TEXT_SECONDARY)
        self.progress_label.grid(row=0, column=0, sticky="w", padx=12, pady=(10, 4))
        self.progress_var = ctk.DoubleVar(value=0)
        self.progress_bar = ctk.CTkProgressBar(pcard, variable=self.progress_var)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        self.progress_percent = ctk.CTkLabel(pcard, text="0%", text_color=Theme.TEXT_SECONDARY)
        self.progress_percent.grid(row=2, column=0, sticky="e", padx=12, pady=(0, 10))

        lcard = ModernCard(parent)
        lcard.grid(row=2, column=0, sticky="nsew")
        lcard.grid_rowconfigure(0, weight=1)
        lcard.grid_columnconfigure(0, weight=1)
        self.log_text = ctk.CTkTextbox(lcard, font=Theme.FONT_MONO)
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self.log_text.configure(state="disabled")

    def _create_footer(self) -> None:
        footer = ctk.CTkFrame(self.root, fg_color=Theme.BG_SECONDARY, height=36)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)
        self.status_label = ctk.CTkLabel(footer, text="Ready", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY)
        self.status_label.pack(side="left", padx=12, pady=6)

    def _browse_input_folder(self) -> None:
        folder = filedialog.askdirectory(title="Select folder with .txt files")
        if folder:
            self.input_folder = Path(folder)
            self._update_input_label()
            self._save_settings()

    def _browse_output_folder(self) -> None:
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder = Path(folder)
            self.output_label.configure(text=str(self.output_folder))
            self._save_settings()

    def _update_input_label(self) -> None:
        if self.input_folder:
            count = len(list(self.input_folder.glob("*.txt")))
            self.input_label.configure(text=f"{self.input_folder.name}\n{count} .txt files")
            self.status_label.configure(text=f"Ready | {count} file(s) selected")
        else:
            self.input_label.configure(text="No folder selected")
            self.status_label.configure(text="Ready")

    def _start_merge(self) -> None:
        if not self.input_folder or not validate_folder_exists(self.input_folder):
            messagebox.showerror("Invalid Input", "Please select a valid input folder")
            return
        count = len(list(self.input_folder.glob("*.txt")))
        if count == 0:
            messagebox.showwarning("No Files", f"No .txt files found in\n{self.input_folder}")
            return
        formats = ["docx", "pdf", "epub"] if self.format_var.get() == "both" else [self.format_var.get()]
        extra_keywords = self._parse_custom_spam_keywords()
        set_extra_spam_keywords(extra_keywords)
        self._add_log_message(f"Custom spam keywords loaded: {len(extra_keywords)}")
        self._save_settings()
        name = f"{self.input_folder.name}_merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.is_processing = True
        self._result_dialog_shown = False
        self.merge_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self._set_progress(0, "Exporting...")
        self.status_label.configure(text="Exporting...")
        threading.Thread(target=self._merge_thread, args=(self.input_folder, name, formats), daemon=True).start()

    def _merge_thread(self, input_folder: Path, output_name: str, formats: list) -> None:
        try:
            self._set_progress(15, "Merging files...")
            merged = self.file_merger.merge_files(input_folder)
            if not merged:
                self._set_progress(0, "Failed - no content")
                self._show_dialog_once("error", "Export Failed", "No content to export.")
                return
            base_name = self._build_output_base_name(merged, output_name)
            self._set_progress(40, "Preparing export...")
            success = 0
            failed: list[str] = []
            for i, fmt in enumerate(formats):
                if fmt == "docx":
                    self._set_progress(45 + i * 25, "Exporting DOCX...")
                    ok, path = DocxExporter(self.config).export(
                        merged,
                        self.output_folder / f"{base_name}.docx",
                        font_name=self.font_var.get(),
                    )
                    if ok and path and path.exists():
                        success += 1
                    else:
                        failed.append("DOCX")
                elif fmt == "pdf":
                    self._set_progress(45 + i * 25, "Exporting PDF...")
                    ok, path = PdfExporter(self.config).export(
                        merged,
                        self.output_folder / f"{base_name}.pdf",
                        font_name=self.font_var.get(),
                    )
                    if ok and path and path.exists():
                        success += 1
                    else:
                        failed.append("PDF")
                elif fmt == "epub":
                    self._set_progress(45 + i * 25, "Exporting EPUB...")
                    ok, path = EpubExporter(self.config).export(
                        merged,
                        self.output_folder / f"{base_name}.epub",
                    )
                    if ok and path and path.exists():
                        success += 1
                    else:
                        failed.append("EPUB")
                self._set_progress(min(95, 40 + int((i + 1) * (55 / max(1, len(formats))))), self.progress_label.cget("text"))

            if success > 0:
                self._set_progress(100, "Completed")
                self._ui(self.status_label.configure, text=f"Completed | {success}/{len(formats)} format(s)")
                if failed:
                    self._show_dialog_once("warning", "Partial Success", f"Success: {success}/{len(formats)}\nFailed: {', '.join(failed)}")
                else:
                    self._show_dialog_once("info", "Success", f"Completed: {success}/{len(formats)} format(s)")
            else:
                self._set_progress(0, "Failed - export error")
                self._show_dialog_once("error", "Export Failed", "No output format was exported successfully.")
        except Exception as exc:
            self.logger.exception("Critical merge thread error")
            self._add_log_message(traceback.format_exc())
            self._set_progress(0, "Failed - internal error")
            self._show_dialog_once("error", "Error", f"Merge failed:\n{exc}")
        finally:
            self.is_processing = False
            self._ui(self.merge_btn.configure, state="normal")
            self._ui(self.cancel_btn.configure, state="disabled")
            if "Completed" not in self.status_label.cget("text"):
                self._ui(self.status_label.configure, text="Ready")

    def _cancel_merge(self) -> None:
        self.is_processing = False
        self._set_progress(0, "Cancelled")
        self.merge_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.status_label.configure(text="Ready")
        messagebox.showinfo("Cancelled", "Merge operation cancelled")

    def _add_log_message(self, message: str) -> None:
        def _write() -> None:
            self.log_text.configure(state="normal")
            self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        self._ui(_write)

    def _ui(self, fn, *args, **kwargs) -> None:
        self.root.after(0, lambda: fn(*args, **kwargs))

    def _set_progress(self, percent: int, label: str) -> None:
        p = max(0, min(100, percent))
        self._ui(self.progress_var.set, p / 100.0)
        self._ui(self.progress_percent.configure, text=f"{p}%")
        self._ui(self.progress_label.configure, text=label)

    def _show_dialog_once(self, level: str, title: str, message: str) -> None:
        if self._result_dialog_shown:
            return
        self._result_dialog_shown = True
        if level == "info":
            self._ui(messagebox.showinfo, title, message)
        elif level == "warning":
            self._ui(messagebox.showwarning, title, message)
        else:
            self._ui(messagebox.showerror, title, message)

    def _on_window_resize(self, _event) -> None:
        width = max(self.root.winfo_width(), 980)
        self.root.tk.call("tk", "scaling", 0.95 if width < 1100 else 1.0)

    def _build_output_base_name(self, content: str, fallback_name: str) -> str:
        chapter_numbers = re.findall(r"บทที่\s*(\d+)", content)
        if chapter_numbers:
            return f"บทที่ {chapter_numbers[0]} - บทที่ {chapter_numbers[-1]}"
        english_chapters = re.findall(r"chapter\s*(\d+)", content, flags=re.IGNORECASE)
        if english_chapters:
            return f"chapter {english_chapters[0]} - chapter {english_chapters[-1]}"
        return fallback_name

    def _parse_custom_spam_keywords(self) -> list[str]:
        raw = self.spam_text.get("1.0", "end").strip()
        if not raw:
            return []
        return [line.strip() for line in raw.splitlines() if line.strip()]

    def _get_settings_path(self) -> Path:
        appdata = os.getenv("APPDATA")
        if appdata:
            base = Path(appdata) / "TextMergeApp"
        else:
            base = Path.home() / ".textmergeapp"
        base.mkdir(parents=True, exist_ok=True)
        return base / "settings.json"

    def _save_settings(self) -> None:
        try:
            payload = {
                "input_folder": str(self.input_folder) if self.input_folder else "",
                "output_folder": str(self.output_folder),
                "font_name": self.font_var.get(),
                "extra_spam_keywords": self._parse_custom_spam_keywords(),
            }
            self.settings_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as e:
            self.logger.warning(f"Failed to save settings: {e}")

    def _load_settings(self) -> None:
        if not self.settings_path.exists():
            return
        try:
            data = json.loads(self.settings_path.read_text(encoding="utf-8"))

            input_folder = data.get("input_folder", "")
            if input_folder:
                candidate = Path(input_folder)
                if candidate.exists():
                    self.input_folder = candidate
                    self._update_input_label()

            output_folder = data.get("output_folder", "")
            if output_folder:
                self.output_folder = Path(output_folder)
                self.output_label.configure(text=str(self.output_folder))

            saved_font = data.get("font_name", "")
            if saved_font and hasattr(self, "font_combo") and saved_font in self.font_combo.cget("values"):
                self.font_var.set(saved_font)

            keywords = data.get("extra_spam_keywords", [])
            if isinstance(keywords, list) and keywords:
                self.spam_text.delete("1.0", "end")
                self.spam_text.insert("1.0", "\n".join([str(k) for k in keywords if str(k).strip()]))
                set_extra_spam_keywords(self._parse_custom_spam_keywords())
        except Exception as e:
            self.logger.warning(f"Failed to load settings: {e}")

    def _on_font_change(self, _value: str) -> None:
        self._save_settings()

    def _on_close(self) -> None:
        self._save_settings()
        self.root.destroy()


def run_gui() -> None:
    root = ctk.CTk()
    TextMergeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
