"""檔案類型定義與分類"""

# RAW 格式（各相機品牌）
RAW_EXTENSIONS = {
    '.arw',   # Sony
    '.cr2',   # Canon
    '.cr3',   # Canon (newer)
    '.nef',   # Nikon
    '.raf',   # Fujifilm
    '.orf',   # Olympus
    '.rw2',   # Panasonic
    '.dng',   # Adobe DNG
    '.pef',   # Pentax
    '.srw',   # Samsung
    '.x3f',   # Sigma
}

# JPEG 格式
JPG_EXTENSIONS = {'.jpg', '.jpeg'}

# HEIC 格式 (含 Fujifilm HIF)
HEIC_EXTENSIONS = {'.heic', '.heif', '.hif'}

# 影片格式
VIDEO_EXTENSIONS = {'.mov', '.mp4', '.avi', '.mkv', '.m4v', '.mts', '.m2ts'}

# 分類對應
FILE_CATEGORIES = {
    'RAW': RAW_EXTENSIONS,
    'JPG': JPG_EXTENSIONS,
    'HEIC': HEIC_EXTENSIONS,
    'VIDEO': VIDEO_EXTENSIONS,
}

def get_file_category(filename: str) -> str | None:
    """根據檔案名稱取得分類"""
    ext = filename.lower()
    # 取得副檔名
    dot_index = ext.rfind('.')
    if dot_index == -1:
        return None
    ext = ext[dot_index:]

    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return None

def get_all_supported_extensions() -> set:
    """取得所有支援的副檔名"""
    all_ext = set()
    for extensions in FILE_CATEGORIES.values():
        all_ext.update(extensions)
    return all_ext
