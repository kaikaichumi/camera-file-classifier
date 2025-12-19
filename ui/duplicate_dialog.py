"""重複檔案處理對話框"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.file_copier import DuplicateAction
from core.i18n import t


class DuplicateDialog(tk.Toplevel):
    """重複檔案處理對話框"""

    def __init__(self, parent, src_path: str, dest_path: str):
        super().__init__(parent)
        self.title(t('file_exists'))
        self.result = DuplicateAction.SKIP

        # 設定視窗屬性
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        # 置中顯示
        self.geometry("500x280")
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        self._create_widgets(src_path, dest_path)

        # 等待視窗關閉
        self.protocol("WM_DELETE_WINDOW", self._on_skip)
        self.wait_window()

    def _create_widgets(self, src_path: str, dest_path: str):
        """建立介面元件"""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 警告圖示與訊息
        msg_frame = ttk.Frame(main_frame)
        msg_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(
            msg_frame,
            text="⚠️",
            font=("Segoe UI", 24)
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(
            msg_frame,
            text=t('file_exists_msg'),
            font=("Microsoft JhengHei UI", 11)
        ).pack(side=tk.LEFT)

        # 檔案資訊
        info_frame = ttk.LabelFrame(main_frame, text=t('file_info'), padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 15))

        src_name = Path(src_path).name
        ttk.Label(
            info_frame,
            text=f"{t('filename')}: {src_name}",
            font=("Microsoft JhengHei UI", 9)
        ).pack(anchor=tk.W)

        ttk.Label(
            info_frame,
            text=f"{t('dest_path')}: {dest_path}",
            font=("Microsoft JhengHei UI", 9),
            wraplength=440
        ).pack(anchor=tk.W, pady=(5, 0))

        # 按鈕區域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)

        # 第一排按鈕（單次操作）
        row1 = ttk.Frame(btn_frame)
        row1.pack(fill=tk.X, pady=(0, 8))

        ttk.Button(row1, text=t('skip'), width=12, command=self._on_skip).pack(side=tk.LEFT, padx=2)
        ttk.Button(row1, text=t('overwrite'), width=12, command=self._on_overwrite).pack(side=tk.LEFT, padx=2)
        ttk.Button(row1, text=t('rename'), width=12, command=self._on_rename).pack(side=tk.LEFT, padx=2)
        ttk.Button(row1, text=t('cancel'), width=12, command=self._on_cancel).pack(side=tk.RIGHT, padx=2)

        # 第二排按鈕（套用到全部）
        row2 = ttk.Frame(btn_frame)
        row2.pack(fill=tk.X)

        ttk.Label(row2, text=t('apply_to_all'), font=("Microsoft JhengHei UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(row2, text=t('skip_all'), width=10, command=self._on_skip_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(row2, text=t('overwrite_all'), width=10, command=self._on_overwrite_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(row2, text=t('rename_all'), width=12, command=self._on_rename_all).pack(side=tk.LEFT, padx=2)

    def _on_skip(self):
        self.result = DuplicateAction.SKIP
        self.destroy()

    def _on_overwrite(self):
        self.result = DuplicateAction.OVERWRITE
        self.destroy()

    def _on_rename(self):
        self.result = DuplicateAction.RENAME
        self.destroy()

    def _on_skip_all(self):
        self.result = DuplicateAction.SKIP_ALL
        self.destroy()

    def _on_overwrite_all(self):
        self.result = DuplicateAction.OVERWRITE_ALL
        self.destroy()

    def _on_rename_all(self):
        self.result = DuplicateAction.RENAME_ALL
        self.destroy()

    def _on_cancel(self):
        self.result = DuplicateAction.CANCEL
        self.destroy()
