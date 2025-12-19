"""檔案掃描模組 - 掃描資料夾並篩選檔案"""

import struct
import re
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

from .file_types import get_file_category, get_all_supported_extensions


@dataclass
class ScannedFile:
    """掃描到的檔案資訊"""
    path: Path
    filename: str
    category: str
    size: int
    capture_time: datetime | None  # 拍攝日期


def _read_exif_datetime(file_path: Path) -> datetime | None:
    """
    從檔案讀取 EXIF 拍攝日期
    支援 JPEG, HEIC/HIF, 及部分 RAW 格式
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(12)

            # JPEG 格式
            if header[:2] == b'\xff\xd8':
                return _read_jpeg_exif(f)

            # HEIC/HEIF/HIF 格式 (ftyp box)
            if header[4:8] == b'ftyp':
                return _read_heic_exif(f)

            # TIFF-based RAW 格式 (ARW, CR2, NEF, DNG, PEF, ORF 等)
            if header[:2] in (b'II', b'MM'):
                f.seek(0)
                return _read_tiff_exif(f)

            # RAF (Fujifilm) - 特殊格式
            if header[:8] == b'FUJIFILM':
                return _read_raf_exif(f)

    except Exception:
        pass

    return None


def _read_jpeg_exif(f) -> datetime | None:
    """讀取 JPEG EXIF 日期"""
    f.seek(2)

    while True:
        marker = f.read(2)
        if len(marker) < 2:
            break

        if marker == b'\xff\xe1':  # APP1 (EXIF)
            length = struct.unpack('>H', f.read(2))[0]
            exif_data = f.read(length - 2)

            if exif_data[:4] == b'Exif':
                return _parse_exif_datetime(exif_data[6:])
            break

        elif marker[0:1] == b'\xff' and marker[1:2] not in (b'\x00', b'\xff'):
            length = struct.unpack('>H', f.read(2))[0]
            f.seek(length - 2, 1)
        else:
            break

    return None


def _read_heic_exif(f) -> datetime | None:
    """讀取 HEIC/HIF EXIF 日期"""
    f.seek(0)
    data = f.read(64 * 1024)

    exif_marker = b'Exif\x00\x00'
    pos = data.find(exif_marker)

    if pos != -1:
        return _parse_exif_datetime(data[pos + 6:])

    return None


def _read_tiff_exif(f) -> datetime | None:
    """讀取 TIFF-based 格式的 EXIF 日期（RAW 檔案）"""
    data = f.read(64 * 1024)
    return _parse_exif_datetime(data)


def _read_raf_exif(f) -> datetime | None:
    """讀取 Fujifilm RAF 格式的 EXIF 日期"""
    f.seek(0)
    data = f.read(256 * 1024)

    for marker in (b'II\x2a\x00', b'MM\x00\x2a'):
        pos = data.find(marker)
        if pos != -1:
            return _parse_exif_datetime(data[pos:])

    return None


def _parse_exif_datetime(data: bytes) -> datetime | None:
    """從 EXIF 資料解析日期時間"""
    if len(data) < 8:
        return None

    try:
        # EXIF 日期格式: "YYYY:MM:DD HH:MM:SS"
        pattern = rb'(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})'
        matches = list(re.finditer(pattern, data))

        if matches:
            datetime_str = matches[0].group(0).decode('ascii')
            return datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")

    except Exception:
        pass

    return None


class FileScanner:
    """檔案掃描器"""

    def __init__(self, source_dir: str):
        self.source_dir = Path(source_dir)
        self.supported_extensions = get_all_supported_extensions()

    def scan(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        recursive: bool = True
    ) -> list[ScannedFile]:
        """
        掃描資料夾中的檔案

        Args:
            start_date: 開始日期（含），None 表示不限制
            end_date: 結束日期（含），None 表示不限制
            recursive: 是否遞迴掃描子資料夾

        Returns:
            符合條件的檔案列表
        """
        files = []
        need_date_filter = start_date is not None or end_date is not None

        if recursive:
            file_iterator = self.source_dir.rglob('*')
        else:
            file_iterator = self.source_dir.glob('*')

        for file_path in file_iterator:
            if not file_path.is_file():
                continue

            # 檢查副檔名
            ext = file_path.suffix.lower()
            if ext not in self.supported_extensions:
                continue

            # 取得檔案分類
            category = get_file_category(file_path.name)
            if category is None:
                continue

            # 取得檔案大小
            stat = file_path.stat()

            # 讀取拍攝日期
            capture_time = _read_exif_datetime(file_path)

            # 若需要日期篩選但讀不到拍攝日期，跳過此檔案
            if need_date_filter and capture_time is None:
                continue

            # 日期篩選
            if capture_time:
                if start_date and capture_time.date() < start_date.date():
                    continue
                if end_date and capture_time.date() > end_date.date():
                    continue

            files.append(ScannedFile(
                path=file_path,
                filename=file_path.name,
                category=category,
                size=stat.st_size,
                capture_time=capture_time
            ))

        # 依拍攝時間排序
        files.sort(key=lambda f: f.capture_time or datetime.min)
        return files

    def get_summary(self, files: list[ScannedFile]) -> dict[str, int]:
        """取得檔案分類統計"""
        summary = {}
        for f in files:
            summary[f.category] = summary.get(f.category, 0) + 1
        return summary
