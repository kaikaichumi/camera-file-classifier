"""日期選擇器元件"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, date
import calendar
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.i18n import t, i18n


class DatePickerDialog(tk.Toplevel):
    """日期選擇對話框"""

    def __init__(self, parent, initial_date: date | None = None):
        super().__init__(parent)
        self.title(t('select_date'))
        self.result: date | None = None

        # 設定視窗屬性
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        # 目前顯示的年月
        today = date.today()
        self.current_date = initial_date or today
        self.display_year = self.current_date.year
        self.display_month = self.current_date.month

        self._create_widgets()

        # 置中
        self.geometry("300x320")
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.wait_window()

    def _create_widgets(self):
        """建立元件"""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 年月導覽
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(nav_frame, text="◀", width=3, command=self._prev_month).pack(side=tk.LEFT)

        self.month_label = ttk.Label(
            nav_frame,
            text="",
            font=("Microsoft JhengHei UI", 12, "bold"),
            anchor=tk.CENTER
        )
        self.month_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        ttk.Button(nav_frame, text="▶", width=3, command=self._next_month).pack(side=tk.RIGHT)

        # 星期標題
        self.weekday_frame = ttk.Frame(main_frame)
        self.weekday_frame.pack(fill=tk.X)
        self._update_weekday_labels()

        # 日期按鈕區
        self.calendar_frame = ttk.Frame(main_frame)
        self.calendar_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # 底部按鈕
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text=t('today'), command=self._select_today).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text=t('clear'), command=self._clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=t('cancel'), command=self._on_cancel).pack(side=tk.RIGHT)

        self._update_calendar()

    def _update_weekday_labels(self):
        """更新星期標籤"""
        for widget in self.weekday_frame.winfo_children():
            widget.destroy()

        weekdays = t('weekdays')
        for day in weekdays:
            lbl = ttk.Label(
                self.weekday_frame,
                text=day,
                width=4,
                anchor=tk.CENTER,
                font=("Microsoft JhengHei UI", 9)
            )
            lbl.pack(side=tk.LEFT, expand=True)

    def _update_calendar(self):
        """更新日曆顯示"""
        # 清除舊的日期按鈕
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # 更新標題
        if i18n.current_lang == 'en':
            month_name = i18n.get_month_name(self.display_month)
            self.month_label.config(text=f"{month_name} {self.display_year}")
        else:
            self.month_label.config(text=t('year_month', year=self.display_year, month=self.display_month))

        # 取得該月資訊
        cal = calendar.Calendar(firstweekday=6)  # 星期日開始
        month_days = cal.monthdayscalendar(self.display_year, self.display_month)

        today = date.today()

        for week in month_days:
            week_frame = ttk.Frame(self.calendar_frame)
            week_frame.pack(fill=tk.X)

            for day in week:
                if day == 0:
                    # 空白
                    lbl = ttk.Label(week_frame, text="", width=4)
                    lbl.pack(side=tk.LEFT, expand=True)
                else:
                    btn = tk.Button(
                        week_frame,
                        text=str(day),
                        width=3,
                        relief=tk.FLAT,
                        command=lambda d=day: self._select_day(d)
                    )

                    # 標記今天
                    if (self.display_year == today.year and
                        self.display_month == today.month and
                        day == today.day):
                        btn.config(bg="#e0e0ff")

                    # 標記已選日期
                    if (self.current_date and
                        self.display_year == self.current_date.year and
                        self.display_month == self.current_date.month and
                        day == self.current_date.day):
                        btn.config(bg="#4a90d9", fg="white")

                    btn.pack(side=tk.LEFT, expand=True, padx=1, pady=1)

    def _prev_month(self):
        """上個月"""
        if self.display_month == 1:
            self.display_month = 12
            self.display_year -= 1
        else:
            self.display_month -= 1
        self._update_calendar()

    def _next_month(self):
        """下個月"""
        if self.display_month == 12:
            self.display_month = 1
            self.display_year += 1
        else:
            self.display_month += 1
        self._update_calendar()

    def _select_day(self, day: int):
        """選擇日期"""
        self.result = date(self.display_year, self.display_month, day)
        self.destroy()

    def _select_today(self):
        """選擇今天"""
        self.result = date.today()
        self.destroy()

    def _clear(self):
        """清除日期"""
        self.result = None
        self.destroy()

    def _on_cancel(self):
        """取消"""
        self.result = self.current_date  # 保持原值
        self.destroy()


class DatePickerEntry(ttk.Frame):
    """日期選擇輸入框"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        self._date: date | None = None
        self._enabled = True

        # 日期顯示
        self.date_var = tk.StringVar(value=t('not_selected'))
        self.entry = ttk.Entry(self, textvariable=self.date_var, width=12, state='readonly')
        self.entry.pack(side=tk.LEFT)

        # 選擇按鈕
        self.btn = ttk.Button(self, text="📅", width=3, command=self._show_picker)
        self.btn.pack(side=tk.LEFT, padx=(2, 0))

    def _show_picker(self):
        """顯示日期選擇器"""
        if not self._enabled:
            return

        dialog = DatePickerDialog(self.winfo_toplevel(), self._date)
        if dialog.result is not None:
            self._date = dialog.result
            self.date_var.set(self._date.strftime("%Y-%m-%d"))
        elif dialog.result is None and self._date is not None:
            # 使用者按了清除
            self._date = None
            self.date_var.set(t('not_selected'))

    def get_date(self) -> date | None:
        """取得選擇的日期"""
        return self._date

    def set_date(self, d: date | None):
        """設定日期"""
        self._date = d
        if d:
            self.date_var.set(d.strftime("%Y-%m-%d"))
        else:
            self.date_var.set(t('not_selected'))

    def set_enabled(self, enabled: bool):
        """設定啟用狀態"""
        self._enabled = enabled
        state = 'normal' if enabled else 'disabled'
        self.btn.config(state=state)
        # 變更外觀以顯示停用狀態
        if enabled:
            self.entry.config(foreground='black')
        else:
            self.entry.config(foreground='gray')

    def update_text(self):
        """更新文字（語言變更時呼叫）"""
        if self._date is None:
            self.date_var.set(t('not_selected'))
