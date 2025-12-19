import zipfile
import os
from pathlib import Path

def create_zip():
    source_dir = Path('dist/CameraFileClassifier')
    output_file = Path('releases/CameraFileClassifier_Portable_v1.0.0.zip')

    # 创建releases目录
    output_file.parent.mkdir(exist_ok=True)

    # 删除旧的zip文件
    if output_file.exists():
        output_file.unlink()

    print(f"Creating portable zip: {output_file}")

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(source_dir.parent)
                print(f"  Adding: {arcname}")
                zipf.write(file_path, arcname)

    file_size = output_file.stat().st_size / (1024 * 1024)
    print(f"\nPortable zip created successfully!")
    print(f"File: {output_file}")
    print(f"Size: {file_size:.2f} MB")

if __name__ == '__main__':
    create_zip()
