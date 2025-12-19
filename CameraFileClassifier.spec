# -*- mode: python ; coding: utf-8 -*-
import sys
import os

# Conda 環境的 Tcl/Tk DLL 路徑
base = sys.base_prefix
lib_bin = os.path.join(base, 'Library', 'bin')
dlls_path = os.path.join(base, 'DLLs')

# 加入 tcl86t.dll 和 tk86t.dll
binaries = [
    (os.path.join(lib_bin, 'tcl86t.dll'), '.'),
    (os.path.join(lib_bin, 'tk86t.dll'), '.'),
]

# Tcl/Tk 資料檔案
tcl_lib = os.path.join(base, 'Library', 'lib', 'tcl8.6')
tk_lib = os.path.join(base, 'Library', 'lib', 'tk8.6')

datas = [('icon.ico', '.')]
if os.path.exists(tcl_lib):
    datas.append((tcl_lib, 'tcl/tcl8.6'))
if os.path.exists(tk_lib):
    datas.append((tk_lib, 'tk/tk8.6'))

# 如果 Tcl/Tk 路徑不存在，試試其他路徑
if len(datas) == 1:
    tcl_lib2 = os.path.join(base, 'tcl', 'tcl8.6')
    tk_lib2 = os.path.join(base, 'tcl', 'tk8.6')
    if os.path.exists(tcl_lib2):
        datas.append((tcl_lib2, 'tcl/tcl8.6'))
    if os.path.exists(tk_lib2):
        datas.append((tk_lib2, 'tk/tk8.6'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=['ctypes', 'ctypes.wintypes'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'PIL.ImageQt', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6'],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CameraFileClassifier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    icon=r'D:\code\claude_test\camera_raw\icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='CameraFileClassifier',
)
