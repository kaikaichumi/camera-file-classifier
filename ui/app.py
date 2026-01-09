"""主應用程式 GUI"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from pathlib import Path
import threading
import os

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.file_scanner import FileScanner
from core.file_copier import FileCopier, DuplicateAction
from core.i18n import t, i18n, I18n
from ui.duplicate_dialog import DuplicateDialog
from ui.date_picker import DatePickerEntry


class CameraFileClassifierApp:
    """相機檔案分類工具主視窗"""

    def __init__(self):
        # 設置 Windows 任務欄圖標 (必須在創建窗口之前設置)
        if sys.platform == 'win32':
            try:
                import ctypes
                myappid = 'mycompany.camerafileclassifier.1.0'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except (ImportError, Exception):
                pass  # ctypes 不可用時忽略

        self.root = tk.Tk()
        self.root.title(t('app_title'))
        self.root.geometry("620x580")
        self.root.resizable(False, False)

        # 設置窗口圖標
        try:
            if getattr(sys, 'frozen', False):
                # 打包後的路徑
                base_path = sys._MEIPASS
            else:
                # 開發環境的路徑
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            icon_path = os.path.join(base_path, 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            pass  # 如果圖標載入失敗，不影響程序運行

        # 變數
        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()
        self.filter_mode = tk.StringVar(value="all")
        self.lang_var = tk.StringVar(value=i18n.current_lang)

        # 掃描結果
        self.scanned_files = []
        self.is_running = False

        # 儲存 UI 元件參考
        self.ui_elements = {}

        self._create_widgets()
        self._center_window()

    def _center_window(self):
        """視窗置中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """建立介面元件"""
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # === 設定區（語言選擇）===
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        # 先建立 combo（會在右邊）
        lang_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.lang_var,
            values=list(I18n.get_available_languages().values()),
            state='readonly',
            width=12
        )
        lang_combo.pack(side=tk.RIGHT)

        # 再建立 label（會在 combo 左邊）
        self.ui_elements['lang_label'] = ttk.Label(settings_frame, text=t('language') + ":")
        self.ui_elements['lang_label'].pack(side=tk.RIGHT, padx=(0, 5))

        # 設定目前語言顯示
        lang_names = I18n.get_available_languages()
        lang_combo.set(lang_names.get(i18n.current_lang, '繁體中文'))
        lang_combo.bind('<<ComboboxSelected>>', self._on_language_change)
        self.lang_combo = lang_combo

        # === 來源資料夾 ===
        self.ui_elements['src_frame'] = ttk.LabelFrame(main_frame, text=t('source_folder'), padding=10)
        self.ui_elements['src_frame'].pack(fill=tk.X, pady=(0, 10))

        ttk.Entry(self.ui_elements['src_frame'], textvariable=self.source_var, width=58).pack(side=tk.LEFT, padx=(0, 10))
        self.ui_elements['src_btn'] = ttk.Button(self.ui_elements['src_frame'], text=t('browse'), command=self._browse_source)
        self.ui_elements['src_btn'].pack(side=tk.LEFT)

        # === 目標資料夾 ===
        self.ui_elements['dest_frame'] = ttk.LabelFrame(main_frame, text=t('dest_folder'), padding=10)
        self.ui_elements['dest_frame'].pack(fill=tk.X, pady=(0, 10))

        ttk.Entry(self.ui_elements['dest_frame'], textvariable=self.dest_var, width=58).pack(side=tk.LEFT, padx=(0, 10))
        self.ui_elements['dest_btn'] = ttk.Button(self.ui_elements['dest_frame'], text=t('browse'), command=self._browse_dest)
        self.ui_elements['dest_btn'].pack(side=tk.LEFT)

        # === 檔案篩選 ===
        self.ui_elements['filter_frame'] = ttk.LabelFrame(main_frame, text=t('file_filter'), padding=10)
        self.ui_elements['filter_frame'].pack(fill=tk.X, pady=(0, 10))

        self.ui_elements['all_radio'] = ttk.Radiobutton(
            self.ui_elements['filter_frame'],
            text=t('all_files'),
            variable=self.filter_mode,
            value="all",
            command=self._on_filter_change
        )
        self.ui_elements['all_radio'].pack(anchor=tk.W)

        date_row = ttk.Frame(self.ui_elements['filter_frame'])
        date_row.pack(fill=tk.X, pady=(5, 0))

        self.ui_elements['date_radio'] = ttk.Radiobutton(
            date_row,
            text=t('date_range'),
            variable=self.filter_mode,
            value="date_range",
            command=self._on_filter_change
        )
        self.ui_elements['date_radio'].pack(side=tk.LEFT)

        self.ui_elements['start_label'] = ttk.Label(date_row, text="  " + t('start'))
        self.ui_elements['start_label'].pack(side=tk.LEFT)
        self.start_date_picker = DatePickerEntry(date_row)
        self.start_date_picker.pack(side=tk.LEFT, padx=(5, 10))
        self.start_date_picker.set_enabled(False)

        self.ui_elements['end_label'] = ttk.Label(date_row, text=t('end'))
        self.ui_elements['end_label'].pack(side=tk.LEFT)
        self.end_date_picker = DatePickerEntry(date_row)
        self.end_date_picker.pack(side=tk.LEFT, padx=(5, 0))
        self.end_date_picker.set_enabled(False)

        # === 分類說明 ===
        self.ui_elements['info_frame'] = ttk.LabelFrame(main_frame, text=t('classification'), padding=10)
        self.ui_elements['info_frame'].pack(fill=tk.X, pady=(0, 10))

        self.ui_elements['info_label'] = ttk.Label(
            self.ui_elements['info_frame'],
            text=t('classification_info'),
            font=("Microsoft JhengHei UI", 9),
            justify=tk.LEFT
        )
        self.ui_elements['info_label'].pack(anchor=tk.W)

        # === 掃描結果 ===
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.X, pady=(0, 10))

        self.result_label = ttk.Label(
            result_frame,
            text=f"{t('scan_result')}: {t('not_scanned')}",
            font=("Microsoft JhengHei UI", 10)
        )
        self.result_label.pack(anchor=tk.W)

        # === 按鈕 ===
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        self.scan_btn = ttk.Button(btn_frame, text=t('scan_files'), command=self._scan_files, width=15)
        self.scan_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.start_btn = ttk.Button(btn_frame, text=t('start_classify'), command=self._start_classify, width=15, state='disabled')
        self.start_btn.pack(side=tk.LEFT)

        self.cancel_btn = ttk.Button(btn_frame, text=t('cancel'), command=self._cancel, width=10, state='disabled')
        self.cancel_btn.pack(side=tk.RIGHT)

        # === 進度條 ===
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        self.status_label = ttk.Label(
            progress_frame,
            text=f"{t('status')}: {t('ready')}",
            font=("Microsoft JhengHei UI", 9)
        )
        self.status_label.pack(anchor=tk.W)

    def _on_language_change(self, event):
        """語言變更"""
        selected = self.lang_combo.get()
        lang_map = {v: k for k, v in I18n.get_available_languages().items()}
        new_lang = lang_map.get(selected, 'zh-TW')

        if new_lang != i18n.current_lang:
            i18n.set_language(new_lang)
            self._update_ui_texts()

    def _update_ui_texts(self):
        """更新所有 UI 文字"""
        self.root.title(t('app_title'))

        # 更新標籤和按鈕
        self.ui_elements['lang_label'].config(text=t('language') + ":")
        self.ui_elements['src_frame'].config(text=t('source_folder'))
        self.ui_elements['src_btn'].config(text=t('browse'))
        self.ui_elements['dest_frame'].config(text=t('dest_folder'))
        self.ui_elements['dest_btn'].config(text=t('browse'))
        self.ui_elements['filter_frame'].config(text=t('file_filter'))
        self.ui_elements['all_radio'].config(text=t('all_files'))
        self.ui_elements['date_radio'].config(text=t('date_range'))
        self.ui_elements['start_label'].config(text="  " + t('start'))
        self.ui_elements['end_label'].config(text=t('end'))
        self.ui_elements['info_frame'].config(text=t('classification'))
        self.ui_elements['info_label'].config(text=t('classification_info'))

        self.scan_btn.config(text=t('scan_files'))
        self.start_btn.config(text=t('start_classify'))
        self.cancel_btn.config(text=t('cancel'))

        # 更新狀態
        if not self.is_running:
            self.status_label.config(text=f"{t('status')}: {t('ready')}")

        # 更新掃描結果
        if not self.scanned_files:
            self.result_label.config(text=f"{t('scan_result')}: {t('not_scanned')}")

        # 更新日期選擇器
        self.start_date_picker.update_text()
        self.end_date_picker.update_text()

    def _browse_source(self):
        """選擇來源資料夾"""
        path = filedialog.askdirectory(title=t('source_folder'))
        if path:
            self.source_var.set(path)
            self.scanned_files = []
            self.result_label.config(text=f"{t('scan_result')}: {t('not_scanned')}")
            self.start_btn.config(state='disabled')

    def _browse_dest(self):
        """選擇目標資料夾"""
        path = filedialog.askdirectory(title=t('dest_folder'))
        if path:
            self.dest_var.set(path)

    def _on_filter_change(self):
        """篩選模式改變"""
        if self.filter_mode.get() == "date_range":
            self.start_date_picker.set_enabled(True)
            self.end_date_picker.set_enabled(True)
        else:
            self.start_date_picker.set_enabled(False)
            self.end_date_picker.set_enabled(False)

    def _scan_files(self):
        """掃描檔案"""
        source = self.source_var.get()
        if not source:
            messagebox.showwarning(t('warning'), t('select_source'))
            return

        if not Path(source).exists():
            messagebox.showerror(t('error'), t('source_not_exist'))
            return

        # 取得日期
        start_date = None
        end_date = None
        if self.filter_mode.get() == "date_range":
            start_d = self.start_date_picker.get_date()
            end_d = self.end_date_picker.get_date()
            if start_d:
                start_date = datetime.combine(start_d, datetime.min.time())
            if end_d:
                end_date = datetime.combine(end_d, datetime.max.time())

        self.status_label.config(text=f"{t('status')}: {t('scanning')}")
        self.root.update()

        try:
            scanner = FileScanner(source)
            self.scanned_files = scanner.scan(start_date, end_date)
            summary = scanner.get_summary(self.scanned_files)

            # 顯示結果
            result_parts = []
            for cat in ['RAW', 'JPG', 'HEIC', 'VIDEO']:
                count = summary.get(cat, 0)
                result_parts.append(f"{cat}: {count}")

            total = len(self.scanned_files)
            self.result_label.config(text=f"{t('scan_result')}: {' | '.join(result_parts)} ({t('total_files', count=total)})")

            if total > 0:
                self.start_btn.config(state='normal')
            else:
                self.start_btn.config(state='disabled')

            self.status_label.config(text=f"{t('status')}: {t('scan_complete')}")

        except Exception as e:
            messagebox.showerror(t('error'), t('copy_failed', error=str(e)))
            self.status_label.config(text=f"{t('status')}: {t('scan_failed')}")

    def _start_classify(self):
        """開始分類"""
        dest = self.dest_var.get()
        if not dest:
            messagebox.showwarning(t('warning'), t('select_dest'))
            return

        if not self.scanned_files:
            messagebox.showwarning(t('warning'), t('scan_first'))
            return

        # 確認
        total = len(self.scanned_files)
        if not messagebox.askyesno(t('confirm'), t('confirm_copy', count=total, dest=dest)):
            return

        self.is_running = True
        self._set_running_state(True)

        # 在背景執行緒執行複製
        thread = threading.Thread(target=self._do_classify, args=(dest,))
        thread.daemon = True
        thread.start()

    def _do_classify(self, dest: str):
        """執行分類（在背景執行緒）"""
        import queue

        # 使用 queue 来同步对话框结果
        dialog_queue = queue.Queue()

        def on_duplicate(src: str, dest: str) -> DuplicateAction:
            # 在主執行緒顯示對話框
            def show_dialog():
                dialog = DuplicateDialog(self.root, src, dest)
                dialog_queue.put(dialog.result)

            self.root.after(0, show_dialog)

            # 等待對話框結果（使用 queue.get() 会阻塞直到有结果，不会卡死UI）
            try:
                result = dialog_queue.get(timeout=300)  # 最多等待5分钟
                return result
            except queue.Empty:
                return DuplicateAction.SKIP

        def on_progress(current: int, total: int, filename: str):
            progress = (current / total) * 100
            self.root.after(0, lambda: self._update_progress(progress, filename, current, total))

        try:
            copier = FileCopier(dest, on_duplicate=on_duplicate, on_progress=on_progress)
            result = copier.copy_files(self.scanned_files)

            # 顯示結果
            self.root.after(0, lambda: self._show_result(result))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(t('error'), t('copy_failed', error=str(e))))

        finally:
            self.root.after(0, lambda: self._set_running_state(False))
            self.is_running = False

    def _update_progress(self, progress: float, filename: str, current: int, total: int):
        """更新進度"""
        self.progress_var.set(progress)
        self.status_label.config(text=f"{t('status')}: {t('copying')} ({current}/{total}) {filename}")

    def _show_result(self, result: dict):
        """顯示結果"""
        self.progress_var.set(100)

        if result['cancelled']:
            self.status_label.config(text=f"{t('status')}: {t('cancelled')}")
            messagebox.showinfo(t('cancel'), t('operation_cancelled'))
        else:
            self.status_label.config(text=f"{t('status')}: {t('complete')}")
            msg = t('copy_complete',
                   total=result['total'],
                   copied=result['copied'],
                   skipped=result['skipped'],
                   overwritten=result['overwritten'],
                   renamed=result['renamed'],
                   failed=result['failed'])
            messagebox.showinfo(t('complete'), msg)

    def _cancel(self):
        """取消操作"""
        self.is_running = False
        self.status_label.config(text=f"{t('status')}: {t('cancelling')}")

    def _set_running_state(self, running: bool):
        """設定執行狀態"""
        if running:
            self.scan_btn.config(state='disabled')
            self.start_btn.config(state='disabled')
            self.cancel_btn.config(state='normal')
        else:
            self.scan_btn.config(state='normal')
            self.start_btn.config(state='normal' if self.scanned_files else 'disabled')
            self.cancel_btn.config(state='disabled')

    def run(self):
        """啟動應用程式"""
        self.root.mainloop()


def main():
    app = CameraFileClassifierApp()
    app.run()


if __name__ == "__main__":
    main()
