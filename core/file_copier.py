"""檔案複製模組 - 複製檔案並處理重複"""

import shutil
from pathlib import Path
from enum import Enum
from typing import Callable

from .file_scanner import ScannedFile


class DuplicateAction(Enum):
    """重複檔案處理方式"""
    SKIP = "skip"           # 略過
    OVERWRITE = "overwrite" # 覆蓋
    RENAME = "rename"       # 重新命名
    SKIP_ALL = "skip_all"   # 全部略過
    OVERWRITE_ALL = "overwrite_all"  # 全部覆蓋
    RENAME_ALL = "rename_all"        # 全部重新命名
    CANCEL = "cancel"       # 取消操作


class FileCopier:
    """檔案複製器"""

    def __init__(
        self,
        dest_dir: str,
        on_duplicate: Callable[[str, str], DuplicateAction] | None = None,
        on_progress: Callable[[int, int, str], None] | None = None
    ):
        """
        初始化複製器

        Args:
            dest_dir: 目標資料夾
            on_duplicate: 遇到重複檔案時的回調函數，傳入 (來源路徑, 目標路徑)，回傳處理方式
            on_progress: 進度回調函數，傳入 (目前索引, 總數, 檔案名稱)
        """
        self.dest_dir = Path(dest_dir)
        self.on_duplicate = on_duplicate
        self.on_progress = on_progress
        self._global_action: DuplicateAction | None = None
        self._cancelled = False

    def copy_files(self, files: list[ScannedFile]) -> dict:
        """
        複製檔案到目標資料夾

        Args:
            files: 要複製的檔案列表

        Returns:
            複製結果統計
        """
        self._global_action = None
        self._cancelled = False

        result = {
            'total': len(files),
            'copied': 0,
            'skipped': 0,
            'overwritten': 0,
            'renamed': 0,
            'failed': 0,
            'cancelled': False
        }

        for i, file in enumerate(files):
            if self._cancelled:
                result['cancelled'] = True
                break

            # 回報進度
            if self.on_progress:
                self.on_progress(i + 1, len(files), file.filename)

            # 建立目標路徑
            category_dir = self.dest_dir / file.category
            category_dir.mkdir(parents=True, exist_ok=True)
            dest_path = category_dir / file.filename

            try:
                copy_result = self._copy_single_file(file.path, dest_path)
                if copy_result == 'copied':
                    result['copied'] += 1
                elif copy_result == 'skipped':
                    result['skipped'] += 1
                elif copy_result == 'overwritten':
                    result['overwritten'] += 1
                elif copy_result == 'renamed':
                    result['renamed'] += 1
                elif copy_result == 'cancelled':
                    result['cancelled'] = True
                    break
            except Exception as e:
                result['failed'] += 1
                print(f"複製失敗: {file.filename} - {e}")

        return result

    def _copy_single_file(self, src: Path, dest: Path) -> str:
        """複製單一檔案"""
        # 檔案不存在，直接複製
        if not dest.exists():
            shutil.copy2(src, dest)
            return 'copied'

        # 檔案已存在，處理重複
        action = self._get_duplicate_action(src, dest)

        if action == DuplicateAction.SKIP:
            return 'skipped'
        elif action == DuplicateAction.OVERWRITE:
            shutil.copy2(src, dest)
            return 'overwritten'
        elif action == DuplicateAction.RENAME:
            new_dest = self._get_unique_filename(dest)
            shutil.copy2(src, new_dest)
            return 'renamed'
        elif action == DuplicateAction.CANCEL:
            self._cancelled = True
            return 'cancelled'

        return 'skipped'

    def _get_duplicate_action(self, src: Path, dest: Path) -> DuplicateAction:
        """取得重複檔案的處理方式"""
        # 如果已設定全域動作
        if self._global_action:
            if self._global_action == DuplicateAction.SKIP_ALL:
                return DuplicateAction.SKIP
            elif self._global_action == DuplicateAction.OVERWRITE_ALL:
                return DuplicateAction.OVERWRITE
            elif self._global_action == DuplicateAction.RENAME_ALL:
                return DuplicateAction.RENAME

        # 詢問使用者
        if self.on_duplicate:
            action = self.on_duplicate(str(src), str(dest))

            # 記住全域動作
            if action in (DuplicateAction.SKIP_ALL, DuplicateAction.OVERWRITE_ALL, DuplicateAction.RENAME_ALL):
                self._global_action = action

            # 轉換為單次動作
            if action == DuplicateAction.SKIP_ALL:
                return DuplicateAction.SKIP
            elif action == DuplicateAction.OVERWRITE_ALL:
                return DuplicateAction.OVERWRITE
            elif action == DuplicateAction.RENAME_ALL:
                return DuplicateAction.RENAME

            return action

        # 預設略過
        return DuplicateAction.SKIP

    def _get_unique_filename(self, path: Path) -> Path:
        """取得不重複的檔案名稱"""
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        counter = 1

        while True:
            new_name = f"{stem}_{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1

    def cancel(self):
        """取消複製操作"""
        self._cancelled = True
