"""多語言支援模組"""

import json
from pathlib import Path

# 語言字串定義
TRANSLATIONS = {
    'zh-TW': {
        'app_title': '相機檔案分類工具',
        'source_folder': '來源資料夾',
        'dest_folder': '目標資料夾',
        'browse': '瀏覽...',
        'file_filter': '檔案篩選',
        'all_files': '全部檔案',
        'date_range': '日期區間',
        'start': '開始:',
        'end': '結束:',
        'not_selected': '未選擇',
        'classification': '分類方式',
        'classification_info': '''檔案將依類型分類到以下子資料夾:
• RAW 檔案 (.ARW, .CR2, .CR3, .NEF, .RAF, .DNG 等) → /RAW
• JPG 檔案 (.JPG, .JPEG) → /JPG
• HEIC 檔案 (.HEIC, .HEIF, .HIF) → /HEIC
• 影片檔案 (.MOV, .MP4, .AVI 等) → /VIDEO''',
        'scan_result': '掃描結果',
        'not_scanned': '尚未掃描',
        'scan_files': '掃描檔案',
        'start_classify': '開始分類',
        'cancel': '取消',
        'status': '狀態',
        'ready': '就緒',
        'scanning': '掃描中...',
        'scan_complete': '掃描完成',
        'scan_failed': '掃描失敗',
        'copying': '正在複製',
        'cancelling': '正在取消...',
        'cancelled': '已取消',
        'complete': '完成',
        'warning': '警告',
        'error': '錯誤',
        'confirm': '確認',
        'select_source': '請選擇來源資料夾',
        'select_dest': '請選擇目標資料夾',
        'source_not_exist': '來源資料夾不存在',
        'scan_first': '請先掃描檔案',
        'confirm_copy': '即將複製 {count} 個檔案到:\n{dest}\n\n確定要開始嗎?',
        'copy_complete': '''複製完成！

總計: {total} 個檔案
已複製: {copied} 個
已略過: {skipped} 個
已覆蓋: {overwritten} 個
已重新命名: {renamed} 個
失敗: {failed} 個''',
        'operation_cancelled': '操作已取消',
        'copy_failed': '複製失敗: {error}',
        'total_files': '共 {count} 個檔案',
        'settings': '設定',
        'language': '語言',
        'select_date': '選擇日期',
        'today': '今天',
        'clear': '清除',
        'year_month': '{year} 年 {month} 月',
        'weekdays': ['日', '一', '二', '三', '四', '五', '六'],
        'file_exists': '檔案已存在',
        'file_exists_msg': '目標位置已有同名檔案，請選擇處理方式：',
        'file_info': '檔案資訊',
        'filename': '檔案名稱',
        'dest_path': '目標位置',
        'skip': '略過',
        'overwrite': '覆蓋',
        'rename': '重新命名',
        'skip_all': '全部略過',
        'overwrite_all': '全部覆蓋',
        'rename_all': '全部重新命名',
        'apply_to_all': '套用到全部:',
    },
    'en': {
        'app_title': 'Camera File Classifier',
        'source_folder': 'Source Folder',
        'dest_folder': 'Destination Folder',
        'browse': 'Browse...',
        'file_filter': 'File Filter',
        'all_files': 'All Files',
        'date_range': 'Date Range',
        'start': 'Start:',
        'end': 'End:',
        'not_selected': 'Not Selected',
        'classification': 'Classification',
        'classification_info': '''Files will be classified into subfolders:
• RAW files (.ARW, .CR2, .CR3, .NEF, .RAF, .DNG, etc.) → /RAW
• JPG files (.JPG, .JPEG) → /JPG
• HEIC files (.HEIC, .HEIF, .HIF) → /HEIC
• Video files (.MOV, .MP4, .AVI, etc.) → /VIDEO''',
        'scan_result': 'Scan Result',
        'not_scanned': 'Not Scanned',
        'scan_files': 'Scan Files',
        'start_classify': 'Start Classify',
        'cancel': 'Cancel',
        'status': 'Status',
        'ready': 'Ready',
        'scanning': 'Scanning...',
        'scan_complete': 'Scan Complete',
        'scan_failed': 'Scan Failed',
        'copying': 'Copying',
        'cancelling': 'Cancelling...',
        'cancelled': 'Cancelled',
        'complete': 'Complete',
        'warning': 'Warning',
        'error': 'Error',
        'confirm': 'Confirm',
        'select_source': 'Please select source folder',
        'select_dest': 'Please select destination folder',
        'source_not_exist': 'Source folder does not exist',
        'scan_first': 'Please scan files first',
        'confirm_copy': 'About to copy {count} files to:\n{dest}\n\nProceed?',
        'copy_complete': '''Copy Complete!

Total: {total} files
Copied: {copied}
Skipped: {skipped}
Overwritten: {overwritten}
Renamed: {renamed}
Failed: {failed}''',
        'operation_cancelled': 'Operation cancelled',
        'copy_failed': 'Copy failed: {error}',
        'total_files': '{count} files total',
        'settings': 'Settings',
        'language': 'Language',
        'select_date': 'Select Date',
        'today': 'Today',
        'clear': 'Clear',
        'year_month': '{month} {year}',
        'weekdays': ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        'file_exists': 'File Exists',
        'file_exists_msg': 'A file with the same name already exists. Choose an action:',
        'file_info': 'File Info',
        'filename': 'Filename',
        'dest_path': 'Destination',
        'skip': 'Skip',
        'overwrite': 'Overwrite',
        'rename': 'Rename',
        'skip_all': 'Skip All',
        'overwrite_all': 'Overwrite All',
        'rename_all': 'Rename All',
        'apply_to_all': 'Apply to all:',
    }
}

MONTH_NAMES = {
    'en': ['', 'January', 'February', 'March', 'April', 'May', 'June',
           'July', 'August', 'September', 'October', 'November', 'December']
}


class I18n:
    """多語言管理類別"""

    _instance = None
    _current_lang = 'zh-TW'
    _config_file = Path(__file__).parent.parent / 'config.json'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """載入設定"""
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self._current_lang = config.get('language', 'zh-TW')
        except Exception:
            pass

    def _save_config(self):
        """儲存設定"""
        try:
            config = {'language': self._current_lang}
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    @property
    def current_lang(self) -> str:
        return self._current_lang

    def set_language(self, lang: str):
        """設定語言"""
        if lang in TRANSLATIONS:
            self._current_lang = lang
            self._save_config()

    def get(self, key: str, **kwargs) -> str:
        """取得翻譯字串"""
        text = TRANSLATIONS.get(self._current_lang, TRANSLATIONS['zh-TW']).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass
        return text

    def get_month_name(self, month: int) -> str:
        """取得月份名稱（英文用）"""
        if self._current_lang == 'en':
            return MONTH_NAMES['en'][month]
        return str(month)

    @staticmethod
    def get_available_languages() -> dict:
        """取得可用語言列表"""
        return {
            'zh-TW': '繁體中文',
            'en': 'English'
        }


# 全域實例
i18n = I18n()


def t(key: str, **kwargs) -> str:
    """翻譯快捷函數"""
    return i18n.get(key, **kwargs)
